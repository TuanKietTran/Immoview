# 014 Remaining Phase 1 operations

Implemented the remaining operational foundations:

- Agency seat limits and agent performance counters; existing owner/admin/agent/viewer roles remain the permission model.
- Replaceable notification provider interface wired into outbox dispatch.
- Public/authenticated DRF rate throttles.
- Liveness/readiness/service health endpoints retained and liveness-tested.
- Celery worker/beat compose services, graceful Gunicorn timeout and compose stop grace period.
- DLQ admin replay/discard actions and creation metric.

Verification: shared/agency tests **11 passed in 0.50s**; Ruff and `docker compose config --quiet` passed. Provider delivery and live worker execution remain unverified.
