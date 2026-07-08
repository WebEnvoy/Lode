# LODE-253 Implementation Contract

## Required Inputs

- Work Items: #253, #254, #255, #256, #257.
- Parent FR: #252.
- Milestone: Lode #14.
- Target branch: `work/lode-253-runtime-boundary`.
- Target worktree: `/Volumes/2T/dev/WebEnvoy/Lode.worktrees/lode-253-runtime-boundary`.

## Ownership Contract

- May edit: `registry/local-packages.json`, `registry/local-query.fixture.json`, `docs/contracts/**`, `tools/**`, `.loom/work-items/LODE-253.md`, `.loom/progress/LODE-253.md`, `.loom/specs/LODE-253/**`.
- Must not edit: App/Core/Harbor repositories, `sources/`, `research/`, GitHub issue/PR/milestone state, real browser/account/profile state.

## Integration Evidence

- Registry entries and query fixture results expose Core-readable boundary fields.
- Focused validator enforces those fields for the six XHS/BOSS package refs.
- Contract docs define closeout evidence and runtime boundary.

## Recheck Condition

Re-run validation after any change to `registry/local-packages.json`, `registry/local-query.fixture.json`, the six XHS/BOSS package manifests, resource requirements, failure mappings, guardrails, or docs/contracts runtime boundary wording.
