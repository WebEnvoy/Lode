# LODE-266 Evidence Map

| Evidence id | Type | Source locator | Consumes | Binding | Freshness | Consumer boundary | Remediation direction |
| --- | --- | --- | --- | --- | --- | --- | --- |
| EV-001 | behavior_evidence | registry/validate-only-runtime-consumption.json | Package/lock/registry/post-check truth | LODE-266/#267 static truth | present | Admission identity only; not runtime success. | Refresh after any bound package or policy change. |
| EV-002 | contract_evidence | registry/validate-only-runtime-consumption.schema.json | EV-001 shape | Exact static shape | present | Schema does not execute a page. | Refresh with truth schema changes. |
| EV-003 | test_evidence | tools/validate_validate_only_runtime_consumption.py | EV-001 EV-002 EV-004 | Cross-asset binding and fail-closed mutations | present | Offline Lode validation only. | Rerun after any truth, fixture, or package change. |
| EV-004 | fixture_evidence | registry/validate-only-runtime-consumption.fixture.json | EV-001 operation identity | Accepted operations and rejection cases | present | Synthetic contract fixture only. | Refresh when acceptance or rejection cases change. |
| EV-005 | fresh_verification_input | .loom/progress/LODE-266.md | EV-001 EV-003 | Current validation summary | present | Current-head review consumes static validation only. | Refresh after each implementation or head change. |
