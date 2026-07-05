# Evidence Map

| Evidence id | Type | Source locator | Consumes | Binding | Freshness | Consumer boundary | Remediation direction |
| --- | --- | --- | --- | --- | --- | --- | --- |
| EV-001 | behavior_evidence | .loom/specs/LODE-145/spec.md | Scenario 1 Scenario 2 Scenario 3 / acceptance criteria | LODE-145 / lifecycle and registry facts behavior | present | review and merge-ready evidence only | Refresh after lifecycle, rollback, registry, or validator scope changes. |
| EV-002 | test_evidence | .loom/progress/LODE-145.md | py_compile, single package validation, registry batch validation, git diff check | LODE-145 / local validation checks | present | review and merge-ready evidence only | Rerun local validation after metadata or validator edits. |
| EV-003 | fresh_verification_input | .loom/progress/LODE-145.md | EV-001 EV-002 | LODE-145 / latest validation summary | present | review and merge-ready evidence only | Refresh progress summary after validation changes. |
