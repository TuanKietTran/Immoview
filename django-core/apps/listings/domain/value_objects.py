from __future__ import annotations
from dataclasses import dataclass
from decimal import Decimal
from typing import Optional
import uuid


@dataclass(frozen=True)
class ListingId:
    value: uuid.UUID

    @classmethod
    def generate(cls) -> "ListingId":
        return cls(uuid.uuid4())

    @classmethod
    def from_str(cls, s: str) -> "ListingId":
        return cls(uuid.UUID(s))


@dataclass(frozen=True)
class Money:
    """CHF amount with currency validation."""
    amount: Decimal
    currency: str = "CHF"

    def __post_init__(self) -> None:
        if self.currency != "CHF":
            raise ValueError("Only CHF is supported")
        if self.amount < 0:
            raise ValueError("Amount cannot be negative")

    def __str__(self) -> str:
        return f"CHF {self.amount:,.0f}"


@dataclass(frozen=True)
class SwissAddress:
    street: str
    street_number: str
    postcode: str  # 4-digit Swiss postcode
    city: str
    canton: str  # 2-letter canton abbreviation

    def __post_init__(self) -> None:
        if len(self.postcode) != 4 or not self.postcode.isdigit():
            raise ValueError(f"Invalid Swiss postcode: {self.postcode!r}")
        valid_cantons = {
            "AG", "AI", "AR", "BE", "BL", "BS", "FR", "GE", "GL", "GR",
            "JU", "LU", "NE", "NW", "OW", "SG", "SH", "SO", "SZ", "TG",
            "TI", "UR", "VD", "VS", "ZG", "ZH",
        }
        if self.canton.upper() not in valid_cantons:
            raise ValueError(f"Invalid Swiss canton: {self.canton!r}")

    @property
    def full_address(self) -> str:
        return f"{self.street} {self.street_number}, {self.postcode} {self.city}, {self.canton}"
