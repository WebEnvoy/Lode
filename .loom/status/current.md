# Current Status

## Derived Fact Chain View

- Item ID: GH-37
- Goal: Docs-only 收敛 Capability package minimum format v0，覆盖 GH-37 manifest/目录结构、GH-38 identity/operation/family/tags、GH-39 lifecycle/version/deprecation/invalidation。
- Scope: 更新 `docs/adr/0002-capability-package-minimum-format.md` 和本事项的最小 Loom carrier。
- Execution Path: docs-only/contract
- Workspace Entry: .
- Recovery Entry: .loom/progress/GH-37.md
- Review Entry: .loom/reviews/GH-37.json
- Validation Entry: `git diff --check`; low-cost repo checks; Loom local checks if available; hosted checks after PR
- Closing Condition: PR ready against `main`; do not merge and do not close GH-36/GH-37/GH-38/GH-39 in this lane.
- Current Checkpoint: merge
- Current Stop: Capability package minimum format v0 contract and current-head docs-only review are recorded for PR #56.
- Next Step: Run PR merge gate, merge PR #56 if hosted checks pass, then perform post-merge closeout.
- Blockers: None for merge-ready after hosted checks pass.
- Latest Validation Summary: `git diff --check`, `git diff --cached --check`, Markdown file existence check, `loom doctor --target /Volumes/2T/.codex/worktrees/stage2/lode-package-format --json`, `loom verify --target /Volumes/2T/.codex/worktrees/stage2/lode-package-format --json`, `loom suite validate --target /Volumes/2T/.codex/worktrees/stage2/lode-package-format --item GH-37 --json`, `loom suite carrier validate --target /Volumes/2T/.codex/worktrees/stage2/lode-package-format --item GH-37 --json`, and post-repair `loom fact-chain --target /Volumes/2T/.codex/worktrees/stage2/lode-package-format --json` pass.
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
