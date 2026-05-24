from __future__ import annotations
from decimal import Decimal
from typing import Optional
import uuid

from apps.listings.domain.entities import Listing, ListingStatus, PropertyType, OfferType
from apps.listings.domain.value_objects import ListingId, Money, SwissAddress
from .models import ListingModel


class ListingRepository:
    def get(self, listing_id: ListingId) -> Optional[Listing]:
        try:
            m = ListingModel.objects.get(pk=listing_id.value)
        except ListingModel.DoesNotExist:
            return None
        return self._to_domain(m)

    def save(self, listing: Listing) -> None:
        ListingModel.objects.update_or_create(
            pk=listing.id.value,
            defaults=self._to_orm_dict(listing),
        )

    def list_published(self) -> list[Listing]:
        qs = ListingModel.objects.filter(status=ListingStatus.PUBLISHED.value)
        return [self._to_domain(m) for m in qs]

    def list_for_agency(self, agency_id: str) -> list[Listing]:
        """All listings for a single agency regardless of status — used by MIS."""
        qs = ListingModel.objects.filter(agency_id=agency_id)
        return [self._to_domain(m) for m in qs]

    @staticmethod
    def _to_domain(m: ListingModel) -> Listing:
        return Listing(
            id=ListingId(m.id),
            agency_id=str(m.agency_id),
            title=m.title,
            description=m.description,
            property_type=PropertyType(m.property_type),
            offer_type=OfferType(m.offer_type),
            address=SwissAddress(
                street=m.street,
                street_number=m.street_number,
                postcode=m.postcode,
                city=m.city,
                canton=m.canton,
            ),
            price=Money(m.price_chf),
            area_m2=m.area_m2,
            rooms=m.rooms,
            status=ListingStatus(m.status),
            created_at=m.created_at.replace(tzinfo=None) if m.created_at else None,
            updated_at=m.updated_at.replace(tzinfo=None) if m.updated_at else None,
        )

    @staticmethod
    def _to_orm_dict(listing: Listing) -> dict:
        return {
            "agency_id": uuid.UUID(listing.agency_id),
            "title": listing.title,
            "description": listing.description,
            "property_type": listing.property_type.value,
            "offer_type": listing.offer_type.value,
            "street": listing.address.street,
            "street_number": listing.address.street_number,
            "postcode": listing.address.postcode,
            "city": listing.address.city,
            "canton": listing.address.canton,
            "price_chf": listing.price.amount,
            "area_m2": listing.area_m2,
            "rooms": listing.rooms,
            "status": listing.status.value,
        }
