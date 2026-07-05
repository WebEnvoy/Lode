# Implementation Contract

## Scope

- Touch only Lode package/schema/fixture/validator facts needed by #177/#178/#179/#180.
- Keep true-write execution blocked and declare validate-only/draft/preview as pre-write modes only.

## Verification

- `python3 -m py_compile tools/lode_validate_package.py`
- `python3 tools/lode_validate_package.py --registry-index registry/local-packages.json --all --json`
- `git diff --check`
