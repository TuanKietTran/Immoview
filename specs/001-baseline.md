# 001 Baseline (2026-10-12)

## Commands and evidence

- `docker compose up -d --build` from `django-core/`: image built and PostgreSQL 16, Redis 7, LocalStack 3.4, and the web container started. The command timed out at the 60-second harness SLA while the web healthcheck was still `starting`; this is a slow first boot, not a confirmed application failure.
- `docker compose logs web`: all existing Django migrations completed successfully, including `agencies`, `shared`, `billing`, `leads`, `listings`, and `valuations`.
- `docker compose exec -T web uv run python manage.py check`: **passed**, `System check identified no issues (0 silenced).`
- `docker compose exec -T web uv run pytest -q`: **failed** because `pytest` is not installed and there are no test dependencies in the image (`Failed to spawn: pytest`).
- `curl http://localhost:8080/health/`: the expected nginx port was not available because nginx waits for the web healthcheck; the host returned an unrelated 404 response. This is **unverified**, not an API health result.
- Repository inspection: Django 5.0.6, Python requirement >=3.12, `psycopg2-binary`, runtime Faker, no root `Makefile`, no root CI workflow, and no discovered Django test modules.

## Confirmed gaps

1. Test/lint/type-check toolchain is absent; baseline tests cannot run.
2. The compose web healthcheck waits during initial startup and prevents nginx from starting within the harness timeout.
3. Dependency pins are stale relative to the brief; Python 3.13+/Django 5.2 LTS and psycopg 3 are not yet configured.
4. The current compose file uses PostgreSQL 16 but not PostGIS.
5. No seed-demo command, root Make targets, or end-to-end CI workflow was found.
6. After switching settings to the required PostGIS backend, local macOS `manage.py check` cannot start without a native GDAL library; the container image now installs `libgdal-dev` and `libgeos-dev` to address this runtime requirement.

## Not claimed

No production readiness, AWS deployment, live Vietnamese-source access, payment-provider integration, or Terraform apply/plan was performed. Live external connectors and all AWS resources remain unverified by design.

## Phase 0 changes after baseline

The Python requirement is now >=3.13, the lock resolves Django 5.2 and psycopg 3, Faker is dev-only, compose uses PostGIS 16, production security headers/defaults were added, and initial Make/CI scaffolding was created. These changes still require container rebuild and full verification.
