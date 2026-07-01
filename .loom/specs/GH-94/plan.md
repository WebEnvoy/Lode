# Plan

- Suite path: minimal

## Implementation

- Add `sites/example/read-public-page/lifecycle-metadata.json`.
- Update `sites/example/read-public-page/manifest.json` so the version/lifecycle metadata asset ref is `present` and carries lifecycle metadata id/version.
- Add GH-94 item-specific Loom carrier and set current status to GH-94 for this PR.

## Validation

- `jq empty sites/example/read-public-page/manifest.json sites/example/read-public-page/lifecycle-metadata.json .loom/bootstrap/init-result.json .loom/specs/GH-94/build-evidence.json .loom/reviews/GH-94.json .loom/reviews/GH-94.spec.json`
- `git diff --check`
- `loom fact-chain --target . --json`
- `loom suite validate --target . --item GH-94 --json`
- `loom suite carrier validate --target . --item GH-94 --json`
- `loom review read --target . --item GH-94 --json`
- PR body/head readback and metadata preflight after PR creation.

## Minimal Path Applicability Records

- full-path-artifacts not_applicable rationale: package-local version/lifecycle metadata PR with no executable code, fixture payloads, generated facts, runtime behavior, dependency changes, external-visible behavior, merge, or issue closeout.
- consumer boundary: the GH-94 lifecycle metadata asset, manifest ref, and item-specific Loom carrier only.
- recheck condition: escalate validation if this PR adds code, fixtures, generated types, post-check logic, validator/registry behavior, storage behavior, dependencies, lockfile implementation, App install/update/rollback behavior, live Harbor matching, provider/profile/session fields, external-visible behavior, or non-GH-94 carrier changes.

## Rollback

Revert the GH-94 PR if the lifecycle metadata asset contradicts ADR 0002, ADR 0004, ADR 0005, issue #94 scope, or the existing GH-90/GH-93 package identity/input/output/resource contracts.
