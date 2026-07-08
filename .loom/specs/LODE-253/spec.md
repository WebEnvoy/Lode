# LODE-253 Spec

## Story Readiness

FR #252 corrects the Lode closeout surface for milestone #14. Lode must provide static capability assets and registry facts that Core can consume, while clearly failing closed for runtime execution, browser identity, profile, source refs, evidence refs, and write submission.

## Suite Path

- Suite path: minimal
- full-path-artifacts not_applicable rationale: This branch changes repo-local Lode assets, registry fixtures, docs, focused validation, and item-specific carriers only. It does not add runtime code, cross-repo API ownership, live evidence storage, true write execution, hosted registry behavior, or browser automation.
- Consumer boundary: Lode validator, local registry, Core/App package discovery, Harbor/Core refs-only evidence requirements, fixture shape, post-check declarations, failure vocabulary, and closeout wording.
- Recheck condition: Upgrade to full suite when a later PR adds live runtime execution, Core result envelopes, Harbor evidence schemas, true write behavior, hosted registry behavior, or cross-repo contract ownership changes.

## Acceptance

- `registry/local-packages.json` exposes Core-readable fields for the six current XHS/BOSS read and write-precheck packages:
  - `site_slug`, `task_kind`, `capability_id`, `operation_id`, `operation_mode`;
  - `runtime_execution: out_of_scope`;
  - `required_browser_session`;
  - `identity_profile_requirements`;
  - `evidence_requirements`;
  - `write_precheck_boundary`;
  - `failure_taxonomy_refs`.
- `registry/local-query.fixture.json` exposes the same boundary fields for Core/App query fixtures.
- XHS packages remain static Lode assets and do not claim live Xiaohongshu execution.
- BOSS packages remain static Lode assets and do not claim live BOSS execution.
- Write-precheck packages must keep `submitted: false`, `no_submit_guard: active`, and `true_write_execution: blocked`.
- Contract docs must say fixture/demo/contract evidence is not runtime/live evidence.

## Failure States

- Missing registry locator or schema locator: Core must fail closed.
- Missing Harbor browser session or identity facts: Core must fail closed with resource-unavailable style classification.
- Missing evidence refs: Core must fail closed; Lode fixtures are not live evidence.
- Write-precheck package claims submit/save/send/publish/apply: invalid contract.

## Non-Goals

- No runtime server.
- No true write capability.
- No real Xiaohongshu/BOSS page access.
- No account/profile/Cookie/session handling.
- No external visible action.
- No Core, Harbor, or App code change.
