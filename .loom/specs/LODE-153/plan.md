# Plan

## Implementation Goal

- Add the first Stage 5 read-only capability catalog metadata fixture in Lode.
- Keep Lode as upstream package truth while App/Core consume refs and metadata only.

## Phases

### Phase 1

- Objective: Add package metadata and lock refs to the sample read-only package.
- Deliverable: `sites/example/read-public-page/catalog-metadata.json`, manifest updates, and package lock updates.
- Exit condition: package metadata is present and points to the same package/version/ref family.

### Phase 2

- Objective: Make the local registry and validator consume catalog metadata.
- Deliverable: `registry/local-packages.json` and `tools/lode_validate_package.py`.
- Exit condition: `python3 tools/lode_validate_package.py sites/example/read-public-page` passes.

## Validation

- `python3 tools/lode_validate_package.py sites/example/read-public-page`
- `git diff --check`
- `loom suite validate --target . --item LODE-153 --json`
- `loom suite evidence validate --target . --item LODE-153 --json`
- `loom suite carrier validate --target . --item LODE-153 --json`
- `loom fact-chain --target . --json`
- `loom verify --target . --json`

## Dependencies

- App consumes catalog metadata as fixture input.
- Core consumes package ref/version/source/lock refs as task attribution input.
- Harbor remains out of scope unless evidence refs become required.

## Ready For Review

- [x] Scope and non-goals are explicit.
- [x] Validator coverage is local and deterministic.
- [x] Lode does not store App local state, Core run truth, or Harbor runtime evidence.
