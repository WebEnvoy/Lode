# LODE-273

## Static Facts

- Item ID: LODE-273
- Goal: Preserve BOSS capability assets while making production runtime admission mechanically disabled/deferred and keeping Xiaohongshu enabled/current.
- Scope: Production package registry, search/detail/validate-only consumption truths, published schemas, validators, fixtures, and LODE-273 carriers.
- Execution Path: work/lode-273-boss-deferred-admission
- Workspace Entry: .
- Recovery Entry: .loom/progress/LODE-273.md
- Review Entry: .loom/reviews/LODE-273.json
- Validation Entry: registry self-tests, package/runtime-boundary validation, Python compile, JSON parse, diff and Loom checks.
- Closing Condition: PR #274 merged after current-head code/spec review and hosted gate; close #273 only as static admission truth, not runtime/live evidence.

## GitHub Binding

- Work Item: https://github.com/WebEnvoy/Lode/issues/273
- Parent FR: https://github.com/WebEnvoy/Lode/issues/252
- Consumers: https://github.com/WebEnvoy/WebEnvoy/issues/281 and https://github.com/WebEnvoy/App/issues/290

## Non-Goals

- No capability asset deletion, runtime server, browser/page execution, BOSS live evidence, external write, profile/Cookie access, or risk-control bypass.

## Associated Artifacts

- .loom/specs/LODE-273/spec.md
- .loom/specs/LODE-273/plan.md
- .loom/specs/LODE-273/implementation-contract.md
- .loom/specs/LODE-273/evidence-map.md
- .loom/specs/LODE-273/task-carrier.md
- registry/local-packages.json
- registry/runtime-consumption-allowlist.json
- registry/detail-runtime-consumption.json
- registry/validate-only-runtime-consumption.json
