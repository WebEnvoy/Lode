# LODE-262 Evidence Map

| Evidence id | Type | Source locator | Consumes | Binding | Freshness | Consumer boundary | Remediation direction |
| --- | --- | --- | --- | --- | --- | --- |
| EV-001 | behavior_evidence | registry/runtime-consumption-allowlist.json | The two proposed lock-bound operation entries and their non-runner boundary | LODE-262 allowlist asset | present | Static admission identity only; not live runtime evidence or operation success. | Refresh for any package, lock, origin, mode, resource, failure, evidence, or post-check change. |
| EV-002 | test_evidence | tools/validate_runtime_consumption_allowlist.py | Exact consumer, lock/origin/mode/resource/failure/evidence/post-check binding and fail-closed mutations including added consumers, missing/empty reject maps, and active lifecycle | LODE-262 offline validator | present | Test evidence covers only Lode static assets. | Rerun after any allowlist or bound package asset change. |
| EV-003 | test_evidence | tools/lode_validate_package.py | Existing package and local registry contracts | LODE-262 package validation | present | Package contract evidence only; no browser or runtime is exercised. | Rerun after any package or local registry change. |
| EV-004 | fresh_verification_input | .loom/progress/LODE-262.md | EV-001 EV-002 EV-003 | LODE-262 latest validation summary | present | Current-head review may consume static asset validation only. | Refresh after every commit, push, PR metadata change, or validation rerun. |
