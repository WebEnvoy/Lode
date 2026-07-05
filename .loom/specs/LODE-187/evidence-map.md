# Evidence Map

| Evidence id | Type | Source locator | Consumes | Binding | Freshness | Consumer boundary | Remediation direction |
| --- | --- | --- | --- | --- | --- | --- | --- |
| EV-001 | behavior_evidence | .loom/specs/LODE-187/spec.md | story readiness, scope, and non-goals | LODE-187 / write-pre candidate fixture | present | review and merge-ready evidence only | Refresh after candidate, registry, or validator scope changes. |
| EV-002 | test_evidence | .loom/progress/LODE-187.md | py_compile, registry validator, diff check, Loom verify/fact-chain | LODE-187 / local validation checks | present | review and merge-ready evidence only | Rerun local validation after package asset or validator edits. |
| EV-003 | fresh_verification_input | .loom/progress/LODE-187.md | EV-001 EV-002 | LODE-187 / latest validation summary | present | review and merge-ready evidence only | Refresh progress summary after validation changes. |
