# Spec

## Goal

Make milestone #8「Lode 资产与校验架构基线」PR-ready as a docs-only architecture baseline covering GH-72 through GH-81.

## Scope

- In scope: `docs/adr/0005-lode-technical-architecture-baseline.md`, `docs/contracts/README.md`, `AGENTS.md`, and GH-73 Loom carrier.
- Out of scope: package files, JSON Schema files, fixtures, validator/packer/tester/registry code, package manager initialization, dependencies, runtime behavior, hosted registry, marketplace, sync, merge, and issue closeout.

## Required Behavior

- The ADR covers Lode JSON/YAML/Markdown assets and the TypeScript-only tooling boundary.
- The ADR defines manifest, schema, fixture, post-check, normalizer/adapter reference responsibilities.
- The ADR states JSON Schema is the formal structured contract carrier; Markdown is explanatory only.
- The ADR defines the minimal offline boundary for validator, packer, tester, and local registry tooling.
- The ADR defines fixture/post-check validation entry expectations and structured failure output.
- The ADR explicitly defers hosted registry, marketplace, team sync, public contribution review, crawler queue, benchmark harness, and true write execution.
- `AGENTS.md` records technical stack, dependency, test, change-scope, and security forbidden-scope constraints.
- `docs/contracts/README.md` links the baseline ADR and identifies future tooling skeleton entry points without creating them.
- Research and cross-repo inputs are explicitly absorbed, cropped, or rejected by locator; the ADR does not say only "reference research".
- PR metadata uses Refs for #72-#81 and does not use close keywords.

## Suite Path

- Suite path: minimal
- Full suite artifacts not_applicable rationale: docs-only PR; no code, schema, API, runtime, fixture, generated fact, package artifact, validator behavior, dependency installation, external-visible behavior, merge, or issue closeout.
- Consumer boundary: `docs/adr/0005-lode-technical-architecture-baseline.md`, `docs/contracts/README.md`, `AGENTS.md`, and GH-73 Loom carriers are the only repository facts consumed by this lane.
- Recheck condition: require stronger/full validation if this PR or a follow-up PR adds code, schema files, package files, runtime behavior, generated facts, fixtures, validator/packer/tester/registry behavior, dependencies, hosted sync/registry behavior, external-visible behavior, merge, or issue closeout.
