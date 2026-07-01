# Plan

- Suite path: minimal

## Implementation

- Add `sites/example/read-public-page/manifest.json` with proposed read-only capability identity and package ref.
- Mark later schema, fixture, resource, and post-check assets as planned and bound to their follow-up Work Items.
- Add GH-90 item-specific Loom carrier and set current status to GH-90 for this PR.

## Validation

- `jq empty sites/example/read-public-page/manifest.json`
- `git diff --check`
- `loom fact-chain --target . --json`
- `loom suite validate --target . --item GH-90 --json`
- `loom suite carrier validate --target . --item GH-90 --json`
- PR body/head readback and metadata preflight after PR creation.

## Minimal Path Applicability Records

- full-path-artifacts not_applicable rationale: manifest-only package identity PR with no executable code, schema files, fixture payloads, generated facts, runtime behavior, dependency changes, external-visible behavior, merge, or issue closeout.
- consumer boundary: the GH-90 manifest and item-specific Loom carrier only.
- recheck condition: escalate validation if this PR adds code, real JSON Schema files, fixtures, generated types, runtime behavior, storage behavior, dependencies, external-visible behavior, or non-GH-90 carrier changes.

## Rollback

Revert the GH-90 PR if the manifest contradicts ADR 0002, ADR 0003, ADR 0005, or issue #90 scope.
