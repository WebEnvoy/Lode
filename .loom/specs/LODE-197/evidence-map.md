# Evidence Map

| Evidence id | Type | Source locator | Consumes | Binding | Freshness | Consumer boundary | Remediation direction |
| --- | --- | --- | --- | --- | --- | --- | --- |
| EV-001 | behavior_evidence | .loom/specs/LODE-197/spec.md | story readiness, scope, non-goals, and suite path | LODE-197 / site knowledge selection behavior | present | review and merge-ready evidence only | Refresh after scope, hierarchy, or first-task boundary changes. |
| EV-002 | test_evidence | .loom/progress/LODE-197.md | local diff/readability/package-validator/Loom validation summary | LODE-197 / local validation checks | present | review and merge-ready evidence only | Rerun local validation after doc or carrier edits. |
| EV-003 | fresh_verification_input | .loom/progress/LODE-197.md | EV-001 EV-002 | LODE-197 / latest validation summary | present | review and merge-ready evidence only | Refresh progress summary after validation changes. |
