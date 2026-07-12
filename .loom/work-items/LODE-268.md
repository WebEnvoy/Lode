# LODE-268

## Static Facts

- Item ID: LODE-268
- Goal: Correct the merged runtime-consumption truth by pinning both output schemas and freezing complete, bounded, source/evidence-bound public detail fields.
- Scope: Lode registry truth, schema, fixture, offline validator, README index, and item-specific carriers only.
- Execution Path: work/lode-268-output-truth-correction
- Workspace Entry: .
- Recovery Entry: .loom/progress/LODE-268.md
- Review Entry: .loom/reviews/LODE-268.json
- Validation Entry: detail self-test, repository validators, Python compile, JSON parse, diff check, and Loom checks.
- Closing Condition: A ready corrective PR proves complete static output truth only; downstream live evidence remains owned by Core, Harbor, and App.

## GitHub Binding

- Work Item: https://github.com/WebEnvoy/Lode/issues/268
- Parent FR: https://github.com/WebEnvoy/Lode/issues/261
- Consumers: https://github.com/WebEnvoy/Harbor/issues/252 and https://github.com/WebEnvoy/WebEnvoy/issues/270

## Associated Artifacts

- .loom/specs/LODE-268/spec.md
- .loom/specs/LODE-268/plan.md
- .loom/specs/LODE-268/implementation-contract.md
- .loom/specs/LODE-268/evidence-map.md
- .loom/specs/LODE-268/task-carrier.md
- registry/detail-runtime-consumption.json
- registry/detail-runtime-consumption.schema.json
- tools/validate_detail_runtime_consumption.py
