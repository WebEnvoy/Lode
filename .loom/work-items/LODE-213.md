# LODE-213

## Static Facts

- Item ID: LODE-213
- Goal: Define Xiaohongshu publish-note write-precheck capability and deliver the real-page write-precheck batch for Lode #200.
- Scope: Covers Lode #200/#213/#214/#215/#216 and semantic stories #21/#22. Ownership is limited to Lode write-precheck package assets, registry fixtures, contract docs, and LODE-213 Loom carriers. Adds Xiaohongshu publish-note precheck and BOSS greet precheck packages, unified expected-change/risk/no-submit output, failure mapping, registry entries, and package contract docs.
- Execution Path: work/lode-200-write-precheck-capabilities
- Workspace Entry: .
- Recovery Entry: .loom/progress/LODE-213.md
- Review Entry: .loom/reviews/LODE-213.json
- Validation Entry: package validator; registry checks; sensitive-material scan; git diff --check; loom verify; loom fact-chain; loom suite checks.
- Closing Condition: Implementation PR merged, #200/#213/#214/#215/#216 closeout evidence posted, and current pointer returns to no_active_item.

## Covered Work Items

- #200 Form real-page write-precheck capabilities.
- #213 Define Xiaohongshu publish draft write-precheck capability.
- #214 Define BOSS greet write-precheck capability.
- #215 Define expected change, risk hints, precheck, and no-submit boundary.
- #216 Define page change, permission, and target-not-writable failure reasons.

## Associated Artifacts

- sites/xiaohongshu/publish-note-precheck/**
- sites/boss/greet-precheck/**
- registry/local-packages.json
- registry/local-query.fixture.json
- docs/contracts/write-precheck-capabilities.md
- README.md
- docs/contracts/README.md
- .loom/specs/LODE-213/**
