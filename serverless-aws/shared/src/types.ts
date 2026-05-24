export interface LeadScoringMessage {
  leadId: string;
  listingId: string;
  agencyId: string;
  name: string;
  email: string;
  phone: string;
  message: string;
  source: string;
  createdAt: string;
  agencyTier: "free" | "starter" | "professional" | "enterprise";
}

export interface LeadScore {
  leadId: string;
  score: number;          // 0–100
  signals: ScoreSignal[];
  computedAt: string;
}

export interface ScoreSignal {
  name: string;
  value: number;
  weight: number;
}

export interface PhotoProcessedEvent {
  listingId: string;
  photoId: string;
  s3KeyOriginal: string;
  s3KeySmall: string;
  s3KeyMedium: string;
  s3KeyLarge: string;
}

export interface LeadCreatedEvent {
  leadId: string;
  listingId: string;
  agencyId: string;
  name: string;
  email: string;
  agencyWebhookUrl?: string;
}
