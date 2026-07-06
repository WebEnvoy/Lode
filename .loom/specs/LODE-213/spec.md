# Spec: Real-Page Write-Precheck Capabilities

## Story Readiness

- User value: A user can prepare Xiaohongshu draft/content edits or BOSS greeting communication with a real-page write-precheck preview before any external action occurs.
- Success experience: Core/App can discover two validate-only packages, understand page and runtime requirements, validate fixture shapes, show expected changes and risk hints, and keep no-submit guard active.
- Failure states: page changed, login required, permission insufficient, target not writable, safety challenge, preview unavailable, evidence expired, user cancelled, resource unavailable, invalid contract, or empty result.
- Sensitive data boundary: Lode stores only package contracts, field/source mapping summaries, placeholder refs, and synthetic fixtures. Lode does not store credentials, account state, browser runtime state, raw page bodies, network bodies, screenshots, production payloads, candidate/customer data, or user business data.
- Non-goals: No real publish, draft save, upload, scheduled publish, BOSS greet, chat, send, apply, resume upload, login automation, safety-control bypass, Harbor/Core/App changes, or sources/research edits.

## Suite Path

- Suite path: minimal
- full-path-artifacts not_applicable rationale: This PR adds repo-local Lode assets, fixtures, registry entries, and docs only; it does not add runtime code, cross-repo API ownership, live evidence storage, or executable browser automation.
- Consumer boundary: validator, registry, Core/App package discovery, resource requirement declaration, fixture shape, expected-change/risk/no-submit output, post-check fixture output, and failure vocabulary.
- Recheck condition: Switch to full suite when a later PR adds live runtime execution, Core result envelopes, Harbor evidence schemas, true write behavior, hosted registry behavior, or cross-repo contract ownership changes.

## Acceptance

- `sites/xiaohongshu/publish-note-precheck` validates as a `validate_only` write-precheck package.
- `sites/boss/greet-precheck` validates as a `validate_only` write-precheck package.
- Local registry resolves both package refs and exposes a write-precheck query result.
- Output fixtures include `expected_change`, `risk_hints`, and `no_submit_guard_status`.
- Failure mapping includes page change, login required, permission insufficient, target not writable, safety challenge, preview unavailable, and user cancellation.
- Contract docs cite absorbed research/source locators and explicitly reject copied runtime code and true write behavior.
- Real page validation is marked pending human runtime when no logged-in site session is available.
