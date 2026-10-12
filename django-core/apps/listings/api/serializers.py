from rest_framework import serializers
from apps.listings.infrastructure.models import ListingModel, PhotoModel, SavedSearchModel


class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhotoModel
        fields = ["id", "cdn_small", "cdn_medium", "cdn_large", "order", "processed"]


class ListingSerializer(serializers.ModelSerializer):
    photos = PhotoSerializer(many=True, read_only=True)
    price_display = serializers.SerializerMethodField()
    address_display = serializers.SerializerMethodField()

    class Meta:
        model = ListingModel
        fields = [
            "id", "agency_id", "title", "description",
            "property_type", "offer_type",
            "street", "street_number", "postcode", "city", "canton",
            "price_chf", "price_vnd", "price_per_m2_vnd", "price_display", "address_display",
            "province_code", "commune_code", "legal_status", "direction", "frontage_m", "alley_width_m",
            "floors", "bedrooms", "project", "developer", "planning_status", "land_use_type",
            "area_m2", "rooms", "status", "view_count",
            "photos", "created_at", "updated_at",
        ]
        read_only_fields = ["id", "view_count", "created_at", "updated_at"]

    def get_price_display(self, obj: ListingModel) -> str:
        return f"CHF {obj.price_chf:,.0f}"

    def get_address_display(self, obj: ListingModel) -> str:
        return f"{obj.street} {obj.street_number}, {obj.postcode} {obj.city}"


class SavedSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavedSearchModel
        fields = ["id", "name", "query", "active", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]


class ListingWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = ListingModel
        fields = [
            "agency_id", "title", "description",
            "property_type", "offer_type",
            "street", "street_number", "postcode", "city", "canton",
            "price_chf", "price_vnd", "price_per_m2_vnd", "province_code", "commune_code",
            "legal_status", "direction", "frontage_m", "alley_width_m", "floors", "bedrooms",
            "project", "developer", "planning_status", "land_use_type", "area_m2", "rooms",
        ]
