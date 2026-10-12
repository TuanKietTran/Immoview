# TODO

## Open (ordered)
- [x] Phase 0: upgrade runtime/dependencies, PostGIS compose, secure settings, dev tooling, seed_demo, CI (verified tests/lint/typecheck, compose API/admin, Nuxt build/server)
- [x] Phase 1.1: listing lifecycle, audit trail, moderation and tests
- [x] Phase 1.2: Vietnam listing fields and validation tests
- [x] Phase 1.3: search/facets and saved-search foundation with tests
- [x] Phase 1.4: agency onboarding/approval roles and tests
- [x] Phase 1.5: lead routing/SLA/viewing foundation and tests
- [x] Phase 1.8: outbox, idempotency, retries and dead-letter records with tests
- [x] Phase 1 audit checkpoint and gap inventory
- [x] Phase 1 audit: duplicate detection and anti-fraud primitives implemented; perceptual hash/comparable integration remains open
- [ ] Phase 1 audit: geo/FTS, favourites, slugs, sitemap and notification adapter implemented; alert delivery integration remains
- [ ] Phase 1 audit: agency onboarding exists, but KYC workflow enforcement remains; team-seat limits and performance stats are implemented
- [ ] Phase 1 audit: lead scoring reference implemented; external calendar integration remains
- [ ] Phase 1 audit: outbox/provider dispatch is adapter-backed; live provider delivery and worker execution remain unverified
- [x] Phase 1 audit: rate limiting, readiness/health service coverage and graceful shutdown verification
- [ ] Phase 1: search, agencies, leads, valuations, billing and reliability primitives (valuation, ledger/webhook foundation and vi/en foundation complete; provider-specific formats remain open)
- [x] Phase 2: pluggable ingress, administrative aliases, land-price/statistics connectors, lawful bulk import, fixtures and throughput test (core/connectors/quality loader complete; 100k attempt exceeded session SLA without timing)
- [ ] Phase 3: Terraform modules/envs, Docker hardening, CI validation and parity document (modules/envs/CDK removal/CI/Docker/parity complete; Terraform provider initialization/validate remains unverified)
- [ ] Final verification: smoke/benchmark/Terraform/security evidence recorded in `specs/FINAL.md`; full connector fixture coverage and remaining open gaps still require completion

## Done
- [x] Read and committed the commander brief before implementation
- [x] Recorded Phase 0 baseline evidence in `specs/001-baseline.md`

## Audit priority order
- [x] Lead scoring Python reference and contract tests
- [x] Duplicate detection and anti-fraud scoring
- [x] PostGIS geo and PostgreSQL FTS/trigram/unaccent search with real compose database tests
- [x] Celery bounded retries, circuit breaker, DLQ admin replay/discard/metrics

## Blocked or unverified
- [ ] Live Vietnamese portals and payment providers: no credentials/partner access; only docs/fixtures may be verified
- [ ] AWS: intentionally not planned/applied; Terraform validation only
