# LODE-209

## Static Facts

- Item ID: LODE-209
- Goal: Define BOSS page/login readiness and convert the real read capability batch for Lode #199.
- Scope: Covers Lode #199/#209/#210/#211/#212 and semantic stories #18/#19/#20. Ownership is limited to Lode BOSS package assets, registry fixtures, contract docs, and LODE-209 Loom carriers. Adds BOSS job search and job detail read packages, resource requirements, fixtures, post-checks, failure mapping, registry entries, and package contract docs.
- Execution Path: work/lode-199-boss-read-capabilities
- Workspace Entry: .
- Recovery Entry: .loom/progress/LODE-209.md
- Review Entry: .loom/reviews/LODE-209.json
- Validation Entry: package validator; registry checks; py_compile; git diff --check; loom verify; loom fact-chain; loom suite checks.
- Closing Condition: Implementation PR merged, #199/#209/#210/#211/#212 closeout evidence posted, and current pointer returns to no_active_item.

## Covered Work Items

- #209 Define BOSS page and login readiness requirements.
- #210 Convert BOSS job search capability.
- #211 Convert BOSS job detail capability.
- #212 Define BOSS failure classification.

## Associated Artifacts

- sites/boss/job-search/**
- sites/boss/read-job-detail/**
- registry/local-packages.json
- registry/local-query.fixture.json
- docs/contracts/boss-read-capabilities.md
- .loom/specs/LODE-209/**
