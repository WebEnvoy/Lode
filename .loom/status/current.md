# Current Status

## Derived Fact Chain View

- Item ID: GH-97
- Goal: Define the sample read package post-check output format so parent FR #88 can consume passed/failed/skipped status, reason, source refs, and evidence refs through the local validator chain.
- Scope: Add `checks/post-check.json`, mark the manifest post-check asset present, update lifecycle/fixture/README wording, extend the stdlib validator to validate the post-check output contract and fixture refs, and maintain GH-97 item-specific Loom carriers.
- Execution Path: milestone-9/post-check-output
- Workspace Entry: .
- Recovery Entry: .loom/progress/GH-97.md
- Review Entry: .loom/reviews/GH-97.json
- Validation Entry: `python3 tools/lode_validate_package.py sites/example/read-public-page --json`; `PYTHONDONTWRITEBYTECODE=1 python3 -m py_compile tools/lode_validate_package.py`; `jq empty sites/example/read-public-page/manifest.json sites/example/read-public-page/lifecycle-metadata.json sites/example/read-public-page/fixtures/read-public-page.fixture.json sites/example/read-public-page/checks/post-check.json .loom/specs/GH-97/build-evidence.json`; `git diff --check`; `loom fact-chain --target . --json`; `loom suite validate --target . --item GH-97 --json`; `loom suite carrier validate --target . --item GH-97 --json`; PR body/head readback.
- Closing Condition: PR for GH-97 is merged, hosted checks are recorded, issue #97 closeout evidence is posted, and the branch/head/PR metadata agree with this carrier.
- Current Checkpoint: build
- Current Stop: GH-97 branch `work/GH-97-post-check-output` is implementing the declarative post-check output asset and validator consumption.
- Next Step: Run local validator, static checks, suite checks, review readback, then create PR when build evidence is current.
- Blockers: None recorded.
- Latest Validation Summary: Local validation passed on 2026-07-01 for `python3 tools/lode_validate_package.py sites/example/read-public-page --json` with status `passed` and no warnings, `PYTHONDONTWRITEBYTECODE=1 python3 -m py_compile tools/lode_validate_package.py`, package/Loom JSON syntax checks, `git diff --check`, `loom doctor --target . --json`, `loom verify --target . --json`, `loom fact-chain --target . --json`, `loom suite validate --target . --item GH-97 --json`, and `loom suite carrier validate --target . --item GH-97 --json`; `loom build --target . --item GH-97 --build-evidence .loom/specs/GH-97/build-evidence.json --json` was classified as a Loom build adapter gap after direct suite and carrier validation passed.
- Recovery Boundary: Re-check if this PR adds dependencies, package manager files, a post-check runner, browser/runtime behavior, Core/Harbor/App behavior, failure mapping finalization beyond existing class names, local resolver/lock behavior, write guardrail behavior, external writes, provider/profile/session fields, or changes outside GH-97 package/validator/carrier scope.
- Current Lane: build

## Runtime Evidence

- Run Entry: not_applicable
- Logs Entry: not_applicable
- Diagnostics Entry: not_applicable
- Verification Entry: .loom/progress/GH-97.md
- Lane Entry: milestone-9/post-check-output

## Sources

- Static Truth: .loom/work-items/GH-97.md
- Dynamic Truth: .loom/progress/GH-97.md
- Locator Truth: .loom/bootstrap/init-result.json
- Fact Chain CLI: loom fact-chain --target . --json

## Notes

- 2026-07-01: GH-97 became the active item for the milestone #9 post-check output PR.
- 2026-07-01: Started from `origin/main` after GH-96 closeout carrier sync merged at `0f29a0a556b0fe18b2b096aaaf43d175bccc8df9`.
- 2026-07-01: CodeGraph was not initialized in this worktree, so structural lookup uses `rg` and direct reads without writing `.codegraph/`.
- 2026-07-01: GH-97 keeps post-check execution, failure mapping finalization, Core fixture consumption, local resolver/lock, and write guardrail behavior deferred to GH-98 through GH-103.
- 2026-07-01: `loom build` was classified as a build adapter gap because the embedded flow did not consume direct suite JSON or the already-present `ownership_constraints`; direct suite and carrier validation passed.
