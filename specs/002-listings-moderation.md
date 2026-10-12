# 002 Listings lifecycle and moderation

Implemented and tested:

- Explicit lifecycle transitions: draft -> pending_review -> published -> reserved/sold/rented/expired -> archived, with controlled reopen to draft.
- Transactional `transition_listing` service uses row locking and rejects invalid transitions.
- Immutable `ListingAuditEvent` records before/after status, actor, reason, metadata, and timestamp.
- Moderation fields for notes, duplicate key, and fraud flags; listing and audit-event admin queues are registered.

Verification: `SECRET_KEY=ci-test-secret DEBUG=true ALLOWED_HOSTS=localhost uv run pytest apps/listings/tests -q` -> **7 passed in 0.70s**. Database migration and live admin verification are pending the next compose rebuild.
