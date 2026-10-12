from __future__ import annotations

import hashlib
import json
import time
from dataclasses import dataclass
from typing import Any, Protocol

from django.db import transaction
from django.utils import timezone

from apps.listings.infrastructure.models import ListingModel

from .models import IngestDeadLetter, IngestRun, RawLanding
from .schemas import NormalizedListing


class Source(Protocol):
    name: str
    def fetch(self, *, etag: str | None = None) -> tuple[list[dict[str, Any]], str | None]: ...


@dataclass
class RateLimiter:
    minimum_interval: float = 1.0
    _last_request: float = 0.0

    def wait(self) -> None:
        elapsed = time.monotonic() - self._last_request
        if elapsed < self.minimum_interval:
            time.sleep(self.minimum_interval - elapsed)
        self._last_request = time.monotonic()


def payload_hash(payload: dict[str, Any]) -> str:
    return hashlib.sha256(json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def quality_check(item: NormalizedListing) -> list[str]:
    errors = []
    if item.price_vnd is not None and item.price_vnd == 0:
        errors.append("zero_price")
    if item.area_m2 > 100_000:
        errors.append("area_outlier")
    return errors


@transaction.atomic
def land_raw(source: str, external_id: str, payload: dict[str, Any]) -> RawLanding:
    digest = payload_hash(payload)
    raw, _ = RawLanding.objects.get_or_create(source=source, external_id=external_id, payload_hash=digest, defaults={"payload": payload})
    return raw


@transaction.atomic
def upsert_listing(item: NormalizedListing) -> ListingModel:
    listing, _ = ListingModel.objects.update_or_create(
        source_external_id=f"{item.source}:{item.external_id}",
        defaults={
            "agency_id": "00000000-0000-0000-0000-000000000000", "title": item.title,
            "description": item.description, "property_type": "house", "offer_type": "sale",
            "street": "", "street_number": "", "postcode": "", "city": "", "canton": "VN",
            "price_chf": 0, "price_vnd": item.price_vnd, "area_m2": item.area_m2,
            "province_code": item.province_code, "commune_code": item.commune_code,
            "contact_phone": item.contact_phone,
        },
    )
    return listing


def ingest_payload(source: str, payloads: list[dict[str, Any]], run: IngestRun | None = None) -> IngestRun:
    run = run or IngestRun.objects.create(source=source)
    for payload in payloads:
        external_id = str(payload.get("external_id", ""))
        try:
            land_raw(source, external_id, payload)
            item = NormalizedListing.model_validate({**payload, "source": source})
            errors = quality_check(item)
            if errors:
                raise ValueError(",".join(errors))
            upsert_listing(item)
            run.fetched_count += 1
            run.imported_count += 1
        except Exception as exc:  # noqa: BLE001
            run.fetched_count += 1
            run.error_count += 1
            IngestDeadLetter.objects.create(run=run, source=source, external_id=external_id, payload=payload, error=str(exc), attempts=1)
    run.status = "completed" if run.error_count == 0 else "completed_with_errors"
    run.finished_at = timezone.now()
    run.save(update_fields=["fetched_count", "imported_count", "error_count", "status", "finished_at"])
    return run


def replay_raw(raw_id: str) -> IngestRun:
    raw = RawLanding.objects.get(pk=raw_id)
    raw.replayed_at = timezone.now()
    raw.save(update_fields=["replayed_at"])
    return ingest_payload(raw.source, [raw.payload])
