# Implementation Contract

## Ownership

- Owner: repo-controller
- Work Item: GH-103
- Branch: `work/GH-103-write-guardrail`

## Write Scope

- `sites/example/read-public-page/write-deferred-guardrail.json`
- `tools/lode_validate_package.py`
- `sites/example/read-public-page/manifest.json`
- `sites/example/read-public-page/package-lock.json`
- `sites/example/read-public-page/lifecycle-metadata.json`
- `registry/local-packages.json`
- `README.md`
- `.loom/work-items/GH-103.md`
- `.loom/progress/GH-103.md`
- `.loom/specs/GH-103/*`
- `.loom/reviews/GH-103*.json`
- `.loom/bootstrap/init-result.json`
- `.loom/status/current.md`

## Forbidden Scope

- WebEnvoy/Core, Harbor, or App repository changes.
- Executable validate-only, draft, preview, or write packages.
- Runtime execution, browser automation, live source/evidence lookup, provider/profile/session fields, cookies, tokens, raw evidence bodies, production payloads, or user business data.
- Hosted registry, marketplace, sync service, crawler queue, benchmark contract, package publishing, or true write capability.
- Merge or issue closeout.

## Acceptance

- Write-deferred guardrail asset is present and directly readable as JSON.
- Manifest, package lock, local registry, lifecycle metadata, and README expose the guardrail consistently.
- Validator returns `passed` with no warnings for automatic repo-local index discovery and explicit `--registry-index registry/local-packages.json`.
- GH-103 `jq -e` structure check confirms guardrail schema version, deferred status, read-only current allowed mode, covered deferred modes, and blocked write execution.
- Loom suite/carrier/readback pass for GH-103 before PR creation.
