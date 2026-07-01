# Implementation Contract

## Ownership

- Package manifest ref: `sites/example/read-public-page/manifest.json`
- Output schema: `sites/example/read-public-page/schemas/output.schema.json`
- Loom carrier: `.loom/work-items/GH-92.md`, `.loom/progress/GH-92.md`, `.loom/specs/GH-92/*`, `.loom/status/current.md`, `.loom/bootstrap/init-result.json`

## Allowed Changes

- Package-local normalized output schema for GH-92.
- Manifest output asset ref status/schema metadata.
- Current item carrier evidence for GH-92.
- PR body that references parent FR #87 without closing it.

## Forbidden Changes

- Resource requirements, fixtures, post-check logic.
- Validator, packer, tester, registry, runner, or CLI code.
- `package.json`, lockfiles, dependency installation, generated outputs, runtime behavior, hosted registry, marketplace, sync, crawler queue, benchmark contract, true write capability, Core/Harbor/App changes, merge, or issue closeout.

## Validation

- `jq empty sites/example/read-public-page/manifest.json sites/example/read-public-page/schemas/output.schema.json`
- `git diff --check`
- `loom fact-chain --target . --json`
- `loom suite validate --target . --item GH-92 --json`
- `loom suite carrier validate --target . --item GH-92 --json`
- PR body/head readback and metadata preflight after PR creation.
