# Implementation Contract

## Ownership

- Lode owns package refs, lifecycle, locks, schemas, fixtures, post-check, catalog metadata, local registry, and validator checks.
- Core owns task admission, Run Record, Result Envelope, and failure attribution truth.
- Harbor owns runtime facts, private capture, redaction, retention, and evidence refs.
- App owns local UI state and display.

## Allowed Edits

- registry/**
- sites/example/read-public-page/catalog-metadata.json
- sites/example/read-page-links/**
- sites/example/read-page-metadata/**
- tools/lode_validate_package.py
- .loom/**/LODE-149*
- .loom/status/current.md
- .loom/bootstrap/init-result.json

## Forbidden Edits

- No App/Core/Harbor implementation changes.
- No hosted registry, marketplace, sync, crawler, runtime execution, real account/profile/session, raw evidence, production data, or write behavior.

## Verification

- python3 -m py_compile tools/lode_validate_package.py
- python3 tools/lode_validate_package.py --registry-index registry/local-packages.json --all --json
- jq -e '.queries[0].results | length == 3' registry/local-query.fixture.json
- jq -e '.candidates | length == 3' registry/read-capability-candidates.json
- git diff --check
- loom suite validate --target . --item LODE-149 --json
- loom suite evidence validate --target . --item LODE-149 --json
- loom suite carrier validate --target . --item LODE-149 --json
- loom fact-chain --target . --json
- loom verify --target . --json
