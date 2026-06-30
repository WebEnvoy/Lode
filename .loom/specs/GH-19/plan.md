# Plan

- Suite path: minimal

## Implementation

- Update `docs/adr/pending-decisions.md` with the accepted read-only candidate class, package minimum shape, research absorption table, explicit non-goals, and write-side deferred boundary.
- Add item-specific Loom carrier files for GH-19.
- Do not create schema files, package scaffolding, fixtures, validator code, or true capability implementations.

## Validation

- `git diff --check`
- `loom doctor --target . --json`
- `loom verify --target . --json`
- `loom fact-chain --target . --json`
- Hosted `py-compile`, `demo-bootstrap`, `repo-local-cli`, `loom-check`, and `loom-pr-merge-gate`

## Minimal Path Applicability Records

- full-path-artifacts not_applicable rationale: docs-only PR; no executable schema/API/runtime behavior, generated facts, package assets, fixtures, workflow logic, or user-facing behavior.
- consumer boundary: GH-19/GH-20 and related issue tree consume the decision surface; Core/App/Harbor use it only as planning input until later schema/contract PRs.
- recheck condition: switch to full suite when a PR adds validators, schemas, capability packages, fixtures, normalizer code, runtime contract fields, hosted registry behavior, write actions, or external evidence capture.

## Rollback

Revert this docs-only PR if the boundary conflicts with a later accepted Lode/Core/Harbor contract.
