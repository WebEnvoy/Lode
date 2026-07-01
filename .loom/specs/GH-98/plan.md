# Plan

- Suite path: minimal

## Implementation

1. Add the declarative failure mapping asset at `sites/example/read-public-page/failure-mapping.json`.
2. Update manifest and lifecycle metadata so the failure mapping asset is present and versioned.
3. Update fixture/output/README wording to point to GH-98 mapping coverage.
4. Extend the stdlib validator to require and validate the failure mapping asset.
5. Add GH-98 item-specific Loom carrier and build evidence.

## Validation

- `python3 tools/lode_validate_package.py sites/example/read-public-page --json`
- `PYTHONDONTWRITEBYTECODE=1 python3 -m py_compile tools/lode_validate_package.py`
- `jq empty sites/example/read-public-page/manifest.json sites/example/read-public-page/lifecycle-metadata.json sites/example/read-public-page/fixtures/read-public-page.fixture.json sites/example/read-public-page/schemas/output.schema.json sites/example/read-public-page/failure-mapping.json .loom/specs/GH-98/build-evidence.json`
- `git diff --check`
- `loom doctor --target . --json`
- `loom verify --target . --json`
- `loom fact-chain --target . --json`
- `loom suite validate --target . --item GH-98 --json`
- `loom suite carrier validate --target . --item GH-98 --json`
- `loom review read --target . --item GH-98 --json`
- PR body/head readback and hosted required checks after PR creation.

## Out-of-Scope Guard

- Stop and split a follow-up if the implementation needs external dependencies, generated schema, Core result-envelope behavior, App copy behavior, runtime/live evidence, Core/Harbor/App code, local resolver/lockfile behavior, or write behavior.
