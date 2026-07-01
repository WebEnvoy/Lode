# Plan

- Suite path: minimal

## Implementation

1. Add the static package lock asset at `sites/example/read-public-page/package-lock.json`.
2. Update manifest, local registry index, and lifecycle metadata so package lock identity is present and versioned.
3. Extend the stdlib validator to require and validate package lock identity, local resolution paths, locked asset refs, and invalidation behavior.
4. Update README wording to explain local lock semantics and boundaries.
5. Add GH-100 item-specific Loom carrier and build evidence.

## Validation

- `python3 tools/lode_validate_package.py sites/example/read-public-page --json`
- `python3 tools/lode_validate_package.py sites/example/read-public-page --registry-index registry/local-packages.json --json`
- `PYTHONDONTWRITEBYTECODE=1 python3 -m py_compile tools/lode_validate_package.py`
- `jq empty sites/example/read-public-page/package-lock.json sites/example/read-public-page/manifest.json sites/example/read-public-page/lifecycle-metadata.json registry/local-packages.json .loom/specs/GH-100/build-evidence.json`
- `git diff --check`
- `loom doctor --target . --json`
- `loom verify --target . --json`
- `loom fact-chain --target . --json`
- `loom suite validate --target . --item GH-100 --json`
- `loom suite carrier validate --target . --item GH-100 --json`
- `loom review read --target . --item GH-100 --json`
- PR body/head readback and hosted required checks after PR creation.

## Out-of-Scope Guard

- Stop and split a follow-up if the implementation needs package manager files, external dependencies, generated outputs, App install/update behavior, hosted registry behavior, Core Run Record/result envelope behavior, runtime/live evidence, Core/Harbor/App code, Core fixture consumption behavior, or write behavior.
