# 013 Celery and reliability execution

Added Celery application configuration, compose `worker` and `beat` services, a bounded-retry outbox task (`max_retries=5`, exponential backoff, jitter), circuit breaker with reset timeout, capped full-jitter delay helper, DLQ creation metrics, and admin replay/discard actions.

`docker compose config --quiet` passed. Ruff passed on reliability code and shared tests returned **5 passed in 0.72s**. No external provider dispatch or production worker run is claimed.
