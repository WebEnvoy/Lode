# Spec

- Suite path: minimal

## Goal

Implement the first repo-local offline validator CLI for the sample read package without introducing dependencies, runtime behavior, package publishing, Core/Harbor/App changes, or post-check/failure-mapping finalization.

## Required Behavior

- Add `tools/lode_validate_package.py` as a Python standard-library CLI.
- The CLI accepts a package root containing `manifest.json`.
- The CLI emits JSON with `schema_version`, `status`, `package_root`, `package_ref`, `errors[]`, `warnings[]`, and `checked_refs[]`.
- The CLI exits nonzero only when validation errors are present.
- The CLI validates manifest version/type, required package identity fields, asset refs, schema identity/version alignment, resource requirement identity, lifecycle identity, fixture identity, normalized fixture output shape, source/evidence ref binding, and forbidden field keys.
- The CLI treats the sample package's planned `post_check` asset as a warning while lifecycle remains `proposed`, not as a pass-blocking error.
- The existing hosted `repo-local-cli` workflow runs the validator against `sites/example/read-public-page`.
- README documents the local validator command and explains the expected planned post-check warning.
- Package wording no longer says validator CLI is absent, while still keeping stable admission blocked on post-check and Core fixture consumption follow-ups.
- PR metadata and Loom carrier bind to GH-96, not INIT-0001 or previous GH-90 through GH-95 Work Items.

## Non-Goals

- Do not add package manager files, external dependencies, a full JSON Schema implementation, generated reports, package publishing, packer/tester/registry tooling, post-check output or runner, failure mapping finalization, local resolver/lockfile behavior, Core fixture consumption, write guardrail behavior, runtime matching, live browser actions, provider/profile/session fields, hosted registry, marketplace, crawler queue, benchmark contract, Core/Harbor/App changes, or true write capability.

## Suite Path

- Suite path: minimal
- Full suite artifacts not_applicable rationale: GH-96 is a narrow repo-local offline validator Work Item with one stdlib Python CLI, no dependencies, no package manager, no generated outputs, no live runtime behavior, no external-visible action, no release, and no issue closeout.
- Consumer boundary: `tools/lode_validate_package.py`, `README.md`, `.github/workflows/loom-check.yml`, sample package metadata wording, `.loom/work-items/GH-96.md`, `.loom/progress/GH-96.md`, `.loom/specs/GH-96/*`, `.loom/status/current.md`, and `.loom/bootstrap/init-result.json`.
- Recheck condition: require stronger/full validation if this PR adds dependencies, generated types, package manager changes, registry/packer/tester behavior, post-check logic, runtime behavior, live Harbor fact matching, provider/profile/session fields, App/Core/Harbor behavior, external-visible writes, or non-GH-96 carrier scope.
