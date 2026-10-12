from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone


TIER_WEIGHTS = {"enterprise": 30, "professional": 20, "starter": 10, "free": 0}
SOURCE_SCORES = {"referral": 1.0, "phone": 0.9, "email": 0.7, "website": 0.6, "portal": 0.5}


@dataclass(frozen=True)
class ScoreSignal:
    name: str
    value: float
    weight: int


@dataclass(frozen=True)
class LeadScore:
    lead_id: str
    score: int
    signals: tuple[ScoreSignal, ...]
    computed_at: str


def score_lead(message: dict, *, now: datetime | None = None) -> LeadScore:
    """Reference implementation of serverless-aws/services/lead-scoring/src/scorer.ts."""
    signals: list[ScoreSignal] = []
    signals.append(ScoreSignal("has_phone", 1 if message["phone"].strip() else 0, 15))
    length_score = min(len(message["message"].strip()) / 100, 1)
    signals.append(ScoreSignal("message_length", length_score, 20))
    signals.append(ScoreSignal("source_quality", SOURCE_SCORES.get(message["source"], 0.5), 25))
    tier_score = TIER_WEIGHTS.get(message["agencyTier"], 0) / 30
    signals.append(ScoreSignal("agency_tier", tier_score, 10))
    current = now or datetime.now(timezone.utc)
    created = datetime.fromisoformat(message["createdAt"].replace("Z", "+00:00"))
    age_seconds = (current - created).total_seconds()
    recency = 1.0 if age_seconds < 3600 else 0.5 if age_seconds < 86400 else 0.2
    signals.append(ScoreSignal("recency", recency, 30))
    raw = sum(signal.value * signal.weight for signal in signals)
    max_possible = sum(signal.weight for signal in signals)
    return LeadScore(message["leadId"], round(raw / max_possible * 100), tuple(signals), current.isoformat().replace("+00:00", "Z"))
