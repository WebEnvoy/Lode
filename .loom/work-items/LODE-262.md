# LODE-262

## Static Facts

- Item ID: LODE-262
- Goal: Freeze the two proposed, lock-bound Xiaohongshu and BOSS read-operation admission entries for Harbor #245 and Core/WebEnvoy #267.
- Scope: Ownership is limited to Lode registry/capability assets, offline validators, tests, and LODE-262 Loom carriers only.
- Execution Path: work/lode-262-allowlist-correction
- Workspace Entry: .
- Recovery Entry: .loom/progress/LODE-262.md
- Review Entry: .loom/reviews/LODE-262.json
- Validation Entry: allowlist validator/self-test, package registry validator, runtime-boundary validator, py_compile, diff check, and Loom fact-chain/suite checks.
- Closing Condition: A reviewed and merged PR proves the static allowlist and fail-closed validator. This does not close a live-runtime user story or prove a site operation succeeded.

## Associated Artifacts

- `registry/runtime-consumption-allowlist.json`
- `tools/validate_runtime_consumption_allowlist.py`
- `.loom/progress/LODE-262.md`
- `.loom/specs/LODE-262/spec.md`
- `.loom/specs/LODE-262/plan.md`
- `.loom/specs/LODE-262/implementation-contract.md`
- `.loom/specs/LODE-262/evidence-map.md`
- `.loom/specs/LODE-262/task-carrier.md`
- `.loom/specs/LODE-262/build-evidence.json`
- `.loom/reviews/LODE-262.spec.json`
- `.loom/reviews/LODE-262.json`

## GitHub Binding

- Work Item: https://github.com/WebEnvoy/Lode/issues/262
- Parent FR: https://github.com/WebEnvoy/Lode/issues/261
