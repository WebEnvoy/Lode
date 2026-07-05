# LODE-187

## Static Facts

- Item ID: LODE-187
- Goal: Select and publish the first low-risk write-precheck capability fixture for Stage 6 consumers.
- Scope: Covers Lode #187/#188/#189/#190 under FR #186; excludes true writes, marketplace, hosted sync, crawler, workflow runtime, Core preview envelopes, Harbor private material, and App UI.
- Execution Path: work/lode-187-write-pre-fixtures
- Workspace Entry: .
- Recovery Entry: .loom/progress/LODE-187.md
- Review Entry: .loom/reviews/LODE-187.json
- Validation Entry: python3 -m py_compile tools/lode_validate_package.py; python3 tools/lode_validate_package.py --registry-index registry/local-packages.json --all --json; git diff --check
- Closing Condition: PR merged, #187/#188/#189/#190/#186 closeout evidence posted, milestone #12 closed with open_issues=0, and current pointer returns to no_active_item.

## Covered Work Items

- #187 select low-risk write-pre candidate.
- #188 add draft/preview fixture.
- #189 extend validator checks.
- #190 output registry query fixture.

## Associated Artifacts

- tools/lode_validate_package.py
- registry/local-query.fixture.json
- sites/example/preview-contact-form/fixtures/core-consumption.fixture.json
- sites/example/preview-contact-form/fixtures/preview-contact-form.fixture.json
- .loom/specs/LODE-187/**
