# Plan

- Suite path: minimal

## Implementation

- Update `docs/adr/0002-capability-package-minimum-format.md` with the GH-36/GH-37/GH-38/GH-39 v0 contract tables and research absorption record.
- Add item-specific GH-37 Loom carrier files.
- Keep PR metadata bound to GH-37 and reference GH-36/GH-38/GH-39 without closing keywords.

## Validation

- `git diff --check`
- Low-cost repository checks available in this docs-only repo
- `loom doctor --target . --json`
- `loom verify --target . --json`
- `loom fact-chain --target . --json`
- Hosted checks after PR creation, if runnable

## Minimal Path Applicability Records

- full-path-artifacts not_applicable rationale: docs-only contract and Loom carrier update; consumer boundary: ADR 0002 and GH-37 carriers; recheck condition: escalate validation if schema/API/runtime code, package artifacts, validator behavior, fixtures, generated facts, or external-visible behavior are added.

## Rollback

Revert the docs-only PR if the v0 field boundaries conflict with a later accepted ADR or cross-repo Core/App contract.
