# Plan

- Suite path: minimal

## Implementation

1. Add `sample_read_package` selection and fixture binding metadata to `sites/example/read-public-page/manifest.json`.
2. Add a matching sample marker to `registry/local-packages.json`.
3. Add lifecycle wording for sample package selection as a promotion requirement and version-relevant binding.
4. Update README with the selected sample package and its boundaries.
5. Add GH-101 item-specific Loom carrier and build evidence.

## Validation

- `python3 tools/lode_validate_package.py sites/example/read-public-page --json`
- `python3 tools/lode_validate_package.py sites/example/read-public-page --registry-index registry/local-packages.json --json`
- `jq empty sites/example/read-public-page/manifest.json sites/example/read-public-page/lifecycle-metadata.json registry/local-packages.json .loom/specs/GH-101/build-evidence.json`
- `git diff --check`
- `loom doctor --target . --json`
- `loom verify --target . --json`
- `loom fact-chain --target . --json`
- `loom suite validate --target . --item GH-101 --json`
- `loom suite carrier validate --target . --item GH-101 --json`
- `loom review read --target . --item GH-101 --json`
- PR body/head readback and hosted required checks after PR creation.

## Out-of-Scope Guard

- Stop and split a follow-up if the implementation needs schema changes, fixture payload changes, validator changes, package lock changes, package manager files, external dependencies, generated outputs, App install/update behavior, hosted registry behavior, Core Run Record/result envelope behavior, runtime/live evidence, Core/Harbor/App code, Core fixture consumption behavior, or write behavior.
