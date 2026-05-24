export interface ValuationRequest {
  canton: string;
  property_type: string;
  offer_type: string;
  area_m2: number;
  rooms?: number;
}

export interface ValuationResponse {
  id: string;
  estimate_chf: string;
  range_low_chf: string;
  range_high_chf: string;
  canton: string;
  property_type: string;
  offer_type: string;
  area_m2: number;
}

export interface Lead {
  id: string;
  listing_id: string;
  agency_id: string;
  name: string;
  email: string;
  status: LeadStatus;
  source: string;
  score: number | null;
  created_at: string;
}

export type LeadStatus =
  | "new"
  | "contacted"
  | "qualified"
  | "viewing_scheduled"
  | "offer_made"
  | "closed_won"
  | "closed_lost";

export interface Listing {
  id: string;
  agency_id: string;
  title: string;
  property_type: string;
  offer_type: string;
  city: string;
  canton: string;
  price_chf: string;
  price_display: string;
  area_m2: number;
  rooms: number | null;
  status: ListingStatus;
  view_count: number;
}

export type ListingStatus = "draft" | "published" | "reserved" | "sold" | "archived";

export interface PaginatedResponse<T> {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
}

// Props passed from Django via data-props attribute
export interface PriceCalculatorProps {
  agencyId: string;
  canton: string;
  avgPrice: number;
}

export interface LeadFunnelProps {
  agencyId: string;
}

export interface ListingBulkEditorProps {
  agencyId: string;
  csrfToken: string;
}
