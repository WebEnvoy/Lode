# Resource Requirements Draft

- status: pointer
- owner: Lode docs / contracts
- linked issue: [#65](https://github.com/WebEnvoy/Lode/issues/65)
- exit condition: remove this pointer after downstream references use ADR / contracts only.

Resource requirement profiles, Harbor facts consumption, `matched` / `unmatched` / `invalid_contract`, and read / validate-only / write-like boundaries are accepted in [ADR 0003](../adr/0003-schema-fixtures-and-post-check.md) and indexed in [contracts](../contracts/).

Judgment: this draft has no remaining independent implementation value. Core admission should read ADR 0003; keeping the body here would create a second resource-matching contract.

Do not use this draft as implementation truth.
