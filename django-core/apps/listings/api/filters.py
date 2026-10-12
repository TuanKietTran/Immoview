import django_filters
from apps.listings.infrastructure.models import ListingModel


class ListingFilter(django_filters.FilterSet):
    min_price = django_filters.NumberFilter(field_name="price_chf", lookup_expr="gte")
    max_price = django_filters.NumberFilter(field_name="price_chf", lookup_expr="lte")
    min_price_vnd = django_filters.NumberFilter(field_name="price_vnd", lookup_expr="gte")
    max_price_vnd = django_filters.NumberFilter(field_name="price_vnd", lookup_expr="lte")
    min_rooms = django_filters.NumberFilter(field_name="rooms", lookup_expr="gte")
    max_rooms = django_filters.NumberFilter(field_name="rooms", lookup_expr="lte")
    min_area = django_filters.NumberFilter(field_name="area_m2", lookup_expr="gte")
    max_area = django_filters.NumberFilter(field_name="area_m2", lookup_expr="lte")

    class Meta:
        model = ListingModel
        fields = {
            "status": ["exact"],
            "offer_type": ["exact"],
            "property_type": ["exact"],
            "canton": ["exact"],
            "postcode": ["exact"],
            "agency_id": ["exact"],
            "province_code": ["exact"],
            "commune_code": ["exact"],
        }
