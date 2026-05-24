import { S3Client } from "@aws-sdk/client-s3";
import { SQSClient } from "@aws-sdk/client-sqs";
import { SNSClient } from "@aws-sdk/client-sns";
import { DynamoDBClient } from "@aws-sdk/client-dynamodb";
import { DynamoDBDocumentClient } from "@aws-sdk/lib-dynamodb";

const endpointOverride = process.env.AWS_ENDPOINT_URL
  ? { endpoint: process.env.AWS_ENDPOINT_URL }
  : {};

const region = process.env.AWS_DEFAULT_REGION ?? "eu-central-1";

export const s3 = new S3Client({ region, ...endpointOverride });
export const sqs = new SQSClient({ region, ...endpointOverride });
export const sns = new SNSClient({ region, ...endpointOverride });

const dynamo = new DynamoDBClient({ region, ...endpointOverride });
export const ddb = DynamoDBDocumentClient.from(dynamo, {
  marshallOptions: { removeUndefinedValues: true },
});
