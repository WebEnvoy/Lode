# Implementation Contract

## Write Ownership

- Allowed: Lode package assets under `sites/boss/**`, repo-local registry files, Lode docs, and LODE-209 Loom carriers.
- Forbidden: Harbor/Core/App repositories, `sources/`, `research/`, runtime execution code, login automation, real account state, raw page/network/evidence material, and external-visible BOSS actions.

## Package Contract

- Use existing `lode.site-capability.manifest.v0` and validator-supported asset roles.
- Keep both packages `operation_mode: read`.
- Declare real runtime requirements only as abstract Harbor facts.
- Mark real page validation as `pending_human_runtime` when no logged-in browser session is available.
- Preserve `securityId` and `encryptJobId` only as search-to-detail refs in input/output contracts and fixtures; do not store account/session material.

## Validation Contract

- `python3 tools/lode_validate_package.py sites/boss/job-search --registry-index registry/local-packages.json --json`
- `python3 tools/lode_validate_package.py sites/boss/read-job-detail --registry-index registry/local-packages.json --json`
- `python3 tools/lode_validate_package.py --registry-index registry/local-packages.json --all --json`
- `python3 -m py_compile tools/lode_validate_package.py`
- `git diff --check`
- `loom verify --target . --json`
- `loom fact-chain --target . --json`
- `loom suite validate --target . --item LODE-209 --json`
- `loom suite evidence validate --target . --item LODE-209 --json`
- `loom suite carrier validate --target . --item LODE-209 --json`
