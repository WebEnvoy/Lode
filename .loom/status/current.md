# Current Status

## Derived Fact Chain View

- Item ID: GH-37
- Goal: Docs-only 收敛 Capability package minimum format v0，覆盖 GH-37 manifest/目录结构、GH-38 identity/operation/family/tags、GH-39 lifecycle/version/deprecation/invalidation。
- Scope: docs-only; update `docs/adr/0002-capability-package-minimum-format.md` and item-specific GH-37 Loom carrier files.
- Execution Path: docs-only/contract
- Workspace Entry: .
- Recovery Entry: .loom/progress/GH-37.md
- Review Entry: .loom/reviews/GH-37.json
- Validation Entry: `git diff --check`; low-cost repo checks; `loom doctor --target . --json`; `loom verify --target . --json`; `loom fact-chain --target . --json`; hosted checks after PR creation
- Closing Condition: PR ready against `main`; do not merge and do not close GH-36/GH-37/GH-38/GH-39 in this lane.
- Current Checkpoint: build_ready_for_pr
- Current Stop: Docs-only v0 contract recorded in ADR 0002; PR ready is the target, not merge-ready.
- Next Step: Commit, push, open PR to `main`, and record hosted check status.
- Blockers: Relative `--target .` can bind Loom commands to the global package; use absolute repo target. Fact-chain based `loom fact-chain` / `loom build` blocks because the fact-chain still expects GH-19 while this status surface records GH-37. See .loom/progress/GH-37.md.
- Latest Validation Summary: `git diff --check`, `git diff --cached --check`, Markdown file existence check, absolute-target `loom doctor`, `loom verify`, `loom suite validate`, and `loom suite carrier validate` pass.
- Recovery Boundary: Keep this lane docs-only. Do not create real capability package, schema, fixture, validator, registry, merge, or issue closeout.
- Current Lane: Stage 2 Lode package format docs-only

## Runtime Evidence

- Run Entry: not_applicable
- Logs Entry: not_applicable
- Diagnostics Entry: not_applicable
- Verification Entry: loom verify --target . --json
- Lane Entry: not_applicable

## Sources

- Static Truth: .loom/work-items/GH-37.md
- Dynamic Truth: .loom/progress/GH-37.md
- Locator Truth: .loom/bootstrap/init-result.json
- Fact Chain CLI: loom fact-chain --target . --json
