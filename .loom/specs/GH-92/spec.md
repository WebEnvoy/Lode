# Spec

- Suite path: minimal

## Goal

Define the normalized output schema for the first low-risk read capability package without implementing later resource, fixture, post-check, validator, registry, or Core-consuming behavior.

## Required Behavior

- Add `sites/example/read-public-page/schemas/output.schema.json`.
- The schema is JSON Schema draft 2020-12 and has a stable Lode schema id/version.
- The schema declares structured `content_detail` normalized data for successful reads.
- The schema declares `source_refs` and `evidence_refs` placeholder shapes without inlining raw evidence.
- The schema represents `available`, `empty`, and `unavailable` states and maps them to Lode failure/result classes.
- The manifest output schema asset ref is marked `present` and points to the schema id/version.
- PR metadata and Loom carrier bind to GH-92, not INIT-0001, GH-90, or GH-91.

## Non-Goals

- Do not define resource requirement details, fixture payloads, post-check logic, validator CLI, package manager files, registry files, lockfiles, or generated outputs.
- Do not change Core, Harbor, App, runtime behavior, hosted registry, marketplace, sync service, crawler queue, benchmark contract, or true write capability.

## Suite Path

- Suite path: minimal
- Full suite artifacts not_applicable rationale: GH-92 is a narrow package-local output schema Work Item with no executable code, dependency changes, runtime behavior, generated facts, external-visible action, release, or issue closeout.
- Consumer boundary: `sites/example/read-public-page/manifest.json`, `sites/example/read-public-page/schemas/output.schema.json`, `.loom/work-items/GH-92.md`, `.loom/progress/GH-92.md`, `.loom/specs/GH-92/*`, `.loom/status/current.md`, and `.loom/bootstrap/init-result.json`.
- Recheck condition: require stronger/full validation if this PR adds code, fixtures, generated types, resource matching, post-check logic, validator/registry behavior, package manager changes, runtime behavior, external-visible writes, or non-GH-92 carrier scope.
