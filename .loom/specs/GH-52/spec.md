# Spec

## Goal

Record the docs-only Stage 2 v0 contract for Lode resource requirements, examples, read-only post-check, package validator reporting, and write-like deferred conditions so Core can consume Lode requirements against Harbor facts without guessing or moving runtime truth into Lode.

## Scope

- In scope: Harbor facts vocabulary consumption, `matched` / `unmatched` / `invalid_contract`, read / validate-only / write-like boundaries, redacted raw and normalized fixture format, read-only post-check and evidence binding, validator input/output/error reporting, write-like deferred conditions, and research absorption decisions.
- Out of scope: real capability packages, JSON Schema files, fixture files, validator code, registry implementation, runtime execution, Core/Harbor/App changes, true write behavior, merge, and issue closeout.

## Required Behavior

- GH-47/GH-48: `docs/draft/resource-requirements.md` and ADR 0003 must state how Lode consumes Harbor facts vocabulary while Harbor remains runtime truth source.
- GH-49: Contract must distinguish `matched`, `unmatched`, and `invalid_contract`.
- GH-50: Contract must distinguish read, validate-only, and write-like resource boundaries.
- GH-51/GH-52: ADR 0003 must state redacted raw fixture and normalized fixture format, source refs, and sensitive-data exclusions.
- GH-53: ADR 0003 must state read-only post-check and evidence binding expectations.
- GH-54: ADR 0003 must state package validator input, output, severity, and error reporting contract without implementing code.
- GH-55: ADR 0003 must state write-like validation deferred conditions and prevent true write side from entering Stage 2.
- Required research locators must have explicit absorption, trimmed reuse, reference-only, or rejection decisions in repository truth carriers.

## Suite Path

- Suite path: minimal
- Full suite artifacts not_applicable rationale: this PR changes Markdown contracts and GH-52 Loom carriers only.
- Consumer boundary: `docs/draft/resource-requirements.md`, ADR 0003, and GH-52 Loom carriers are the only repository facts consumed by this lane.
- Recheck condition: require full suite or stronger validation if this PR adds executable code, real package files, schema files, fixtures, validators, registry behavior, runtime behavior, generated facts, external-visible behavior, merge, or issue closeout.
