# Implementation Contract

## Ownership

- Owner: repo-controller
- Work Item: GH-101
- Branch: `work/GH-101-sample-read-package`

## Write Scope

- `sites/example/read-public-page/manifest.json`
- `sites/example/read-public-page/lifecycle-metadata.json`
- `registry/local-packages.json`
- `README.md`
- `.loom/work-items/GH-101.md`
- `.loom/progress/GH-101.md`
- `.loom/specs/GH-101/*`
- `.loom/reviews/GH-101*.json`
- `.loom/bootstrap/init-result.json`
- `.loom/status/current.md`

## Forbidden Scope

- New sample packages, schema changes, fixture payload changes, validator expansion, package lock behavior changes, package manager initialization, dependencies, generated outputs, generated reports, package publishing, or installer behavior.
- App install/update/pin/rollback/sync behavior, hosted registry, marketplace, crawler queue, benchmark contract, or true write execution.
- Core Run Record/result envelope behavior, runtime, browser, Core, Harbor, App, provider/profile/session/cookie/token/raw evidence fields, production payloads, or user business data.
- Core fixture consumption behavior, write guardrail behavior, merge, or issue closeout.

## Acceptance

- Manifest declares the selected sample package, fixture binding, consumer entrypoints, and non-claimed boundaries.
- Local registry exposes the same sample marker and fixture path.
- Lifecycle metadata includes `sample_read_package_selected`.
- Validator returns `passed` with no warnings for both automatic repo-local index discovery and explicit `--registry-index registry/local-packages.json`.
- Loom suite/carrier/readback pass for GH-101 before PR creation.
