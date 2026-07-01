# Current Status

## Derived Fact Chain View

- Item ID: GH-96
- Goal: Provide the first minimal offline validator CLI that reads the sample package, validates manifest/schema/fixture/post-check references, and emits a machine-readable report for parent FR #88.
- Scope: Add `tools/lode_validate_package.py`, document the command, wire it into the existing `repo-local-cli` hosted check, update sample package wording now that validator coverage exists, and maintain GH-96 item-specific Loom carrier files.
- Execution Path: milestone-9/validator-cli
- Workspace Entry: .
- Recovery Entry: .loom/progress/GH-96.md
- Review Entry: .loom/reviews/GH-96.json
- Validation Entry: `python3 tools/lode_validate_package.py sites/example/read-public-page --json`; `PYTHONDONTWRITEBYTECODE=1 python3 -m py_compile tools/lode_validate_package.py`; `ruby -e 'require "yaml"; YAML.load_file(".github/workflows/loom-check.yml")'`; `jq empty sites/example/read-public-page/manifest.json sites/example/read-public-page/lifecycle-metadata.json sites/example/read-public-page/fixtures/read-public-page.fixture.json`; `git diff --check`; `loom fact-chain --target . --json`; `loom suite validate --target . --item GH-96 --json`; `loom suite carrier validate --target . --item GH-96 --json`; PR body/head readback.
- Closing Condition: PR for GH-96 is merged, hosted checks are recorded, issue #96 closeout evidence is posted, and the branch/head/PR metadata agree with this carrier.
- Current Checkpoint: merge
- Current Stop: PR #118 is open for GH-96; PR body/head metadata is synced on `work/GH-96-validator-cli`, and hosted `repo-local-cli` has validated the new package validator command.
- Next Step: Push merge-checkpoint carrier sync, refresh PR body/head metadata, rerun hosted checks, and merge after gate pass.
- Blockers: None recorded.
- Latest Validation Summary: Local validation passed on 2026-07-01 for validator report shape, `PYTHONDONTWRITEBYTECODE=1 python3 -m py_compile tools/lode_validate_package.py`, workflow YAML parse, package/Loom JSON checks, `git diff --check`, `loom doctor --target . --json`, `loom verify --target . --json`, `loom fact-chain --target . --json`, `loom suite validate --target . --item GH-96 --json`, and `loom suite carrier validate --target . --item GH-96 --json`; validator returned `passed_with_warnings` with only the expected GH-97 planned post-check warning; `loom build --target . --item GH-96 --build-evidence .loom/specs/GH-96/build-evidence.json --json` was classified as a Loom build adapter gap after direct suite and carrier validation passed.
- Recovery Boundary: Re-check if this PR adds dependencies, package manager files, a full JSON Schema engine, generated outputs, post-check runner/output, failure mapping finalization, local resolver/lock behavior, Core fixture consumption behavior, write guardrail behavior, runtime behavior, external writes, provider/profile/session fields, or changes outside GH-96 validator CLI and carrier scope.
- Current Lane: merge

## Runtime Evidence

- Run Entry: not_applicable
- Logs Entry: not_applicable
- Diagnostics Entry: not_applicable
- Verification Entry: .loom/progress/GH-96.md
- Lane Entry: milestone-9/validator-cli

## Sources

- Static Truth: .loom/work-items/GH-96.md
- Dynamic Truth: .loom/progress/GH-96.md
- Locator Truth: .loom/bootstrap/init-result.json
- Fact Chain CLI: loom fact-chain --target . --json

## Notes

- 2026-07-01: GH-96 became the active item for the milestone #9 validator CLI PR.
- 2026-07-01: Started from `origin/main` after GH-95 closeout carrier sync merged at `f4d0dcf928bd161346a5a15839b9ae9663ac58f7`.
- 2026-07-01: CodeGraph was not initialized in this worktree, so structural lookup fell back to `rg --files` and direct reads without writing `.codegraph/`.
- 2026-07-01: GH-96 keeps post-check output, failure mapping finalization, Core fixture consumption, and write guardrail behavior deferred to GH-97 through GH-103.
- 2026-07-01: `loom build` was classified as a build adapter gap because the embedded flow did not consume direct suite JSON or the already-present `ownership_constraints`; direct suite and carrier validation passed.
- 2026-07-01: Added GH-96 spec and semantic review records for implementation head `20b3c1c5cb98052c5035668de354f95cbb2344cd`.
- 2026-07-01: PR #118 was created for `work/GH-96-validator-cli`; hosted run `28540145616` passed `repo-local-cli`, including the new validator command, but `loom-pr-merge-gate` blocked because the carrier still declared checkpoint `build`.
