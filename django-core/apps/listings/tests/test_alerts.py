import uuid

import pytest

from apps.listings.alerts import dispatch_listing_alerts
from apps.listings.infrastructure.models import ListingModel, SavedSearchModel
from apps.shared.notifications import LoggingNotificationProvider, configure_provider


@pytest.mark.django_db
def test_saved_search_alert_uses_notification_provider() -> None:
    agency_id = uuid.uuid4()
    listing = ListingModel.objects.create(
        agency_id=agency_id,
        title="Da Nang home",
        description="fixture",
        property_type="house",
        offer_type="sale",
        street="",
        street_number="",
        postcode="",
        city="Da Nang",
        canton="VN",
        price_chf=0,
        price_vnd=2_000_000_000,
        area_m2=80,
        province_code="48",
        commune_code="48001",
    )
    user_id = uuid.uuid4()
    SavedSearchModel.objects.create(user_id=user_id, name="Da Nang", query={"province_code": "48", "max_price_vnd": 3_000_000_000})
    SavedSearchModel.objects.create(user_id=uuid.uuid4(), name="Other", query={"province_code": "01"})
    provider = LoggingNotificationProvider([])
    configure_provider(provider)
    assert dispatch_listing_alerts(listing) == 1
    assert provider.sent[0][0] == "saved_search.match"
    assert provider.sent[0][1]["user_id"] == str(user_id)
