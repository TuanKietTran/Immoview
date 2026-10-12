# Specifications

| Spec | Topic | State |
|---|---|---|
| [000-brief](000-brief.md) | Revival plan and non-negotiable rules | active |
| [001-baseline](001-baseline.md) | Compose, migration, test, and repository baseline | complete |
| [002-listings-moderation](002-listings-moderation.md) | Listing lifecycle, audit trail, and moderation foundation | implemented; tests passed |
| [003-vietnam-listing-fields](003-vietnam-listing-fields.md) | VND pricing and post-reform Vietnamese listing fields | implemented; tests passed |
| [004-search-saved-searches](004-search-saved-searches.md) | VND facets and saved-search API foundation | implemented; tests passed |
| [005-agency-onboarding](005-agency-onboarding.md) | Agency approval workflow and KYC metadata | implemented; tests passed |
| [006-leads-routing](006-leads-routing.md) | Lead routing, SLA, activity and viewing foundation | implemented; tests passed |
| [007-reliability-primitives](007-reliability-primitives.md) | Outbox, idempotency, and dead-letter records | implemented; tests passed |
| [008-phase1-audit](008-phase1-audit.md) | Line-by-line Phase 1 gap audit | complete; gaps tracked |
| [009-lead-scoring](009-lead-scoring.md) | Python reference for Lambda lead scoring contract | implemented; fixture tests passed |
| [011-duplicate-fraud](011-duplicate-fraud.md) | Duplicate fingerprint and anti-fraud flags | implemented; unit tests passed |
| [012-postgres-search](012-postgres-search.md) | PostGIS geo and PostgreSQL FTS/trigram search | implemented; compose test passed |
| [013-celery-reliability](013-celery-reliability.md) | Celery retries, circuit breaker and DLQ operations | implemented; config/tests passed |
| [014-remaining-phase1-operations](014-remaining-phase1-operations.md) | Seats/stats, notifications, throttling, health and shutdown | implemented; tests/config passed |
| [015-valuation-v1](015-valuation-v1.md) | Deterministic commune/comparable VND valuation model | implemented; tests passed |
| [016-billing-webhooks](016-billing-webhooks.md) | Double-entry ledger and payment webhook verification | implemented; fixture tests passed |
| [017-i18n](017-i18n.md) | Django/Nuxt vi/en i18n foundation | implemented; Nuxt build passed |
| [018-favourites-seo](018-favourites-seo.md) | Unique favourites and listing slug foundation | implemented; test passed |
| [019-throughput](019-throughput.md) | 100k synthetic idempotent import benchmark | compose run twice; counts stable |
| [010-vn-sources](010-vn-sources.md) | Vietnam source research and lawful ingress status | decision recorded; live access unverified |
| [020-infra-parity](020-infra-parity.md) | CDK-to-Terraform parity and unverified deployment items | scaffold; parity unverified |
| [FINAL](FINAL.md) | Final implemented/verified/unverified summary | planned |
