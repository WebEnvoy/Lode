# Current Status

## Derived Fact Chain View

- Item ID: GH-95
- Goal: Define the redacted fixture format for the first low-risk read capability package, separating forbidden raw source material, normalized sample data, and source/evidence placeholder refs.
- Scope: Add `sites/example/read-public-page/fixtures/read-public-page.fixture.json`, mark the manifest fixture asset ref as present, update lifecycle lock input to include the fixture version, and keep ownership constraints limited to GH-95 fixture plus item-specific carrier files.
- Execution Path: milestone-9/redacted-fixture-format
- Workspace Entry: .
- Recovery Entry: .loom/progress/GH-95.md
- Review Entry: .loom/reviews/GH-95.json
- Validation Entry: `jq empty sites/example/read-public-page/manifest.json sites/example/read-public-page/lifecycle-metadata.json sites/example/read-public-page/fixtures/read-public-page.fixture.json`; `git diff --check`; `loom fact-chain --target . --json`; `loom suite validate --target . --item GH-95 --json`; `loom suite carrier validate --target . --item GH-95 --json`; PR body/head readback.
- Closing Condition: PR for GH-95 is merged, hosted checks are recorded, issue #95 closeout evidence is posted, and the branch/head/PR metadata agree with this carrier.
- Current Checkpoint: build
- Current Stop: GH-95 redacted fixture format implementation is locally validated on `work/GH-95-redacted-fixture`.
- Next Step: Commit the implementation, produce current-head review records, create the PR, and verify PR body/head readback.
- Blockers: None recorded.
- Latest Validation Summary: Local validation passed on 2026-07-01 for `jq empty` over manifest/lifecycle/fixture/Loom JSON, targeted `jq -e` fixture reference checks, `git diff --check`, `loom fact-chain --target . --json`, `loom suite validate --target . --item GH-95 --json`, and `loom suite carrier validate --target . --item GH-95 --json`; `loom build --target . --item GH-95 --build-evidence .loom/specs/GH-95/build-evidence.json --json` was classified as a Loom build adapter gap after direct suite and carrier validation passed.
- Recovery Boundary: Re-check if this PR adds validator CLI, post-check output, failure mapping finalization, local resolver/lock behavior, Core fixture consumption behavior, write guardrail behavior, runtime behavior, external writes, provider/profile/session fields, or changes outside GH-95 fixture format and carrier scope.
- Current Lane: build

## Runtime Evidence

- Run Entry: not_applicable
- Logs Entry: not_applicable
- Diagnostics Entry: not_applicable
- Verification Entry: .loom/progress/GH-95.md
- Lane Entry: milestone-9/redacted-fixture-format

## Sources

- Static Truth: .loom/work-items/GH-95.md
- Dynamic Truth: .loom/progress/GH-95.md
- Locator Truth: .loom/bootstrap/init-result.json
- Fact Chain CLI: loom fact-chain --target . --json

## Notes

- 2026-07-01: GH-95 became the active item for the milestone #9 redacted fixture format PR.
- 2026-07-01: Started from `origin/main` after GH-94 closeout carrier sync merged at `c6d0b963a5ecdbb522b26b7a4a22e5c522d5484f`.
- 2026-07-01: `loom resume --target . --json` correctly blocked on terminal GH-94 `closed_out`; GH-95 proceeds through a new item-specific carrier.
- 2026-07-01: First GH-95 fact-chain attempt failed because `Evidence Freshness` used the invalid value `pending_validation`; carrier was corrected to `current` and fact-chain passed.
- 2026-07-01: GH-95 local JSON/diff/fact-chain/suite/carrier validation passed before current-head review.
