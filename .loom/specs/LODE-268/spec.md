# LODE-268 Spec

## Suite Path

- Suite path: minimal
- full-path-artifacts not_applicable rationale: This batch changes static JSON truth, schema, offline validation, and item carriers only; consumer boundary: suite validation, review, merge-ready, and closeout consume spec.md, plan.md, evidence-map.md, task-carrier.md, and implementation-contract.md but do not require suite-index.md, research.md, contracts.md, or readiness-checklist.md; recheck condition: switch to full suite for runtime APIs, browser/session behavior, live evidence storage, result-envelope ownership, or true write behavior.

## Acceptance

- Public input contains only a non-constructible opaque `detail_ref`.
- Unknown, wrong-kind, cross-site, cross-identity, cross-run, expired, reused, or caller-constructed refs reject.
- Both proposed detail packages bind exact package, lock, version, origin, and critical asset SHA-256 values.
- Refs-only evidence and a passed post-check are required; every declared rejection has an executable mutation test.
- Lode remains static truth and makes no live-success claim.

## Non-Goals

No other repository changes, browser/account access, live evidence, write action, merge, or issue closeout.
