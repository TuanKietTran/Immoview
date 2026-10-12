# TODO

## Open (ordered)
- [x] Phase 0: upgrade runtime/dependencies, PostGIS compose, secure settings, dev tooling, seed_demo, CI (verified tests/lint/typecheck, compose API/admin, Nuxt build/server)
- [x] Phase 1.1: listing lifecycle, audit trail, moderation and tests
- [x] Phase 1.2: Vietnam listing fields and validation tests
- [x] Phase 1.3: search/facets and saved-search foundation with tests
- [x] Phase 1.4: agency onboarding/approval roles and tests
- [x] Phase 1.5: lead routing/SLA/viewing foundation and tests
- [x] Phase 1.8: outbox, idempotency, retries and dead-letter records with tests
- [ ] Phase 1 audit: lifecycle exists, but duplicate detection (address+geo+price+image hash) and anti-fraud flags (price outlier, reused phone, stock photo) are missing
- [ ] Phase 1 audit: Vietnam fields exist, but PostGIS geo radius/polygon/bbox, Postgres FTS/trigram/unaccent, favourites, alerts provider, SEO slugs and sitemap are missing
- [ ] Phase 1 audit: agency onboarding exists, but KYC workflow enforcement, team-seat limits and performance stats are missing
- [ ] Phase 1 audit: lead routing/SLA/viewings/activity foundation exists, but Python lead-scoring reference matching the Lambda contract and calendar integration are missing
- [ ] Phase 1 audit: outbox/idempotency/DLQ records exist, but Celery worker/beat, bounded retries with backoff+jitter, circuit breaker, DLQ replay/discard/metrics are missing
- [ ] Phase 1 audit: rate limiting, readiness/health service coverage and graceful shutdown verification are missing
- [ ] Phase 1: search, agencies, leads, valuations, billing and reliability primitives (audit gaps above remain open)
- [ ] Phase 2: pluggable ingress, administrative aliases, land-price/statistics connectors, lawful bulk import, fixtures and throughput test
- [ ] Phase 3: Terraform modules/envs, Docker hardening, CI validation and parity document (validate-only scaffold passes; parity open)
- [ ] Final verification: tests/lint/typecheck/build, specs/FINAL.md, commit and push all milestones

## Done
- [x] Read and committed the commander brief before implementation
- [x] Recorded Phase 0 baseline evidence in `specs/001-baseline.md`

## Audit priority order
- [ ] Lead scoring Python reference and contract tests
- [ ] Duplicate detection and anti-fraud scoring
- [ ] PostGIS geo and PostgreSQL FTS/trigram/unaccent search with real compose database tests
- [ ] Celery bounded retries, circuit breaker, DLQ admin replay/discard/metrics

## Blocked or unverified
- [ ] Live Vietnamese portals and payment providers: no credentials/partner access; only docs/fixtures may be verified
- [ ] AWS: intentionally not planned/applied; Terraform validation only
