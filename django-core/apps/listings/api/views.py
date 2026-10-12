import logging
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema

from apps.listings.infrastructure.models import ListingModel, PhotoModel, SavedSearchModel
from apps.listings.domain.services import publish_listing, archive_listing
from apps.listings.infrastructure.repositories import ListingRepository
from apps.listings.domain.value_objects import ListingId
from apps.shared.audit import log_action
from apps.shared.metrics import increment
from apps.shared.permissions import IsAgencyMember, AgentRequired
from .serializers import ListingSerializer, ListingWriteSerializer, SavedSearchSerializer
from .filters import ListingFilter

logger = logging.getLogger(__name__)


class SavedSearchViewSet(viewsets.ModelViewSet):
    serializer_class = SavedSearchSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ["get", "post", "patch", "delete", "head", "options"]

    def get_queryset(self):
        return SavedSearchModel.objects.filter(user_id=self.request.user.id)

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user.id)


class ListingViewSet(viewsets.ModelViewSet):
    queryset = ListingModel.objects.select_related().prefetch_related("photos").all()
    filterset_class = ListingFilter
    search_fields = ["title", "description", "city", "postcode"]
    ordering_fields = ["price_chf", "created_at", "area_m2", "rooms"]
    ordering = ["-created_at"]

    def get_serializer_class(self):
        if self.action in ("create", "update", "partial_update"):
            return ListingWriteSerializer
        return ListingSerializer

    def get_permissions(self):
        if self.action in ("list", "retrieve", "photo_ready_webhook"):
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated(), IsAgencyMember()]

    def get_queryset(self):
        qs = super().get_queryset()
        # Authenticated agency members only see their own agency's listings
        membership = getattr(self.request, "active_membership", None)
        if (
            membership
            and not getattr(self.request.user, "is_staff_immoview", False)
            and self.action not in ("list", "retrieve")
        ):
            return qs.filter(agency_id=membership.agency_id)
        return qs

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        ListingModel.objects.filter(pk=instance.pk).update(view_count=instance.view_count + 1)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @extend_schema(responses={200: ListingSerializer})
    @action(detail=True, methods=["post"])
    def publish(self, request, pk=None):
        repo = ListingRepository()
        listing = repo.get(ListingId.from_str(pk))
        if listing is None:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        try:
            publish_listing(listing)
            repo.save(listing)
        except ValueError as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_400_BAD_REQUEST)
        log_action(action="listing.publish", resource_type="listing", resource_id=pk, request=request)
        increment("immoview.listing.published", tags=[f"agency:{listing.agency_id}"])
        model = ListingModel.objects.get(pk=pk)
        return Response(ListingSerializer(model).data)

    @extend_schema(responses={200: ListingSerializer})
    @action(detail=True, methods=["post"])
    def archive(self, request, pk=None):
        repo = ListingRepository()
        listing = repo.get(ListingId.from_str(pk))
        if listing is None:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        archive_listing(listing)
        repo.save(listing)
        log_action(action="listing.archive", resource_type="listing", resource_id=pk, request=request)
        model = ListingModel.objects.get(pk=pk)
        return Response(ListingSerializer(model).data)

    @action(
        detail=False,
        methods=["post"],
        url_path="webhooks/photo-ready",
        permission_classes=[permissions.AllowAny],
    )
    def photo_ready_webhook(self, request):
        data = request.data
        photo_id = data.get("photoId")
        listing_id = data.get("listingId")
        if not photo_id or not listing_id:
            return Response(
                {"detail": "Missing photoId or listingId"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        updated = PhotoModel.objects.filter(
            id=photo_id, listing_id=listing_id
        ).update(
            cdn_small=data.get("s3KeySmall", ""),
            cdn_medium=data.get("s3KeyMedium", ""),
            cdn_large=data.get("s3KeyLarge", ""),
            processed=True,
        )
        if updated == 0:
            logger.warning(
                "photo_ready_webhook: no photo found for photo=%s listing=%s",
                photo_id, listing_id,
            )
            return Response({"detail": "Photo not found"}, status=status.HTTP_404_NOT_FOUND)
        logger.info("Photo %s for listing %s marked processed", photo_id, listing_id)
        return Response({"status": "ok"})
