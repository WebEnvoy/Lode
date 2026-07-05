# Spec

## Goal

- Make the sample read-only capability expose lifecycle, compatibility, lock, previous-known-good, rollback, and registry status facts that App and Core can consume.
- Preserve Lode as package/version/lifecycle truth owner without storing App UI intent, Core run truth, Harbor runtime state, or raw evidence.

## Suite Path

- Suite path: minimal
- full-path-artifacts not_applicable rationale: this PR is a bounded Stage 5 package metadata and offline validator slice for repo-local assets; consumer boundary: App/Core consume refs and status facts, not runtime truth; recheck condition: switch to full suite when adding hosted registry, package distribution, runtime execution, user overlays, repair draft promotion, or cross-repo schema ownership changes.

## Scenarios

- Scenario 1: Given the sample read-public-page package, when consumers read lifecycle metadata, then they can distinguish proposed, active, suspected_broken, broken, and deprecated states with transition meanings.
- Scenario 2: Given App/Core need a fallback, when they read catalog or registry metadata, then they can find current/latest/default_locked versions and previous-known-good rollback refs without package body duplication.
- Scenario 3: Given Lode validator runs against the registry, when `--all` is used, then every repo-local package entry is validated through the same package checks.

## Boundaries

- In scope: sample package lifecycle metadata, compatibility range, package lock rollback refs, catalog/registry lifecycle fields, validator checks, and README validation command.
- Out of scope: repair draft lifecycle, user overlay/fork asset boundary, hosted registry, marketplace, sync, crawler queue, runtime execution, App install state, Core run records, Harbor evidence payloads, and Stage 6 write behavior.

## Acceptance Criteria

- [x] Lifecycle metadata declares Stage 5 lifecycle states and transitions.
- [x] Version identity exposes current/latest/default_locked and compatibility range.
- [x] Package lock, catalog, and registry expose previous-known-good/rollback refs.
- [x] Validator checks lifecycle vocabulary, compatibility, rollback, registry version status, and registry batch validation.
- [x] No raw evidence, runtime session, credential, profile, production payload, or user business data is introduced.
