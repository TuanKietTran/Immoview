# 016 Billing ledger and payment webhook verification

Implemented a DB-backed double-entry ledger with non-negative/one-sided entry constraints and an atomic posting service requiring balanced positive debit/credit totals.

Added provider-neutral webhook verification for VNPay, MoMo, ZaloPay, VietQR and Stripe using canonical HMAC payloads, provider allow-listing, and unique provider/event replay protection. Shared idempotency records remain available for endpoint-level deduplication.

Verification: billing tests **2 passed in 0.50s**. Provider-specific canonical formats, sandbox fixtures, live credentials, VAT/e-invoice hooks, and settlement reconciliation remain unverified/open.
