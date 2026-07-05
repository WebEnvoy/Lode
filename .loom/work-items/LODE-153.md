# LODE-153

## Static Facts

- Item ID: LODE-153
- Goal: Expose Stage 5 read-only capability catalog metadata for App Library consumption
- Scope: Add local package catalog metadata, package lock refs, registry discoverability, and validator coverage for the sample read-only package
- Execution Path: stage5/read-only-capability-catalog
- Workspace Entry: .
- Recovery Entry: .loom/progress/LODE-153.md
- Review Entry: .loom/reviews/LODE-153.json
- Validation Entry: python3 tools/lode_validate_package.py sites/example/read-public-page && git diff --check
- Closing Condition: Lode #153 catalog metadata fixture is validated and consumed by App/Core dependency PRs without storing App state or runtime truth in Lode

## Associated Artifacts

- `.loom/work-items/LODE-153.md`
- `.loom/progress/LODE-153.md`
- `.loom/reviews/LODE-153.json`
- `.loom/status/current.md`
- `registry/local-packages.json`
- `sites/example/read-public-page/catalog-metadata.json`
- `sites/example/read-public-page/manifest.json`
- `sites/example/read-public-page/package-lock.json`
- `tools/lode_validate_package.py`
