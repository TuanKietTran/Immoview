import type { SNSHandler, SNSEvent } from "aws-lambda";
import { logger } from "@real-estate/shared";
import type { LeadCreatedEvent } from "@real-estate/shared";
import { sendEmailNotification } from "./email-notifier";
import { writeInAppNotification } from "./in-app-notifier";
import { dispatchAgencyWebhook } from "./webhook-notifier";

export const handler: SNSHandler = async (event: SNSEvent) => {
  logger.info("notifications invoked", { record_count: event.Records.length });

  for (const record of event.Records) {
    const payload: LeadCreatedEvent = JSON.parse(record.Sns.Message);

    const results = await Promise.allSettled([
      sendEmailNotification(payload),
      writeInAppNotification(payload),
      dispatchAgencyWebhook(payload),
    ]);

    results.forEach((r, i) => {
      const channel = ["email", "in-app", "webhook"][i]!;
      if (r.status === "rejected") {
        logger.error("notification channel failed", {
          channel,
          lead_id: payload.leadId,
          agency_id: payload.agencyId,
          error: String(r.reason),
        });
      } else {
        logger.info("notification sent", { channel, lead_id: payload.leadId });
      }
    });
  }
};
