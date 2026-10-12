from __future__ import annotations

import hashlib
import statistics
from decimal import Decimal
from typing import Iterable


def make_duplicate_key(
    *, address: str, latitude: Decimal | None, longitude: Decimal | None,
    price_vnd: int | None, image_hashes: Iterable[str],
) -> str:
    """Stable duplicate fingerprint; geo is rounded to ~11m to tolerate GPS noise."""
    geo = "" if latitude is None or longitude is None else f"{latitude:.4f},{longitude:.4f}"
    images = ",".join(sorted(set(image_hashes)))
    raw = "|".join((" ".join(address.lower().split()), geo, str(price_vnd or ""), images))
    return hashlib.sha256(raw.encode()).hexdigest()


def fraud_flags(
    *, price_vnd: int | None, comparable_prices: Iterable[int], phone: str,
    reused_phones: set[str], image_hashes: Iterable[str], stock_photo_hashes: set[str],
) -> list[str]:
    flags: list[str] = []
    prices = [price for price in comparable_prices if price > 0]
    if price_vnd and len(prices) >= 3:
        median = statistics.median(prices)
        if price_vnd < median * Decimal("0.5") or price_vnd > median * Decimal("2"):
            flags.append("price_outlier")
    normalized_phone = "".join(ch for ch in phone if ch.isdigit())
    if normalized_phone and normalized_phone in reused_phones:
        flags.append("reused_phone")
    if set(image_hashes).intersection(stock_photo_hashes):
        flags.append("stock_photo")
    return flags
