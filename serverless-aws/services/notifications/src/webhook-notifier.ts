import type { LeadCreatedEvent } from "@real-estate/shared";

export async function dispatchAgencyWebhook(lead: LeadCreatedEvent): Promise<void> {
  if (!lead.agencyWebhookUrl) return;

  const resp = await fetch(lead.agencyWebhookUrl, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      event: "lead.created",
      leadId: lead.leadId,
      listingId: lead.listingId,
      name: lead.name,
      email: lead.email,
    }),
    signal: AbortSignal.timeout(5000),
  });

  if (!resp.ok) {
    console.warn(`Webhook to ${lead.agencyWebhookUrl} failed: ${resp.status}`);
  } else {
    console.log("Webhook dispatched to", lead.agencyWebhookUrl);
  }
}
