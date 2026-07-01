# Spec

- Suite path: minimal

## Goal

Define package ref and lock semantics for the sample read package through a static package lock asset and offline validator checks, without adding App install/update behavior, hosted registry, Core Run Record behavior, runtime behavior, Core/Harbor/App code, or write behavior.

## Required Behavior

- Add `sites/example/read-public-page/package-lock.json`.
- The package lock declares `lock_ref`, package ref/version, capability id, operation id, operation mode, lifecycle, repo-local resolution paths, locked asset refs, and invalidation behavior.
- Manifest asset refs mark `package_lock` as present.
- `registry/local-packages.json` includes `lock_ref` and `lock_path`, while remaining repo-local only.
- Lifecycle metadata records `package_lock_present`, package lock asset version, and lock invalidation/relock triggers.
- The validator requires and validates the package lock asset identity/version, package/capability binding, local resolution paths, locked asset ref/version/path alignment, and invalidation behavior shape.
- Validator report for `sites/example/read-public-page` remains clean for automatic and explicit registry-index validation.
- README explains that the lock is a local verifiable contract, not App install/update, hosted registry, Core Run Record, or runtime execution.
- PR metadata and Loom carrier bind to GH-100, not INIT-0001 or previous Work Items.

## Non-Goals

- Do not add App install/update/pin/rollback/sync behavior, hosted registry, marketplace, package publishing, Core Run Record/result envelope behavior, runtime execution, provider/profile/session fields, Core fixture consumption behavior, write guardrail behavior, crawler queue, benchmark contract, Core/Harbor/App changes, external writes, or true write capability.

## Suite Path

- Suite path: minimal
- Full suite artifacts not_applicable rationale: GH-100 is a narrow package lock asset and stdlib validator extension with no dependencies, runtime behavior, external-visible action, release, or issue closeout.
- Consumer boundary: `sites/example/read-public-page/package-lock.json`, package manifest/lifecycle metadata, `registry/local-packages.json`, `tools/lode_validate_package.py`, `README.md`, `.loom/work-items/GH-100.md`, `.loom/progress/GH-100.md`, `.loom/specs/GH-100/*`, `.loom/bootstrap/init-result.json`, and `.loom/status/current.md`.
- Recheck condition: require stronger/full validation if this PR adds App/Core/Harbor behavior, generated outputs, dependencies, package manager changes, hosted registry behavior, runtime/live matching, provider/profile/session fields, external-visible writes, or non-GH-100 carrier scope.
