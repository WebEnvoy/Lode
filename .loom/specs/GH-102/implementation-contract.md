# Implementation Contract

## Ownership

- Owner: repo-controller
- Work Item: GH-102
- Branch: `work/GH-102-core-fixture`

## Write Scope

- `sites/example/read-public-page/fixtures/core-consumption.fixture.json`
- `sites/example/read-public-page/manifest.json`
- `sites/example/read-public-page/package-lock.json`
- `sites/example/read-public-page/lifecycle-metadata.json`
- `registry/local-packages.json`
- `README.md`
- `.loom/work-items/GH-102.md`
- `.loom/progress/GH-102.md`
- `.loom/specs/GH-102/*`
- `.loom/reviews/GH-102*.json`
- `.loom/bootstrap/init-result.json`
- `.loom/status/current.md`

## Forbidden Scope

- WebEnvoy/Core, Harbor, or App repository changes.
- Core result envelope schema, runtime execution, browser automation, live source/evidence lookup, provider/profile/session fields, cookies, tokens, raw evidence bodies, production payloads, or user business data.
- Hosted registry, marketplace, sync service, crawler queue, benchmark contract, package publishing, write guardrail behavior, or true write capability.
- Merge or issue closeout.

## Acceptance

- Core consumption fixture is present and directly readable as JSON.
- Manifest, package lock, local registry, lifecycle metadata, and README expose the fixture consistently.
- Validator returns `passed` with no warnings for automatic repo-local index discovery and explicit `--registry-index registry/local-packages.json`.
- GH-102 `jq -e` structure check confirms expected fixture fields and false runtime/write claims.
- Loom suite/carrier/readback pass for GH-102 before PR creation.
