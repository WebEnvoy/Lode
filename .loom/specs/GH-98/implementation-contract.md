# Implementation Contract

## Ownership

- Owner: repo-controller
- Work Item: GH-98
- Branch: `work/GH-98-failure-mapping`

## Write Scope

- `sites/example/read-public-page/failure-mapping.json`
- `sites/example/read-public-page/manifest.json`
- `sites/example/read-public-page/lifecycle-metadata.json`
- `sites/example/read-public-page/fixtures/read-public-page.fixture.json`
- `sites/example/read-public-page/schemas/output.schema.json`
- `tools/lode_validate_package.py`
- `README.md`
- `.loom/work-items/GH-98.md`
- `.loom/progress/GH-98.md`
- `.loom/specs/GH-98/*`
- `.loom/reviews/GH-98*.json`
- `.loom/status/current.md`

## Forbidden Scope

- New dependencies or package manager initialization.
- Generated schema/types/reports committed to the repo.
- Core result envelope schema, App UI copy contract, runtime/live matching, Harbor evidence schema, provider/profile/session state, cookies, tokens, raw evidence bodies, production payloads, or user business data.
- Local resolver, lockfile, registry, packer, tester behavior, Core fixture consumption behavior, write guardrail behavior, hosted registry, marketplace, crawler queue, benchmark contract, Core/Harbor/App changes, merge, or issue closeout.

## Acceptance

- The validator returns `passed` with no warnings for the sample package.
- `failure-mapping.json` declares `invalid_contract`, `resource_unavailable`, `site_changed`, and `empty_result`.
- The mapping keeps exact Core envelope fields and App copy outside Lode ownership.
- Loom suite/carrier/review readback pass for GH-98 before PR creation.
