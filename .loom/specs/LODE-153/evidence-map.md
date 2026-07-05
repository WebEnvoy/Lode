# Evidence Map

| Evidence id | Type | Source locator | Consumes | Binding | Freshness | Consumer boundary | Remediation direction |
| --- | --- | --- | --- | --- | --- | --- | --- |
| EV-001 | behavior_evidence | .loom/specs/LODE-153/spec.md | Scenario 1 Scenario 2 / acceptance criteria | LODE-153 / catalog metadata fixture behavior | present | review and merge-ready evidence only | Refresh after catalog metadata scope changes. |
| EV-002 | test_evidence | .loom/progress/LODE-153.md | validator and git diff checks | LODE-153 / local validation checks | present | review and merge-ready evidence only | Rerun local validation after fixture or validator edits. |
| EV-003 | fresh_verification_input | .loom/progress/LODE-153.md | EV-001 EV-002 | LODE-153 / latest validation summary | present | review and merge-ready evidence only | Refresh progress summary after validation changes. |
