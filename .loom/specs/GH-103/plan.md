# Plan

- Suite path: minimal

## Implementation

1. Add the static `write-deferred-guardrail.json` asset under the sample package.
2. Expose the guardrail through manifest asset refs and sample package consumer entrypoints.
3. Lock the guardrail in `package-lock.json` and add invalidation/relock wording for guardrail changes.
4. Add the guardrail path and asset role to the repo-local registry.
5. Record lifecycle version identity, promotion requirements, and README consumer-boundary wording.
6. Extend the existing validator only enough to load and fail closed on guardrail identity and deferred/blocked boundary drift.
7. Add GH-103 item-specific Loom carriers and build evidence.

## Validation

- `python3 tools/lode_validate_package.py sites/example/read-public-page --json`
- `python3 tools/lode_validate_package.py sites/example/read-public-page --registry-index registry/local-packages.json --json`
- `PYTHONDONTWRITEBYTECODE=1 python3 -m py_compile tools/lode_validate_package.py`
- `jq empty sites/example/read-public-page/manifest.json sites/example/read-public-page/package-lock.json sites/example/read-public-page/lifecycle-metadata.json registry/local-packages.json sites/example/read-public-page/write-deferred-guardrail.json .loom/specs/GH-103/build-evidence.json`
- `jq -e '<GH-103 write guardrail structure check>' sites/example/read-public-page/write-deferred-guardrail.json`
- `git diff --check`
- `loom doctor --target . --json`
- `loom verify --target . --json`
- `loom fact-chain --target . --json`
- `loom suite validate --target . --item GH-103 --json`
- `loom suite carrier validate --target . --item GH-103 --json`
- `loom review read --target . --item GH-103 --json`
- PR body/head readback and hosted required checks after PR creation.

## Out-of-Scope Guard

- Stop and split a follow-up if the implementation needs Core/Harbor/App code, executable validate-only/draft/preview/write packages, runtime/live evidence, provider/profile/session fields, validator redesign, package manager files, generated outputs, hosted registry behavior, marketplace behavior, sync service, crawler queue, benchmark contract, or true write execution.
