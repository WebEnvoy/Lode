# Implementation Contract

## Ownership

- Owner: repo-controller
- Work Item: GH-99
- Branch: `work/GH-99-local-package-resolution`

## Write Scope

- `registry/local-packages.json`
- `tools/lode_validate_package.py`
- `README.md`
- `sites/example/read-public-page/manifest.json`
- `sites/example/read-public-page/lifecycle-metadata.json`
- `.loom/work-items/GH-99.md`
- `.loom/progress/GH-99.md`
- `.loom/specs/GH-99/*`
- `.loom/reviews/GH-99*.json`
- `.loom/bootstrap/init-result.json`
- `.loom/status/current.md`

## Forbidden Scope

- Package manager initialization, dependencies, generated outputs, generated registry artifacts, lockfiles, or package publishing.
- Package ref/lock semantics beyond local package resolution.
- Hosted registry, marketplace, sync service, install/update/pin/rollback behavior, crawler queue, benchmark contract, or true write execution.
- Runtime, browser, Core, Harbor, App, provider/profile/session/cookie/token/raw evidence fields, production payloads, or user business data.
- Core fixture consumption behavior, write guardrail behavior, merge, or issue closeout.

## Acceptance

- The validator returns `passed` with no warnings for both automatic repo-local index discovery and explicit `--registry-index registry/local-packages.json`.
- `registry/local-packages.json` maps the sample `package_ref` to a repo-relative package root and manifest path aligned with the manifest.
- Validator checked refs include `local_registry_index`.
- Loom suite/carrier/review readback pass for GH-99 before PR creation.
