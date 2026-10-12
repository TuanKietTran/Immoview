# 023 Ingest quality and benchmark

The ingest admin exposes run counts and computed success rate, while `load_ingest_sample` loads deterministic synthetic records through the same ingest pipeline and reports elapsed seconds and rows/second. It accepts 1..100,000 records.

Verification: connector and ingest tests **10 passed**. A 1,000-row test-settings run completed with `fetched=1000 imported=1000 errors=0 elapsed_s=1.900 rows_per_s=526.3`. The 100,000-row run was attempted under SQLite test settings but exceeded the host job SLA and exited without a timing line; no 100k completion is claimed.
