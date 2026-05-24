from rest_framework import serializers
from apps.billing.infrastructure.models import InvoiceModel


class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvoiceModel
        fields = ["id", "agency_id", "amount_chf", "status", "period_start", "period_end", "due_date", "paid_at", "created_at"]
        read_only_fields = ["id", "created_at"]
