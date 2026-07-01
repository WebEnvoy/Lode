# Spec

- Suite path: minimal

## Goal

Provide a Core-readable fixture for the first sample read package so Core can consume repo-local package identity, lock, input schema, normalized output schema, fixture, post-check, and failure mapping references for admission/schema validation, without changing Core/Harbor/App code or claiming runtime execution.

## Required Behavior

- Add `sites/example/read-public-page/fixtures/core-consumption.fixture.json`.
- The fixture declares package ref, lock ref, capability identity, operation mode, owner boundaries, repo-local registry/manifest/lock paths, required package asset paths, an input validation case, a normalized output validation case, a post-check fixture output case, and required failure mapping classes.
- Manifest asset refs expose `core_consumption_fixture` as a present GH-102 asset with fixture id/version.
- Package lock includes the `core_consumption_fixture` locked asset and treats changes to its resolution, schema validation cases, or expected result as relock-relevant.
- Local registry exposes `core_consumption_fixture_path` and includes `core_consumption_fixture` in `asset_roles`.
- Lifecycle metadata records the core consumption fixture in lock input/version identity and keeps the package lifecycle `proposed`.
- README documents the Core consumption fixture and states it is not Core runtime execution, a Core result envelope, stable admission, or write behavior.
- Existing package validation remains clean for automatic local registry discovery and explicit registry-index validation.
- A GH-102-specific `jq -e` check proves the fixture is directly readable and keeps runtime/write claims false.
- PR metadata and Loom carrier bind to GH-102, not INIT-0001 or previous Work Items.

## Non-Goals

- Do not modify WebEnvoy/Core, Harbor, or App.
- Do not define a Core result envelope schema.
- Do not execute runtime/browser/live checks or look up live source/evidence.
- Do not add hosted registry, marketplace, sync service, crawler queue, benchmark contract, package publishing, write guardrail behavior, or true write capability.
- Do not store cookies, tokens, account state, raw evidence bodies, complete DOM, HAR, screenshots, production payloads, or user business data.

## Suite Path

- Suite path: minimal
- Full suite artifacts not_applicable rationale: GH-102 is a narrow repo-local fixture/discoverability change with no dependencies, runtime behavior, external-visible action, release, or issue closeout.
- Consumer boundary: `sites/example/read-public-page/fixtures/core-consumption.fixture.json`, package manifest/lock/lifecycle metadata, `registry/local-packages.json`, `README.md`, `.loom/work-items/GH-102.md`, `.loom/progress/GH-102.md`, `.loom/specs/GH-102/*`, `.loom/bootstrap/init-result.json`, and `.loom/status/current.md`.
- Recheck condition: require stronger/full validation if this PR adds Core/Harbor/App behavior, generated outputs, dependencies, package manager changes, hosted registry behavior, runtime/live matching, provider/profile/session fields, external-visible writes, or non-GH-102 carrier scope.
