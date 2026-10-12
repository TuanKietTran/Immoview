# 011 Duplicate and fraud detection

Added stable duplicate fingerprints from normalized address, rounded geo, VND price, and sorted image hashes. Added explicit fraud flags for price outliers against comparables, reused phone numbers, and known stock-photo hashes.

Verification: fraud tests **2 passed in 0.12s**. Image perceptual-hash generation and production comparable queries remain integration work.
