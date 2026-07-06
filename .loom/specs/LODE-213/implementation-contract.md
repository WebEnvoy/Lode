# Implementation Contract

## Write Ownership

- Allowed: Lode package assets under `sites/xiaohongshu/publish-note-precheck/**` and `sites/boss/greet-precheck/**`, repo-local registry files, Lode docs, and LODE-213 Loom carriers.
- Forbidden: Harbor/Core/App repositories, `sources/`, `research/`, runtime execution code, login automation, real account state, raw page/network/evidence material, and external-visible Xiaohongshu or BOSS actions.

## Package Contract

- Use existing `lode.site-capability.manifest.v0` and validator-supported asset roles.
- Keep both packages `operation_mode: validate_only`.
- Declare real runtime requirements only as abstract Harbor facts.
- Mark real page validation as pending human runtime when no logged-in browser session is available.
- Preserve Xiaohongshu publish/editor target refs and BOSS job/recruiter refs only as write-precheck target references; do not store account/session material.
- Keep `no_submit_guard: active` and `true_write_execution: blocked` in registry and fixtures.

## Validation Contract

- `python3 tools/lode_validate_package.py sites/xiaohongshu/publish-note-precheck --registry-index registry/local-packages.json --json`
- `python3 tools/lode_validate_package.py sites/boss/greet-precheck --registry-index registry/local-packages.json --json`
- `python3 tools/lode_validate_package.py --registry-index registry/local-packages.json --all --json`
- `PYTHONDONTWRITEBYTECODE=1 python3 -m py_compile tools/lode_validate_package.py`
- sensitive-material key scan for new write-precheck packages and registry entries
- `git diff --check`
- `loom verify --target . --json`
- `loom fact-chain --target . --json`
- `loom suite validate --target . --item LODE-213 --json`
- `loom suite evidence validate --target . --item LODE-213 --json`
- `loom suite carrier validate --target . --item LODE-213 --json`
