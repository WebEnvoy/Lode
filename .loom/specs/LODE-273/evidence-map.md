# Evidence Map

| Evidence | Locator | Proves | Boundary |
| --- | --- | --- | --- |
| Registry truth | registry/local-packages.json | Per-package production admission state | Static capability truth only |
| Operation truths | registry/runtime-consumption-allowlist.json; registry/detail-runtime-consumption.json; registry/validate-only-runtime-consumption.json | Search/detail/precheck policy consistency | No runtime execution |
| Published schemas | registry/detail-runtime-consumption.schema.json; registry/validate-only-runtime-consumption.schema.json | Schema-only consumers reject inversion | No BOSS availability claim |
| Validators | tools/validate_*runtime_consumption.py | Missing/unknown/inverted/drift states fail closed | Offline only |
| Review | .loom/reviews/LODE-273.json | Current-head semantics reviewed | Merge gate only |
