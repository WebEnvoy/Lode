# LODE-266 Implementation Contract

## Required Inputs

- Parent FR #265; anchor #266; covered Work Item #267.
- Branch `work/lode-266-write-precheck-runtime-consumption`; workspace `.`.
- Existing package/lock/registry truth from LODE-236, LODE-241, LODE-262, and merged PR #264.

## Boundary

The output is static Lode truth. Consumers must match exact package, relocked lock identity, every critical asset SHA-256, version, origin, operation, page/resources, current refs, field sources, evidence, and post-check requirements. Freshness covers merged-head, page, identity, session, run, result, resources, field sources, evidence, post-check, and submitted-result refs. Any write/submit request, drift, stale/missing refs, challenge, or result other than `submitted=false` rejects. Harbor owns page/session/evidence facts; Core owns admission/run/result; Lode runs neither.

The all-package validator and hosted validation commands execute the strict JSON Schema using pinned `jsonschema`; dependency absence is a validation failure. Fixture rejection declarations and executable mutations must remain an exact ordered set.
