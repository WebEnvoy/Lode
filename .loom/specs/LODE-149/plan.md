# Plan

## Steps

1. Reuse the existing read-public-page package shape for two additional reserved-domain read candidates.
2. Generalize package-lock path validation so every repo-local package can validate by manifest identity.
3. Add candidate selection and local registry query fixture files.
4. Add Core admission fields to catalog metadata and validate them.
5. Run validator, query fixture checks, sensitive material scan, diff check, Loom checks, PR gate, merge, and closeout.

## Out of Scope

- Hosted registry, marketplace, sync, crawler, runtime execution, App UI, Core run records, Harbor evidence payloads, private browser material, and true write behavior.
