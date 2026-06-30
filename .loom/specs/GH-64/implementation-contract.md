# Implementation Contract

## Ownership

- Docs: `docs/README.md`, `docs/contracts/README.md`, `docs/draft/*.md`
- Loom carrier: `.loom/work-items/GH-64.md`, `.loom/progress/GH-64.md`, `.loom/specs/GH-64/*`, `.loom/reviews/GH-64.json`, `.loom/reviews/GH-64.spec.json`, `.loom/status/current.md`, `.loom/bootstrap/init-result.json`

## Allowed Changes

- Docs-only directory semantics, draft lifecycle rules, draft disposition table, short pointers to accepted ADR/contracts, deferred draft metadata, and item-specific GH-64 Loom carrier updates.
- Current-head review records for this docs-only PR.

## Forbidden Changes

- Product semantics changes.
- Real capability package files.
- JSON Schema files.
- Fixture files.
- Validator code.
- Registry implementation.
- Runtime behavior.
- Core, Harbor, WebEnvoy, or App changes.
- Empty `docs/guides/`.
- Merge or issue closeout.

## Validation

- `git diff --check`
- JSON validation for `.loom/**/*.json`
- `loom fact-chain --target /absolute/repo --json`
- `loom suite validate --target /absolute/repo --item GH-64 --json`
- `loom suite carrier validate --target /absolute/repo --item GH-64 --json`
- Hosted checks after PR update
