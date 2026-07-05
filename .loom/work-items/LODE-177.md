# LODE-177

## Static Facts

- Item ID: LODE-177
- Goal: Complete validate-only, draft, and preview capability package contract spine without true-write execution.
- Scope: Batch covers Lode #177, #178, #179, and #180 under FR #176.
- Execution Path: stage6/write-precheck-package-spine
- Workspace Entry: .
- Recovery Entry: .loom/progress/LODE-177.md
- Review Entry: .loom/reviews/LODE-177.json
- Validation Entry: python3 -m py_compile tools/lode_validate_package.py; python3 tools/lode_validate_package.py --registry-index registry/local-packages.json --all --json; git diff --check
- Closing Condition: Repo-local Lode package facts express validate-only/draft/preview metadata, schemas, write-precheck resource requirements, and no-submit guard while true write remains blocked.

## Covered Work Items

- #177 extend package metadata for validate-only/draft/preview.
- #178 add input/output schemas.
- #179 define write-precheck resource requirements.
- #180 declare no-submit and validate-only guard.

## Associated Artifacts

- tools/lode_validate_package.py
- registry/local-packages.json
- registry/local-query.fixture.json
- sites/example/preview-contact-form/**
- .loom/specs/LODE-177/**
- .loom/status/current.md
