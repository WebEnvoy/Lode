# Implementation Contract

## Work Item

- Item ID: GH-94
- Primary issue: https://github.com/WebEnvoy/Lode/issues/94
- Parent FR: https://github.com/WebEnvoy/Lode/issues/87
- Branch: work/GH-94-version-lifecycle
- Suite path: minimal

## Implementation Contract

- Write ownership is limited to the sample read package lifecycle metadata, manifest ref, and GH-94 Loom carrier.
- Preserve existing package identity from GH-90, input schema from GH-91, output schema from GH-92, and resource requirements from GH-93.
- Keep lifecycle `proposed`; do not claim stable default execution before fixture, post-check, validator, and Core consumption checks land.
- Lock input must be a declarative input contract only; do not create a lockfile, registry implementation, installer, or App UI.
- Deprecation and invalidation must be status metadata only; do not save live evidence, runtime state, credentials, production payloads, or user business data.

## Forbidden Scope

- Fixture payloads.
- Post-check logic or payloads.
- Validator, packer, tester, registry code, package manager initialization, dependencies, lockfiles, generated outputs, runtime behavior, live Harbor fact matching, provider/profile/session/cookie/token/raw evidence fields, hosted registry, marketplace, sync, crawler queue, benchmark contract, true write execution, Core, Harbor, App, or other repositories.
