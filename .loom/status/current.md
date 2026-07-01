# Current Status

## Derived Fact Chain View

- Item ID: GH-98
- Goal: Define the sample read package failure mapping so parent FR #88 can consume `invalid_contract`, `resource_unavailable`, `site_changed`, and `empty_result` without Core/App guessing categories from scattered package text.
- Scope: Add `failure-mapping.json`, mark it present in the manifest and lifecycle metadata, align output schema/fixture/README wording, extend the stdlib validator to require and validate the failure mapping asset, and maintain GH-98 item-specific Loom carriers.
- Execution Path: milestone-9/failure-mapping
- Workspace Entry: .
- Recovery Entry: .loom/progress/GH-98.md
- Review Entry: .loom/reviews/GH-98.json
- Validation Entry: `python3 tools/lode_validate_package.py sites/example/read-public-page --json`; `PYTHONDONTWRITEBYTECODE=1 python3 -m py_compile tools/lode_validate_package.py`; `jq empty sites/example/read-public-page/manifest.json sites/example/read-public-page/lifecycle-metadata.json sites/example/read-public-page/fixtures/read-public-page.fixture.json sites/example/read-public-page/schemas/output.schema.json sites/example/read-public-page/failure-mapping.json .loom/specs/GH-98/build-evidence.json`; `git diff --check`; `loom fact-chain --target . --json`; `loom suite validate --target . --item GH-98 --json`; `loom suite carrier validate --target . --item GH-98 --json`; PR body/head readback.
- Closing Condition: PR for GH-98 is merged, hosted checks are recorded, issue #98 closeout evidence is posted, and the branch/head/PR metadata agree with this carrier.
- Current Checkpoint: build
- Current Stop: GH-98 branch `work/GH-98-failure-mapping` is implementing the failure mapping asset and validator consumption.
- Next Step: Run Loom fact-chain/suite checks, review readback, then create PR when build evidence is current.
- Blockers: None recorded.
- Latest Validation Summary: Local validation passed on 2026-07-01 for `python3 tools/lode_validate_package.py sites/example/read-public-page --json` with status `passed` and no warnings, `PYTHONDONTWRITEBYTECODE=1 python3 -m py_compile tools/lode_validate_package.py`, package/Loom JSON syntax checks, `git diff --check`, `loom doctor --target . --json`, `loom verify --target . --json`, `loom fact-chain --target . --json`, `loom suite validate --target . --item GH-98 --json`, and `loom suite carrier validate --target . --item GH-98 --json`; `loom build --target . --item GH-98 --build-evidence .loom/specs/GH-98/build-evidence.json --json` was classified as a Loom build adapter gap after direct suite and carrier validation passed.
- Recovery Boundary: Re-check if this PR adds dependencies, package manager files, Core result envelope schema, App UI copy contract, runtime/live behavior, Harbor evidence schema, local resolver/lock behavior, write guardrail behavior, external writes, provider/profile/session fields, or changes outside GH-98 package/validator/carrier scope.
- Current Lane: build

## Runtime Evidence

- Run Entry: not_applicable
- Logs Entry: not_applicable
- Diagnostics Entry: not_applicable
- Verification Entry: .loom/progress/GH-98.md
- Lane Entry: milestone-9/failure-mapping

## Sources

- Static Truth: .loom/work-items/GH-98.md
- Dynamic Truth: .loom/progress/GH-98.md
- Locator Truth: .loom/bootstrap/init-result.json
- Fact Chain CLI: loom fact-chain --target . --json

## Notes

- 2026-07-01: GH-98 became the active item for the milestone #9 failure mapping PR.
- 2026-07-01: Started from `origin/main` after GH-97 closeout carrier sync merged at `da96bfcdc46399e24bd654380a2bbe4ebe1b3e1a`.
- 2026-07-01: CodeGraph was not initialized in this worktree, so structural lookup uses `rg` and direct reads without writing `.codegraph/`.
- 2026-07-01: GH-98 keeps Core result envelope schema, App UI copy, Core fixture consumption, local resolver/lock, and write guardrail behavior deferred to later Work Items.
- 2026-07-01: `loom build` was classified as a build adapter gap because the embedded flow did not consume direct suite JSON or the already-present `ownership_constraints`; direct suite and carrier validation passed.
