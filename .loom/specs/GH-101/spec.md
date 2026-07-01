# Spec

- Suite path: minimal

## Goal

Select the first low-risk sample read package and bind it to the existing redacted fixture so Core-facing follow-up work has one repo-local package reference to consume, without changing schemas, fixture payloads, validator behavior, package lock semantics, runtime behavior, Core/Harbor/App code, or write behavior.

## Required Behavior

- `sites/example/read-public-page/manifest.json` declares `sample_read_package.status` as `selected`.
- The sample selection explains why the package is low risk: reserved public Example Domain content, read-only operation mode, summary-only fixture, placeholder source/evidence refs, and no account/session/runtime/production/user data.
- The sample metadata binds to the existing fixture id, fixture version, fixture path, redaction mode, normalized output schema, local registry index, manifest path, and package lock.
- `registry/local-packages.json` exposes the same sample package marker and fixture path for repo-local discovery.
- Lifecycle metadata includes `sample_read_package_selected` as a promotion requirement and treats sample selection or fixture binding changes as version-relevant.
- README documents the selected sample package and explicitly states that this does not claim Core fixture consumption, stable admission, runtime execution, or write behavior.
- Existing package validation remains clean for automatic local registry discovery and explicit registry-index validation.
- PR metadata and Loom carrier bind to GH-101, not INIT-0001 or previous Work Items.

## Non-Goals

- Do not create a second sample package, alter fixture content, change input/output schema, change package lock semantics, extend validator code, add App/Core/Harbor behavior, add hosted registry/marketplace/sync behavior, execute runtime/live checks, create Core fixture consumption behavior, create write guardrail behavior, or claim true write capability.

## Suite Path

- Suite path: minimal
- Full suite artifacts not_applicable rationale: GH-101 is a narrow sample-selection metadata and docs change over an already validated package, with no dependencies, runtime behavior, external-visible action, release, or issue closeout.
- Consumer boundary: `sites/example/read-public-page/manifest.json`, `sites/example/read-public-page/lifecycle-metadata.json`, `registry/local-packages.json`, `README.md`, `.loom/work-items/GH-101.md`, `.loom/progress/GH-101.md`, `.loom/specs/GH-101/*`, `.loom/bootstrap/init-result.json`, and `.loom/status/current.md`.
- Recheck condition: require stronger/full validation if this PR changes schema, fixture payloads, package lock behavior, validator logic, dependencies, generated outputs, App/Core/Harbor behavior, runtime/live evidence, provider/profile/session fields, external-visible writes, or non-GH-101 carrier scope.
