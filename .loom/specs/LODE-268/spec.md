# LODE-268 Spec

## Suite Path

- Suite path: minimal
- full-path-artifacts not_applicable rationale: This batch changes static JSON truth, schema, offline validation, and item carriers only; consumer boundary: suite validation, review, merge-ready, and closeout consume spec.md, plan.md, evidence-map.md, task-carrier.md, and implementation-contract.md but do not require suite-index.md, research.md, contracts.md, or readiness-checklist.md; recheck condition: switch to full suite for runtime APIs, browser/session behavior, live evidence storage, result-envelope ownership, or true write behavior.

## Acceptance

- Public input contains only a non-constructible opaque `detail_ref`.
- Unknown, wrong-kind, cross-site, cross-identity, cross-run, expired, reused, or caller-constructed refs reject.
- Both proposed detail packages bind exact package, lock, version, origin, and critical asset SHA-256 values.
- Both package output schema paths and SHA-256 values are pinned, and their required normalized fields cover the complete XHS note and BOSS job public detail shapes.
- Every public field is source/evidence bound; summaries are non-empty, bounded, and non-synthetic.
- BOSS security identifiers remain Core-internal behind the opaque detail ref; raw DOM, network bodies, xsec tokens, cookies, tokens, and profile material are forbidden.
- The BOSS detail package is relocked to `0.1.1`; its public output schema requires opaque `detail_ref` and does not require or permit raw `securityId` / `encryptJobId`, while `0.1.0` remains the previous-known-good rollback ref.
- Refs-only evidence and a passed post-check are required; every declared rejection has an executable mutation test.
- Lode remains static truth and makes no live-success claim.

## Non-Goals

No other repository changes, browser/account access, live evidence, write action, merge, or issue closeout.
