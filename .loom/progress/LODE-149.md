# LODE-149 Progress

## Dynamic Facts

- Item ID: LODE-149
- Current Checkpoint: merge
- Current Stop: Three read capability assets, registry query fixture, and validator checks are implemented locally.
- Next Step: Hosted gate and merge are next; post-merge closeout follows.
- Blockers: None recorded.
- Latest Validation Summary: python3 -m py_compile tools/lode_validate_package.py; python3 tools/lode_validate_package.py --registry-index registry/local-packages.json --all --json; jq registry query/candidate checks; git diff --check; loom suite validate/evidence/carrier; loom fact-chain; loom verify passed locally before PR. Loom verify reports Codex plugin runtime cache stale while CLI/source payload is 0.28.0; treated as host runtime cache surface, not repo code.
- Recovery Boundary: Lode package/catalog/lifecycle/schema/fixture truth only; no hosted registry, marketplace, runtime execution, Core run truth, App UI changes, Harbor private material, raw evidence, or Stage 6 write behavior.
- Current Lane: stage5 Lode read capability assets

## Execution Ledger

- Ledger Binding: recovery_entry
- Plan Locator: .loom/specs/LODE-149/plan.md
- Acceptance Locator: .loom/specs/LODE-149/spec.md
- Validation Evidence Locator: .loom/specs/LODE-149/evidence-map.md
- Handoff Notes Locator: .loom/specs/LODE-149/task-carrier.md
- Evidence Freshness: current
