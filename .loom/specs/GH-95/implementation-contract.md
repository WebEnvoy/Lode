# Implementation Contract

## Work Item

- Item ID: GH-95
- Primary issue: https://github.com/WebEnvoy/Lode/issues/95
- Parent FR: https://github.com/WebEnvoy/Lode/issues/88
- Branch: work/GH-95-redacted-fixture
- Suite path: minimal

## Implementation Contract

- Write ownership is limited to the sample read package fixture, manifest/lifecycle fixture refs, and GH-95 Loom carrier.
- Preserve existing package identity from GH-90, input schema from GH-91, output schema from GH-92, resource requirements from GH-93, and lifecycle metadata from GH-94.
- Keep lifecycle `proposed`; a fixture file does not imply stable default execution.
- Source/evidence refs must be placeholders suitable for offline fixture review; do not add live Harbor evidence, local paths, storage URLs, profile/provider/session details, credentials, production payloads, or user business data.
- Defer validator CLI checks to GH-96, post-check output to GH-97, failure mapping finalization to GH-98, and Core fixture consumption to GH-102.

## Forbidden Scope

- Validator, packer, tester, registry code, package manager initialization, dependencies, lockfiles, generated outputs, post-check payloads or runners, failure mapping finalization, local resolver/lock behavior, Core fixture consumption behavior, write guardrail behavior, runtime behavior, live Harbor fact matching, provider/profile/session/cookie/token/raw evidence fields, hosted registry, marketplace, sync, crawler queue, benchmark contract, true write execution, Core, Harbor, App, other repositories, merge, or issue closeout.
