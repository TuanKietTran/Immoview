import type { LeadCreatedEvent } from "@real-estate/shared";

const DJANGO_INTERNAL_URL = process.env.DJANGO_INTERNAL_URL ?? "http://web:8000";

export async function writeInAppNotification(lead: LeadCreatedEvent): Promise<void> {
  const resp = await fetch(`${DJANGO_INTERNAL_URL}/api/v1/leads/${lead.leadId}/notify/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-Internal-Token": process.env.INTERNAL_API_TOKEN ?? "",
    },
    body: JSON.stringify({ leadId: lead.leadId, agencyId: lead.agencyId }),
  });

  if (!resp.ok) {
    console.warn(`In-app notify failed for lead ${lead.leadId}: ${resp.status}`);
  } else {
    console.log("In-app notification written for lead", lead.leadId);
  }
}
