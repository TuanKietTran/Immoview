import uuid

import pytest

from apps.listings.application import InvalidListingTransition, transition_listing
from apps.listings.domain.entities import ListingStatus
from apps.listings.infrastructure.models import ListingAuditEvent, ListingModel


@pytest.fixture
def listing(db: None) -> ListingModel:
    return ListingModel.objects.create(
        agency_id=uuid.uuid4(), title="Test", description="Test", property_type="apartment",
        offer_type="sale", street="Nguyen Hue", street_number="1", postcode="8000",
        city="Ho Chi Minh City", canton="VN", price_chf=100, area_m2=50,
    )


@pytest.mark.django_db
def test_moderation_transition_writes_audit_event(listing: ListingModel) -> None:
    updated = transition_listing(listing.id, ListingStatus.PENDING_REVIEW.value, reason="submitted")
    assert updated.status == ListingStatus.PENDING_REVIEW.value
    event = ListingAuditEvent.objects.get(listing=listing)
    assert (event.from_status, event.to_status, event.reason) == ("draft", "pending_review", "submitted")


@pytest.mark.django_db
def test_invalid_transition_is_rejected_without_audit(listing: ListingModel) -> None:
    with pytest.raises(InvalidListingTransition):
        transition_listing(listing.id, ListingStatus.SOLD.value)
    assert ListingAuditEvent.objects.filter(listing=listing).count() == 0
