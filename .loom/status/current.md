# Current Status

## Derived Fact Chain View

- Item ID: LODE-145
- Goal: Expose Stage 5 read-only capability lifecycle, lock, rollback, and registry validation facts for App/Core consumption.
- Scope: Batch covers Lode issues #145, #146, #147, #148, and #152 through the sample read-only package lifecycle metadata, package lock, catalog metadata, repo-local registry, and offline validator.
- Execution Path: stage5/read-only-capability-lifecycle-facts
- Workspace Entry: .
- Recovery Entry: .loom/progress/LODE-145.md
- Review Entry: .loom/reviews/LODE-145.json
- Validation Entry: python3 tools/lode_validate_package.py sites/example/read-public-page --registry-index registry/local-packages.json --json; python3 tools/lode_validate_package.py --registry-index registry/local-packages.json --all --json; git diff --check
- Closing Condition: Lode lifecycle/version/lock/rollback facts validate locally and remain consumable as refs only by App/Core without hosted registry, runtime execution, or private evidence storage.
- Current Checkpoint: implemented
- Current Stop: Lifecycle/version/rollback registry facts and validator checks are implemented locally.
- Next Step: Run full local validation, commit, push PR, then consume hosted gate before merge.
- Blockers: None recorded.
- Latest Validation Summary: python3 -m py_compile tools/lode_validate_package.py; python3 tools/lode_validate_package.py sites/example/read-public-page --registry-index registry/local-packages.json --json; python3 tools/lode_validate_package.py --registry-index registry/local-packages.json --all --json; git diff --check passed locally before PR.
- Recovery Boundary: Lode package lifecycle metadata and validator only; no hosted registry, marketplace, Core run truth, App install truth, Harbor runtime/session/evidence payload, or Stage 6 write behavior.
- Current Lane: stage5 Lode lifecycle facts

## Runtime Evidence

- Run Entry: .loom/progress/LODE-145.md
- Logs Entry: local terminal validation
- Diagnostics Entry: .loom/specs/LODE-145/evidence-map.md
- Verification Entry: loom verify --target . --json
- Lane Entry: not_applicable

## Sources

- Static Truth: .loom/work-items/LODE-145.md
- Dynamic Truth: .loom/progress/LODE-145.md
- Locator Truth: .loom/bootstrap/init-result.json
- Fact Chain CLI: loom fact-chain --target . --json
