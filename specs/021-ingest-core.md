# 021 Ingest pipeline core

Added `apps.ingest` with Source protocol, immutable raw landing payload/hash/timestamp, Pydantic normalized listing schema, quality checks, idempotent listing upsert by source external ID, IngestRun accounting, ingest dead letters, replay timestamps, rate limiter, and conditional-request-capable Source interface.

Verification: ingest tests **2 passed in 1.06s**; source-specific fetch/retry orchestration and live connectors remain open.
