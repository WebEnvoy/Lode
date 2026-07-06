# Current Status

## Derived Fact Chain View

- Item ID: LODE-205
- Goal: Define Xiaohongshu login/page readiness and convert the real read capability batch for Lode #198.
- Scope: Covers Lode #198/#205/#206/#207/#208 and semantic stories #15/#16/#17. Ownership is limited to Lode package assets, registry fixtures, contract docs, and LODE-205 Loom carriers. Adds Xiaohongshu search and note-detail read packages, resource requirements, fixtures, post-checks, failure mapping, registry entries, and package contract docs.
- Execution Path: work/lode-198-xhs-read-capabilities
- Workspace Entry: .
- Recovery Entry: .loom/progress/LODE-205.md
- Review Entry: .loom/reviews/LODE-205.json
- Validation Entry: package validator; registry checks; py_compile; git diff --check; loom verify; loom fact-chain.
- Closing Condition: Implementation PR merged, #198/#205/#206/#207/#208 closeout evidence posted, and current pointer returns to no_active_item.
- Current Checkpoint: merge
- Current Stop: PR #221 has a controller-authored review carrier and refreshed PR metadata for the current branch head.
- Next Step: Controlled merge by the main controller, then post-merge closeout evidence for #198/#205/#206/#207/#208.
- Blockers: None recorded.
- Latest Validation Summary: `python3 tools/lode_validate_package.py sites/xiaohongshu/search-notes --registry-index registry/local-packages.json --json`; `python3 tools/lode_validate_package.py sites/xiaohongshu/read-note-detail --registry-index registry/local-packages.json --json`; `python3 tools/lode_validate_package.py --registry-index registry/local-packages.json --all --json`; `python3 -m py_compile tools/lode_validate_package.py`; `git diff --check`; `loom doctor --target . --json`; `loom verify --target . --json`; `loom fact-chain --target . --json`; `loom suite validate --target . --item LODE-205 --json`; `loom suite evidence validate --target . --item LODE-205 --json`; `loom suite carrier validate --target . --item LODE-205 --json` passed locally. Hosted py-compile, demo-bootstrap, repo-local-cli, and loom-check passed on PR #221 run 28771263137. Live Xiaohongshu page validation remains pending human-owned logged-in runtime and is not fabricated.
- Recovery Boundary: Lode package/catalog/fixture/contract truth only; no Stage 7, no Xiaohongshu write or engagement action, no login automation, no batch crawling, no captcha or safety-control bypass, no Harbor/Core/App changes, and no `sources/` or `research/` edits.
- Current Lane: FR #198 Xiaohongshu real read-only capability conversion

## Runtime Evidence

- Run Entry: .loom/progress/LODE-205.md
- Logs Entry: not_applicable
- Diagnostics Entry: not_applicable
- Verification Entry: loom verify --target . --json
- Lane Entry: .loom/specs/LODE-205/task-carrier.md

## Sources

- Static Truth: .loom/work-items/LODE-205.md
- Dynamic Truth: .loom/progress/LODE-205.md
- Locator Truth: .loom/bootstrap/init-result.json
- Fact Chain CLI: loom fact-chain --target . --json
