# Optional Result-View Declaration

This contract lets a capability package describe an optional result view without making that
view authoritative or executable inside Lode. Structured output remains the result truth, and
consumers always retain the standard renderer.

## Catalog Contract

Every current `catalog-metadata.json` explicitly exposes `result_view` in one of two states.
For backward compatibility, a missing field has the same standard-renderer-only meaning as
`absent` and is not an invalid package:

- `absent`: only `status: absent` and `fallback: standard_renderer`; this is a valid package.
- `present`: conforms to
  [`schemas/result-view-declaration.schema.json`](../../schemas/result-view-declaration.schema.json)
  and declares its own version, view identity/version, immutable package-scoped `resource_ref`,
  package-relative `resource_path`, output compatibility, SHA-256 digest, current package
  `lock_ref`, and the mandatory standard-renderer fallback.

Compatibility may name the exact normalized output schema ref/version, one or more stable
`result_kind` values, or both. When both are present, both constraints must match the current
package output.

## Validation And Ownership

- Lode owns the declaration, resource identity, compatibility metadata, and package lock.
- Core may record the declaration and lock refs selected when a result is generated.
- App may display compatibility and fall back to its standard renderer.
- A present resource must resolve inside the capability package, match its SHA-256 digest, and
  appear as `result_view_resource` in both manifest `asset_refs` and package `locked_assets`.
- Malformed declarations, output mismatches, out-of-root paths, missing files, integrity drift,
  or lock drift are `invalid_contract`/`unsupported_version` failures and must not activate the
  optional view.

This contract does not define HTML/Component execution, a resource loading protocol, sandboxing,
remote scripts, runtime access, or an App/Core action bridge.
