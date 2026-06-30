# Plan

- Suite path: minimal

## Implementation

- Add `docs/README.md` with `adr/`, `contracts/`, and `draft/` semantics.
- Add `docs/contracts/README.md` as an ADR-backed contract index without duplicating specs.
- Rewrite `docs/draft/README.md` with lifecycle rules and the full draft disposition table.
- Replace accepted draft bodies with short pointers to ADR / contracts.
- Keep only deferred draft material that has owner, linked issue, and exit condition.
- Add item-specific GH-64 Loom carrier files.

## Validation

- `git diff --check`
- JSON validation for `.loom/**/*.json`
- `loom fact-chain --target . --json`
- `loom suite validate --target . --item GH-64 --json`
- `loom suite carrier validate --target . --item GH-64 --json`
- Hosted checks after PR creation

## Minimal Path Applicability Records

- full-path-artifacts not_applicable rationale: docs-only closeout and Loom carrier update.
- consumer boundary: `docs/README.md`, `docs/contracts/README.md`, `docs/draft/*.md`, and GH-64 carriers.
- recheck condition: escalate validation if schema/API/runtime code, package artifacts, validator behavior, fixtures, generated facts, external-visible behavior, merge, or issue closeout are added.

## Rollback

Revert the docs-only PR if the closeout table points to the wrong authoritative ADR/contract or if a later accepted ADR changes draft lifecycle semantics.
