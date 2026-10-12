from decimal import Decimal

import pytest
from hypothesis import given, strategies as st

from apps.listings.domain.vietnam import VNDPrice


def test_vnd_rejects_fractional_decimal() -> None:
    with pytest.raises(ValueError):
        VNDPrice.from_decimal(Decimal("100.5"))


def test_vnd_per_square_metre_is_integer() -> None:
    assert VNDPrice(1_000_000).per_square_metre(Decimal("40")) == VNDPrice(25_000)


@given(st.integers(min_value=0, max_value=10**15), st.decimals(min_value="0.01", max_value="10000", allow_nan=False, allow_infinity=False))
def test_vnd_price_never_creates_negative_unit_price(amount: int, area: Decimal) -> None:
    assert VNDPrice(amount).per_square_metre(area).amount >= 0
