# Plan

- Suite path: minimal

## Implementation

1. Add a standard-library Python CLI at `tools/lode_validate_package.py`.
2. Validate the sample package's manifest, schema refs, resource requirements, lifecycle metadata, fixture binding, forbidden fields, and planned post-check status.
3. Emit a machine-readable report with status, errors, warnings, and checked refs.
4. Document the command in `README.md`.
5. Add the validator command to the existing `repo-local-cli` hosted check.
6. Update sample package wording to reflect that GH-96 validator coverage now exists while post-check/Core consumption remain open.
7. Add GH-96 item-specific Loom carrier and review evidence.

## Validation

- `python3 tools/lode_validate_package.py sites/example/read-public-page --json`
- `PYTHONDONTWRITEBYTECODE=1 python3 -m py_compile tools/lode_validate_package.py`
- `ruby -e 'require "yaml"; YAML.load_file(".github/workflows/loom-check.yml")'`
- `jq empty sites/example/read-public-page/manifest.json sites/example/read-public-page/lifecycle-metadata.json sites/example/read-public-page/fixtures/read-public-page.fixture.json .loom/bootstrap/init-result.json .loom/specs/GH-96/build-evidence.json`
- `git diff --check`
- `loom doctor --target . --json`
- `loom verify --target . --json`
- `loom fact-chain --target . --json`
- `loom suite validate --target . --item GH-96 --json`
- `loom suite carrier validate --target . --item GH-96 --json`
- `loom review read --target . --item GH-96 --json`
- PR body/head readback and hosted required checks after PR creation.

## Out-of-Scope Guard

- Stop and split a follow-up if the implementation needs external dependencies, package manager initialization, generated reports, post-check execution, failure mapping finalization, Core/Harbor/App behavior, runtime/live evidence, or write behavior.
