import uuid

import pytest
from django.core.exceptions import ValidationError

from apps.listings.infrastructure.models import ListingModel


@pytest.fixture
def vietnam_listing() -> ListingModel:
    return ListingModel(
        agency_id=uuid.uuid4(), title="Nhà phố", description="Mô tả", property_type="house",
        offer_type="sale", street="Nguyen Van Linh", street_number="1", postcode="5500", city="Đà Nẵng", canton="VN",
        price_chf=0, area_m2=80, price_vnd=4_000_000_000, province_code="48", commune_code="48001",
        legal_status="so_do", planning_status="unknown", land_use_type="residential",
    )


@pytest.mark.django_db
def test_vietnam_listing_carries_post_reform_codes(vietnam_listing: ListingModel) -> None:
    vietnam_listing.full_clean()
    assert vietnam_listing.province_code == "48"
    assert vietnam_listing.commune_code == "48001"


@pytest.mark.django_db
def test_price_per_m2_requires_total_vnd_price(vietnam_listing: ListingModel) -> None:
    vietnam_listing.price_vnd = None
    vietnam_listing.price_per_m2_vnd = 50_000_000
    with pytest.raises(ValidationError):
        vietnam_listing.full_clean()
