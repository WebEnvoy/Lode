# Evidence Map

| Evidence id | Type | Source locator | Consumes | Binding | Freshness | Consumer boundary | Remediation direction |
| --- | --- | --- | --- | --- | --- | --- | --- |
| EV-001 | behavior_evidence | .loom/specs/LODE-156/spec.md | Scenario 1 Scenario 2 Scenario 3 Scenario 4 / acceptance criteria | LODE-156 / repair draft and overlay/fork behavior | present | review and merge-ready evidence only | Refresh after repair, overlay/fork, package update acceptance, or validator scope changes. |
| EV-002 | test_evidence | .loom/progress/LODE-156.md | py_compile, single package validation, registry batch validation, git diff check | LODE-156 / local validation checks | present | review and merge-ready evidence only | Rerun local validation after metadata or validator edits. |
| EV-003 | fresh_verification_input | .loom/progress/LODE-156.md | EV-001 EV-002 | LODE-156 / latest validation summary | present | review and merge-ready evidence only | Refresh progress summary after validation changes. |
