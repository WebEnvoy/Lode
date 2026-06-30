# Spec

## Goal

Make Lode docs draft closeout PR-ready without changing product semantics: `docs/` has minimal directory semantics, `docs/draft/` has lifecycle rules and a complete disposition table, accepted Stage 2 draft truth is replaced by short pointers to ADR / contracts, and deferred drafts have owner, linked issue, and exit condition.

## Scope

- In scope: `docs/README.md`, `docs/contracts/README.md`, `docs/draft/README.md`, all current `docs/draft/*.md`, and GH-64 Loom carriers.
- Out of scope: product semantics changes, package/schema/validator/runtime code, real package files, fixtures, generated facts, guides, merge, issue closeout, and changes outside WebEnvoy/Lode.

## Required Behavior

- `docs/README.md` defines only `adr/`, `contracts/`, and `draft/`; no empty `guides/`.
- `docs/draft/README.md` states draft lifetime rules: short-lived, status, owner, linked issue, exit condition, and not implementation truth.
- Every current `docs/draft/*.md` appears in the disposition table with file, current use, status, target location, linked issue, and action.
- Accepted Stage 2 contracts point to ADR / contracts instead of keeping duplicate draft truth.
- Pending/deferred drafts include owner, linked issue, and exit condition.
- PR metadata references GH-62/GH-63/GH-64/GH-65/GH-66 without close keywords.

## Suite Path

- Suite path: minimal
- Full suite artifacts not_applicable rationale: docs-only PR; no code, schema, API, runtime, fixture, generated fact, package artifact, validator behavior, external-visible behavior, merge, or issue closeout.
- Consumer boundary: `docs/README.md`, `docs/contracts/README.md`, `docs/draft/*.md`, and GH-64 Loom carriers are the only repository facts consumed by this lane.
- Recheck condition: require full suite or stronger validation if this PR or a follow-up PR adds code, schema, API, runtime behavior, generated facts, fixtures, package artifacts, validator behavior, external-visible behavior, merge, or issue closeout.
