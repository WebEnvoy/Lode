# Plan

## Implementation Goal

- Complete the Lode lifecycle facts needed by App #134 and Core #145 without expanding beyond Stage 5 read-only capability productization.

## Phases

### Phase 1

- Objective: Add lifecycle and rollback facts to the sample read-only package.
- Deliverable: `lifecycle-metadata.json`, `package-lock.json`, `catalog-metadata.json`, and manifest metadata updates.
- Exit condition: package metadata exposes lifecycle state vocabulary, compatibility range, and previous-known-good refs.

### Phase 2

- Objective: Make repo-local registry and validator consume those facts.
- Deliverable: `registry/local-packages.json`, `tools/lode_validate_package.py`, and README command update.
- Exit condition: single-package and registry batch validator commands pass.

## Validation

- `python3 -m py_compile tools/lode_validate_package.py`
- `python3 tools/lode_validate_package.py sites/example/read-public-page --registry-index registry/local-packages.json --json`
- `python3 tools/lode_validate_package.py --registry-index registry/local-packages.json --all --json`
- `git diff --check`
- `loom suite validate --target . --item LODE-145 --json`
- `loom suite evidence validate --target . --item LODE-145 --json`
- `loom suite carrier validate --target . --item LODE-145 --json`
- `loom fact-chain --target . --json`
- `loom verify --target . --json`

## Dependencies

- App #134 can display lifecycle/rollback facts from Lode catalog/registry refs.
- Core #145 can consume lifecycle/rollback refs for admission and failure attribution.
- Harbor remains out of scope because this batch does not store or inspect runtime evidence payloads.

## Ready For Review

- [x] Scope and non-goals are explicit.
- [x] Validator coverage is local and deterministic.
- [x] Lode remains package truth owner only.
