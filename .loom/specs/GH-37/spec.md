# Spec

## Goal

Record the minimum v0 contract for Lode site capability packages so Core can reference admission fields and App Library can display package metadata without guessing.

## Scope

- In scope: docs-only contract for package minimum format, manifest/root rules, capability identity, operation/family/tags, lifecycle, version locking, deprecation, invalidation, App Library fields, Core admission fields, non-goals, and research absorption decisions.
- Out of scope: real package files, JSON Schema, fixtures, validator, registry, runtime execution, hosted marketplace, live write behavior, issue closeout, and merge-ready.

## Required Behavior

- GH-37: ADR 0002 must state required manifest/root boundaries, optional support references, forbidden contents, package type, failure classification, and non-goals.
- GH-38: ADR 0002 must state `capability_id`, `operation_id`, `capability_family`, operation mode, tags, display consumption, and admission boundary.
- GH-39: ADR 0002 must state lifecycle, version identity, version lock consumption, deprecation, invalidation markers, and repair/deferred boundaries.
- Research locators from GH-36/GH-37/GH-38/GH-39 must have explicit absorption, trimmed reuse, reference-only, or rejection decisions in a repository truth carrier.

## Suite Path

- Suite path: minimal
- Full suite artifacts not_applicable: rationale: this PR changes Markdown contracts and item-specific Loom carriers only; consumer boundary: ADR 0002 plus GH-37 Loom carrier are the only repository facts consumed by this lane; recheck condition: require full suite or stronger validation if this PR adds executable code, package files, schema, fixtures, validators, registry behavior, runtime behavior, generated facts, or external writes.
