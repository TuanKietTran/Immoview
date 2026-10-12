terraform {
  required_version = ">= 1.8.0"
  required_providers { aws = { source = "hashicorp/aws", version = "~> 6.0" } }
}
provider "aws" { region = var.aws_region }
variable "aws_region" {
  type    = string
  default = "ap-southeast-1"
}
module "app" {
  source = "../../modules/ingest"
  name   = "immoview-prod"
  tags   = { service = "immoview", environment = "prod", managed_by = "terraform" }
}
output "raw_ingest_bucket" { value = module.app.raw_bucket }
output "ingest_dlq_arn" { value = module.app.dlq_arn }
