# Plan

- Suite path: minimal

## Implementation

- Add `sites/example/read-public-page/schemas/output.schema.json`.
- Update `sites/example/read-public-page/manifest.json` so the normalized output schema asset ref is `present` and carries schema id/version.
- Add GH-92 item-specific Loom carrier and set current status to GH-92 for this PR.

## Validation

- `jq empty sites/example/read-public-page/manifest.json sites/example/read-public-page/schemas/output.schema.json .loom/bootstrap/init-result.json .loom/specs/GH-92/build-evidence.json .loom/reviews/GH-92.json .loom/reviews/GH-92.spec.json`
- `git diff --check`
- `loom fact-chain --target . --json`
- `loom suite validate --target . --item GH-92 --json`
- `loom suite carrier validate --target . --item GH-92 --json`
- `loom review read --target . --item GH-92 --json`
- PR body/head readback and metadata preflight after PR creation.

## Minimal Path Applicability Records

- full-path-artifacts not_applicable rationale: package-local output schema PR with no executable code, fixture payloads, generated facts, runtime behavior, dependency changes, external-visible behavior, merge, or issue closeout.
- consumer boundary: the GH-92 output schema, manifest ref, and item-specific Loom carrier only.
- recheck condition: escalate validation if this PR adds code, fixtures, generated types, resource matching, post-check logic, validator/registry behavior, storage behavior, dependencies, external-visible behavior, or non-GH-92 carrier changes.

## Rollback

Revert the GH-92 PR if the output schema contradicts ADR 0002, ADR 0003, ADR 0005, issue #92 scope, or the existing GH-90/GH-91 package identity and input schema.
