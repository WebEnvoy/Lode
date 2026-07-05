# Spec

## Story Readiness

- User value: Core/App can consume Lode-owned read capability assets beyond one sample package, with clear version, lock, lifecycle, schema, fixture, post-check, and admission facts.
- Success experience: local registry lists three low-risk read capabilities and exposes a query fixture with Core admission fields.
- Failure and unavailable states: invalid contract, asset missing, unsupported version, registry unavailable, resource unavailable, site changed, empty result, post-check failed, and evidence expired.
- Sensitive data boundary: no credentials, cookies, tokens, profile state, runtime session, live tab state, raw evidence body, full DOM, HAR, screenshots, production payload, or user business data.
- Non-goals: hosted registry, marketplace, sync, crawler queue, runtime execution, App UI, Core run truth, Harbor private capture, and Stage 6 write behavior.
- Dependency facts: Lode owns package/catalog/version/schema/fixture truth; Core owns run/result envelope truth; Harbor owns runtime/evidence refs; App owns UI intent.

## Goal

- Promote the first read-only capability set from single sample package to three repo-local, validator-backed capability assets.
- Add local registry query fixture and Core admission fields without creating hosted distribution or runtime execution.

## Suite Path

- Suite path: minimal
- full-path-artifacts not_applicable rationale: bounded Stage 5 package metadata/schema/fixture/validator slice; consumer boundary: Core/App consume refs and static facts only; recheck condition: switch to full suite when adding hosted registry, package distribution, runtime execution, private material handling, or cross-repo schema ownership changes.

## Scenarios

- Scenario 1: Given App/Core ask for read capabilities, the local registry query fixture returns three low-risk read package refs with lock/version/lifecycle/schema/resource/post-check facts.
- Scenario 2: Given a package is validated, every manifest asset ref resolves to schema, resource requirements, fixture, post-check, catalog, lifecycle, repair, overlay, and lock assets.
- Scenario 3: Given Core performs admission, catalog metadata exposes package_ref, version, lock_ref, manifest_path, input/output schema ids, resource requirement id, post_check id, lifecycle, and operation_mode.
- Scenario 4: Given the validator scans assets, forbidden private/runtime/raw material is rejected.

## Acceptance Criteria

- [x] Three low-risk read capability candidates are selected.
- [x] Each selected capability has input/output schema and resource requirements.
- [x] Each selected capability has fixture and post-check assets.
- [x] Catalog metadata exposes Core admission fields.
- [x] Local registry query fixture returns all selected read capabilities.
- [x] Validator batch passes for all registry entries and the query fixture.
