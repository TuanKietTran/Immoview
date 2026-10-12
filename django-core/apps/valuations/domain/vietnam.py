from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class Comparable:
    price_vnd: int
    area_m2: Decimal
    commune_code: str

    @property
    def price_per_m2(self) -> Decimal:
        return Decimal(self.price_vnd) / self.area_m2


def estimate_vnd(
    *, area_m2: Decimal, commune_code: str, comparables: list[Comparable], official_price_per_m2: int | None = None,
) -> dict:
    """Reproducible v1 estimator; callers provide immutable fixture comparables/tables."""
    if area_m2 <= 0:
        raise ValueError("area must be positive")
    local = [item.price_per_m2 for item in comparables if item.commune_code == commune_code and item.area_m2 > 0]
    if not local and official_price_per_m2 is None:
        raise ValueError("at least one comparable or official price is required")
    comparable_rate = sum(local, Decimal(0)) / len(local) if local else Decimal(official_price_per_m2)
    drivers = {"comparable_rate_vnd_m2": str(comparable_rate)}
    if official_price_per_m2 is not None:
        drivers["official_rate_vnd_m2"] = str(official_price_per_m2)
        rate = (comparable_rate + Decimal(official_price_per_m2)) / 2 if local else comparable_rate
    else:
        rate = comparable_rate
    estimate = int((area_m2 * rate).quantize(Decimal("1")))
    spread = int(estimate * Decimal("0.15"))
    return {
        "estimate_vnd": estimate,
        "range_low_vnd": estimate - spread,
        "range_high_vnd": estimate + spread,
        "confidence": "medium" if local and official_price_per_m2 is not None else "low",
        "drivers": drivers,
    }
