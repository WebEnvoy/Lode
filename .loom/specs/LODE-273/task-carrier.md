# Task Carrier

| carrier_type | carrier_locator | source_value | normalized_status | relationship | work_item_locator | breakdown_unit_locator | spec_scenario_locator | plan_phase_locator | validation_strategy_locator | provenance | freshness_rule |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| github_issue | https://github.com/WebEnvoy/Lode/issues/273 | BOSS deferred admission truth | in_progress | primary | .loom/work-items/LODE-273.md | .loom/specs/LODE-273/plan.md | .loom/specs/LODE-273/spec.md#lode-273-spec | .loom/specs/LODE-273/plan.md | .loom/specs/LODE-273/implementation-contract.md#implementation-contract | PR #274 head and validator evidence | Recheck after head, policy, schema, validator, review, gate, or issue state changes. |
