# 008 Phase 1 audit checkpoint

Audited Phase 1 items 1–5 and 8 against `specs/000-brief.md` after the initial 18-test batch.

## Present and verified

- Listing lifecycle domain transitions, moderation fields/admin, and transactional audit events.
- VND integer fields, post-reform province/commune code columns, legal/planning fields.
- Basic numeric filters and saved-search persistence/API foundation.
- Agency onboarding/approval state machine and KYC metadata.
- Least-loaded lead routing, SLA timestamp, activity record, viewing slot validation.
- Database outbox, idempotency hash/replay record, and dead-letter record/admin visibility.

## Missing and now tracked in `specs/TODO.md`

- Duplicate detection using address + geo + price + image hash; anti-fraud price outlier, reused phone, and stock-photo flags.
- PostGIS radius/polygon/bbox search tests against compose PostgreSQL; PostgreSQL FTS/trigram/unaccent; favourites; provider-backed alerts; SEO slugs/sitemap.
- Enforced KYC workflow, team-seat limits, and agent performance statistics.
- Lead-scoring Python reference matching `serverless-aws/services/lead-scoring`; real calendar integration.
- Celery worker/beat, bounded retry backoff+jitter, circuit breaker, DLQ replay/discard/metrics.
- Rate limiting, complete readiness/health service coverage, and graceful shutdown verification.

No missing item is marked done. Priority implementation order is lead scoring, duplicate/fraud, geo/FTS, then task reliability.
