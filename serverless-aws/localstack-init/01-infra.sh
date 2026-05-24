#!/bin/bash
set -uo pipefail

REGION="eu-central-1"

echo "==> Creating S3 buckets..."
awslocal s3 mb s3://listings-raw --region $REGION || echo "  listings-raw already exists"
awslocal s3 mb s3://listings-cdn --region $REGION || echo "  listings-cdn already exists"

echo "==> Creating DynamoDB table..."
awslocal dynamodb create-table \
  --table-name lead-scores \
  --attribute-definitions AttributeName=leadId,AttributeType=S \
  --key-schema AttributeName=leadId,KeyType=HASH \
  --billing-mode PAY_PER_REQUEST \
  --region $REGION 2>/dev/null || echo "  lead-scores already exists"

awslocal dynamodb update-time-to-live \
  --table-name lead-scores \
  --time-to-live-specification "Enabled=true,AttributeName=ttl" \
  --region $REGION 2>/dev/null || true

echo "==> Creating SQS queues..."
awslocal sqs create-queue --queue-name lead-scoring-dlq --region $REGION 2>/dev/null || true

SCORING_DLQ_ARN=$(awslocal sqs get-queue-attributes \
  --queue-url http://localhost:4566/000000000000/lead-scoring-dlq \
  --attribute-names QueueArn \
  --query Attributes.QueueArn \
  --output text \
  --region $REGION)

awslocal sqs create-queue \
  --queue-name lead-scoring \
  --attributes "{\"VisibilityTimeout\":\"90\",\"RedrivePolicy\":\"{\\\"deadLetterTargetArn\\\":\\\"${SCORING_DLQ_ARN}\\\",\\\"maxReceiveCount\\\":\\\"3\\\"}\"}" \
  --region $REGION 2>/dev/null || true

echo "==> Creating SNS topics..."
awslocal sns create-topic --name listing-photo-ready --region $REGION 2>/dev/null || true
awslocal sns create-topic --name lead-created --region $REGION 2>/dev/null || true

echo "==> Deploying Lambda functions..."

deploy_lambda() {
  local name=$1
  local src_js=$2
  local timeout=$3
  local memory=$4
  local env_vars=$5
  local zip_path="/tmp/${name}.zip"

  if [ ! -f "$src_js" ]; then
    echo "  ${name}: ${src_js} not found — skipping (run 'bun run bundle' first)"
    return 0
  fi

  zip -j "$zip_path" "$src_js"

  # Lambdas run in sibling containers; they reach LocalStack via its service name, not localhost
  awslocal lambda create-function \
    --function-name "$name" \
    --runtime nodejs20.x \
    --handler handler.handler \
    --zip-file "fileb://${zip_path}" \
    --role arn:aws:iam::000000000000:role/lambda-role \
    --timeout "$timeout" \
    --memory-size "$memory" \
    --environment "Variables={AWS_ENDPOINT_URL=http://localstack:4566,AWS_ACCESS_KEY_ID=test,AWS_SECRET_ACCESS_KEY=test,AWS_DEFAULT_REGION=eu-central-1,${env_vars}}" \
    --region $REGION 2>/dev/null || \
  awslocal lambda update-function-code \
    --function-name "$name" \
    --zip-file "fileb://${zip_path}" \
    --region $REGION

  echo "  ${name}: deployed"
}

deploy_lambda "image-pipeline" \
  "/app/services/image-pipeline/dist/handler.js" \
  300 1024 \
  "S3_LISTINGS_CDN=listings-cdn,SNS_PHOTO_READY_ARN=arn:aws:sns:eu-central-1:000000000000:listing-photo-ready"

if awslocal lambda get-function --function-name image-pipeline --region $REGION > /dev/null 2>&1; then
  echo "  Waiting for image-pipeline to become Active..."
  awslocal lambda wait function-active-v2 --function-name image-pipeline --region $REGION 2>/dev/null || true

  awslocal lambda add-permission \
    --function-name image-pipeline \
    --statement-id s3-trigger \
    --action lambda:InvokeFunction \
    --principal s3.amazonaws.com \
    --source-arn arn:aws:s3:::listings-raw \
    --region $REGION 2>/dev/null || true

  awslocal s3api put-bucket-notification-configuration \
    --bucket listings-raw \
    --notification-configuration '{"LambdaFunctionConfigurations":[{"LambdaFunctionArn":"arn:aws:lambda:eu-central-1:000000000000:function:image-pipeline","Events":["s3:ObjectCreated:*"]}]}' \
    --region $REGION && echo "  image-pipeline: S3 trigger attached" || echo "  image-pipeline: S3 trigger warning (non-fatal)"
fi

deploy_lambda "lead-scoring" \
  "/app/services/lead-scoring/dist/handler.js" \
  90 256 \
  "DYNAMODB_LEAD_SCORES_TABLE=lead-scores"

if awslocal lambda get-function --function-name lead-scoring --region $REGION > /dev/null 2>&1; then
  awslocal lambda create-event-source-mapping \
    --function-name lead-scoring \
    --event-source-arn arn:aws:sqs:eu-central-1:000000000000:lead-scoring \
    --batch-size 10 \
    --function-response-types ReportBatchItemFailures \
    --region $REGION 2>/dev/null || echo "  lead-scoring: event source mapping already exists"
fi

deploy_lambda "notifications" \
  "/app/services/notifications/dist/handler.js" \
  30 256 \
  "DJANGO_INTERNAL_URL=http://web:8000"

if awslocal lambda get-function --function-name notifications --region $REGION > /dev/null 2>&1; then
  awslocal sns subscribe \
    --topic-arn arn:aws:sns:eu-central-1:000000000000:lead-created \
    --protocol lambda \
    --notification-endpoint arn:aws:lambda:eu-central-1:000000000000:function:notifications \
    --region $REGION 2>/dev/null || echo "  notifications: SNS subscription already exists"
fi

echo ""
echo "==> LocalStack init complete."
echo "S3 buckets:"
awslocal s3 ls
echo "SQS queues:"
awslocal sqs list-queues --region $REGION --query 'QueueUrls' --output text
echo "SNS topics:"
awslocal sns list-topics --region $REGION --query 'Topics[*].TopicArn' --output text
echo "DynamoDB tables:"
awslocal dynamodb list-tables --region $REGION --query 'TableNames' --output text
echo "Lambdas:"
awslocal lambda list-functions --region $REGION --query 'Functions[*].FunctionName' --output text
