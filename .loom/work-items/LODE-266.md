# LODE-266

## Static Facts

- Item ID: LODE-266
- Goal: Freeze lock-bound validate-only runtime-consumption truth for Xiaohongshu publish-note-precheck and BOSS greet-precheck, covering #266 and #267.
- Scope: Lode registry/schema/fixture, bound package post-checks, offline validator, tests, and LODE-266 carriers only.
- Execution Path: work/lode-266-write-precheck-runtime-consumption
- Workspace Entry: .
- Recovery Entry: .loom/progress/LODE-266.md
- Review Entry: .loom/reviews/LODE-266.json
- Validation Entry: validate-only self-test, all-package validation, runtime-boundary validation, Python compile, diff check, and Loom suite checks.
- Closing Condition: A ready PR proves static validate-only consumption truth. It does not prove live runtime success and does not authorize submit/write.

## Associated Artifacts

- `registry/validate-only-runtime-consumption.json`
- `registry/validate-only-runtime-consumption.schema.json`
- `registry/validate-only-runtime-consumption.fixture.json`
- `tools/validate_validate_only_runtime_consumption.py`
- `.loom/progress/LODE-266.md`
- `.loom/specs/LODE-266/spec.md`
- `.loom/specs/LODE-266/plan.md`
- `.loom/specs/LODE-266/implementation-contract.md`
- `.loom/specs/LODE-266/evidence-map.md`
- `.loom/specs/LODE-266/task-carrier.md`
- `.loom/specs/LODE-266/build-evidence.json`

## GitHub Binding

- Anchor Work Item: https://github.com/WebEnvoy/Lode/issues/266
- Covered Work Item: https://github.com/WebEnvoy/Lode/issues/267
- Parent FR: https://github.com/WebEnvoy/Lode/issues/265
