from __future__ import annotations

import random
import time
from collections.abc import Callable
from threading import Lock
from typing import TypeVar

T = TypeVar("T")


class CircuitOpen(RuntimeError):
    pass


class CircuitBreaker:
    def __init__(self, failure_threshold: int = 3, reset_timeout: float = 30.0) -> None:
        self.failure_threshold = failure_threshold
        self.reset_timeout = reset_timeout
        self.failures = 0
        self.opened_at: float | None = None
        self._lock = Lock()

    def call(self, function: Callable[..., T], *args, **kwargs) -> T:
        with self._lock:
            if self.opened_at is not None:
                if time.monotonic() - self.opened_at < self.reset_timeout:
                    raise CircuitOpen("circuit is open")
                self.opened_at = None
                self.failures = 0
        try:
            result = function(*args, **kwargs)
        except Exception:
            with self._lock:
                self.failures += 1
                if self.failures >= self.failure_threshold:
                    self.opened_at = time.monotonic()
            raise
        with self._lock:
            self.failures = 0
        return result


def retry_delay(attempt: int, base: float = 1.0, cap: float = 60.0, random_fn: Callable[[], float] = random.random) -> float:
    """Exponential backoff with full jitter, capped for safe external calls."""
    return min(cap, base * (2**attempt)) * random_fn()
