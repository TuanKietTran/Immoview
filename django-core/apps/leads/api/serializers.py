from rest_framework import serializers
from apps.leads.infrastructure.models import LeadModel


class LeadSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeadModel
        fields = [
            "id", "listing_id", "agency_id", "name", "email", "phone",
            "message", "source", "status", "score", "created_at", "updated_at",
        ]
        read_only_fields = ["id", "status", "score", "sqs_message_id", "created_at", "updated_at"]


class LeadCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeadModel
        fields = ["id", "listing_id", "agency_id", "name", "email", "phone", "message", "source"]
        read_only_fields = ["id"]
