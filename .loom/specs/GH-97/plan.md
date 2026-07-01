# Plan

- Suite path: minimal

## Implementation

1. Add the declarative post-check asset under `sites/example/read-public-page/checks/`.
2. Update manifest and lifecycle metadata so the post-check asset is present and versioned.
3. Update fixture/README wording to remove the GH-97 planned-post-check placeholder.
4. Extend the stdlib validator's existing `validate_post_check` hook to validate the post-check result contract and fixture ref bindings.
5. Add GH-97 item-specific Loom carrier and build evidence.

## Validation

- `python3 tools/lode_validate_package.py sites/example/read-public-page --json`
- `PYTHONDONTWRITEBYTECODE=1 python3 -m py_compile tools/lode_validate_package.py`
- `jq empty sites/example/read-public-page/manifest.json sites/example/read-public-page/lifecycle-metadata.json sites/example/read-public-page/fixtures/read-public-page.fixture.json sites/example/read-public-page/checks/post-check.json .loom/specs/GH-97/build-evidence.json`
- `git diff --check`
- `loom doctor --target . --json`
- `loom verify --target . --json`
- `loom fact-chain --target . --json`
- `loom suite validate --target . --item GH-97 --json`
- `loom suite carrier validate --target . --item GH-97 --json`
- `loom review read --target . --item GH-97 --json`
- PR body/head readback and hosted required checks after PR creation.

## Out-of-Scope Guard

- Stop and split a follow-up if the implementation needs external dependencies, generated schema, post-check execution, runtime/live evidence, Core/Harbor/App behavior, local resolver/lockfile behavior, failure mapping finalization, or write behavior.
