from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional

from .value_objects import ListingId, Money, SwissAddress


class ListingStatus(str, Enum):
    DRAFT = "draft"
    PUBLISHED = "published"
    RESERVED = "reserved"
    SOLD = "sold"
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
    rooms: Optional[float]
    status: ListingStatus = ListingStatus.DRAFT
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)

    def publish(self) -> None:
        if self.status not in (ListingStatus.DRAFT, ListingStatus.ARCHIVED):
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

    def _touch(self) -> None:
        from datetime import datetime
        self.updated_at = datetime.utcnow()
