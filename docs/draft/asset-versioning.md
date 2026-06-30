# Asset Versioning Draft

- status: pointer
- owner: Lode docs / contracts
- linked issue: [#65](https://github.com/WebEnvoy/Lode/issues/65)
- exit condition: remove this pointer after downstream references use ADR / contracts only.

Asset version identity, dependency freshness, invalidation, Core Run Record reference boundaries, and deferred overlay conflict handling are accepted in [ADR 0004](../adr/0004-asset-types-and-registry.md). Remaining overlay / fork conflict details are tracked by [PD-0012](../adr/pending-decisions.md#pd-0012).

Judgment: this draft has no remaining independent implementation value. The stable version/reference pieces are in ADR 0004; unresolved overlay conflict behavior belongs to PD-0012, not a draft copy.

Do not use this draft as implementation truth.
