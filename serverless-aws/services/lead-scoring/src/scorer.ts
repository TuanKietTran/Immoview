import type { LeadScoringMessage, LeadScore, ScoreSignal } from "@real-estate/shared";

const TIER_WEIGHTS: Record<string, number> = {
  enterprise: 30,
  professional: 20,
  starter: 10,
  free: 0,
};

export function scoreLead(msg: LeadScoringMessage): LeadScore {
  const signals: ScoreSignal[] = [];

  // Completeness: phone provided
  const hasPhone = msg.phone.trim().length > 0;
  signals.push({ name: "has_phone", value: hasPhone ? 1 : 0, weight: 15 });

  // Completeness: message length
  const msgLen = msg.message.trim().length;
  const msgScore = Math.min(msgLen / 100, 1);
  signals.push({ name: "message_length", value: msgScore, weight: 20 });

  // Source quality
  const sourceScores: Record<string, number> = {
    referral: 1.0,
    phone: 0.9,
    email: 0.7,
    website: 0.6,
    portal: 0.5,
  };
  const sourceScore = sourceScores[msg.source] ?? 0.5;
  signals.push({ name: "source_quality", value: sourceScore, weight: 25 });

  // Agency tier (higher tier agency = better-qualified leads on average)
  const tierScore = (TIER_WEIGHTS[msg.agencyTier] ?? 0) / 30;
  signals.push({ name: "agency_tier", value: tierScore, weight: 10 });

  // Recency: created within the last hour gets a bonus
  const ageMs = Date.now() - new Date(msg.createdAt).getTime();
  const recencyScore = ageMs < 3_600_000 ? 1.0 : ageMs < 86_400_000 ? 0.5 : 0.2;
  signals.push({ name: "recency", value: recencyScore, weight: 30 });

  const raw = signals.reduce((acc, s) => acc + s.value * s.weight, 0);
  const maxPossible = signals.reduce((acc, s) => acc + s.weight, 0);
  const score = Math.round((raw / maxPossible) * 100);

  return {
    leadId: msg.leadId,
    score,
    signals,
    computedAt: new Date().toISOString(),
  };
}
