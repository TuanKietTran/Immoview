from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional
import uuid


class SubscriptionTier(str, Enum):
    FREE = "free"
    STARTER = "starter"
    PROFESSIONAL = "professional"
    ENTERPRISE = "enterprise"


@dataclass
class Agency:
    id: uuid.UUID
    name: str
    email: str
    phone: str
    canton: str
    subscription_tier: SubscriptionTier = SubscriptionTier.FREE
    is_active: bool = True
    created_at: datetime = field(default_factory=datetime.utcnow)

    @property
    def max_listings(self) -> int:
        return {
            SubscriptionTier.FREE: 3,
            SubscriptionTier.STARTER: 25,
            SubscriptionTier.PROFESSIONAL: 100,
            SubscriptionTier.ENTERPRISE: 10_000,
        }[self.subscription_tier]

    def upgrade(self, new_tier: SubscriptionTier) -> None:
        tiers = list(SubscriptionTier)
        if tiers.index(new_tier) <= tiers.index(self.subscription_tier):
            raise ValueError(f"Cannot downgrade from {self.subscription_tier} to {new_tier} here")
        self.subscription_tier = new_tier
