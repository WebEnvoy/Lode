# LODE-262 Implementation Contract

## Required Inputs

- Work Item: #262; Parent FR: #261; Milestone: Lode #14.
- Consumers: Harbor #245 and Core/WebEnvoy #267.
- Branch: `work/lode-262-allowlist-correction`; worktree: `.`.

## Boundary

The output is a static Lode capability asset. `allowed_consumers` must exactly equal Harbor #245 and Core/WebEnvoy #267 with their declared purposes. The failure map must contain exactly the declared conditions, each set to `reject`. Consumers must reject contract drift and must not infer active lifecycle, live evidence, or operation success. Harbor owns browser/session/evidence facts and Core owns task/run envelopes.
