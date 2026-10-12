2026-10-12 — Treat the committed `specs/000-brief.md` as the controlling scope and keep all implementation claims evidence-based.
2026-10-12 — Use Django 5.2 LTS target, Python 3.13+, psycopg 3, and PostGIS; remove runtime Faker and psycopg2-binary.
2026-10-12 — Use pytest-django with factory_boy and Hypothesis as development-only tooling; baseline proved pytest is currently absent.
2026-10-12 — Use Celery with Redis for background work and a database dead-letter model/admin path when implementing reliability primitives.
2026-10-12 — Use lawful partner feeds or validated agency bulk imports only; do not build portal scrapers or bypass robots.txt/terms.
2026-10-12 — Use fixture/docs verification for Vietnam sources and label every connector not tested with live credentials as unverified.
2026-10-12 — Use Terraform as the AWS source of truth and restrict checks to fmt, backend-less init, validate, and static scans; never run plan/apply.
2026-10-12 — The initial compose timeout is recorded as slow first boot while web health was starting; migrations and `manage.py check` passed, while pytest failed because it is not installed.
2026-10-12 — PostGIS is enabled through Django's PostGIS backend and the runtime image installs GDAL/GEOS native libraries; compose uses amd64 emulation for the PostGIS image on Apple Silicon.
2026-10-12 — CI uses a PostGIS service and injects non-production settings rather than weakening production `SECRET_KEY` handling.
2026-10-12 — Listing lifecycle now requires draft -> pending_review -> published before reservation/sale; rented and expired are explicit terminal/active transitions and are covered by domain tests.
2026-10-12 — Terraform files remain future-phase work and are not marked complete; no AWS plan/apply was run.
2026-10-12 — Keep nginx on development host port 8081 because an unrelated local process owns 8080; verified API/admin through nginx on 8081.
2026-10-12 — Use the generated Nuxt Nitro server directly for local verification because this Nuxt preview wrapper mis-parses the host argument; the generated server returned HTTP 200.
2026-10-12 — Enforce listing transitions in a row-locked application service and write an audit event in the same transaction; invalid transitions produce no audit record.
2026-10-12 — Add Vietnamese fields as nullable migration-safe columns while legacy Swiss columns remain; VND amounts are integer đồng and per-m² values require a total VND price.
2026-10-12 — Store saved-search criteria as versionable JSON owned by UUID user_id, with unique names per user; advanced geo/full-text indexes remain separate work.
2026-10-12 — Agency approval is a locked onboarding state machine; KYC stores immutable-provider metadata and checksum, not document bytes in the database.
2026-10-12 — Route leads to the least-loaded candidate with deterministic UUID tie-breaking, set a bounded SLA deadline, and append an assignment activity in one transaction.
2026-10-12 — Persist outbox, idempotency, and dead-letter records in Django first; idempotency hashes the canonical request and uses a savepoint to safely handle concurrent duplicate keys.
2026-10-12 — The Phase 1 audit marks only tested foundations complete; all listed duplicate/fraud, geo/FTS, provider, Celery, circuit-breaker, metrics, and operational gaps remain open until verified.
