from __future__ import annotations

import hashlib
import hmac
import json
from typing import Any

from django.db import IntegrityError

from apps.billing.infrastructure.models import PaymentWebhookEvent

SUPPORTED_PROVIDERS = frozenset({"vnpay", "momo", "zalopay", "vietqr", "stripe"})


def canonical_payload(payload: dict[str, Any]) -> bytes:
    return json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()


def verify_signature(provider: str, payload: dict[str, Any], signature: str, secret: str) -> bool:
    if provider not in SUPPORTED_PROVIDERS:
        raise ValueError("unsupported payment provider")
    expected = hmac.new(secret.encode(), canonical_payload(payload), hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, signature)


def claim_webhook(provider: str, event_id: str, payload: dict[str, Any], signature: str, secret: str) -> bool:
    if not verify_signature(provider, payload, signature, secret):
        raise ValueError("invalid webhook signature")
    try:
        PaymentWebhookEvent.objects.create(
            provider=provider, event_id=event_id,
            payload_hash=hashlib.sha256(canonical_payload(payload)).hexdigest(),
        )
    except IntegrityError:
        return False
    return True
