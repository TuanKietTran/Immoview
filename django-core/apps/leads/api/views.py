import json
import logging
from decouple import config
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.leads.infrastructure.models import LeadModel
from apps.agencies.infrastructure.models import AgencyModel
from apps.shared.audit import log_action
from apps.shared.metrics import increment
from apps.shared.permissions import IsAgencyMember, AgentRequired
from .serializers import LeadSerializer, LeadCreateSerializer

logger = logging.getLogger(__name__)


class LeadViewSet(viewsets.ModelViewSet):
    queryset = LeadModel.objects.all()
    search_fields = ["name", "email"]
    ordering = ["-created_at"]

    def get_serializer_class(self):
        if self.action == "create":
            return LeadCreateSerializer
        return LeadSerializer

    def get_permissions(self):
        if self.action in ("create", "notify"):
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated(), IsAgencyMember()]

    def get_queryset(self):
        qs = super().get_queryset()
        membership = getattr(self.request, "active_membership", None)
        if membership and not getattr(self.request.user, "is_staff_immoview", False):
            return qs.filter(agency_id=membership.agency_id)
        return qs

    def perform_create(self, serializer):
        lead = serializer.save()
        increment("immoview.lead.created", tags=[f"agency:{lead.agency_id}", f"source:{lead.source}"])
        self._enqueue_for_scoring(lead)
        self._publish_lead_created(lead)

    def _enqueue_for_scoring(self, lead: LeadModel) -> None:
        from apps.shared.aws import sqs_client
        queue_url = config("SQS_LEAD_SCORING_URL", default="")
        if not queue_url:
            return
        try:
            agency_tier = "free"
            try:
                agency = AgencyModel.objects.get(pk=lead.agency_id)
                agency_tier = agency.subscription_tier
            except AgencyModel.DoesNotExist:
                pass

            msg_kwargs: dict = {
                "QueueUrl": queue_url,
                "MessageBody": json.dumps({
                    "leadId": str(lead.id),
                    "listingId": str(lead.listing_id),
                    "agencyId": str(lead.agency_id),
                    "name": lead.name,
                    "email": lead.email,
                    "phone": lead.phone,
                    "message": lead.message,
                    "source": lead.source,
                    "createdAt": lead.created_at.isoformat(),
                    "agencyTier": agency_tier,
                }),
            }
            if queue_url.endswith(".fifo"):
                msg_kwargs["MessageGroupId"] = str(lead.agency_id)
            sqs_client().send_message(**msg_kwargs)
            logger.info("Enqueued lead %s for scoring", lead.id)
        except Exception:
            logger.exception("Failed to enqueue lead %s — proceeding without scoring", lead.id)

    def _publish_lead_created(self, lead: LeadModel) -> None:
        from apps.shared.aws import sns_client
        topic_arn = config("SNS_LEAD_CREATED_ARN", default="")
        if not topic_arn:
            return
        try:
            sns_client().publish(
                TopicArn=topic_arn,
                Message=json.dumps({
                    "leadId": str(lead.id),
                    "listingId": str(lead.listing_id),
                    "agencyId": str(lead.agency_id),
                    "name": lead.name,
                    "email": lead.email,
                }),
                Subject="lead.created",
                MessageAttributes={
                    "eventType": {"DataType": "String", "StringValue": "lead.created"},
                },
            )
        except Exception:
            logger.exception("Failed to publish lead.created for %s", lead.id)

    @action(detail=True, methods=["post"], permission_classes=[permissions.AllowAny])
    def notify(self, request, pk=None):
        """Internal endpoint called by the notifications Lambda."""
        lead = self.get_object()
        lead.save(update_fields=["updated_at"])
        return Response({"status": "ok"})

    @action(detail=True, methods=["get"])
    def score(self, request, pk=None):
        """Fetch the lead score from DynamoDB (written by lead-scoring Lambda)."""
        from apps.shared.aws import dynamodb_resource
        table_name = config("DYNAMODB_LEAD_SCORES_TABLE", default="lead-scores")
        try:
            table = dynamodb_resource().Table(table_name)
            item = table.get_item(Key={"leadId": pk}).get("Item")
            if item is None:
                return Response({"detail": "Score not yet available."}, status=status.HTTP_404_NOT_FOUND)
            return Response({
                "leadId": item["leadId"],
                "score": int(item["score"]),
                "signals": item.get("signals", []),
                "computedAt": item.get("computedAt"),
            })
        except Exception:
            logger.exception("DynamoDB score fetch failed for lead %s", pk)
            return Response({"detail": "Score service unavailable."}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

    @action(detail=True, methods=["post"])
    def contact(self, request, pk=None):
        lead = self.get_object()
        if lead.status != "new":
            return Response({"detail": "Lead already processed"}, status=status.HTTP_400_BAD_REQUEST)
        lead.status = "contacted"
        lead.save(update_fields=["status", "updated_at"])
        log_action(action="lead.contact", resource_type="lead", resource_id=pk, request=request)
        return Response(LeadSerializer(lead).data)

    @action(detail=True, methods=["post"])
    def qualify(self, request, pk=None):
        lead = self.get_object()
        lead.status = "qualified"
        lead.save(update_fields=["status", "updated_at"])
        log_action(action="lead.qualify", resource_type="lead", resource_id=pk, request=request)
        return Response(LeadSerializer(lead).data)
