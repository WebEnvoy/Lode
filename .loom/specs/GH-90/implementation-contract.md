# Implementation Contract

## Ownership

- Package manifest: `sites/example/read-public-page/manifest.json`
- Loom carrier: `.loom/work-items/GH-90.md`, `.loom/progress/GH-90.md`, `.loom/specs/GH-90/*`, `.loom/status/current.md`, `.loom/bootstrap/init-result.json`

## Allowed Changes

- Manifest-only sample read package identity for GH-90.
- Current item carrier evidence for GH-90.
- PR body that references parent FR #87 without closing it.

## Forbidden Changes

- Input/output/source schema files.
- Fixture payloads.
- Post-check logic.
- Validator, packer, tester, registry, runner, or CLI code.
- `package.json`, lockfiles, dependency installation, generated outputs, runtime behavior, hosted registry, marketplace, sync, crawler queue, benchmark contract, true write capability, Core/Harbor/App changes, merge, or issue closeout.

## Validation

- `jq empty sites/example/read-public-page/manifest.json`
- `git diff --check`
- `loom fact-chain --target . --json`
- `loom suite validate --target . --item GH-90 --json`
- `loom suite carrier validate --target . --item GH-90 --json`
- PR body/head readback and metadata preflight after PR creation.
