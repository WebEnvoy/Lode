# Spec: Stage 6 Write-Precheck Package Spine

## Story Readiness

- User value: a caller can discover that a capability is safe for validate-only/draft/preview and cannot be mistaken for a real submit capability.
- Success experience: Core can consume package ref, operation mode, schemas, resource requirements, and guard facts without copying Lode package truth.
- Failure states: unsupported operation mode, invalid schema, missing package asset, missing write-precheck Harbor facts, or true-write request blocked by no-submit guard.
- Sensitive data boundary: no credentials, profile state, runtime session, live tab, raw DOM/network/evidence, production payload, or user business data may enter package assets.
- Non-goals: marketplace, hosted sync, generic workflow runtime, real writes, approval execution, and later expected-change/post-check FRs.

## Scenarios

- A validate-only package declares package metadata, input/output schemas, resource requirements, and no-submit guard facts.
- The local registry can resolve the package for Core contract tests.
- Validator rejects missing no-submit guard facts or private material.
