# Evidence Map

| Evidence id | Type | Source locator | Consumes | Binding | Freshness | Consumer boundary | Remediation direction |
| --- | --- | --- | --- | --- | --- | --- | --- |
| EV-001 | behavior_evidence | .loom/specs/LODE-149/spec.md | scenarios and acceptance criteria | LODE-149 / read capability asset behavior | present | review and merge-ready evidence only | Refresh after schema, fixture, catalog, registry, or validator scope changes. |
| EV-002 | test_evidence | .loom/progress/LODE-149.md | py_compile, registry validator, query fixture checks, diff check | LODE-149 / local validation checks | present | review and merge-ready evidence only | Rerun local validation after metadata or validator edits. |
| EV-003 | fresh_verification_input | .loom/progress/LODE-149.md | EV-001 EV-002 | LODE-149 / latest validation summary | present | review and merge-ready evidence only | Refresh progress summary after validation changes. |
