# 015 Valuation model v1

Added a deterministic Vietnamese VND estimator accepting commune-scoped comparables and optional official price-table rate. It returns estimate, ±15% interval, confidence, and driver explanations; no live market data is embedded.

Verification: valuation tests **2 passed in 0.10s**. Persistence/history/API integration remains open.
