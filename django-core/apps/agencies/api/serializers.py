from rest_framework import serializers
from apps.agencies.infrastructure.models import AgencyModel


class AgencySerializer(serializers.ModelSerializer):
    class Meta:
        model = AgencyModel
        fields = ["id", "name", "email", "phone", "canton", "subscription_tier", "is_active", "created_at"]
        read_only_fields = ["id", "created_at"]
