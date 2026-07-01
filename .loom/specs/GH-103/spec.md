# Spec

- Suite path: minimal

## Goal

Make the first sample read package fail closed on non-target write-side behavior by declaring validate-only, draft, preview, and true write capability modes deferred, without adding runtime execution or changing Core/Harbor/App code.

## Required Behavior

- Add `sites/example/read-public-page/write-deferred-guardrail.json`.
- The guardrail declares package ref, capability identity, current operation mode `read`, deferred write-side modes, blocked claims, validate-only boundary, draft/preview boundary, true write entry conditions, and admission rejection conditions.
- Manifest asset refs expose `write_deferred_guardrail` as a present GH-103 asset with guardrail id/version.
- Package lock includes the guardrail locked asset and treats guardrail identity/path/boundary changes as invalidation or relock relevant.
- Local registry exposes `write_deferred_guardrail_path` and includes `write_deferred_guardrail` in `asset_roles`.
- Lifecycle metadata records the guardrail in promotion requirements, lock input, version identity, and revalidation triggers while keeping lifecycle `proposed`.
- Validator loads the guardrail asset, verifies identity/package/capability alignment, requires deferred status, requires coverage for validate-only/draft/preview/write modes, requires current allowed mode to remain `read`, and requires write execution to stay blocked.
- README documents the guardrail as an offline fail-closed declaration and states it does not execute or authorize write-side behavior.
- Existing package validation remains clean for automatic local registry discovery and explicit registry-index validation.
- A GH-103-specific `jq -e` check proves the guardrail is directly readable and keeps deferred/blocked status.
- PR metadata and Loom carrier bind to GH-103, not INIT-0001 or previous Work Items.

## Non-Goals

- Do not modify WebEnvoy/Core, Harbor, or App.
- Do not implement executable validate-only, draft, preview, or write packages.
- Do not execute runtime/browser/live checks or external-visible writes.
- Do not add hosted registry, marketplace, sync service, crawler queue, benchmark contract, package publishing, or true write capability.
- Do not store cookies, tokens, account state, raw evidence bodies, complete DOM, HAR, screenshots, production payloads, or user business data.

## Suite Path

- Suite path: minimal
- Full suite artifacts not_applicable rationale: GH-103 is a narrow static guardrail/discoverability/validator change with no dependencies, runtime behavior, external-visible action, release, or issue closeout.
- Consumer boundary: `sites/example/read-public-page/write-deferred-guardrail.json`, `tools/lode_validate_package.py`, package manifest/lock/lifecycle metadata, `registry/local-packages.json`, `README.md`, `.loom/work-items/GH-103.md`, `.loom/progress/GH-103.md`, `.loom/specs/GH-103/*`, `.loom/bootstrap/init-result.json`, and `.loom/status/current.md`.
- Recheck condition: require stronger/full validation if this PR adds Core/Harbor/App behavior, generated outputs, dependencies, package manager changes, hosted registry behavior, runtime/live matching, provider/profile/session fields, external-visible writes, or non-GH-103 carrier scope.
