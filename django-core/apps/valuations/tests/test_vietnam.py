from decimal import Decimal

import pytest

from apps.valuations.domain.vietnam import Comparable, estimate_vnd


def test_vietnam_valuation_is_reproducible_and_explained() -> None:
    result = estimate_vnd(
        area_m2=Decimal("50"), commune_code="48001",
        comparables=[Comparable(1_000_000_000, Decimal("50"), "48001"), Comparable(1_200_000_000, Decimal("60"), "48001")],
        official_price_per_m2=15_000_000,
    )
    assert result["estimate_vnd"] == 875_000_000
    assert result["confidence"] == "medium"
    assert "comparable_rate_vnd_m2" in result["drivers"]


def test_valuation_requires_data() -> None:
    with pytest.raises(ValueError):
        estimate_vnd(area_m2=Decimal("50"), commune_code="48001", comparables=[])
