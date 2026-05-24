import type { SQSHandler, SQSRecord } from "aws-lambda";
import { PutCommand } from "@aws-sdk/lib-dynamodb";
import { ddb, logger } from "@real-estate/shared";
import type { LeadScoringMessage } from "@real-estate/shared";
import { scoreLead } from "./scorer";

const TABLE = process.env.DYNAMODB_LEAD_SCORES_TABLE!;

export const handler: SQSHandler = async (event) => {
  logger.info("lead-scoring invoked", { record_count: event.Records.length });

  const results = await Promise.allSettled(event.Records.map(processRecord));

  const failures = results
    .map((r, i) => ({ r, record: event.Records[i]! }))
    .filter(({ r }) => r.status === "rejected");

  if (failures.length > 0) {
    const ids = failures.map(({ record }) => record.messageId).join(", ");
    logger.error("partial batch failure", { failed: failures.length, total: event.Records.length, message_ids: ids });
    throw new Error(`${failures.length}/${event.Records.length} records failed: ${ids}`);
  }

  logger.info("lead-scoring complete", { processed: event.Records.length });
};

async function processRecord(record: SQSRecord): Promise<void> {
  const msg: LeadScoringMessage = JSON.parse(record.body);
  const scored = scoreLead(msg);

  await ddb.send(new PutCommand({
    TableName: TABLE,
    Item: {
      leadId: scored.leadId,
      score: scored.score,
      signals: scored.signals,
      computedAt: scored.computedAt,
      ttl: Math.floor(Date.now() / 1000) + 90 * 24 * 3600,
    },
    ConditionExpression: "attribute_not_exists(leadId) OR computedAt < :now",
    ExpressionAttributeValues: { ":now": scored.computedAt },
  }));

  logger.info("lead scored", {
    lead_id: scored.leadId,
    score: scored.score,
    agency_id: msg.agencyId,
    source: msg.source,
  });
}
