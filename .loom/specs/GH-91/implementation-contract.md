# Implementation Contract

## Ownership

- Package manifest ref: `sites/example/read-public-page/manifest.json`
- Input schema: `sites/example/read-public-page/schemas/input.schema.json`
- Loom carrier: `.loom/work-items/GH-91.md`, `.loom/progress/GH-91.md`, `.loom/specs/GH-91/*`, `.loom/status/current.md`, `.loom/bootstrap/init-result.json`

## Allowed Changes

- Package-local input schema for GH-91.
- Manifest input asset ref status/schema metadata.
- Current item carrier evidence for GH-91.
- PR body that references parent FR #87 without closing it.

## Forbidden Changes

- Normalized output schema, source schema, resource requirements, fixtures, post-check logic.
- Validator, packer, tester, registry, runner, or CLI code.
- `package.json`, lockfiles, dependency installation, generated outputs, runtime behavior, hosted registry, marketplace, sync, crawler queue, benchmark contract, true write capability, Core/Harbor/App changes, merge, or issue closeout.

## Validation

- `jq empty sites/example/read-public-page/manifest.json sites/example/read-public-page/schemas/input.schema.json`
- `git diff --check`
- `loom fact-chain --target . --json`
- `loom suite validate --target . --item GH-91 --json`
- `loom suite carrier validate --target . --item GH-91 --json`
- PR body/head readback and metadata preflight after PR creation.
