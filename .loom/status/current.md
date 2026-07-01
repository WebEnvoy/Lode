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
- Current Stop: PR #104 is open and semantic review artifacts are being recorded after hosted merge gate requested current-head review.
- Next Step: Commit and push GH-90 review artifacts, update PR metadata head SHA, then rerun hosted checks.
- Blockers: None recorded.
- Latest Validation Summary: Local validation passed for `jq empty sites/example/read-public-page/manifest.json .loom/bootstrap/init-result.json .loom/specs/GH-90/build-evidence.json`, `git diff --check`, `loom fact-chain --target . --json`, `loom suite validate --target . --item GH-90 --json`, and `loom suite carrier validate --target . --item GH-90 --json`. PR #104 metadata preflight/readback passed for head `8560e142aba8ca732ea3d8e38a5f55111ecd974f`; hosted checks passed except `loom-pr-merge-gate`, which blocked on missing current-head review before GH-90 review artifacts were recorded.
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
