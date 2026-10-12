import uuid

import pytest

from apps.shared.models import DeadLetterTask, OutboxEvent
from apps.shared.reliability import claim_idempotency, dead_letter, enqueue_outbox, record_response


@pytest.mark.django_db
def test_idempotency_replays_same_request_and_rejects_different_payload() -> None:
    key, endpoint = "abc", "/api/payments"
    first, created = claim_idempotency(key, endpoint, {"amount": 10})
    assert created is True
    record_response(first, 201, {"ok": True})
    replay, created = claim_idempotency(key, endpoint, {"amount": 10})
    assert created is False
    assert replay.response_body == {"ok": True}
    with pytest.raises(ValueError):
        claim_idempotency(key, endpoint, {"amount": 11})


@pytest.mark.django_db
def test_outbox_and_dead_letter_are_persisted() -> None:
    event = enqueue_outbox("lead.created", "lead", str(uuid.uuid4()), {"id": 1})
    letter = dead_letter("send_notification", {"id": 1}, RuntimeError("provider timeout"), 3)
    assert OutboxEvent.objects.get(pk=event.pk).status == "pending"
    assert DeadLetterTask.objects.get(pk=letter.pk).attempts == 3
