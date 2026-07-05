# LODE-182

## Static Facts

- Item ID: LODE-182
- Goal: Express expected change, risk hints, preview post-check, and preview failure classes for Stage 6 write-precheck packages.
- Scope: Covers Lode #182/#183/#184/#185 under FR #181; excludes true writes, marketplace, hosted sync, generic workflow runtime, Core preview envelopes, Harbor evidence bodies, and App UI.
- Execution Path: work/lode-182-expected-change-preview
- Workspace Entry: .
- Recovery Entry: .loom/progress/LODE-182.md
- Review Entry: .loom/reviews/LODE-182.json
- Validation Entry: python3 -m py_compile tools/lode_validate_package.py; python3 tools/lode_validate_package.py --registry-index registry/local-packages.json --all --json; git diff --check
- Closing Condition: PR merged, #182/#183/#184/#185/#181 closeout evidence posted, and current pointer remains no_active_item.

## Covered Work Items

- #182 define expected change schema.
- #183 define risk hint taxonomy.
- #184 define preview post-check.
- #185 define preview failure classification.

## Associated Artifacts

- tools/lode_validate_package.py
- sites/example/preview-contact-form/schemas/output.schema.json
- sites/example/preview-contact-form/fixtures/preview-contact-form.fixture.json
- sites/example/preview-contact-form/checks/post-check.json
- sites/example/preview-contact-form/failure-mapping.json
- sites/example/preview-contact-form/fixtures/core-consumption.fixture.json
- .loom/specs/LODE-182/**
