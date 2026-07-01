# Spec

- Suite path: minimal

## Goal

Create the first low-risk read capability package manifest instance for milestone #9 without implementing the later schema, fixture, validator, registry, or Core-consuming steps.

## Required Behavior

- Add one `site-capability` manifest under `sites/example/read-public-page/`.
- The manifest declares package identity, `package_ref`, site/origin, capability id, operation id/ref, family, operation mode, target type, version, lifecycle, tags, and entrypoint ref.
- The manifest is read-only and uses only reserved-domain sample metadata.
- Follow-up assets for input schema, output schema, resource requirements, fixture, and post-check are referenced as `planned` with their owning Work Item ids.
- The package does not contain cookies, tokens, profile state, runtime session state, live tab state, production payloads, raw evidence bodies, or user business data.
- PR metadata and Loom carrier bind to GH-90, not INIT-0001 or GH-84.

## Non-Goals

- Do not create input/output/source JSON Schema files.
- Do not create fixtures, post-check implementations, validator CLI, package manager files, registry files, lockfiles, or generated outputs.
- Do not change Core, Harbor, App, runtime behavior, hosted registry, marketplace, sync service, crawler queue, benchmark contract, or true write capability.

## Suite Path

- Suite path: minimal
- Full suite artifacts not_applicable rationale: GH-90 is a narrow manifest-instance Work Item that creates no code, executable schema validation, fixtures, runtime behavior, generated facts, external-visible action, or release.
- Consumer boundary: `sites/example/read-public-page/manifest.json`, `.loom/work-items/GH-90.md`, `.loom/progress/GH-90.md`, `.loom/specs/GH-90/*`, `.loom/status/current.md`, and `.loom/bootstrap/init-result.json`.
- Recheck condition: require stronger/full validation if this PR adds code, real schemas, fixture bodies, post-check logic, validator/registry behavior, package manager changes, runtime behavior, external-visible writes, or non-GH-90 carrier scope.
