# Implementation Contract

## Write Ownership

- Allowed: `sites/boss/job-search/**`, `sites/boss/read-job-detail/**`, `sites/boss/greet-precheck/**`, `registry/local-packages.json`, `registry/local-query.fixture.json`, Lode contract docs, and LODE-241 Loom carriers.
- Forbidden: Harbor/Core/App repositories, `sources/`, `research/`, runtime execution code, login automation, real account state, raw page/network/evidence material, external-visible BOSS actions, merge, and issue closeout.

## Package Contract

- Reuse existing `lode.site-capability.manifest.v0` and validator-supported asset roles.
- Keep `job-search` and `read-job-detail` as `operation_mode: read`.
- Keep `greet-precheck` as `operation_mode: validate_only`.
- Declare real runtime requirements only as abstract Harbor/Core facts.
- Keep source and evidence material refs-only; do not inline raw runtime evidence.
- Preserve `securityId` and `encryptJobId` only as job follow-up refs in input/output contracts and fixtures, not as account/session material.
- Keep `no_submit_guard: active`, `true_write_execution: blocked`, and `external_submit: false` for greet precheck.

## Validation Contract

- `python3 tools/lode_validate_package.py sites/boss/job-search --registry-index registry/local-packages.json --json`
- `python3 tools/lode_validate_package.py sites/boss/read-job-detail --registry-index registry/local-packages.json --json`
- `python3 tools/lode_validate_package.py sites/boss/greet-precheck --registry-index registry/local-packages.json --json`
- `python3 tools/lode_validate_package.py --registry-index registry/local-packages.json --all --json`
- `PYTHONDONTWRITEBYTECODE=1 python3 -m py_compile tools/lode_validate_package.py`
- JSON readability check for touched package and registry JSON
- `git diff --check`
- `loom fact-chain --target . --json`
- `loom verify --target . --json`
- `loom suite validate --target . --item LODE-241 --json`
- `loom suite evidence validate --target . --item LODE-241 --json`
- `loom suite carrier validate --target . --item LODE-241 --json`
