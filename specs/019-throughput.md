# 019 Idempotent synthetic import benchmark

Added `seed_throughput`, using deterministic `source_external_id` plus PostgreSQL `bulk_create(ignore_conflicts=True)` in batches.

Compose PostGIS results, run sequentially twice:

- Run 1: `requested=100000 total=100000 elapsed_seconds=17.031`
- Run 2: `requested=100000 total=100000 elapsed_seconds=14.292`

The equal totals demonstrate idempotent repeat behavior for this synthetic fixture. This is not a production throughput/SLA claim.
