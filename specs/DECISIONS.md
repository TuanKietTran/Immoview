2026-10-12 — Treat the committed `specs/000-brief.md` as the controlling scope and keep all implementation claims evidence-based.
2026-10-12 — Use Django 5.2 LTS target, Python 3.13+, psycopg 3, and PostGIS; remove runtime Faker and psycopg2-binary.
2026-10-12 — Use pytest-django with factory_boy and Hypothesis as development-only tooling; baseline proved pytest is currently absent.
2026-10-12 — Use Celery with Redis for background work and a database dead-letter model/admin path when implementing reliability primitives.
2026-10-12 — Use lawful partner feeds or validated agency bulk imports only; do not build portal scrapers or bypass robots.txt/terms.
2026-10-12 — Use fixture/docs verification for Vietnam sources and label every connector not tested with live credentials as unverified.
2026-10-12 — Use Terraform as the AWS source of truth and restrict checks to fmt, backend-less init, validate, and static scans; never run plan/apply.
2026-10-12 — The initial compose timeout is recorded as slow first boot while web health was starting; migrations and `manage.py check` passed, while pytest failed because it is not installed.
2026-10-12 — PostGIS is enabled through Django's PostGIS backend and the runtime image installs GDAL/GEOS native libraries; local macOS verification is blocked unless those libraries are available.
2026-10-12 — CI uses a PostGIS service and injects non-production settings rather than weakening production `SECRET_KEY` handling.
