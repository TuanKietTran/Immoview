# TODO

## Open (ordered)
- [ ] Phase 0: upgrade runtime/dependencies, PostGIS compose, secure settings, dev tooling, seed_demo, CI
- [ ] Phase 1: listing lifecycle/moderation and Vietnam-specific fields (lifecycle state machine and VND invariant started; moderation/address fields open)
- [ ] Phase 1: search, agencies, leads, valuations, billing and reliability primitives
- [ ] Phase 2: pluggable ingress, administrative aliases, land-price/statistics connectors, lawful bulk import, fixtures and throughput test
- [ ] Phase 3: Terraform modules/envs, Docker hardening, CI validation and parity document (validate-only scaffold passes; parity open)
- [ ] Final verification: tests/lint/typecheck/build, specs/FINAL.md, commit and push all milestones

## Done
- [x] Read and committed the commander brief before implementation
- [x] Recorded Phase 0 baseline evidence in `specs/001-baseline.md`

## Blocked or unverified
- [ ] Live Vietnamese portals and payment providers: no credentials/partner access; only docs/fixtures may be verified
- [ ] AWS: intentionally not planned/applied; Terraform validation only
