# Current Status

## Derived Fact Chain View

- Item ID: GH-100
- Goal: Define package ref and lock semantics for the sample read package, including capability identity, version, lock ref, locked assets, and invalidation behavior, without implementing App install/update, hosted registry, Core Run Record, runtime, or write behavior.
- Scope: Add `sites/example/read-public-page/package-lock.json`, mark the package lock present in the manifest/local registry/lifecycle metadata, extend the stdlib validator to validate lock identity and locked asset refs, update README wording, and maintain GH-100 item-specific Loom carriers.
- Execution Path: milestone-9/package-ref-lock
- Workspace Entry: .
- Recovery Entry: .loom/progress/GH-100.md
- Review Entry: .loom/reviews/GH-100.json
- Validation Entry: `python3 tools/lode_validate_package.py sites/example/read-public-page --json`; `python3 tools/lode_validate_package.py sites/example/read-public-page --registry-index registry/local-packages.json --json`; `PYTHONDONTWRITEBYTECODE=1 python3 -m py_compile tools/lode_validate_package.py`; `jq empty sites/example/read-public-page/package-lock.json sites/example/read-public-page/manifest.json sites/example/read-public-page/lifecycle-metadata.json registry/local-packages.json .loom/specs/GH-100/build-evidence.json`; `git diff --check`; `loom fact-chain --target . --json`; `loom suite validate --target . --item GH-100 --json`; `loom suite carrier validate --target . --item GH-100 --json`; PR body/head readback.
- Closing Condition: PR for GH-100 is merged, hosted checks are recorded, issue #100 closeout evidence is posted, and the branch/head/PR metadata agree with this carrier.
- Current Checkpoint: build
- Current Stop: GH-100 branch `work/GH-100-package-ref-lock` is defining package ref / lock semantics through `package-lock.json` and validator consumption.
- Next Step: Run Loom fact-chain/suite checks, review readback, then create PR when build evidence is current.
- Blockers: None recorded.
- Latest Validation Summary: Local validation passed on 2026-07-01 for `python3 tools/lode_validate_package.py sites/example/read-public-page --json`, `python3 tools/lode_validate_package.py sites/example/read-public-page --registry-index registry/local-packages.json --json`, `PYTHONDONTWRITEBYTECODE=1 python3 -m py_compile tools/lode_validate_package.py`, package/Loom JSON syntax checks, `git diff --check`, `loom doctor --target . --json`, `loom verify --target . --json`, `loom fact-chain --target . --json`, `loom suite validate --target . --item GH-100 --json`, and `loom suite carrier validate --target . --item GH-100 --json`; both validator invocations returned status `passed` with no warnings and checked `package_lock`; `loom build --target . --item GH-100 --build-evidence .loom/specs/GH-100/build-evidence.json --json` was classified as a Loom build adapter gap after direct suite and carrier validation passed.
- Recovery Boundary: Re-check if this PR adds package manager files, dependencies, generated outputs, App install/update/pin/rollback/sync behavior, hosted registry, marketplace, runtime behavior, Core/Harbor/App behavior, Core Run Record/result envelope behavior, Core fixture consumption behavior, write guardrail behavior, external writes, provider/profile/session fields, or changes outside GH-100 package lock/validator/package metadata/carrier scope.
- Current Lane: build

## Runtime Evidence

- Run Entry: not_applicable
- Logs Entry: not_applicable
- Diagnostics Entry: not_applicable
- Verification Entry: .loom/progress/GH-100.md
- Lane Entry: milestone-9/package-ref-lock

## Sources

- Static Truth: .loom/work-items/GH-100.md
- Dynamic Truth: .loom/progress/GH-100.md
- Locator Truth: .loom/bootstrap/init-result.json
- Fact Chain CLI: loom fact-chain --target . --json

## Notes

- 2026-07-01: GH-100 became the active item for the milestone #9 package ref / lock semantics PR.
- 2026-07-01: Started from `origin/main` after GH-99 closeout carrier sync merged at `22132bdec95096a0793674a9e0c6ba14ffb8ee52`.
- 2026-07-01: CodeGraph was not initialized in this worktree, so structural lookup uses `rg` and direct reads without writing `.codegraph/`.
- 2026-07-01: GH-100 keeps Core fixture consumption and write guardrail behavior deferred to later Work Items.
- 2026-07-01: `loom build` was classified as a build adapter gap because the embedded flow did not consume direct suite JSON or the already-present `ownership_constraints`; direct suite and carrier validation passed.
