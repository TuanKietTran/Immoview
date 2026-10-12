variable "name" { type = string }
variable "tags" {
  type    = map(string)
  default = {}
}

resource "aws_s3_bucket" "raw" {
  bucket        = "${var.name}-raw-ingest"
  force_destroy = false
  tags          = var.tags
}

resource "aws_s3_bucket_public_access_block" "raw" {
  bucket                  = aws_s3_bucket.raw.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_versioning" "raw" {
  bucket = aws_s3_bucket.raw.id
  versioning_configuration { status = "Enabled" }
}

resource "aws_sqs_queue" "dlq" {
  name                      = "${var.name}-ingest-dlq"
  message_retention_seconds = 1209600
  tags                      = var.tags
}

output "raw_bucket" { value = aws_s3_bucket.raw.bucket }
output "dlq_arn" { value = aws_sqs_queue.dlq.arn }
