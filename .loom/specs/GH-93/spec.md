# Spec

- Suite path: minimal

## Goal

Define resource requirements for the first low-risk read capability package without implementing fixtures, post-check logic, validator behavior, runtime matching, registry behavior, or cross-repo consumption.

## Required Behavior

- Add `sites/example/read-public-page/resource-requirements.json`.
- The resource requirements asset declares a stable id/version and binds to the existing package, input schema, output schema, operation ref, and read operation mode.
- The asset declares Harbor runtime, public navigation, snapshot summary, refmap/source ref, and evidence ref needs.
- The asset states Lode/Core/Harbor ownership boundaries: Lode declares requirements, Core matches, Harbor owns live runtime facts and evidence.
- The asset distinguishes `matched`, `unmatched`, and `invalid_contract`.
- The asset maps resource-related failure classes without redefining the Core result envelope.
- The asset explicitly forbids provider/profile/session/cookie/token/raw evidence/live tab/local path fields.
- The manifest resource requirements asset ref is marked `present` and points to the asset id/version.
- PR metadata and Loom carrier bind to GH-93, not INIT-0001, GH-90, GH-91, or GH-92.

## Non-Goals

- Do not add fixtures, post-check payloads, validator CLI, package manager files, registry files, lockfiles, generated outputs, runtime matching, provider/profile selection, Core/Harbor/App changes, hosted registry, marketplace, sync service, crawler queue, benchmark contract, or true write capability.

## Suite Path

- Suite path: minimal
- Full suite artifacts not_applicable rationale: GH-93 is a narrow package-local resource declaration Work Item with no executable code, dependency changes, fixture payloads, runtime behavior, generated facts, external-visible action, release, or issue closeout.
- Consumer boundary: `sites/example/read-public-page/manifest.json`, `sites/example/read-public-page/resource-requirements.json`, `.loom/work-items/GH-93.md`, `.loom/progress/GH-93.md`, `.loom/specs/GH-93/*`, `.loom/status/current.md`, and `.loom/bootstrap/init-result.json`.
- Recheck condition: require stronger/full validation if this PR adds code, fixtures, generated types, post-check logic, validator/registry behavior, package manager changes, runtime behavior, live Harbor fact matching, provider/profile/session fields, external-visible writes, or non-GH-93 carrier scope.
