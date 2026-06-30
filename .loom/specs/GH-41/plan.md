# Plan

- Suite path: minimal

## Implementation

- Update `docs/adr/0004-asset-types-and-registry.md` with GH-40/GH-41/GH-42 asset taxonomy, locator, dependency, freshness, invalidation, consumer, and research absorption contract.
- Update `docs/adr/0003-schema-fixtures-and-post-check.md` with GH-43/GH-44/GH-45/GH-46 input schema, normalized output, source ref/payload, failure mapping, and research absorption contract.
- Add item-specific GH-41 Loom carrier files.
- Keep PR metadata bound to GH-41 and reference GH-40/GH-41/GH-42/GH-43/GH-44/GH-45/GH-46 without closing keywords.

## Validation

- `git diff --check`
- JSON validation for `.loom/**/*.json`
- `loom fact-chain --target . --json`
- `loom suite validate --target . --item GH-41 --json`
- `loom suite carrier validate --target . --item GH-41 --json`
- Hosted basic checks after PR creation

## Minimal Path Applicability Records

- full-path-artifacts not_applicable rationale: docs-only contract and Loom carrier update.
- consumer boundary: ADR 0003, ADR 0004, and GH-41 carriers.
- recheck condition: escalate validation if schema/API/runtime code, package artifacts, validator behavior, fixtures, generated facts, external-visible behavior, or issue closeout are added.

## Rollback

Revert the docs-only PR if the v0 boundaries conflict with a later accepted ADR or cross-repo Core/App/Harbor contract.
