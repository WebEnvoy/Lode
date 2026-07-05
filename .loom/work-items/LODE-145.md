# LODE-145

## Static Facts

- Item ID: LODE-145
- Goal: Expose Stage 5 read-only capability lifecycle, lock, rollback, and registry validation facts for App/Core consumption.
- Scope: Batch covers Lode issues #145, #146, #147, #148, and #152 through the sample read-only package lifecycle metadata, package lock, catalog metadata, repo-local registry, and offline validator.
- Execution Path: stage5/read-only-capability-lifecycle-facts
- Workspace Entry: .
- Recovery Entry: .loom/progress/LODE-145.md
- Review Entry: .loom/reviews/LODE-145.json
- Validation Entry: python3 tools/lode_validate_package.py sites/example/read-public-page --registry-index registry/local-packages.json --json; python3 tools/lode_validate_package.py --registry-index registry/local-packages.json --all --json; git diff --check
- Closing Condition: Lode lifecycle/version/lock/rollback facts validate locally and remain consumable as refs only by App/Core without hosted registry, runtime execution, or private evidence storage.

## Covered Work Items

- #145 define read capability version, lock, and compatibility semantics.
- #146 define active, suspected-broken, broken, and deprecated lifecycle states.
- #147 add rollback and previous-known-good metadata.
- #148 update local registry lifecycle fields.
- #152 extend validator for multi-package checks.

## Associated Artifacts

- `.loom/work-items/LODE-145.md`
- `.loom/progress/LODE-145.md`
- `.loom/reviews/LODE-145.json`
- `.loom/specs/LODE-145/spec.md`
- `.loom/specs/LODE-145/plan.md`
- `.loom/specs/LODE-145/implementation-contract.md`
- `.loom/specs/LODE-145/evidence-map.md`
- `.loom/specs/LODE-145/task-carrier.md`
- `.loom/status/current.md`
- `sites/example/read-public-page/lifecycle-metadata.json`
- `sites/example/read-public-page/package-lock.json`
- `sites/example/read-public-page/catalog-metadata.json`
- `sites/example/read-public-page/manifest.json`
- `registry/local-packages.json`
- `tools/lode_validate_package.py`
- `README.md`
