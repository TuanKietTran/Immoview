import uuid

import pytest
from django.db import IntegrityError

from apps.listings.api.filters import ListingFilter
from apps.listings.infrastructure.models import ListingModel, SavedSearchModel


@pytest.mark.django_db
def test_vnd_facets_filter_listings() -> None:
    ListingModel.objects.create(
        agency_id=uuid.uuid4(), title="Vietnam home", description="home", property_type="house",
        offer_type="sale", street="A", street_number="1", postcode="5500", city="Da Nang", canton="VN",
        price_chf=0, price_vnd=2_000_000_000, area_m2=80, province_code="48", commune_code="48001",
    )
    result = ListingFilter({"min_price_vnd": "1000000000", "province_code": "48"}, queryset=ListingModel.objects.all()).qs
    assert result.count() == 1


@pytest.mark.django_db
def test_saved_search_names_are_unique_per_user() -> None:
    user_id = uuid.uuid4()
    SavedSearchModel.objects.create(user_id=user_id, name="Da Nang", query={"province_code": "48"})
    with pytest.raises(IntegrityError):
        SavedSearchModel.objects.create(user_id=user_id, name="Da Nang", query={})
