# 004 Search and saved-search foundation

Implemented:

- VND price and post-reform province/commune filters in `ListingFilter`.
- Saved searches with per-user ownership, JSON query payload, active flag, timestamps, and unique name per user.
- REST routes under `/api/v1/listings/saved-searches/` with authenticated ownership filtering.
- Listing serializers expose Vietnamese fields.

Verification: listing test suite **11 passed in 0.58s**. Full PostGIS geo search, Vietnamese unaccent/trigram indexes, alert delivery, and map bbox search remain open.
