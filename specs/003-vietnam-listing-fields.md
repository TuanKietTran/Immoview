# 003 Vietnam listing fields

Added nullable migration-safe Vietnamese marketplace fields to listings: VND total and per-m² integer prices, post-reform province/commune codes, legal/planning/land-use status, direction, frontage, alley width, floors, bedrooms, project, and developer.

`ListingModel.clean()` rejects a per-m² VND value without a total VND price. Existing legacy address/CHF columns remain during the migration window so current seed/API clients do not break.

Verification: listing suite returned **9 passed in 0.54s**. The new migration is `0003_vietnam_fields`; live compose migration is pending the next rebuild.
