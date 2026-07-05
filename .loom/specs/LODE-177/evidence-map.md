# Evidence Map

| Evidence id | Type | Source locator | Consumes | Binding | Freshness | Consumer boundary | Remediation direction |
| --- | --- | --- | --- | --- | --- | --- | --- |
| EV-001 | behavior_evidence | .loom/specs/LODE-177/spec.md | scenarios and acceptance criteria | LODE-177 / write-precheck package contract behavior | present | review and merge-ready evidence only | Refresh after package schema, guard, registry, or validator scope changes. |
| EV-002 | test_evidence | .loom/progress/LODE-177.md | py_compile, registry validator, diff check, Loom verify/fact-chain | LODE-177 / local validation checks | present | review and merge-ready evidence only | Rerun local validation after metadata, fixture, or validator edits. |
| EV-003 | fresh_verification_input | .loom/progress/LODE-177.md | EV-001 EV-002 | LODE-177 / latest validation summary | present | review and merge-ready evidence only | Refresh progress summary after validation changes. |
