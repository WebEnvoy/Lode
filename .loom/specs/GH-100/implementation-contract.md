# Implementation Contract

## Ownership

- Owner: repo-controller
- Work Item: GH-100
- Branch: `work/GH-100-package-ref-lock`

## Write Scope

- `sites/example/read-public-page/package-lock.json`
- `sites/example/read-public-page/manifest.json`
- `sites/example/read-public-page/lifecycle-metadata.json`
- `registry/local-packages.json`
- `tools/lode_validate_package.py`
- `README.md`
- `.loom/work-items/GH-100.md`
- `.loom/progress/GH-100.md`
- `.loom/specs/GH-100/*`
- `.loom/reviews/GH-100*.json`
- `.loom/bootstrap/init-result.json`
- `.loom/status/current.md`

## Forbidden Scope

- Package manager initialization, dependencies, generated outputs, generated lock artifacts, package publishing, or installer behavior.
- App install/update/pin/rollback/sync behavior, hosted registry, marketplace, crawler queue, benchmark contract, or true write execution.
- Core Run Record/result envelope behavior, runtime, browser, Core, Harbor, App, provider/profile/session/cookie/token/raw evidence fields, production payloads, or user business data.
- Core fixture consumption behavior, write guardrail behavior, merge, or issue closeout.

## Acceptance

- The validator returns `passed` with no warnings for both automatic repo-local index discovery and explicit `--registry-index registry/local-packages.json`.
- `package-lock.json` binds the sample package_ref, capability id, version, local resolution paths, locked asset versions, and invalidation behavior.
- Validator checked refs include `package_lock`.
- Loom suite/carrier/review readback pass for GH-100 before PR creation.
