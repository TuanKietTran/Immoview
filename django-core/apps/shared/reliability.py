from __future__ import annotations

import hashlib
import json
from datetime import timedelta
from typing import Any

from django.db import IntegrityError, transaction
from django.utils import timezone

from .models import DeadLetterTask, IdempotencyRecord, OutboxEvent


def request_hash(payload: Any) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str).encode()
    return hashlib.sha256(encoded).hexdigest()


@transaction.atomic
def claim_idempotency(key: str, endpoint: str, payload: Any, ttl_hours: int = 24) -> tuple[IdempotencyRecord, bool]:
    digest = request_hash(payload)
    try:
        with transaction.atomic():
            record = IdempotencyRecord.objects.create(
                key=key, endpoint=endpoint, request_hash=digest,
                expires_at=timezone.now() + timedelta(hours=ttl_hours),
            )
        return record, True
    except IntegrityError:
        record = IdempotencyRecord.objects.get(key=key, endpoint=endpoint)
        if record.request_hash != digest:
            raise ValueError("Idempotency key was reused with a different request")
        return record, False


def record_response(record: IdempotencyRecord, status_code: int, body: dict) -> None:
    record.response_code = status_code
    record.response_body = body
    record.save(update_fields=["response_code", "response_body"])


def enqueue_outbox(event_type: str, aggregate_type: str, aggregate_id: str, payload: dict) -> OutboxEvent:
    return OutboxEvent.objects.create(event_type=event_type, aggregate_type=aggregate_type, aggregate_id=aggregate_id, payload=payload)


def dead_letter(task_name: str, payload: dict, error: Exception, attempts: int) -> DeadLetterTask:
    return DeadLetterTask.objects.create(task_name=task_name, payload=payload, error=str(error), attempts=attempts)
