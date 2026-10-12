from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class VNDPrice:
    """Whole Vietnamese đồng, never represented as a floating point value."""

    amount: int

    def __post_init__(self) -> None:
        if isinstance(self.amount, bool) or not isinstance(self.amount, int):
            raise TypeError("VND amount must be an integer")
        if self.amount < 0:
            raise ValueError("VND amount cannot be negative")

    @classmethod
    def from_decimal(cls, value: Decimal) -> "VNDPrice":
        if value != value.to_integral_value():
            raise ValueError("VND must be a whole đồng amount")
        return cls(int(value))

    def per_square_metre(self, area_m2: Decimal) -> "VNDPrice":
        if area_m2 <= 0:
            raise ValueError("area must be positive")
        return VNDPrice(round(self.amount / area_m2))
