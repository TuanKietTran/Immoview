"""
Heuristic valuation model — intentionally simple for Phase 1.
Replace with a proper regression model in a later phase.
"""
from decimal import Decimal

# CHF per m² base rates by canton (rough market approximation)
CANTON_BASE_RATES: dict[str, Decimal] = {
    "ZH": Decimal("8500"),
    "GE": Decimal("9200"),
    "BS": Decimal("8000"),
    "ZG": Decimal("9500"),
    "VD": Decimal("7800"),
    "BE": Decimal("6500"),
    "LU": Decimal("6800"),
    "SG": Decimal("5900"),
    "AG": Decimal("5600"),
    "GR": Decimal("5200"),
    "TI": Decimal("6200"),
    "FR": Decimal("5800"),
}
DEFAULT_RATE = Decimal("6000")

PROPERTY_TYPE_MULTIPLIERS = {
    "apartment": Decimal("1.0"),
    "house": Decimal("1.15"),
    "commercial": Decimal("0.85"),
    "land": Decimal("0.45"),
    "parking": Decimal("0.20"),
}

OFFER_TYPE_MULTIPLIERS = {
    "sale": Decimal("1.0"),
    "rent": Decimal("0.0045"),  # monthly rent ≈ 0.45% of sale value
}


def estimate_price(
    canton: str,
    property_type: str,
    offer_type: str,
    area_m2: float,
    rooms: float | None = None,
) -> dict:
    base = CANTON_BASE_RATES.get(canton.upper(), DEFAULT_RATE)
    prop_mult = PROPERTY_TYPE_MULTIPLIERS.get(property_type, Decimal("1.0"))
    offer_mult = OFFER_TYPE_MULTIPLIERS.get(offer_type, Decimal("1.0"))

    estimate = Decimal(str(area_m2)) * base * prop_mult * offer_mult
    # ±15% confidence band
    low = estimate * Decimal("0.85")
    high = estimate * Decimal("1.15")

    return {
        "estimate_chf": round(estimate, -3),
        "range_low_chf": round(low, -3),
        "range_high_chf": round(high, -3),
        "canton": canton,
        "property_type": property_type,
        "offer_type": offer_type,
        "area_m2": area_m2,
    }
