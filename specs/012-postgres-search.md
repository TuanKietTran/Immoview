# 012 PostGIS and PostgreSQL search

Added PostgreSQL-only search helpers using the compose PostGIS database:

- `ST_DWithin` geography radius search.
- Latitude/longitude bbox filtering.
- `ST_Contains` WKT polygon search.
- `unaccent` + `to_tsvector`/`plainto_tsquery` full-text search.
- `pg_trgm` similarity search.

Migration `0006_postgres_search` enables `unaccent` and `pg_trgm` on PostgreSQL and safely skips extensions on SQLite test settings.

Verification: real compose PostGIS test returned **1 passed in 2.45s**, covering radius, bbox, polygon, unaccent FTS, and trigram search.
