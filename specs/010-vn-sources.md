# 010 Vietnam sources and ingress decision record

**Research date:** 2026-10-12 (web search performed first; package resolution also refreshed through uv). **Status:** design/fixtures only; no live credentials or live ingestion verification.

## Administrative structure

The 2025 reform changes the application model from province/district/commune to province/centrally governed city plus commune-level units (communes, wards and special zones). The research trail uses the Government policy portal and National Assembly resolutions: [xaydungchinhsach.chinhphu.vn](https://xaydungchinhsach.chinhphu.vn/) and Resolution 202/2025/QH15. The commonly reported result is 34 provincial-level units and a new commune-level code list effective with the 2025 reorganisation. Exact codes and old-to-new mappings must be loaded from the official General Statistics Office/Ministry of Home Affairs publication, not hand-entered from news summaries.

**Decision:** model `Province` and `Commune`, retain immutable source codes, and store `AdministrativeAlias(old_name, old_code, current_unit, valid_from, valid_to, source_url)`. District is an historical alias only. The loader will reject duplicate current codes and unresolved mappings. Current official code-file ingestion is **unverified** until a fixture is checked into the repository.

## Land-price tables

Land Law 2024 and its implementing instruments make provincial land-price tables effective/versioned data rather than one global table. Candidate official publication channels are provincial People's Committee portals and the Ministry of Natural Resources and Environment/land administration portals. Tables may be PDF, spreadsheet, or scanned material.

**Decision:** ingest the original bytes into immutable raw landing with SHA-256 and publication/effective dates; parse only approved PDF/XLSX fixtures with schema validation, unit checks, and manual review for OCR. Never overwrite a table: version by province and effective date. No 2026 live table is claimed as verified.

## Official rates and market data

Use State Bank of Vietnam publication pages for official FX/reference rates and policy-rate notices; use GSO and Ministry of Construction releases for statistics and market reports; check the national real-estate information system and Land Registry publications for public datasets. Each connector records source URL, retrieval time, licence/terms evidence, raw hash, and quality status. Live access is **unverified**.

## Listing portals and bulk import

No scraper is planned for batdongsan.com.vn, Chợ Tốt/Nhà Tốt, Alonhadat, Mogi, or similar portals. The allowed source types are a signed partner API/feed, licensed export, or agency-provided upload. The fallback deliverable is a CSV/XLSX/JSON template with dry-run validation, row-level errors, idempotency key, and an import report. This complies with the brief's terms/robots restriction; portal access remains **unverified**.

## Geocoding

Decision: use a provider interface with a self-hosted Nominatim/OSM deployment as the default open option, or a licensed Vietnamese commercial provider when an agency supplies a contract. Cache normalized address + provider/version, rate-limit requests, and never send sensitive contact fields. No live geocoding call is verified.

## Payments and operational controls

VNPay, MoMo, ZaloPay and VietQR/NAPAS connectors will be signature-verified against provider sandbox documentation/fixtures, with replay protection and idempotency; Stripe remains an international adapter. No credentials or live webhook tests exist, so all connector labels must say **verified against docs/fixtures, not live**.

## Ingress contract

`Source -> fetch (terms/robots/rate limit) -> RawLanding(payload, sha256, fetched_at) -> Pydantic normalize -> idempotent upsert -> quality checks/metrics -> IngestRun`. Retryable safe fetches use bounded exponential backoff with jitter; exhausted runs become dead letters and can be replayed from raw landing. No connector may silently discard a raw payload.
