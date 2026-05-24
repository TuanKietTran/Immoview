from rest_framework import serializers
from apps.listings.infrastructure.models import ListingModel, PhotoModel


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
            "price_chf", "price_display", "address_display",
            "area_m2", "rooms", "status", "view_count",
            "photos", "created_at", "updated_at",
        ]
        read_only_fields = ["id", "view_count", "created_at", "updated_at"]

    def get_price_display(self, obj: ListingModel) -> str:
        return f"CHF {obj.price_chf:,.0f}"

    def get_address_display(self, obj: ListingModel) -> str:
        return f"{obj.street} {obj.street_number}, {obj.postcode} {obj.city}"


class ListingWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = ListingModel
        fields = [
            "agency_id", "title", "description",
            "property_type", "offer_type",
            "street", "street_number", "postcode", "city", "canton",
            "price_chf", "area_m2", "rooms",
        ]
