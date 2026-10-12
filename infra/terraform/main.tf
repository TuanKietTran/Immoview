terraform {
  required_version = ">= 1.8.0"
  required_providers { aws = { source = "hashicorp/aws", version = "~> 6.0" } }
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

module "ingest" {
  source = "./modules/ingest"
  name   = "immoview-${var.environment}"
  tags   = var.tags
}

output "raw_ingest_bucket" { value = module.ingest.raw_bucket }
output "ingest_dlq_arn" { value = module.ingest.dlq_arn }
