# Implementation Contract

## Ownership

- Package manifest ref: `sites/example/read-public-page/manifest.json`
- Resource requirements asset: `sites/example/read-public-page/resource-requirements.json`
- Loom carrier: `.loom/work-items/GH-93.md`, `.loom/progress/GH-93.md`, `.loom/specs/GH-93/*`, `.loom/status/current.md`, `.loom/bootstrap/init-result.json`

## Allowed Changes

- Package-local resource requirements for GH-93.
- Manifest resource asset ref status/resource metadata.
- Current item carrier evidence for GH-93.
- PR body that references parent FR #87 without closing it.

## Forbidden Changes

- Fixtures, post-check logic, validator, packer, tester, registry, runner, or CLI code.
- `package.json`, lockfiles, dependency installation, generated outputs, runtime behavior, live Harbor fact matching, provider/profile/session fields, hosted registry, marketplace, sync, crawler queue, benchmark contract, true write capability, Core/Harbor/App changes, merge, or issue closeout.

## Validation

- `jq empty sites/example/read-public-page/manifest.json sites/example/read-public-page/resource-requirements.json`
- `git diff --check`
- `loom fact-chain --target . --json`
- `loom suite validate --target . --item GH-93 --json`
- `loom suite carrier validate --target . --item GH-93 --json`
- PR body/head readback and metadata preflight after PR creation.
