# Current Status

## Derived Fact Chain View

- Item ID: LODE-268
- Goal: Freeze strict runtime-consumption truth for Xiaohongshu note detail and BOSS job detail reads.
- Scope: Lode registry truth, schema, fixture, offline validator, README index, and item-specific carriers only.
- Execution Path: work/lode-268-detail-runtime-consumption
- Workspace Entry: .
- Recovery Entry: .loom/progress/LODE-268.md
- Review Entry: .loom/reviews/LODE-268.json
- Validation Entry: detail self-test, repository validators, Python compile, JSON parse, diff check, and Loom checks.
- Closing Condition: A ready PR proves static capability truth only; downstream live evidence remains owned by Core, Harbor, and App.
- Current Checkpoint: merge
- Current Stop: Product head `88bf540` and current semantic reviews passed; PR #270 is ready except for shared carrier convergence.
- Next Step: Consume hosted merge gate, merge PR #270, and record Lode static-truth closeout without claiming live execution.
- Blockers: None recorded.
- Latest Validation Summary: 2026-07-12T01:32+08:00 passed detail self-tests, all-package validation including both runtime-consumption reports, existing read allowlist regression, runtime-boundary validation, Python compile, all-JSON parse, and diff check.
- Recovery Boundary: No browser, production page, account, session, runtime execution, write action, merge, or issue closeout.
- Current Lane: LODE-268 dual-site detail runtime-consumption truth.

## Runtime Evidence

- Run Entry: not_applicable; Lode is not a runtime runner
- Logs Entry: not_applicable
- Diagnostics Entry: not_applicable
- Verification Entry: `loom verify --target . --json`
- Lane Entry: LODE-268 static detail truth

## Sources

- Static Truth: .loom/work-items/LODE-268.md
- Dynamic Truth: .loom/progress/LODE-268.md
- Locator Truth: .loom/bootstrap/init-result.json
- Fact Chain CLI: `loom fact-chain --target . --json`
