# Spec

## Goal

Record the docs-only v0 contract for Lode asset/workflow references and input/output/source shapes so Core and App can consume package semantics without guessing or pulling runtime data into Lode.

## Scope

- In scope: docs-only contract tables for site capability, workflow package, domain skill, site adapter, deferred asset types, asset locators, package dependencies, input schema shape, normalized output shape, source payload/ref boundary, result classification, failure mapping, non-goals, and research absorption decisions.
- Out of scope: real capability package, JSON Schema files, fixtures, validators, registry code, workflow runner, runtime execution, hosted marketplace, live write behavior, issue closeout, and merge.

## Required Behavior

- GH-40/GH-41: ADR 0004 must state taxonomy boundaries for `site-capability`, `workflow-package`, `domain-skill`, `site-adapter`, deferred benchmark/crawler/marketplace scope, and consumer fields.
- GH-42: ADR 0004 must state package-internal and package-external locator rules, dependency locking, freshness, invalidation, and secret/profile/live-data exclusions.
- GH-43/GH-44: ADR 0003 must state docs-level input schema fields, sensitivity handling, resource refs, and examples without creating validators.
- GH-45: ADR 0003 must state normalized output schema, result classes, and Core Result Envelope alignment boundary.
- GH-46: ADR 0003 must state source payload vs source ref shape and failure mapping to Core/App.
- Required research locators must have explicit absorption, trimmed reuse, reference-only, or rejection decisions in repository truth carriers.

## Suite Path

- Suite path: minimal
- Full suite artifacts not_applicable rationale: this PR changes Markdown contracts and GH-41 Loom carriers only.
- Consumer boundary: ADR 0003, ADR 0004, and GH-41 Loom carriers are the only repository facts consumed by this lane.
- Recheck condition: require full suite or stronger validation if this PR adds executable code, real package files, schema files, fixtures, validators, registry behavior, runtime behavior, generated facts, external-visible behavior, or issue closeout.
