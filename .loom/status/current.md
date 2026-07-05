# Current Status

## Derived Fact Chain View

- Item ID: LODE-182
- Goal: Express expected change, risk hints, preview post-check, and preview failure classes for Stage 6 write-precheck packages.
- Scope: Covers Lode #182/#183/#184/#185 under FR #181; excludes true writes, marketplace, hosted sync, generic workflow runtime, Core preview envelopes, Harbor evidence bodies, and App UI.
- Execution Path: work/lode-182-expected-change-preview
- Workspace Entry: .
- Recovery Entry: .loom/progress/LODE-182.md
- Review Entry: .loom/reviews/LODE-182.json
- Validation Entry: python3 -m py_compile tools/lode_validate_package.py; python3 tools/lode_validate_package.py --registry-index registry/local-packages.json --all --json; git diff --check
- Closing Condition: PR merged, #182/#183/#184/#185/#181 closeout evidence posted, and current pointer remains no_active_item.
- Current Checkpoint: implementation_validated
- Current Stop: expected change schema, risk hint taxonomy, preview post-check, and preview failure classes are implemented locally.
- Next Step: Create PR and run hosted gate.
- Blockers: None recorded.
- Latest Validation Summary: `python3 -m py_compile tools/lode_validate_package.py`; `python3 tools/lode_validate_package.py --registry-index registry/local-packages.json --all --json`; `git diff --check`; `loom verify --target . --json`; `loom fact-chain --target . --json`; `loom suite validate --target . --item LODE-182 --json`; `loom suite evidence validate --target . --item LODE-182 --json`; `loom suite carrier validate --target . --item LODE-182 --json` passed locally.
- Recovery Boundary: Lode package/schema/fixture truth only; no true writes, hosted sync, marketplace, runtime execution, Core run truth, App UI, or Harbor private material.
- Current Lane: stage6 expected change preview semantics

## Runtime Evidence

- Run Entry: not_applicable
- Logs Entry: not_applicable
- Diagnostics Entry: not_applicable
- Verification Entry: loom verify --target . --json
- Lane Entry: .loom/specs/LODE-182/task-carrier.md

## Sources

- Static Truth: .loom/work-items/LODE-182.md
- Dynamic Truth: .loom/progress/LODE-182.md
- Locator Truth: .loom/bootstrap/init-result.json
- Fact Chain CLI: loom fact-chain --target . --json
