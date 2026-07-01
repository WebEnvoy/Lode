# Plan

- Suite path: minimal

## Implementation

1. Add the Core-readable `core-consumption.fixture.json` asset under the sample package fixture directory.
2. Expose the new fixture through manifest asset refs and sample package consumer entrypoints.
3. Lock the new fixture in `package-lock.json` and add relock wording for fixture case changes.
4. Add the fixture path and asset role to the repo-local registry.
5. Record lifecycle version identity and README consumer-boundary wording.
6. Add GH-102 item-specific Loom carriers and build evidence.

## Validation

- `python3 tools/lode_validate_package.py sites/example/read-public-page --json`
- `python3 tools/lode_validate_package.py sites/example/read-public-page --registry-index registry/local-packages.json --json`
- `jq empty sites/example/read-public-page/manifest.json sites/example/read-public-page/package-lock.json sites/example/read-public-page/lifecycle-metadata.json registry/local-packages.json sites/example/read-public-page/fixtures/core-consumption.fixture.json .loom/specs/GH-102/build-evidence.json`
- `jq -e '<GH-102 core fixture structure check>' sites/example/read-public-page/fixtures/core-consumption.fixture.json`
- `git diff --check`
- `loom doctor --target . --json`
- `loom verify --target . --json`
- `loom fact-chain --target . --json`
- `loom suite validate --target . --item GH-102 --json`
- `loom suite carrier validate --target . --item GH-102 --json`
- `loom review read --target . --item GH-102 --json`
- PR body/head readback and hosted required checks after PR creation.

## Out-of-Scope Guard

- Stop and split a follow-up if the implementation needs Core/Harbor/App code, Core result envelope fields, runtime/live evidence, provider/profile/session fields, validator redesign, package manager files, generated outputs, hosted registry behavior, marketplace behavior, write guardrail behavior, or true write execution.
