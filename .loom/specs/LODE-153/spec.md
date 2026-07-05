# Spec

## Goal

- Make the sample read-only capability package consumable as a catalog entry by App Library and Core attribution fixtures.
- Preserve Lode as the package/catalog/version/test metadata truth owner without storing App install state, Core run truth, or Harbor runtime evidence.

## Suite Path

- Suite path: minimal
- full-path-artifacts not_applicable rationale: this PR is a narrow fixture/schema/validator slice for one local read-only package; consumer boundary: suite validation, review, merge-ready, and closeout consume spec.md, plan.md, evidence-map.md, and task-carrier.md only; recheck condition: switch to full suite when this branch adds hosted registry sync, package publication, marketplace distribution, or cross-repo contract ownership changes.

## Scenarios

- Scenario 1: Given the sample read-public-page package, when the validator runs, then catalog metadata, package lock, manifest, and registry index refs are present and internally consistent.
- Scenario 2: Given App/Core consumers, when they read the fixture, then they can distinguish package ref, version, status, risk, lock ref, and read-only boundary without treating Lode as App install truth or Core run truth.

## Boundaries

- In scope: `catalog-metadata.json`, manifest/package-lock wiring, local registry discoverability, and validator coverage.
- Out of scope: hosted registry, marketplace sync, runtime execution, App local UI state, Core run records, Harbor evidence payloads, and Stage 6 write behavior.

## Acceptance Criteria

- [x] Catalog metadata is present for the sample package.
- [x] Package lock and manifest expose stable refs/version metadata.
- [x] Local registry points to the package.
- [x] Validator checks catalog identity, lock ref, version, status, risk, and read-only boundaries.
