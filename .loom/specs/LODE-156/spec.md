# Spec

## Story Readiness

- User value: when a read-only capability breaks or is suspected broken, users can see whether a repair draft exists, why it exists, who owns the failure, and what validation must pass before update.
- Success experience: App/Core can read Lode-owned refs-only fixtures for failure-to-repair mapping, repair draft status, overlay/fork boundaries, private invalidation boundaries, and package update acceptance.
- Failure and unavailable states: invalid contract, site changed, post-check failed, evidence expired, local-only report, candidate repair draft, validated draft, promoted draft, and rejected draft.
- Sensitive data boundary: Lode assets must not contain credentials, cookies, tokens, profile state, runtime session state, live tab state, raw evidence bodies, full DOM, network archives, production payloads, or user business data.
- Non-goals: marketplace, hosted sync, crawler queue, real runtime execution, private browser capture, App/Core/Harbor truth storage, true write behavior, and Stage 6 write-side workflows.
- Dependency facts: Lode owns package/version/repair draft metadata; Core owns run/result truth; Harbor owns runtime/evidence refs and freshness; App owns local UI intent and display only.

## Goal

- Make the sample read-only capability expose repair draft, overlay/fork, failure mapping, and package update acceptance facts that App and Core can consume.
- Preserve Lode as package and repair draft truth owner without storing App UI intent, Core run truth, Harbor runtime state, or raw evidence.

## Suite Path

- Suite path: minimal
- full-path-artifacts not_applicable rationale: this PR is a bounded Stage 5 package metadata and offline validator slice for repo-local assets; consumer boundary: App/Core consume refs and status facts, not runtime truth; recheck condition: switch to full suite when adding hosted registry, package distribution, runtime execution, user overlay promotion, true write behavior, or cross-repo schema ownership changes.

## Scenarios

- Scenario 1: Given Core/App receive a failure class, when Lode repair facts are read, then users can see the owner, repair action, and display-safe summary for invalid contract, site changed, post-check failed, and evidence expired failures.
- Scenario 2: Given a repair draft exists, when consumers inspect it, then they can distinguish candidate, validated, promoted, and rejected states and see validation/promotion requirements.
- Scenario 3: Given a user report or local override exists, when App shows it, then the metadata keeps it local-only or refs-only and does not turn private browser material into a Lode asset.
- Scenario 4: Given a package update candidate is proposed, when validation runs, then sensitive material exclusion and previous-known-good retention are checked before promotion is considered.

## Boundaries

- In scope: repair draft fixture, overlay/fork metadata fixture, failure mapping additions, package lock/catalog/registry refs, validator checks, and Loom carrier for this Lode batch.
- Out of scope: marketplace, hosted sync, crawler queue, runtime execution, App install state, Core run records, Harbor evidence payloads, private browser material, and Stage 6 write behavior.

## Acceptance Criteria

- [x] Failure-to-repair mapping covers invalid_contract, site_changed, post_check_failed, and evidence_expired.
- [x] Repair draft lifecycle declares candidate, validated, promoted, and rejected states with transitions.
- [x] Overlay/fork metadata declares user_overlay, fork, and repair_draft boundaries.
- [x] Private invalidation remains local_signal_only and platform report remains a public fix candidate.
- [x] Draft validation and promotion checks require validator pass, sensitive material scan, previous-known-good retention, and package version or asset version update.
- [x] Validator checks repair draft and overlay/fork metadata identity, lifecycle, boundaries, and forbidden fields.
- [x] No raw evidence, runtime session, credential, profile, production payload, or user business data is introduced.
