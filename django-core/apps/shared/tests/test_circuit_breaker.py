import pytest

from apps.shared.circuit_breaker import CircuitBreaker, CircuitOpen, retry_delay
from apps.shared.tasks import publish_outbox


def test_circuit_opens_after_threshold_failures() -> None:
    breaker = CircuitBreaker(failure_threshold=2, reset_timeout=60)

    def broken():
        raise RuntimeError("down")

    with pytest.raises(RuntimeError):
        breaker.call(broken)
    with pytest.raises(RuntimeError):
        breaker.call(broken)
    with pytest.raises(CircuitOpen):
        breaker.call(lambda: "ok")


def test_retry_delay_is_jittered_and_capped() -> None:
    assert retry_delay(3, base=2, cap=10, random_fn=lambda: 0.5) == 5
    assert retry_delay(10, base=2, cap=10, random_fn=lambda: 1.0) == 10


def test_celery_task_has_bounded_retry_policy() -> None:
    assert publish_outbox.max_retries == 5
    assert publish_outbox.retry_backoff is True
    assert publish_outbox.retry_jitter is True
