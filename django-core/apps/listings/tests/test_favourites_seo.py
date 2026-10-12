import uuid

import pytest
from django.db import IntegrityError

from apps.listings.infrastructure.models import FavouriteModel, ListingModel
from apps.listings.seo import ensure_slug


@pytest.mark.django_db
def test_favourite_is_unique_per_user_and_slug_is_stable() -> None:
    listing = ListingModel.objects.create(
        agency_id=uuid.uuid4(), title="Nhà mặt phố Đà Nẵng", description="x", property_type="house",
        offer_type="sale", street="A", street_number="1", postcode="5500", city="Da Nang", canton="VN", price_chf=0, area_m2=50,
    )
    user_id = uuid.uuid4()
    FavouriteModel.objects.create(user_id=user_id, listing=listing)
    assert ensure_slug(listing).startswith("nha-mat-pho-a-nang-")
    with pytest.raises(IntegrityError):
        FavouriteModel.objects.create(user_id=user_id, listing=listing)
