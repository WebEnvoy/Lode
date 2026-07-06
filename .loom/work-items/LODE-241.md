# LODE-241

## Static Facts

- Item ID: LODE-241
- Goal: Implement the BOSS real read and write-precheck package batch for FR #240.
- Scope: Covers GitHub issues #240, #241, #242, #243, and #244. Ownership is limited to BOSS package assets, local registry fixtures, package contracts, and LODE-241 Loom carriers. It refreshes `job-search`, `read-job-detail`, and `greet-precheck` as consumable real-site capability definitions with refs-only evidence requirements and no-submit write-precheck boundaries.
- Execution Path: work/lode-241-boss-real-read-write-precheck
- Workspace Entry: .
- Recovery Entry: .loom/progress/LODE-241.md
- Review Entry: .loom/reviews/LODE-241.json
- Validation Entry: package validator, registry validation, py_compile, JSON readability, git diff --check, Loom fact-chain, Loom verify, suite validation, and PR metadata readback.
- Closing Condition: Implementation PR is ready for review with branch/head/PR metadata bound to LODE-241. This worker must not merge the PR or close issues.

## Covered Issues

- #240 Implement BOSS real read and write-precheck capability.
- #241 Implement BOSS job search read capability.
- #242 Implement BOSS job detail read capability.
- #243 Implement BOSS greet write-precheck capability.
- #244 Define BOSS failure classification, post-checks, and evidence requirements.

## Associated Artifacts

- sites/boss/job-search/**
- sites/boss/read-job-detail/**
- sites/boss/greet-precheck/**
- registry/local-packages.json
- registry/local-query.fixture.json
- docs/contracts/boss-read-capabilities.md
- docs/contracts/write-precheck-capabilities.md
- docs/contracts/README.md
- .loom/specs/LODE-241/**
