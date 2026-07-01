# Spec

- Suite path: minimal

## Goal

Implement local package resolution for the sample read package using a repo-local index and offline validator checks, without adding hosted registry, install/update, lockfile, runtime, Core, Harbor, App, or write behavior.

## Required Behavior

- Add `registry/local-packages.json` as the repo-local index for the sample package.
- The index contains one entry for `lode://site-capability/example/read-public-page@0.1.0`.
- The entry resolves from `package_ref` to repo-relative `package_path` and `manifest_path`.
- The entry mirrors manifest package type, site slug, capability id, operation id, operation mode, version, lifecycle, and asset roles.
- The index explicitly declares hosted registry, marketplace/sync, runtime execution, provider/profile/session selection, and write capability as out of scope.
- The validator automatically checks `registry/local-packages.json` when validating inside this repository.
- The validator also supports explicit `--registry-index registry/local-packages.json` validation.
- Validator report checked refs include `local_registry_index`.
- Package lifecycle/README wording no longer claims local package resolution is missing after GH-99.
- PR metadata and Loom carrier bind to GH-99, not INIT-0001 or previous Work Items.

## Non-Goals

- Do not define package ref/lock semantics beyond local package resolution.
- Do not add a lockfile, generated registry output, package manager files, dependencies, install/update/pin/rollback behavior, hosted registry, marketplace, sync service, package publishing, runtime execution, provider/profile/session fields, Core fixture consumption behavior, write guardrail behavior, crawler queue, benchmark contract, Core/Harbor/App changes, external writes, or true write capability.

## Suite Path

- Suite path: minimal
- Full suite artifacts not_applicable rationale: GH-99 is a narrow repo-local index and stdlib validator extension with no dependencies, runtime behavior, external-visible action, release, or issue closeout.
- Consumer boundary: `registry/local-packages.json`, `tools/lode_validate_package.py`, package manifest/lifecycle wording, `README.md`, `.loom/work-items/GH-99.md`, `.loom/progress/GH-99.md`, `.loom/specs/GH-99/*`, `.loom/bootstrap/init-result.json`, and `.loom/status/current.md`.
- Recheck condition: require stronger/full validation if this PR adds lockfile semantics, generated outputs, dependencies, package manager changes, hosted registry behavior, runtime/live matching, provider/profile/session fields, Core/Harbor/App behavior, external-visible writes, or non-GH-99 carrier scope.
