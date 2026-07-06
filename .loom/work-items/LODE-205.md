# LODE-205

## Static Facts

- Item ID: LODE-205
- Goal: Define Xiaohongshu login/page readiness and convert the real read capability batch for Lode #198.
- Scope: Covers Lode #198/#205/#206/#207/#208 and semantic stories #15/#16/#17. Adds Xiaohongshu search and note-detail read packages, resource requirements, fixtures, post-checks, failure mapping, registry entries, and package contract docs.
- Execution Path: work/lode-198-xhs-read-capabilities
- Workspace Entry: /Volumes/2T/dev/WebEnvoy/Lode.worktrees/lode-198-xhs-read-capabilities
- Recovery Entry: .loom/progress/LODE-205.md
- Review Entry: .loom/reviews/LODE-205.json
- Validation Entry: package validator; registry checks; py_compile; git diff --check; loom verify; loom fact-chain.
- Closing Condition: PR Ready only. Do not merge, close issues, run Stage 7, or perform Xiaohongshu write/engagement actions.

## Covered Work Items

- #205 Define Xiaohongshu login and page readiness requirements.
- #206 Convert Xiaohongshu search capability.
- #207 Convert Xiaohongshu note detail capability.
- #208 Define Xiaohongshu failure classification.

## Associated Artifacts

- sites/xiaohongshu/search-notes/**
- sites/xiaohongshu/read-note-detail/**
- registry/local-packages.json
- registry/local-query.fixture.json
- docs/contracts/xiaohongshu-read-capabilities.md
- .loom/specs/LODE-205/**
