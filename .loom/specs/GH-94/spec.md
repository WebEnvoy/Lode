# Spec

- Suite path: minimal

## Goal

Define version and lifecycle metadata for the first low-risk read capability package without implementing fixtures, post-check logic, validator behavior, registry behavior, lockfile behavior, App install/update/rollback UI, runtime matching, or cross-repo consumption.

## Required Behavior

- Add `sites/example/read-public-page/lifecycle-metadata.json`.
- The lifecycle metadata asset declares a stable id/version and binds to the existing package, package version, capability id, operation id, and read operation mode.
- The asset declares lifecycle state, stable admission boundary, promotion requirements, demotion triggers, and version identity rules.
- The asset declares lock input fields that a later App/Core lock or run record can consume without defining a lockfile, registry, hosted marketplace, or UI.
- The asset declares current deprecation status and invalidation status without marking the proposed package stable.
- The asset maps version/lifecycle/deprecation/invalidation-related failure classes without redefining the Core result envelope.
- The asset explicitly forbids provider/profile/session/cookie/token/raw evidence/live tab/local path fields.
- The manifest version/lifecycle asset ref is marked `present` and points to the asset id/version.
- PR metadata and Loom carrier bind to GH-94, not INIT-0001 or previous GH-90 through GH-93 Work Items.

## Non-Goals

- Do not add fixtures, post-check payloads, validator CLI, package manager files, registry files, lockfiles, generated outputs, runtime matching, provider/profile selection, App install/update/rollback behavior, Core/Harbor/App changes, hosted registry, marketplace, sync service, crawler queue, benchmark contract, or true write capability.

## Suite Path

- Suite path: minimal
- Full suite artifacts not_applicable rationale: GH-94 is a narrow package-local version/lifecycle metadata Work Item with no executable code, dependency changes, fixture payloads, runtime behavior, generated facts, external-visible action, release, or issue closeout.
- Consumer boundary: `sites/example/read-public-page/manifest.json`, `sites/example/read-public-page/lifecycle-metadata.json`, `.loom/work-items/GH-94.md`, `.loom/progress/GH-94.md`, `.loom/specs/GH-94/*`, `.loom/status/current.md`, and `.loom/bootstrap/init-result.json`.
- Recheck condition: require stronger/full validation if this PR adds code, fixtures, generated types, post-check logic, validator/registry behavior, package manager changes, runtime behavior, live Harbor fact matching, provider/profile/session fields, lockfile implementation, App install/update/rollback behavior, external-visible writes, or non-GH-94 carrier scope.
