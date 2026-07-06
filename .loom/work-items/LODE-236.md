# LODE-236

## Static Facts

- Item ID: LODE-236
- Goal: Implement the Xiaohongshu real read and write-precheck package batch for FR #235.
- Scope: Covers GitHub issues #235, #236, #237, #238, and #239. Ownership is limited to Xiaohongshu package assets, local registry fixtures, package contracts, and LODE-236 Loom carriers. It refreshes `search-notes`, `read-note-detail`, and `publish-note-precheck` as consumable real-site capability definitions with refs-only evidence requirements and no-submit write-precheck boundaries.
- Execution Path: work/lode-236-xhs-real-read-write-precheck
- Workspace Entry: /Volumes/2T/dev/WebEnvoy/Lode.worktrees/lode-236-xhs-real-read-write-precheck
- Recovery Entry: .loom/progress/LODE-236.md
- Review Entry: .loom/reviews/LODE-236.json
- Validation Entry: package validator, py_compile, JSON readability, git diff --check, Loom fact-chain, Loom verify, suite validation, and PR metadata readback.
- Closing Condition: Implementation PR is ready for review with branch/head/PR metadata bound to LODE-236. This worker must not merge the PR or close issues.

## Covered Issues

- #235 Implement Xiaohongshu real read and write-precheck capability.
- #236 Implement Xiaohongshu search result read capability.
- #237 Implement Xiaohongshu note detail read capability.
- #238 Implement Xiaohongshu publish draft write-precheck capability.
- #239 Define Xiaohongshu failure classification, post-checks, and evidence requirements.

## Associated Artifacts

- sites/xiaohongshu/search-notes/**
- sites/xiaohongshu/read-note-detail/**
- sites/xiaohongshu/publish-note-precheck/**
- registry/local-packages.json
- registry/local-query.fixture.json
- docs/contracts/xiaohongshu-read-capabilities.md
- docs/contracts/write-precheck-capabilities.md
- docs/contracts/README.md
- .loom/specs/LODE-236/**
