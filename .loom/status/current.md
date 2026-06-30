# Current Status

## Derived Fact Chain View

- Item ID: GH-70
- Goal: Upgrade the repository Loom workflow pin from 0.21.1 to 0.22.1.
- Scope: Update `.github/workflows/loom-check.yml` and record the minimum item-specific Loom carrier for this workflow-only maintenance PR.
- Execution Path: ci-maintenance/loom-version-pin
- Workspace Entry: .
- Recovery Entry: .loom/progress/GH-70.md
- Review Entry: .loom/reviews/GH-70.json
- Validation Entry: `git diff --check`; hosted GitHub Actions checks for PR #69.
- Closing Condition: PR #69 is merged and GH-70 contains post-merge closeout evidence.
- Current Checkpoint: merge
- Current Stop: PR #69 is ready for hosted merge gate on the GH-70 workflow-only maintenance carrier.
- Next Step: Run hosted checks for PR #69, merge after required checks pass, then record closeout evidence for GH-70.
- Blockers: None recorded.
- Latest Validation Summary: PR head 73d25b7829eb18edaf0b12a68ec1d0a02cbe3346 contains the Loom workflow pin update to 0.22.1 plus the GH-70 item-specific maintenance carrier; no product docs, product contracts, code, roadmap, issue tree, plugin cache path, or historical INIT-0001 migration changed.
- Recovery Boundary: Workflow-only maintenance; re-review if the PR changes product code, product docs, roadmap, issue tree, workflow command structure, schema/API/runtime behavior, fixtures, or `.loom` carriers beyond GH-70 status/review/progress evidence.
- Current Lane: ci-maintenance

## Runtime Evidence

- Run Entry: not_applicable
- Logs Entry: not_applicable
- Diagnostics Entry: not_applicable
- Verification Entry: .loom/progress/GH-70.md
- Lane Entry: lode-ci

## Sources

- Static Truth: .loom/work-items/GH-70.md
- Dynamic Truth: .loom/progress/GH-70.md
- Locator Truth: .loom/bootstrap/init-result.json
- Fact Chain CLI: loom fact-chain --target . --json
