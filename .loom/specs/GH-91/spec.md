# Spec

- Suite path: minimal

## Goal

Define the input schema for the first low-risk read capability package without implementing later validation, fixture, post-check, registry, or Core-consuming behavior.

## Required Behavior

- Add `sites/example/read-public-page/schemas/input.schema.json`.
- The schema is JSON Schema draft 2020-12 and has a stable Lode schema id/version.
- The schema requires a public `url` input and restricts it to the package manifest origins for Example Domain.
- The schema declares optional `requested_fields` and `include_source_refs` inputs with safe examples.
- The schema records field sensitivity and invalid input classes without storing cookies, tokens, profile state, runtime session state, raw evidence bodies, production payloads, or user business data.
- The manifest input schema asset ref is marked `present` and points to the schema id/version.
- PR metadata and Loom carrier bind to GH-91, not INIT-0001 or GH-90.

## Non-Goals

- Do not define normalized output schema, source schema, resource requirement details, fixture payloads, post-check logic, validator CLI, package manager files, registry files, lockfiles, or generated outputs.
- Do not change Core, Harbor, App, runtime behavior, hosted registry, marketplace, sync service, crawler queue, benchmark contract, or true write capability.

## Suite Path

- Suite path: minimal
- Full suite artifacts not_applicable rationale: GH-91 is a narrow package-local input schema Work Item with no executable code, dependency changes, runtime behavior, generated facts, external-visible action, release, or issue closeout.
- Consumer boundary: `sites/example/read-public-page/manifest.json`, `sites/example/read-public-page/schemas/input.schema.json`, `.loom/work-items/GH-91.md`, `.loom/progress/GH-91.md`, `.loom/specs/GH-91/*`, `.loom/status/current.md`, and `.loom/bootstrap/init-result.json`.
- Recheck condition: require stronger/full validation if this PR adds code, fixtures, generated types, resource matching, post-check logic, validator/registry behavior, package manager changes, runtime behavior, external-visible writes, or non-GH-91 carrier scope.
