# LODE-231 Implementation Contract

## Write Ownership

- Allowed: `docs/contracts/bb-sites-xhs-boss-absorption-freeze.md`, docs indexes, README link, and `.loom/**/LODE-231*` carriers.
- Forbidden: `sites/**` package semantics, `registry/**`, `tools/**`, Harbor/Core/App repos, `sources/**`, `research/**`, live runtime artifacts, issue closeout, merge.

## Validation Expectation

- `python3 tools/lode_validate_package.py --registry-index registry/local-packages.json --all --json`
- JSON readability for changed/new JSON carriers if any.
- `git diff --check`
- `loom verify --target . --json`
- `loom fact-chain --target . --json`
- `loom suite validate --target . --item LODE-231 --json` and carrier/evidence checks when the local Loom surface can consume the minimal suite.
