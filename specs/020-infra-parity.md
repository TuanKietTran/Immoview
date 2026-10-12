# 020 Terraform parity

Terraform is now the intended source of truth. The initial validate-only scaffold covers the raw-ingest versioned/private S3 bucket and ingest DLQ; it does not yet claim parity with the CDK stack.

## Explicitly unverified

No `terraform plan` or `terraform apply` was run. No AWS account, credentials, resources, DNS, certificates, networking, ECS, RDS, Redis, Lambda triggers, alarms, or IAM roles were contacted or created. Full CDK parity remains open in `specs/TODO.md`.
