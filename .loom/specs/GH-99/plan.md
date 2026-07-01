# Plan

- Suite path: minimal

## Implementation

1. Add the repo-local package index at `registry/local-packages.json`.
2. Extend the stdlib validator to discover and validate the repo-local index when present.
3. Add an explicit `--registry-index` validator option for direct local index checks.
4. Update package lifecycle/README wording to reflect GH-99 local resolution coverage.
5. Add GH-99 item-specific Loom carrier and build evidence.

## Validation

- `python3 tools/lode_validate_package.py sites/example/read-public-page --json`
- `python3 tools/lode_validate_package.py sites/example/read-public-page --registry-index registry/local-packages.json --json`
- `PYTHONDONTWRITEBYTECODE=1 python3 -m py_compile tools/lode_validate_package.py`
- `jq empty registry/local-packages.json sites/example/read-public-page/manifest.json sites/example/read-public-page/lifecycle-metadata.json .loom/specs/GH-99/build-evidence.json`
- `git diff --check`
- `loom doctor --target . --json`
- `loom verify --target . --json`
- `loom fact-chain --target . --json`
- `loom suite validate --target . --item GH-99 --json`
- `loom suite carrier validate --target . --item GH-99 --json`
- `loom review read --target . --item GH-99 --json`
- PR body/head readback and hosted required checks after PR creation.

## Out-of-Scope Guard

- Stop and split a follow-up if the implementation needs lockfile semantics, package manager files, external dependencies, generated outputs, hosted registry behavior, package installation, runtime/live evidence, Core/Harbor/App code, Core fixture consumption behavior, or write behavior.
