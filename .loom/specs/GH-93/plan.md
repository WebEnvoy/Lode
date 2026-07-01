# Plan

- Suite path: minimal

## Implementation

- Add `sites/example/read-public-page/resource-requirements.json`.
- Update `sites/example/read-public-page/manifest.json` so the resource requirements asset ref is `present` and carries resource id/version.
- Add GH-93 item-specific Loom carrier and set current status to GH-93 for this PR.

## Validation

- `jq empty sites/example/read-public-page/manifest.json sites/example/read-public-page/resource-requirements.json .loom/bootstrap/init-result.json .loom/specs/GH-93/build-evidence.json .loom/reviews/GH-93.json .loom/reviews/GH-93.spec.json`
- `git diff --check`
- `loom fact-chain --target . --json`
- `loom suite validate --target . --item GH-93 --json`
- `loom suite carrier validate --target . --item GH-93 --json`
- `loom review read --target . --item GH-93 --json`
- PR body/head readback and metadata preflight after PR creation.

## Minimal Path Applicability Records

- full-path-artifacts not_applicable rationale: package-local resource requirements PR with no executable code, fixture payloads, generated facts, runtime behavior, dependency changes, external-visible behavior, merge, or issue closeout.
- consumer boundary: the GH-93 resource requirements asset, manifest ref, and item-specific Loom carrier only.
- recheck condition: escalate validation if this PR adds code, fixtures, generated types, post-check logic, validator/registry behavior, storage behavior, dependencies, live Harbor matching, provider/profile/session fields, external-visible behavior, or non-GH-93 carrier changes.

## Rollback

Revert the GH-93 PR if the resource requirements asset contradicts ADR 0002, ADR 0003, ADR 0005, issue #93 scope, or the existing GH-90/GH-92 package identity/input/output contracts.
