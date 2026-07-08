# LODE-253 Plan

## Steps

1. Read governance, roadmap, and issue context for #252-#257.
2. Create the requested formal worktree and branch.
3. Add Core-readable registry/runtime boundary fields to existing Lode assets.
4. Add focused validation that checks registry and query fixture consumption fields.
5. Add contract docs and item-specific Loom carrier.
6. Run focused validation and repository checks.

## Ownership

- Write scope: Lode registry, capability boundary docs, validator, and LODE-253 Loom carrier.
- Forbidden scope: App, Core, Harbor, external sites, accounts, profiles, cookies, live browser state, issue/PR/milestone writes.

## Validation Strategy

- `python3 tools/validate_runtime_boundary_contract.py`
- `python3 tools/lode_validate_package.py --registry-index registry/local-packages.json --all --json`
- `PYTHONDONTWRITEBYTECODE=1 python3 -m py_compile tools/lode_validate_package.py tools/validate_runtime_boundary_contract.py`
- JSON readability for touched JSON and carrier JSON.
- `git diff --check`
- Loom fact-chain/verify/suite carrier checks when available.
