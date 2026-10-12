# 023 Ingest quality and benchmark

The ingest admin exposes run counts and computed success rate, while `load_ingest_sample` loads deterministic synthetic records through the same ingest pipeline and reports elapsed seconds and rows/second. It accepts 1..100,000 records.

Verification: connector and ingest tests **10 passed**. A 1,000-row test-settings run completed with `fetched=1000 imported=1000 errors=0 elapsed_s=1.900 rows_per_s=526.3`.

A fresh SQLite test-settings 100,000-row idempotency run completed twice through `load_ingest_sample --count 100000 --source synthetic-100k`:

- run 1: `fetched=100000 imported=100000 errors=0 elapsed_s=208.041 rows_per_s=480.7`
- run 2: `fetched=100000 imported=100000 errors=0 elapsed_s=121.266 rows_per_s=824.6`

Post-run counts: `listings=100000`, `raw=100000`, `runs=[(100000,100000,0,completed),(100000,100000,0,completed)]`. This verifies deterministic idempotent counts, not a production SLA.
