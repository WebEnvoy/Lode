# Implementation Contract

## Ownership

- Primary Work Item: GH-96
- Parent FR: GH-88
- Branch: `work/GH-96-validator-cli`
- Owner: repo-controller

## Allowed Writes

- `tools/lode_validate_package.py`
- `README.md`
- `.github/workflows/loom-check.yml`
- `sites/example/read-public-page/manifest.json`
- `sites/example/read-public-page/lifecycle-metadata.json`
- `sites/example/read-public-page/fixtures/read-public-page.fixture.json`
- `.loom/work-items/GH-96.md`
- `.loom/progress/GH-96.md`
- `.loom/specs/GH-96/*`
- `.loom/reviews/GH-96*.json`
- `.loom/status/current.md`
- `.loom/bootstrap/init-result.json`

## Forbidden Writes

- Package manager files or dependency lockfiles.
- Generated validator reports committed to the repo.
- Post-check output contract, post-check runner, or failure mapping finalization.
- Local resolver, lockfile, registry, packer, tester, Core fixture consumption, or write guardrail behavior.
- Runtime, browser, Core, Harbor, App, provider/profile/session/evidence, hosted registry, marketplace, crawler queue, benchmark, or live write behavior.

## Acceptance

- The validator command reads `sites/example/read-public-page` and emits a structured report with no errors.
- The expected planned post-check remains a warning until GH-97.
- Hosted `repo-local-cli` runs the validator command.
- Loom fact-chain, suite validation, carrier validation, review read, and PR metadata preflight pass for GH-96.
