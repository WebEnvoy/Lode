# LODE-156 Progress

## Dynamic Facts

- Item ID: LODE-156
- Current Checkpoint: closeout_retired
- Current Stop: Repair draft facts batch is merged and the current pointer retire PR returns the repo to no_active_item.
- Next Step: Merge retire PR after hosted gate.
- Blockers: None recorded.
- Latest Validation Summary: loom fact-chain --target . --json; loom verify --target . --json; git diff --check passed locally before retire PR. Loom verify reports Codex plugin runtime cache stale while CLI/source payload is 0.28.0; treated as host runtime cache surface, not repo code.
- Recovery Boundary: Lode package repair metadata and validator only; no hosted registry, marketplace, Core run truth, App install truth, Harbor runtime/session/evidence payload, private browser material, or Stage 6 write behavior.
- Current Lane: stage5 Lode repair draft facts

## Execution Ledger

- Ledger Binding: recovery_entry
- Plan Locator: .loom/specs/LODE-156/plan.md
- Acceptance Locator: .loom/specs/LODE-156/spec.md
- Validation Evidence Locator: .loom/specs/LODE-156/evidence-map.md
- Handoff Notes Locator: .loom/specs/LODE-156/task-carrier.md
- Evidence Freshness: current
