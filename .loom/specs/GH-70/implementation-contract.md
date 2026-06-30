# Implementation Contract

## Work Item

- Item: GH-70
- Execution Entry: .loom/progress/GH-70.md

## Approved Spec

- Spec Path: .loom/specs/GH-70/spec.md
- Spec Review Entry: .loom/reviews/GH-70.spec.json

## Implementation Scope

- In Scope: `.github/workflows/loom-check.yml` `LOOM_VERSION` pin and GH-70 carrier evidence.
- Out Of Scope: product code, product docs, roadmap, issue tree, schema/API/runtime contracts, fixtures, generated facts, and historical INIT-0001 migration.

## Validation Plan

- Automated Checks: `git diff --check`; hosted GitHub Actions checks for PR #69.
- Manual Verification: PR body and fact-chain item both bind to GH-70.

## Risks And Rollback

- Risks: Hosted gate may expose new v0.22.1 requirements.
- Rollback Boundary: Revert the workflow version-pin PR if v0.22.1 cannot run the existing gate entry.

## Host Binding

- Pull Request: https://github.com/WebEnvoy/Lode/pull/69
- Reviewed Head: ef97e3fcb63ac85e9306583682c86043a443f911
