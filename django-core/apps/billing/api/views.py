from rest_framework import viewsets, permissions
from apps.billing.infrastructure.models import InvoiceModel
from .serializers import InvoiceSerializer


class InvoiceViewSet(viewsets.ModelViewSet):
    queryset = InvoiceModel.objects.all()
    serializer_class = InvoiceSerializer
    permission_classes = [permissions.IsAuthenticated]
    ordering = ["-created_at"]

    def get_queryset(self):
        qs = super().get_queryset()
        agency_id = self.request.query_params.get("agency_id")
        if agency_id:
            qs = qs.filter(agency_id=agency_id)
        return qs
