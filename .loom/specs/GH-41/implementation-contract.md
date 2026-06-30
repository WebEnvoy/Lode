# Implementation Contract

- Write scope: `docs/adr/0004-asset-types-and-registry.md`, `docs/adr/0003-schema-fixtures-and-post-check.md`, `.loom/**/GH-41*`, `.loom/status/current.md`, and `.loom/bootstrap/init-result.json` only for active item readout.
- Forbidden scope: real capability package, schema, fixture, validator, registry, workflow runner, runtime code, hosted marketplace, live write behavior, issue closeout, merge, `INIT-0001`, and unrelated Work Items #47/#51/#55.
- Validation floor: `git diff --check`, JSON validation, Loom local checks with blocker classification, and hosted checks after PR creation if available.
