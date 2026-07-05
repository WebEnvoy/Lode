# LODE-149

## Static Facts

- Item ID: LODE-149
- Goal: Complete Stage 5 read capability lifecycle/catalog foundation for first 2-3 low-risk read capability assets.
- Scope: Batch covers Lode issues #149, #150, #151, #154, and #155. Parent FR readback/closeout covers #139, #140, and #141 after merge.
- Execution Path: stage5/read-capability-assets
- Workspace Entry: .
- Recovery Entry: .loom/progress/LODE-149.md
- Review Entry: .loom/reviews/LODE-149.json
- Validation Entry: python3 -m py_compile tools/lode_validate_package.py; python3 tools/lode_validate_package.py --registry-index registry/local-packages.json --all --json; jq local registry query/candidate checks; git diff --check
- Closing Condition: Three repo-local read capability packages validate with schema, resource requirements, fixtures, post-checks, Core admission fields, and local registry query fixture; no runtime/private/write material enters Lode.

## Covered Work Items

- #149 select first 2-3 low-risk read capability candidates.
- #150 add input/output schema and resource requirements for each capability.
- #151 add fixture and post-check for each capability.
- #154 define Core admission fields.
- #155 output local registry query fixture.

## Associated Artifacts

- registry/local-packages.json
- registry/read-capability-candidates.json
- registry/local-query.fixture.json
- sites/example/read-public-page/**
- sites/example/read-page-links/**
- sites/example/read-page-metadata/**
- tools/lode_validate_package.py
- .loom/specs/LODE-149/**
- .loom/status/current.md
- .loom/bootstrap/init-result.json
