terraform {
  required_version = ">= 1.8.0"
  required_providers {
    aws = { source = "hashicorp/aws", version = "~> 6.0" }
  }
}

provider "aws" {
  region = var.aws_region
  default_tags { tags = var.tags }
}

variable "aws_region" { type = string }
variable "environment" { type = string }
variable "tags" {
  type    = map(string)
  default = {}
}

resource "aws_s3_bucket" "raw_ingest" {
  bucket        = "immoview-${var.environment}-raw-ingest"
  force_destroy = false
}

resource "aws_s3_bucket_public_access_block" "raw_ingest" {
  bucket                  = aws_s3_bucket.raw_ingest.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_versioning" "raw_ingest" {
  bucket = aws_s3_bucket.raw_ingest.id
  versioning_configuration { status = "Enabled" }
}

resource "aws_sqs_queue" "ingest_dlq" {
  name                      = "immoview-${var.environment}-ingest-dlq"
  message_retention_seconds = 1209600
}

output "raw_ingest_bucket" { value = aws_s3_bucket.raw_ingest.bucket }
output "ingest_dlq_arn" { value = aws_sqs_queue.ingest_dlq.arn }
