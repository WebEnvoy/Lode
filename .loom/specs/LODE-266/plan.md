# LODE-266 Plan

1. Bind the origin/main worktree and take over the current Loom pointer with LODE-266.
2. Add schema, registry truth, fixture, submitted=false post-check requirements, and offline fail-closed validation.
3. Run targeted and repository validation, then create a ready PR anchored by #266 and covering #267.

## Ownership

- May edit: Lode registry/schema/fixtures, the two bound post-check contracts, offline validator, and LODE-266 carriers.
- Must not edit: Other repositories, live runtime/account/session material, unrelated assets, issue state, or merge state.
