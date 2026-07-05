# Evidence Map

| Evidence id | Type | Source locator | Consumes | Binding | Freshness | Consumer boundary | Remediation direction |
| --- | --- | --- | --- | --- | --- | --- | --- |
| EV-001 | behavior_evidence | .loom/specs/LODE-182/spec.md | story readiness, scope, and non-goals | LODE-182 / expected change preview semantics | present | review and merge-ready evidence only | Refresh after package schema, post-check, failure mapping, or validator scope changes. |
| EV-002 | test_evidence | .loom/progress/LODE-182.md | py_compile, registry validator, diff check, Loom verify/fact-chain | LODE-182 / local validation checks | present | review and merge-ready evidence only | Rerun local validation after package asset or validator edits. |
| EV-003 | fresh_verification_input | .loom/progress/LODE-182.md | EV-001 EV-002 | LODE-182 / latest validation summary | present | review and merge-ready evidence only | Refresh progress summary after validation changes. |
