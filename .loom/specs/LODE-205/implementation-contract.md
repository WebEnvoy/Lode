# Implementation Contract

## Write Ownership

- Allowed: Lode package assets under `sites/xiaohongshu/**`, repo-local registry files, Lode docs, and LODE-205 Loom carriers.
- Forbidden: Harbor/Core/App repositories, `sources/`, `research/`, runtime execution code, login automation, real account state, raw page/network/evidence material, and external-visible Xiaohongshu actions.

## Package Contract

- Use existing `lode.site-capability.manifest.v0` and validator-supported asset roles.
- Keep both packages `operation_mode: read`.
- Declare real runtime requirements only as abstract Harbor facts.
- Mark real page validation as `pending_human_runtime` when no logged-in browser session is available.
- Preserve `xsec_token` only as a signed note-ref field in input/output contracts and fixtures; do not store account/session material.

## Validation Contract

- `python3 tools/lode_validate_package.py sites/xiaohongshu/search-notes --registry-index registry/local-packages.json --json`
- `python3 tools/lode_validate_package.py sites/xiaohongshu/read-note-detail --registry-index registry/local-packages.json --json`
- `python3 tools/lode_validate_package.py --registry-index registry/local-packages.json --all --json`
- `python3 -m py_compile tools/lode_validate_package.py`
- `git diff --check`
- `loom verify --target . --json`
- `loom fact-chain --target . --json`
