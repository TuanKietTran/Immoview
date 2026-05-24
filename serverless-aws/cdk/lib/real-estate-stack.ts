import * as cdk from "aws-cdk-lib";
import { Construct } from "constructs";
import * as s3 from "aws-cdk-lib/aws-s3";
import * as sqs from "aws-cdk-lib/aws-sqs";
import * as sns from "aws-cdk-lib/aws-sns";
import * as snsSubscriptions from "aws-cdk-lib/aws-sns-subscriptions";
import * as lambda from "aws-cdk-lib/aws-lambda";
import * as lambdaEventSources from "aws-cdk-lib/aws-lambda-event-sources";
import * as dynamodb from "aws-cdk-lib/aws-dynamodb";
import * as iam from "aws-cdk-lib/aws-iam";
import * as path from "path";

export class RealEstateStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    // ── S3 Buckets ───────────────────────────────────────────────────────────

    const rawBucket = new s3.Bucket(this, "ListingsRaw", {
      bucketName: "listings-raw",
      removalPolicy: cdk.RemovalPolicy.DESTROY,
      autoDeleteObjects: true,
      cors: [{
        allowedMethods: [s3.HttpMethods.PUT, s3.HttpMethods.POST],
        allowedOrigins: ["*"],
        allowedHeaders: ["*"],
      }],
    });

    const cdnBucket = new s3.Bucket(this, "ListingsCdn", {
      bucketName: "listings-cdn",
      removalPolicy: cdk.RemovalPolicy.DESTROY,
      autoDeleteObjects: true,
      publicReadAccess: false,
    });

    // ── SNS Topics ───────────────────────────────────────────────────────────

    const photoReadyTopic = new sns.Topic(this, "ListingPhotoReady", {
      topicName: "listing-photo-ready",
      displayName: "Listing Photo Ready",
    });

    const leadCreatedTopic = new sns.Topic(this, "LeadCreated", {
      topicName: "lead-created",
      displayName: "Lead Created",
    });

    // ── SQS Queues ───────────────────────────────────────────────────────────

    const leadScoringDlq = new sqs.Queue(this, "LeadScoringDlq", {
      queueName: "lead-scoring-dlq",
      retentionPeriod: cdk.Duration.days(14),
    });

    const leadScoringQueue = new sqs.Queue(this, "LeadScoringQueue", {
      queueName: "lead-scoring",
      visibilityTimeout: cdk.Duration.seconds(90),
      deadLetterQueue: { queue: leadScoringDlq, maxReceiveCount: 3 },
    });

    // ── DynamoDB ─────────────────────────────────────────────────────────────

    const leadScoresTable = new dynamodb.Table(this, "LeadScores", {
      tableName: "lead-scores",
      partitionKey: { name: "leadId", type: dynamodb.AttributeType.STRING },
      billingMode: dynamodb.BillingMode.PAY_PER_REQUEST,
      removalPolicy: cdk.RemovalPolicy.DESTROY,
      timeToLiveAttribute: "ttl",
    });

    // ── Lambda: Image Pipeline ───────────────────────────────────────────────

    const imagePipelineFn = new lambda.Function(this, "ImagePipeline", {
      functionName: "image-pipeline",
      runtime: lambda.Runtime.NODEJS_20_X,
      handler: "handler.handler",
      code: lambda.Code.fromAsset(
        path.join(__dirname, "../../services/image-pipeline/dist")
      ),
      timeout: cdk.Duration.minutes(5),
      memorySize: 1024,
      environment: {
        S3_LISTINGS_CDN: cdnBucket.bucketName,
        SNS_PHOTO_READY_ARN: photoReadyTopic.topicArn,
        AWS_ENDPOINT_URL: process.env.AWS_ENDPOINT_URL ?? "",
      },
    });

    rawBucket.grantRead(imagePipelineFn);
    cdnBucket.grantWrite(imagePipelineFn);
    photoReadyTopic.grantPublish(imagePipelineFn);

    imagePipelineFn.addEventSource(
      new lambdaEventSources.S3EventSource(rawBucket, {
        events: [s3.EventType.OBJECT_CREATED],
      })
    );

    // ── Lambda: Lead Scoring ─────────────────────────────────────────────────

    const leadScoringFn = new lambda.Function(this, "LeadScoring", {
      functionName: "lead-scoring",
      runtime: lambda.Runtime.NODEJS_20_X,
      handler: "handler.handler",
      code: lambda.Code.fromAsset(
        path.join(__dirname, "../../services/lead-scoring/dist")
      ),
      timeout: cdk.Duration.seconds(90),
      memorySize: 256,
      environment: {
        DYNAMODB_LEAD_SCORES_TABLE: leadScoresTable.tableName,
        AWS_ENDPOINT_URL: process.env.AWS_ENDPOINT_URL ?? "",
      },
    });

    leadScoresTable.grantWriteData(leadScoringFn);
    leadScoringFn.addEventSource(
      new lambdaEventSources.SqsEventSource(leadScoringQueue, {
        batchSize: 10,
        reportBatchItemFailures: true,
      })
    );

    // ── Lambda: Notifications ────────────────────────────────────────────────

    const notificationsFn = new lambda.Function(this, "Notifications", {
      functionName: "notifications",
      runtime: lambda.Runtime.NODEJS_20_X,
      handler: "handler.handler",
      code: lambda.Code.fromAsset(
        path.join(__dirname, "../../services/notifications/dist")
      ),
      timeout: cdk.Duration.seconds(30),
      memorySize: 256,
      environment: {
        DJANGO_INTERNAL_URL: process.env.DJANGO_INTERNAL_URL ?? "http://web:8000",
        AWS_ENDPOINT_URL: process.env.AWS_ENDPOINT_URL ?? "",
      },
    });

    leadCreatedTopic.addSubscription(
      new snsSubscriptions.LambdaSubscription(notificationsFn)
    );

    // ── Outputs ──────────────────────────────────────────────────────────────

    new cdk.CfnOutput(this, "RawBucketName", { value: rawBucket.bucketName });
    new cdk.CfnOutput(this, "CdnBucketName", { value: cdnBucket.bucketName });
    new cdk.CfnOutput(this, "LeadScoringQueueUrl", { value: leadScoringQueue.queueUrl });
    new cdk.CfnOutput(this, "LeadCreatedTopicArn", { value: leadCreatedTopic.topicArn });
    new cdk.CfnOutput(this, "PhotoReadyTopicArn", { value: photoReadyTopic.topicArn });
    new cdk.CfnOutput(this, "LeadScoresTableName", { value: leadScoresTable.tableName });
  }
}
