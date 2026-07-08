# LODE-253

## Static Facts

- Item ID: LODE-253
- Goal: Correct Lode runtime-boundary and Core consumption contracts for FR #252.
- Scope: Covers GitHub issues #253, #254, #255, #256, and #257. Ownership is limited to Lode capability assets, repo-local registry/query fixtures, contract docs, focused validation, and this LODE-253 carrier. It does not create a runtime runner or live evidence.
- Execution Path: work/lode-253-runtime-boundary
- Workspace Entry: .
- Recovery Entry: .loom/progress/LODE-253.md
- Review Entry: .loom/reviews/LODE-253.json
- Validation Entry: focused runtime-boundary validator, package registry validator, JSON readability, py_compile, git diff --check, Loom fact-chain/verify/suite carrier checks when available.
- Closing Condition: PR #258 is reviewed, gated, merged to main, and issues #253-#257 receive post-merge closeout evidence. No issue closeout before merge.

## Covered Issues

- #253 Revise Lode closeout wording and evidence boundary.
- #254 Define Core registry consumption contract.
- #255 Calibrate Xiaohongshu read and write-precheck capability boundary.
- #256 Calibrate BOSS read and write-precheck capability boundary.
- #257 Mark write-precheck no-submit capability boundary.

## Associated Artifacts

- registry/local-packages.json
- registry/local-query.fixture.json
- docs/contracts/runtime-boundary-closeout.md
- docs/contracts/README.md
- tools/validate_runtime_boundary_contract.py
- .loom/progress/LODE-253.md
- .loom/specs/LODE-253/build-evidence.json
- .loom/specs/LODE-253/evidence-map.md
- .loom/specs/LODE-253/implementation-contract.md
- .loom/specs/LODE-253/plan.md
- .loom/specs/LODE-253/spec.md
- .loom/specs/LODE-253/task-carrier.md
