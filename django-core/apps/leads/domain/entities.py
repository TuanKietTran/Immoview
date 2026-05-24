from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional
import uuid


class LeadStatus(str, Enum):
    NEW = "new"
    CONTACTED = "contacted"
    QUALIFIED = "qualified"
    VIEWING_SCHEDULED = "viewing_scheduled"
    OFFER_MADE = "offer_made"
    CLOSED_WON = "closed_won"
    CLOSED_LOST = "closed_lost"


class LeadSource(str, Enum):
    WEBSITE = "website"
    PHONE = "phone"
    EMAIL = "email"
    REFERRAL = "referral"
    PORTAL = "portal"


@dataclass
class Lead:
    id: uuid.UUID
    listing_id: uuid.UUID
    agency_id: uuid.UUID
    name: str
    email: str
    phone: str
    message: str
    source: LeadSource = LeadSource.WEBSITE
    status: LeadStatus = LeadStatus.NEW
    score: Optional[int] = None  # 0-100, written by Lambda scorer
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)

    def contact(self) -> None:
        if self.status != LeadStatus.NEW:
            raise ValueError("Lead already processed")
        self.status = LeadStatus.CONTACTED
        self._touch()

    def qualify(self) -> None:
        self.status = LeadStatus.QUALIFIED
        self._touch()

    def close_won(self) -> None:
        self.status = LeadStatus.CLOSED_WON
        self._touch()

    def close_lost(self, reason: Optional[str] = None) -> None:
        self.status = LeadStatus.CLOSED_LOST
        self._touch()

    def _touch(self) -> None:
        self.updated_at = datetime.utcnow()
