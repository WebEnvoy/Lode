# Plan

- Suite path: minimal

## Implementation

- Add `sites/example/read-public-page/schemas/input.schema.json`.
- Update `sites/example/read-public-page/manifest.json` so the input schema asset ref is `present` and carries schema id/version.
- Add GH-91 item-specific Loom carrier and set current status to GH-91 for this PR.

## Validation

- `jq empty sites/example/read-public-page/manifest.json sites/example/read-public-page/schemas/input.schema.json .loom/bootstrap/init-result.json .loom/specs/GH-91/build-evidence.json .loom/reviews/GH-91.json .loom/reviews/GH-91.spec.json`
- `git diff --check`
- `loom fact-chain --target . --json`
- `loom suite validate --target . --item GH-91 --json`
- `loom suite carrier validate --target . --item GH-91 --json`
- `loom review read --target . --item GH-91 --json`
- PR body/head readback and metadata preflight after PR creation.

## Minimal Path Applicability Records

- full-path-artifacts not_applicable rationale: package-local input schema PR with no executable code, fixture payloads, generated facts, runtime behavior, dependency changes, external-visible behavior, merge, or issue closeout.
- consumer boundary: the GH-91 input schema, manifest ref, and item-specific Loom carrier only.
- recheck condition: escalate validation if this PR adds code, output/source schema, fixtures, generated types, resource matching, post-check logic, validator/registry behavior, storage behavior, dependencies, external-visible behavior, or non-GH-91 carrier changes.

## Rollback

Revert the GH-91 PR if the input schema contradicts ADR 0002, ADR 0003, ADR 0005, issue #91 scope, or the existing GH-90 package identity.
