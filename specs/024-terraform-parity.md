# 024 Terraform parity

Replaced the prior CDK implementation with shared Terraform ingest infrastructure and dev/staging/prod roots. Added private/versioned S3 raw landing, SQS DLQ, parity documentation, CI coverage, and frontend Dockerfiles.

Validation is intentionally validate-only. Terraform formatting ran; provider initialization was cancelled after network wait in this session, so `terraform validate` is not claimed here. No AWS plan/apply was performed.
