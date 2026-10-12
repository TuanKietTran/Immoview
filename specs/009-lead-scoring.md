# 009 Lead scoring reference

Added `apps.leads.scoring.score_lead`, a Python reference matching the TypeScript Lambda contract: identical message fields, five signal names/weights, source/tier defaults, recency windows, 0–100 rounded score, and output identifiers/signals/timestamp.

Verification: contract tests **2 passed in 0.12s**. This is a local reference/fixture implementation; no live Lambda invocation was performed.
