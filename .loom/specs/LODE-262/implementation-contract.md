# LODE-262 Implementation Contract

## Required Inputs

- Work Item: #262; Parent FR: #261; Milestone: Lode #14.
- Consumers: Harbor #245 and Core/WebEnvoy #267.
- Branch: `work/lode-262-runtime-consumption-allowlist`; worktree: `.`.

## Boundary

The output is a static Lode capability asset. Consumers must reject entries on contract drift and must not infer active lifecycle, live evidence, or operation success. Harbor owns browser/session/evidence facts and Core owns task/run envelopes.
