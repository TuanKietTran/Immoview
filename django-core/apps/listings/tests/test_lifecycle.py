from apps.listings.domain.entities import Listing, ListingStatus, OfferType, PropertyType
from apps.listings.domain.value_objects import ListingId, Money, SwissAddress


def listing() -> Listing:
    return Listing(
        id=ListingId.generate(), agency_id="agency-1", title="Home", description="Home",
        property_type=PropertyType.APARTMENT, offer_type=OfferType.SALE,
        address=SwissAddress("Main", "1", "8000", "Zurich", "ZH"),
        price=Money(100), area_m2=50, rooms=2,
    )


def test_listing_requires_review_before_publishing() -> None:
    item = listing()
    item.submit_for_review()
    item.publish()
    item.mark_reserved()
    item.mark_sold()
    assert item.status == ListingStatus.SOLD


def test_expired_listing_cannot_be_reserved() -> None:
    item = listing()
    item.submit_for_review()
    item.publish()
    item.expire()
    assert item.status == ListingStatus.EXPIRED
