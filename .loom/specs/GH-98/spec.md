# Spec

- Suite path: minimal

## Goal

Define the first sample read package failure mapping and make the existing offline validator consume it without adding Core/App behavior, runtime behavior, dependencies, or a result-envelope schema.

## Required Behavior

- Add `sites/example/read-public-page/failure-mapping.json`.
- Mark the sample package manifest `failure_mapping` asset as `present` and align lifecycle/fixture/output/README wording.
- The failure mapping asset declares `invalid_contract`, `resource_unavailable`, `site_changed`, and `empty_result`.
- Each failure class declares trigger, owner, Core consumer hints, App consumer hints, and a recovery hint.
- The mapping explicitly keeps Core result envelope fields and App UI copy out of Lode ownership.
- The validator requires and validates the failure mapping asset identity/version, package/capability binding, required class presence, and basic consumer mapping shape.
- The validator report for `sites/example/read-public-page` remains clean after GH-98.
- PR metadata and Loom carrier bind to GH-98, not INIT-0001 or previous Work Items.

## Non-Goals

- Do not add a Core result envelope schema, App UI copy contract, runtime/live matching, Harbor evidence schema, local resolver/lockfile behavior, Core fixture consumption behavior, write guardrail behavior, hosted registry, marketplace, crawler queue, benchmark contract, Core/Harbor/App changes, external writes, or true write capability.

## Suite Path

- Suite path: minimal
- Full suite artifacts not_applicable rationale: GH-98 is a narrow package asset and stdlib validator extension with no dependencies, runtime behavior, external-visible action, release, or issue closeout.
- Consumer boundary: `sites/example/read-public-page/failure-mapping.json`, package manifest/lifecycle/fixture/output wording, `tools/lode_validate_package.py`, `README.md`, `.loom/work-items/GH-98.md`, `.loom/progress/GH-98.md`, `.loom/specs/GH-98/*`, and `.loom/status/current.md`.
- Recheck condition: require stronger/full validation if this PR adds Core/App/Harbor behavior, generated schema, dependencies, package manager changes, runtime/live matching, provider/profile/session fields, external-visible writes, or non-GH-98 carrier scope.
