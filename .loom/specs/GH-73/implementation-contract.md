# Implementation Contract

## Ownership

- Docs: `docs/adr/0005-lode-technical-architecture-baseline.md`, `docs/contracts/README.md`, `AGENTS.md`
- Loom carrier: `.loom/work-items/GH-73.md`, `.loom/progress/GH-73.md`, `.loom/specs/GH-73/*`, `.loom/status/current.md`, `.loom/bootstrap/init-result.json`

## Allowed Changes

- Docs-only technical architecture baseline for GH-72 through GH-81.
- Current item carrier evidence for GH-73.
- PR body that references GH-72 through GH-81 with Refs only.

## Forbidden Changes

- Product code.
- Package files.
- JSON Schema files.
- Fixture files.
- Validator, packer, tester, registry, runner, or CLI code.
- `package.json`, lockfiles, or dependency installation.
- Runtime behavior.
- Hosted registry, marketplace, sync, public contribution review, crawler queue, benchmark harness, or true write execution.
- Core, Harbor, WebEnvoy, App, `research/`, or `sources/` changes.
- Merge or issue closeout.

## Validation

- `git diff --check`
- Markdown readability check
- JSON validation for `.loom/**/*.json`
- `loom fact-chain --target . --json`
- `loom suite validate --target . --item GH-73 --json`
- `loom suite carrier validate --target . --item GH-73 --json`
- PR body/head readback and metadata preflight when available
