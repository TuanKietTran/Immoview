from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import Enum

from .value_objects import ListingId, Money, SwissAddress


class ListingStatus(str, Enum):
    DRAFT = "draft"
    PENDING_REVIEW = "pending_review"
    PUBLISHED = "published"
    RESERVED = "reserved"
    SOLD = "sold"
    RENTED = "rented"
    EXPIRED = "expired"
    ARCHIVED = "archived"


class PropertyType(str, Enum):
    APARTMENT = "apartment"
    HOUSE = "house"
    COMMERCIAL = "commercial"
    LAND = "land"
    PARKING = "parking"


class OfferType(str, Enum):
    SALE = "sale"
    RENT = "rent"


@dataclass
class Listing:
    id: ListingId
    agency_id: str
    title: str
    description: str
    property_type: PropertyType
    offer_type: OfferType
    address: SwissAddress
    price: Money
    area_m2: float
    rooms: float | None
    status: ListingStatus = ListingStatus.DRAFT
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    def submit_for_review(self) -> None:
        if self.status != ListingStatus.DRAFT:
            raise ValueError("Only draft listings can enter review")
        self.status = ListingStatus.PENDING_REVIEW
        self._touch()

    def publish(self) -> None:
        if self.status not in (ListingStatus.PENDING_REVIEW, ListingStatus.ARCHIVED):
            raise ValueError(f"Cannot publish a listing with status {self.status}")
        self.status = ListingStatus.PUBLISHED
        self._touch()

    def archive(self) -> None:
        if self.status == ListingStatus.ARCHIVED:
            return
        self.status = ListingStatus.ARCHIVED
        self._touch()

    def mark_reserved(self) -> None:
        if self.status != ListingStatus.PUBLISHED:
            raise ValueError("Only published listings can be reserved")
        self.status = ListingStatus.RESERVED
        self._touch()

    def mark_sold(self) -> None:
        if self.status not in (ListingStatus.PUBLISHED, ListingStatus.RESERVED):
            raise ValueError("Can only mark published or reserved listings as sold")
        self.status = ListingStatus.SOLD
        self._touch()

    def mark_rented(self) -> None:
        if self.status not in (ListingStatus.PUBLISHED, ListingStatus.RESERVED):
            raise ValueError("Can only mark published or reserved listings as rented")
        self.status = ListingStatus.RENTED
        self._touch()

    def expire(self) -> None:
        if self.status not in (ListingStatus.PUBLISHED, ListingStatus.RESERVED):
            raise ValueError("Only active listings can expire")
        self.status = ListingStatus.EXPIRED
        self._touch()

    def _touch(self) -> None:
        self.updated_at = datetime.now(UTC)
