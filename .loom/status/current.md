# Current Status

## Derived Fact Chain View

- Item ID: GH-90
- Goal: Define the first sample read package manifest instance with package identity, operation, family, tags, and entrypoint/ref.
- Scope: Add the minimum proposed `site-capability` manifest for the reserved-domain sample read package and record item-specific GH-90 Loom carrier evidence.
- Execution Path: milestone-9/read-package-manifest
- Workspace Entry: .
- Recovery Entry: .loom/progress/GH-90.md
- Review Entry: .loom/reviews/GH-90.json
- Validation Entry: `jq empty sites/example/read-public-page/manifest.json`; `git diff --check`; `loom fact-chain --target . --json`; `loom suite validate --target . --item GH-90 --json`; `loom suite carrier validate --target . --item GH-90 --json`; PR body/head readback.
- Closing Condition: PR for GH-90 is merged, hosted checks are recorded, issue #90 closeout evidence is posted, and the branch/head/PR metadata agree with this carrier.
- Current Checkpoint: build
- Current Stop: PR #104 is open; hosted gate run `28532434367` was classified as post-review work-item carrier drift, and review/status carrier evidence is being refreshed without implementation changes.
- Next Step: Commit and push the carrier-only review/status refresh, update PR metadata Head SHA, then rerun hosted checks.
- Blockers: None recorded.
- Latest Validation Summary: Local validation passed for `jq empty sites/example/read-public-page/manifest.json .loom/bootstrap/init-result.json .loom/specs/GH-90/build-evidence.json .loom/reviews/GH-90.json .loom/reviews/GH-90.spec.json`, `git diff --check`, `loom fact-chain --target . --json`, `loom suite validate --target . --item GH-90 --json`, `loom suite carrier validate --target . --item GH-90 --json`, and `loom review read --target . --item GH-90 --json` at head `f024e6231bfac4c30b4f40d29a8cd5247f2a3e79`. Hosted PR #104 checks passed except `loom-pr-merge-gate` on run `28532434367`, classified as post-review work-item carrier drift; this carrier-only update only refreshes review/status/progress/spec-review evidence for the existing manifest scope.
- Recovery Boundary: Re-check if this PR adds schema files, fixtures, validator code, registry behavior, runtime behavior, external writes, or changes outside GH-90 manifest/carrier scope.
- Current Lane: implementation

## Runtime Evidence

- Run Entry: not_applicable
- Logs Entry: not_applicable
- Diagnostics Entry: not_applicable
- Verification Entry: .loom/progress/GH-90.md
- Lane Entry: milestone-9/read-package-manifest

## Sources

- Static Truth: .loom/work-items/GH-90.md
- Dynamic Truth: .loom/progress/GH-90.md
- Locator Truth: .loom/bootstrap/init-result.json
- Fact Chain CLI: loom fact-chain --target . --json

## Notes

- 2026-07-01: GH-90 became the active item for the first milestone #9 implementation PR.
- 2026-07-01: Hosted run `28532434367` failed only `loom-pr-merge-gate`; failure was classified as review evidence stale because `.loom/work-items/GH-90.md` changed after reviewed head `8560e142aba8ca732ea3d8e38a5f55111ecd974f`.
