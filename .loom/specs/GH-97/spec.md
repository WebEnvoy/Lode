# Spec

- Suite path: minimal

## Goal

Define the first sample read package post-check output format and make the existing offline validator consume it without adding a runner, runtime behavior, dependencies, or cross-repo changes.

## Required Behavior

- Add `sites/example/read-public-page/checks/post-check.json`.
- Mark the sample package manifest `post_check` asset as `present` and align lifecycle/fixture metadata wording.
- The post-check asset declares `passed`, `failed`, and `skipped` status values.
- The post-check asset declares required output fields: `status`, `reason`, `source_refs`, and `evidence_refs`.
- The post-check asset includes declarative requirements for target location and normalized field source/evidence binding.
- The post-check asset includes a fixture output that passes using the existing redacted fixture source/evidence refs.
- The validator checks post-check identity/version alignment, package/capability binding, output status vocabulary, required output fields, requirements, fixture output reason, and source/evidence ref membership.
- The validator report for `sites/example/read-public-page` is clean after GH-97, with no planned post-check warning.
- README explains that post-check is a declarative asset and does not execute browser runtime or Core result-envelope behavior.
- PR metadata and Loom carrier bind to GH-97, not INIT-0001 or previous Work Items.

## Non-Goals

- Do not add a post-check runner, browser automation steps, live evidence access, Core result envelope, Harbor evidence schema, failure mapping finalization beyond existing class names, local resolver/lockfile behavior, Core fixture consumption behavior, write guardrail behavior, hosted registry, marketplace, crawler queue, benchmark contract, Core/Harbor/App changes, external writes, or true write capability.

## Suite Path

- Suite path: minimal
- Full suite artifacts not_applicable rationale: GH-97 is a narrow package asset and stdlib validator extension with no dependencies, runtime behavior, external-visible action, release, or issue closeout.
- Consumer boundary: `sites/example/read-public-page/checks/post-check.json`, package manifest/lifecycle/fixture wording, `tools/lode_validate_package.py`, `README.md`, `.loom/work-items/GH-97.md`, `.loom/progress/GH-97.md`, `.loom/specs/GH-97/*`, and `.loom/status/current.md`.
- Recheck condition: require stronger/full validation if this PR adds a runner, generated schema, dependencies, package manager changes, runtime/live Harbor matching, Core/Harbor/App behavior, provider/profile/session fields, external-visible writes, or non-GH-97 carrier scope.
