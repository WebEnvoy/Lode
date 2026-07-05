# Current Status

## Derived Fact Chain View

- Item ID: LODE-156
- Goal: Expose Stage 5 failure-to-repair, repair draft lifecycle, overlay/fork boundary, and package update acceptance facts for App/Core consumption.
- Scope: Batch covers Lode issues #156, #157, #158, #159, #160, #161, #162, #163, #164, #165, and #166 through refs-only repair draft and overlay/fork metadata fixtures plus offline validator checks.
- Execution Path: stage5/read-only-repair-draft-facts
- Workspace Entry: .
- Recovery Entry: .loom/progress/LODE-156.md
- Review Entry: .loom/reviews/LODE-156.json
- Validation Entry: python3 -m py_compile tools/lode_validate_package.py; python3 tools/lode_validate_package.py sites/example/read-public-page --registry-index registry/local-packages.json --json; python3 tools/lode_validate_package.py --registry-index registry/local-packages.json --all --json; git diff --check
- Closing Condition: Lode repair draft and overlay/fork facts validate locally and remain consumable as refs-only package metadata by App/Core without hosted sync, marketplace, crawler queue, runtime execution, raw evidence, or write behavior.
- Current Checkpoint: implemented
- Current Stop: Repair draft, overlay/fork, and sensitive material boundary facts are implemented locally.
- Next Step: Run full local validation, commit, push PR, then consume hosted gate before merge.
- Blockers: None recorded.
- Latest Validation Summary: python3 -m py_compile tools/lode_validate_package.py; python3 tools/lode_validate_package.py sites/example/read-public-page --registry-index registry/local-packages.json --json; python3 tools/lode_validate_package.py --registry-index registry/local-packages.json --all --json; git diff --check; loom suite validate --target . --item LODE-156 --json; loom suite evidence validate --target . --item LODE-156 --json; loom suite carrier validate --target . --item LODE-156 --json; loom fact-chain --target . --json; loom verify --target . --json passed locally before PR. Loom verify reports Codex plugin runtime cache stale while CLI/source payload is 0.28.0; treated as host runtime cache surface, not repo code.
- Recovery Boundary: Lode package repair metadata and validator only; no hosted registry, marketplace, Core run truth, App install truth, Harbor runtime/session/evidence payload, private browser material, or Stage 6 write behavior.
- Current Lane: stage5 Lode repair draft facts

## Runtime Evidence

- Run Entry: .loom/progress/LODE-156.md
- Logs Entry: local terminal validation
- Diagnostics Entry: .loom/specs/LODE-156/evidence-map.md
- Verification Entry: loom verify --target . --json
- Lane Entry: not_applicable

## Sources

- Static Truth: .loom/work-items/LODE-156.md
- Dynamic Truth: .loom/progress/LODE-156.md
- Locator Truth: .loom/bootstrap/init-result.json
- Fact Chain CLI: loom fact-chain --target . --json
