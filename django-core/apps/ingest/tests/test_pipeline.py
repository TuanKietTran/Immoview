import pytest

from apps.ingest.models import IngestDeadLetter, RawLanding
from apps.ingest.pipeline import ingest_payload, replay_raw


@pytest.mark.django_db
def test_ingest_normalizes_upserts_and_is_idempotent() -> None:
    payload = {"external_id": "a-1", "title": "Nhà", "description": "x", "price_vnd": 1000, "area_m2": 50, "province_code": "48", "commune_code": "48001"}
    first = ingest_payload("fixture", [payload])
    second = ingest_payload("fixture", [payload])
    assert first.imported_count == second.imported_count == 1
    assert RawLanding.objects.count() == 1


@pytest.mark.django_db
def test_quality_error_goes_to_dead_letter_and_raw_replay_is_recorded() -> None:
    payload = {"external_id": "bad", "title": "Bad", "area_m2": 0}
    run = ingest_payload("fixture", [payload])
    assert run.error_count == 1
    assert IngestDeadLetter.objects.get().status == "pending"
    raw = RawLanding.objects.get()
    replay_raw(str(raw.id))
    assert RawLanding.objects.get().replayed_at is not None
