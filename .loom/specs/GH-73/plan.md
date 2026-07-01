# Plan

- Suite path: minimal

## Implementation

- Add ADR 0005 as the milestone #8 technical architecture baseline.
- Update `docs/contracts/README.md` to index ADR 0005 and point future tooling Work Items to it.
- Update `AGENTS.md` with technical stack, dependency, test, change-scope, and security constraints.
- Add GH-73 item-specific Loom carrier and set current status to GH-73 for this PR.

## Validation

- `git diff --check`
- Markdown readability check for edited docs and carrier files.
- JSON validation for `.loom/**/*.json`
- `loom fact-chain --target . --json`
- `loom suite validate --target . --item GH-73 --json`
- `loom suite carrier validate --target . --item GH-73 --json`
- PR body/head readback and metadata preflight when available.

## Minimal Path Applicability Records

- full-path-artifacts not_applicable rationale: docs-only architecture baseline.
- consumer boundary: `docs/adr/0005-lode-technical-architecture-baseline.md`, `docs/contracts/README.md`, `AGENTS.md`, and GH-73 carriers.
- recheck condition: escalate validation if code, schema, package artifact, fixture, generated fact, validator/packer/tester/registry behavior, dependency installation, runtime behavior, hosted sync/registry behavior, external-visible behavior, merge, or issue closeout is added.

## Rollback

Revert the docs-only PR if ADR 0005 contradicts ADR 0002/0003/0004, the issue bodies #72-#81, or the cross-repo ownership boundary in Core/App contracts.
