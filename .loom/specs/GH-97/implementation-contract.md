# Implementation Contract

## Ownership

- Owner: repo-controller
- Work Item: GH-97
- Branch: `work/GH-97-post-check-output`

## Write Scope

- `sites/example/read-public-page/checks/post-check.json`
- `sites/example/read-public-page/manifest.json`
- `sites/example/read-public-page/lifecycle-metadata.json`
- `sites/example/read-public-page/fixtures/read-public-page.fixture.json`
- `tools/lode_validate_package.py`
- `README.md`
- `.loom/work-items/GH-97.md`
- `.loom/progress/GH-97.md`
- `.loom/specs/GH-97/*`
- `.loom/reviews/GH-97*.json`
- `.loom/status/current.md`

## Forbidden Scope

- New dependencies or package manager initialization.
- Generated schema/types/reports committed to the repo.
- Post-check runner, browser automation, runtime/live evidence, Core result envelope, Harbor evidence schema, provider/profile/session state, cookies, tokens, raw evidence bodies, production payloads, or user business data.
- Failure mapping finalization beyond existing class names, local resolver/lockfile behavior, Core fixture consumption behavior, write guardrail behavior, hosted registry, marketplace, crawler queue, benchmark contract, Core/Harbor/App changes, merge, or issue closeout.

## Acceptance

- The validator returns `passed` with no warnings for the sample package.
- `checks/post-check.json` declares status, reason, source refs, and evidence refs.
- The sample fixture post-check output binds only to declared fixture refs.
- Loom suite/carrier/review readback pass for GH-97 before PR creation.
