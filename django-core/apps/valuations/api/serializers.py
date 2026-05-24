from rest_framework import serializers
from apps.valuations.infrastructure.models import ValuationModel


class ValuationRequestSerializer(serializers.Serializer):
    canton = serializers.CharField(max_length=2)
    property_type = serializers.ChoiceField(choices=["apartment", "house", "commercial", "land", "parking"])
    offer_type = serializers.ChoiceField(choices=["sale", "rent"])
    area_m2 = serializers.FloatField(min_value=5)
    rooms = serializers.FloatField(required=False, allow_null=True)
    listing_id = serializers.UUIDField(required=False, allow_null=True)


class ValuationResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = ValuationModel
        fields = ["id", "estimate_chf", "range_low_chf", "range_high_chf", "canton", "property_type", "offer_type", "area_m2", "created_at"]
