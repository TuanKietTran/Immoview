import type { S3Event, S3Handler } from "aws-lambda";
import { GetObjectCommand, PutObjectCommand } from "@aws-sdk/client-s3";
import { PublishCommand } from "@aws-sdk/client-sns";
import sharp from "sharp";
import { s3, sns, logger } from "@real-estate/shared";
import type { PhotoProcessedEvent } from "@real-estate/shared";

const CDN_BUCKET = process.env.S3_LISTINGS_CDN!;
const SNS_PHOTO_READY_ARN = process.env.SNS_PHOTO_READY_ARN!;

const SIZES = {
  small:  { width: 400,  height: 280  },
  medium: { width: 800,  height: 560  },
  large:  { width: 1600, height: 1120 },
} as const;

export const handler: S3Handler = async (event: S3Event) => {
  logger.info("image-pipeline invoked", { record_count: event.Records.length });

  for (const record of event.Records) {
    const bucket = record.s3.bucket.name;
    const key = decodeURIComponent(record.s3.object.key.replace(/\+/g, " "));

    const parts = key.split("/");
    if (parts.length < 3) {
      logger.warn("unexpected key format — skipping", { key });
      continue;
    }
    const [listingId, photoId] = parts;

    const getResp = await s3.send(new GetObjectCommand({ Bucket: bucket, Key: key }));
    if (!getResp.Body) throw new Error(`Empty body for key ${key}`);

    const imageBuffer = Buffer.from(await getResp.Body.transformToByteArray());
    const processedKeys: Record<string, string> = {};

    for (const [sizeName, dims] of Object.entries(SIZES)) {
      const resized = await sharp(imageBuffer)
        .resize(dims.width, dims.height, { fit: "cover", position: "centre" })
        .jpeg({ quality: 82, progressive: true })
        .toBuffer();

      const destKey = `${listingId}/${photoId}/${sizeName}.jpg`;
      await s3.send(new PutObjectCommand({
        Bucket: CDN_BUCKET,
        Key: destKey,
        Body: resized,
        ContentType: "image/jpeg",
        CacheControl: "public, max-age=31536000, immutable",
      }));
      processedKeys[sizeName] = destKey;
      logger.info("image resized", { size: sizeName, dest_key: destKey, bytes: resized.length });
    }

    const payload: PhotoProcessedEvent = {
      listingId,
      photoId,
      s3KeyOriginal: key,
      s3KeySmall:  processedKeys["small"]!,
      s3KeyMedium: processedKeys["medium"]!,
      s3KeyLarge:  processedKeys["large"]!,
    };

    await sns.send(new PublishCommand({
      TopicArn: SNS_PHOTO_READY_ARN,
      Message: JSON.stringify(payload),
      Subject: "listing.photo.ready",
      MessageAttributes: {
        eventType:  { DataType: "String", StringValue: "listing.photo.ready" },
        listingId:  { DataType: "String", StringValue: listingId },
      },
    }));

    logger.info("photo pipeline complete", { listing_id: listingId, photo_id: photoId });
  }
};
