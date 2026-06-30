# Plan

- Suite path: minimal

## Implementation

- Update `docs/draft/resource-requirements.md` with Harbor facts vocabulary consumption, matching states, and read / validate-only / write-like resource boundaries.
- Update `docs/adr/0003-schema-fixtures-and-post-check.md` with GH-47 through GH-55 contract tables for resources, fixtures, post-check, package validator v0, write-like deferred conditions, and research absorption boundaries.
- Add item-specific GH-52 Loom carrier files.
- Keep PR metadata bound to GH-52 and reference GH-47/GH-48/GH-49/GH-50/GH-51/GH-52/GH-53/GH-54/GH-55 without closing keywords.

## Validation

- `git diff --check`
- JSON validation for `.loom/**/*.json`
- `loom fact-chain --target /Volumes/2T/.codex/worktrees/stage2/lode-resource-validator --json`
- `loom suite validate --target /Volumes/2T/.codex/worktrees/stage2/lode-resource-validator --item GH-52 --json`
- `loom suite carrier validate --target /Volumes/2T/.codex/worktrees/stage2/lode-resource-validator --item GH-52 --json`
- Hosted basic checks after PR creation

## Minimal Path Applicability Records

- full-path-artifacts not_applicable rationale: docs-only contract and Loom carrier update.
- consumer boundary: `docs/draft/resource-requirements.md`, ADR 0003, and GH-52 carriers.
- recheck condition: escalate validation if schema/API/runtime code, package artifacts, validator behavior, fixtures, generated facts, external-visible behavior, merge, or issue closeout are added.

## Rollback

Revert the docs-only PR if the v0 boundaries conflict with a later accepted ADR or cross-repo Core/App/Harbor contract.
