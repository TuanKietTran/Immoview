import uuid

import pytest

from apps.listings.infrastructure.models import ListingModel
from apps.listings.search import bbox_search, polygon_search, radius_search, text_search, trigram_search


@pytest.fixture
def spatial_listings(db: None) -> list[ListingModel]:
    base = dict(
        agency_id=uuid.uuid4(), description="Căn hộ gần sông", property_type="apartment",
        offer_type="sale", street="A", street_number="1", postcode="5500", city="Da Nang",
        canton="VN", price_chf=0, area_m2=60,
    )
    near = ListingModel.objects.create(title="River apartment", latitude=16.0544, longitude=108.2022, **base)
    far = ListingModel.objects.create(title="Far house", latitude=21.0285, longitude=105.8542, **{**base, "description": "Nhà ngoại ô"})
    return [near, far]


@pytest.mark.django_db
def test_postgis_radius_bbox_polygon_and_unaccent_fts(spatial_listings: list[ListingModel]) -> None:
    near = radius_search(ListingModel.objects.all(), 16.0544, 108.2022, 1000)
    assert near.count() == 1
    assert bbox_search(ListingModel.objects.all(), 16, 108, 17, 109).count() == 1
    assert polygon_search(ListingModel.objects.all(), "POLYGON((108 16,109 16,109 17,108 17,108 16))").count() == 1
    assert text_search(ListingModel.objects.all(), "can ho").count() == 1
    assert trigram_search(ListingModel.objects.all(), "apartment").count() == 1
