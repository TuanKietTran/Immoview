from datetime import datetime, timezone

from apps.leads.scoring import score_lead


BASE = {
    "leadId": "lead-1", "listingId": "listing-1", "agencyId": "agency-1", "name": "A",
    "email": "a@example.com", "phone": "0901", "message": "I want to view this home soon.",
    "source": "referral", "createdAt": "2026-01-01T11:30:00Z", "agencyTier": "enterprise",
}


def test_reference_matches_lambda_signal_contract() -> None:
    result = score_lead(BASE, now=datetime(2026, 1, 1, 12, tzinfo=timezone.utc))
    assert result.lead_id == "lead-1"
    assert result.score == 86
    assert [(s.name, s.weight) for s in result.signals] == [
        ("has_phone", 15), ("message_length", 20), ("source_quality", 25),
        ("agency_tier", 10), ("recency", 30),
    ]


def test_reference_defaults_unknown_source_and_tier_like_lambda() -> None:
    message = {**BASE, "source": "unknown", "agencyTier": "unknown"}
    assert 0 <= score_lead(message, now=datetime(2026, 1, 3, tzinfo=timezone.utc)).score <= 100
