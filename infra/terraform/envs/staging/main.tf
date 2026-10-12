module "core" {
  source      = "../.."
  environment = "staging"
  aws_region  = var.aws_region
  tags        = { Environment = "staging", ManagedBy = "terraform" }
}

variable "aws_region" {
  type    = string
  default = "ap-southeast-1"
}
