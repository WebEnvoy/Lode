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
- Closing Condition: PR #56 merged into `main`; hosted required checks passed; issue closeout is owned by the coordinator as the next external step.
- Current Checkpoint: closed_out
- Current Stop: Post-merge carrier closeout recorded for WebEnvoy/Lode#56.
- Next Step: No further action for GH-37/GH-38/GH-39 after coordinator issue closeout comments are posted and covered issues are closed.
- Blockers: None
- Latest Validation Summary: Post-merge closeout consumed PR #56, head 8cb0e9de8e60eb874e30c913acb6f0dd020bf16a, merge commit 124da50040c97c97d40442c8b7cdeb1ab0ef4928, target branch main, and hosted run 28437893338 with all required checks passing.
- Recovery Boundary: Terminal carrier for docs-only capability package minimum format contract; open new Work Items for package/schema/fixture/validator implementation.
- Current Lane: terminal closeout

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
