# 007 Reliability primitives

Added database-backed reliability records:

- Transactional outbox events with pending status, availability, attempts, and admin visibility.
- Idempotency records keyed by endpoint + client key, request hash, replay response, and expiry; reuse with a different payload is rejected.
- Dead-letter task records with payload, error, attempt count, status, and admin visibility.

Helpers are in `apps.shared.reliability`; provider dispatch, bounded Celery retries, replay/discard actions, and metrics remain open.

Verification: shared, leads, agencies, and listings suites **18 passed in 0.65s**.
