from decimal import Decimal

from apps.listings.fraud import fraud_flags, make_duplicate_key


def test_duplicate_key_is_stable_for_normalized_address_and_images() -> None:
    kwargs = {"address": "  12 Nguyen Hue ", "latitude": Decimal("10.123456"), "longitude": Decimal("106.123456"), "price_vnd": 1_000_000_000, "image_hashes": ["b", "a"]}
    assert make_duplicate_key(**kwargs) == make_duplicate_key(**{**kwargs, "address": "12   nguyen hue", "image_hashes": ["a", "b"]})


def test_fraud_flags_price_phone_and_stock_photo() -> None:
    flags = fraud_flags(
        price_vnd=3_000_000_000,
        comparable_prices=[900_000_000, 1_000_000_000, 1_100_000_000],
        phone="+84 901-234",
        reused_phones={"84901234"},
        image_hashes=["stock-1"],
        stock_photo_hashes={"stock-1"},
    )
    assert flags == ["price_outlier", "reused_phone", "stock_photo"]
