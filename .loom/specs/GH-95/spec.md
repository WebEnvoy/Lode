# Spec

- Suite path: minimal

## Goal

Define the package-local redacted fixture format for the first low-risk read capability package without implementing validator CLI, post-check output, failure mapping finalization, local package resolution, Core consumption behavior, write guardrails, or runtime behavior.

## Required Behavior

- Add `sites/example/read-public-page/fixtures/read-public-page.fixture.json`.
- The fixture declares a stable fixture id/version and binds to the existing package, capability id, operation id, read operation mode, source shape hint, and normalized output schema.
- The fixture separates redacted source summary material from the normalized sample output.
- The fixture declares source/evidence placeholder refs and binds normalized public fields back to those refs.
- The fixture explicitly lists raw source, runtime identity, evidence body, local storage, production payload, and user business data fields that must not appear in Lode fixtures.
- The fixture states that GH-96 owns offline validator checks, GH-97 owns post-check output, and GH-98 owns failure mapping finalization.
- The manifest fixture asset ref is marked `present` and points to the fixture id/version.
- The lifecycle lock input includes the fixture asset version and no longer treats the GH-95 fixture as a planned placeholder.
- PR metadata and Loom carrier bind to GH-95, not INIT-0001 or previous GH-90 through GH-94 Work Items.

## Non-Goals

- Do not add validator CLI, package manager files, dependencies, generated outputs, post-check payloads or runners, failure mapping finalization, local resolver/registry/lockfile behavior, Core fixture consumption behavior, write guardrail behavior, runtime matching, provider/profile/session/cookie/token/raw evidence fields, Core/Harbor/App changes, hosted registry, marketplace, sync service, crawler queue, benchmark contract, or true write capability.

## Suite Path

- Suite path: minimal
- Full suite artifacts not_applicable rationale: GH-95 is a narrow package-local fixture format Work Item with no executable code, dependency changes, post-check runner, validator behavior, generated facts, runtime behavior, external-visible action, release, or issue closeout.
- Consumer boundary: `sites/example/read-public-page/fixtures/read-public-page.fixture.json`, `sites/example/read-public-page/manifest.json`, `sites/example/read-public-page/lifecycle-metadata.json`, `.loom/work-items/GH-95.md`, `.loom/progress/GH-95.md`, `.loom/specs/GH-95/*`, `.loom/status/current.md`, and `.loom/bootstrap/init-result.json`.
- Recheck condition: require stronger/full validation if this PR adds code, generated types, post-check logic, validator/registry behavior, package manager changes, runtime behavior, live Harbor fact matching, provider/profile/session fields, App/Core/Harbor behavior, external-visible writes, or non-GH-95 carrier scope.
