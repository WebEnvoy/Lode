# Plan

- Suite path: minimal

## Implementation

- Add the redacted fixture at `sites/example/read-public-page/fixtures/read-public-page.fixture.json`.
- Update `sites/example/read-public-page/manifest.json` so the GH-95 fixture asset ref is `present` and carries fixture id/version metadata.
- Update `sites/example/read-public-page/lifecycle-metadata.json` so lock input lists the fixture asset version and leaves post-check as a planned placeholder.
- Add GH-95 item-specific Loom carrier and set current status to GH-95 for this PR.

## Validation

- `jq empty sites/example/read-public-page/manifest.json sites/example/read-public-page/lifecycle-metadata.json sites/example/read-public-page/fixtures/read-public-page.fixture.json .loom/bootstrap/init-result.json .loom/specs/GH-95/build-evidence.json`
- `git diff --check`
- `loom fact-chain --target . --json`
- `loom suite validate --target . --item GH-95 --json`
- `loom suite carrier validate --target . --item GH-95 --json`
- `loom review read --target . --item GH-95 --json`
- PR body/head readback and metadata preflight after PR creation.

## Minimal Path Applicability Records

- full-path-artifacts not_applicable rationale: package-local fixture format PR with no executable code, generated facts, runtime behavior, dependency changes, post-check runner, validator behavior, external-visible behavior, merge, or issue closeout.
- consumer boundary: the GH-95 fixture file, manifest/lifecycle fixture refs, and item-specific Loom carrier only.
- recheck condition: escalate validation if this PR adds code, generated types, post-check logic, validator/registry behavior, storage behavior, dependencies, lockfile implementation, Core fixture consumption behavior, App/Core/Harbor changes, live Harbor matching, provider/profile/session fields, external-visible behavior, or non-GH-95 carrier changes.

## Rollback

Revert the GH-95 PR if the fixture format leaks forbidden raw/runtime/evidence/user data, contradicts ADR 0002, ADR 0003, ADR 0005, issue #95 scope, or the existing GH-90/GH-94 package identity/input/output/resource/lifecycle contracts.
