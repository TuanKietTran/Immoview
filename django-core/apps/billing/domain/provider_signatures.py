from __future__ import annotations

import hashlib
import hmac
import json
from collections.abc import Mapping
from typing import Any
from urllib.parse import urlencode


def _json(payload: Mapping[str, Any]) -> str:
    return json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def _hmac_sha256(secret: str, data: str) -> str:
    return hmac.new(secret.encode(), data.encode(), hashlib.sha256).hexdigest()


def vnpay_base(payload: Mapping[str, Any]) -> str:
    filtered = {key: value for key, value in payload.items() if key not in {"vnp_SecureHash", "vnp_SecureHashType"}}
    return urlencode(sorted((key, str(value)) for key, value in filtered.items()))


def momo_base(payload: Mapping[str, Any]) -> str:
    preferred = ["accessKey", "amount", "extraData", "ipnUrl", "orderId", "orderInfo", "partnerCode", "redirectUrl", "requestId", "requestType"]
    keys = [key for key in preferred if key in payload] or sorted(payload)
    return "&".join(f"{key}={payload[key]}" for key in keys)


def zalopay_base(payload: Mapping[str, Any]) -> str:
    fields = ["app_id", "app_trans_id", "app_user", "amount", "app_time", "embed_data", "item"]
    return "|".join(str(payload.get(field, "")) for field in fields)


def vietqr_base(payload: Mapping[str, Any]) -> str:
    return _json(payload)


def stripe_base(payload: Mapping[str, Any]) -> str:
    timestamp = payload.get("t")
    body = payload.get("body")
    if timestamp is None or body is None:
        raise ValueError("stripe fixture requires t and body")
    return f"{timestamp}.{body}"


BASE_BUILDERS = {
    "vnpay": vnpay_base,
    "momo": momo_base,
    "zalopay": zalopay_base,
    "vietqr": vietqr_base,
    "stripe": stripe_base,
}


def canonical_for_provider(provider: str, payload: Mapping[str, Any]) -> str:
    try:
        return BASE_BUILDERS[provider](payload)
    except KeyError as exc:
        raise ValueError("unsupported payment provider") from exc


def sign_provider_payload(provider: str, payload: Mapping[str, Any], secret: str) -> str:
    return _hmac_sha256(secret, canonical_for_provider(provider, payload))
