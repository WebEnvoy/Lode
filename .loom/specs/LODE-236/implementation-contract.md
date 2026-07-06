# Implementation Contract

## Write Ownership

- Allowed: `sites/xiaohongshu/search-notes/**`, `sites/xiaohongshu/read-note-detail/**`, `sites/xiaohongshu/publish-note-precheck/**`, `registry/local-packages.json`, `registry/local-query.fixture.json`, Lode contract docs, and LODE-236 Loom carriers.
- Forbidden: Harbor/Core/App repositories, `sources/`, `research/`, runtime execution code, login automation, real account state, raw page/network/evidence material, external-visible Xiaohongshu actions, merge, and issue closeout.

## Package Contract

- Reuse existing `lode.site-capability.manifest.v0` and validator-supported asset roles.
- Keep `search-notes` and `read-note-detail` as `operation_mode: read`.
- Keep `publish-note-precheck` as `operation_mode: validate_only`.
- Declare real runtime requirements only as abstract Harbor/Core facts.
- Keep source and evidence material refs-only; do not inline raw runtime evidence.
- Preserve `xsec_token` only as a signed note-ref field in input/output contracts and fixtures, not as account/session material.
- Keep `no_submit_guard: active`, `true_write_execution: blocked`, and `external_submit: false` for publish precheck.

## Validation Contract

- `python3 tools/lode_validate_package.py sites/xiaohongshu/search-notes --registry-index registry/local-packages.json --json`
- `python3 tools/lode_validate_package.py sites/xiaohongshu/read-note-detail --registry-index registry/local-packages.json --json`
- `python3 tools/lode_validate_package.py sites/xiaohongshu/publish-note-precheck --registry-index registry/local-packages.json --json`
- `python3 tools/lode_validate_package.py --registry-index registry/local-packages.json --all --json`
- `python3 -m py_compile tools/lode_validate_package.py`
- JSON readability check for touched package and registry JSON
- `git diff --check`
- `loom fact-chain --target . --json`
- `loom verify --target . --json`
- `loom suite validate --target . --item LODE-236 --json`
- `loom suite evidence validate --target . --item LODE-236 --json`
- `loom suite carrier validate --target . --item LODE-236 --json`
