# CDK to Terraform parity

Terraform now owns the ingest infrastructure previously represented by `serverless-aws/cdk`: versioned private S3 raw landing and SQS ingest DLQ, with dev/staging/prod environment roots and shared module.

Parity is structural and validation-only. No AWS credentials are available in this session; no plan/apply or remote resource inspection was performed. Terraform formatting and `terraform validate` are the verification boundary.
