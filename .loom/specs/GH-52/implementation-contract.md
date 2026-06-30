# Implementation Contract

## Ownership

- Docs: `docs/draft/resource-requirements.md`, `docs/adr/0003-schema-fixtures-and-post-check.md`
- Loom carrier: `.loom/work-items/GH-52.md`, `.loom/progress/GH-52.md`, `.loom/specs/GH-52/*`, `.loom/reviews/GH-52.json`, `.loom/status/current.md`, `.loom/bootstrap/init-result.json`

## Allowed Changes

- Docs-only contract tables and examples for Stage 2 resource requirements, fixtures, read-only post-check, package validator v0, and write-like deferred conditions.
- Item-specific GH-52 Loom carrier updates needed for fact-chain, suite, carrier, and PR gate consumption.

## Forbidden Changes

- Real capability package files.
- JSON Schema files.
- Fixture files beyond docs examples.
- Validator code.
- Registry implementation.
- Runtime behavior.
- Core, Harbor, or App changes.
- True write-side behavior.
- Merge or issue closeout.

## Validation

- `git diff --check`
- JSON validation
- `loom fact-chain --target /absolute/repo --json`
- `loom suite validate --target /absolute/repo --item GH-52 --json`
- `loom suite carrier validate --target /absolute/repo --item GH-52 --json`
- Hosted basic checks after PR update
