module "core" {
  source      = "../.."
  environment = "prod"
  aws_region  = var.aws_region
  tags        = { Environment = "prod", ManagedBy = "terraform" }
}

variable "aws_region" {
  type    = string
  default = "ap-southeast-1"
}
