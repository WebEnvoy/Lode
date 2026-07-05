# LODE-156

## Static Facts

- Item ID: LODE-156
- Goal: Expose Stage 5 failure-to-repair, repair draft lifecycle, overlay/fork boundary, and package update acceptance facts for App/Core consumption.
- Scope: Batch covers Lode issues #156, #157, #158, #159, #160, #161, #162, #163, #164, #165, and #166 through refs-only repair draft and overlay/fork metadata fixtures plus offline validator checks.
- Execution Path: stage5/read-only-repair-draft-facts
- Workspace Entry: .
- Recovery Entry: .loom/progress/LODE-156.md
- Review Entry: .loom/reviews/LODE-156.json
- Validation Entry: python3 -m py_compile tools/lode_validate_package.py; python3 tools/lode_validate_package.py sites/example/read-public-page --registry-index registry/local-packages.json --json; python3 tools/lode_validate_package.py --registry-index registry/local-packages.json --all --json; git diff --check
- Closing Condition: Lode repair draft and overlay/fork facts validate locally and remain consumable as refs-only package metadata by App/Core without hosted sync, marketplace, crawler queue, runtime execution, raw evidence, or write behavior.

## Covered Work Items

- #156 define failure-to-repair mapping.
- #157 define repair draft lifecycle.
- #158 define user report, platform fix, and local override boundary.
- #159 add repair draft fixture.
- #160 define user overlay / fork / draft asset boundary.
- #161 define draft validation and promotion checks.
- #162 define private invalidation and platform report boundary.
- #163 add overlay/fork metadata fixture.
- #164 add site-change failure sample.
- #165 define repair draft to package update acceptance path.
- #166 add sensitive material exclusion checks.

## Associated Artifacts

- `.loom/work-items/LODE-156.md`
- `.loom/progress/LODE-156.md`
- `.loom/reviews/LODE-156.json`
- `.loom/specs/LODE-156/spec.md`
- `.loom/specs/LODE-156/plan.md`
- `.loom/specs/LODE-156/implementation-contract.md`
- `.loom/specs/LODE-156/evidence-map.md`
- `.loom/specs/LODE-156/task-carrier.md`
- `.loom/status/current.md`
- `sites/example/read-public-page/repair/repair-draft.fixture.json`
- `sites/example/read-public-page/repair/overlay-fork-metadata.fixture.json`
- `sites/example/read-public-page/failure-mapping.json`
- `sites/example/read-public-page/catalog-metadata.json`
- `sites/example/read-public-page/manifest.json`
- `sites/example/read-public-page/package-lock.json`
- `registry/local-packages.json`
- `tools/lode_validate_package.py`
