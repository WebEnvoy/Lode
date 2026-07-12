# LODE-268 Evidence Map

| Evidence id | Type | Source locator | Consumes | Binding | Freshness | Consumer boundary | Remediation direction |
| --- | --- | --- | --- | --- | --- | --- | --- |
| EV-001 | behavior_evidence | registry/detail-runtime-consumption.json | Package, lock, ref, resource, failure, evidence, and post-check truth | LODE-268 static truth | present | Admission truth only; not runtime success. | Refresh after any bound asset or policy change. |
| EV-002 | contract_evidence | registry/detail-runtime-consumption.schema.json | EV-001 shape | Exact static shape | present | Schema does not execute a page. | Refresh with truth shape changes. |
| EV-003 | test_evidence | tools/validate_detail_runtime_consumption.py | EV-001 EV-002 EV-004 | Digest binding and fail-closed mutations | present | Offline Lode validation only. | Rerun after truth, fixture, or package changes. |
| EV-004 | fixture_evidence | registry/detail-runtime-consumption.fixture.json | EV-001 rejection policy | Accepted input and rejection cases | present | Synthetic contract fixture only. | Refresh when acceptance changes. |
| EV-005 | fresh_verification_input | .loom/progress/LODE-268.md | EV-001 EV-003 | Current validation summary | present | Current-head review consumes static validation only. | Refresh after implementation or head changes. |
