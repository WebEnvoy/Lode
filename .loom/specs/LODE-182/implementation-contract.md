# Implementation Contract

## Scope

- Touch only Lode preview package assets, package validator checks, and item-specific Loom carrier for #182/#183/#184/#185.
- Keep true-write execution blocked and keep all values redacted or ref-only.

## Verification

- `python3 -m py_compile tools/lode_validate_package.py`
- `python3 tools/lode_validate_package.py --registry-index registry/local-packages.json --all --json`
- `git diff --check`
