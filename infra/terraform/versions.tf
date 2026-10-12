terraform {
  backend "s3" {
    # Environment overlays provide the real backend configuration at deploy time.
    # Validation uses -backend=false and never contacts AWS.
  }
}
