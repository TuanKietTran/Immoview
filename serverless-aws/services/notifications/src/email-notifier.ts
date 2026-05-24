import { SESClient, SendEmailCommand } from "@aws-sdk/client-ses";
import type { LeadCreatedEvent } from "@real-estate/shared";

const ses = new SESClient({
  region: process.env.AWS_DEFAULT_REGION ?? "eu-central-1",
  ...(process.env.AWS_ENDPOINT_URL ? { endpoint: process.env.AWS_ENDPOINT_URL } : {}),
});

const FROM = process.env.SES_FROM_EMAIL ?? "noreply@realestate.local";

export async function sendEmailNotification(lead: LeadCreatedEvent): Promise<void> {
  await ses.send(new SendEmailCommand({
    Source: FROM,
    Destination: { ToAddresses: [lead.email] },
    Message: {
      Subject: { Data: "Your property enquiry has been received" },
      Body: {
        Text: {
          Data: [
            `Dear ${lead.name},`,
            "",
            "Thank you for your enquiry. Our team will be in touch shortly.",
            "",
            `Reference: ${lead.leadId}`,
          ].join("\n"),
        },
      },
    },
  }));
  console.log("Email sent to", lead.email, "for lead", lead.leadId);
}
