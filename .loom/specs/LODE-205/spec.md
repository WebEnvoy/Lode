# Spec: Xiaohongshu Real Read Capabilities

## Story Readiness

- User value: A user with an existing Xiaohongshu identity environment can ask WebEnvoy to read real search results and one note detail through Lode packages.
- Success experience: Core/App can discover two Xiaohongshu read packages, understand required runtime facts, validate fixture shapes, pass a search result follow-up ref into detail, and show actionable failure reasons.
- Failure states: not logged in, login expired, page not ready, signed note ref missing, site changed, safety challenge, required field missing, network/resource unavailable, invalid contract, or empty result.
- Sensitive data boundary: Lode stores only package contracts, field/source mapping summaries, placeholder refs, and synthetic fixtures. Lode does not store credentials, account state, browser runtime state, raw page bodies, network bodies, screenshots, production payloads, or user business data.
- Non-goals: No Stage 7, no login automation, no comments/feed/profile/creator-center, no note posting, commenting, liking, following, messaging, upload, deletion, batch crawling, safety-control bypass, Harbor/Core/App changes, or sources/research edits.

## Suite Path

- Suite path: minimal
- full-path-artifacts not_applicable rationale: This PR adds repo-local Lode assets and fixtures only; it does not add runtime code, cross-repo API ownership, live evidence storage, or executable browser automation.
- Consumer boundary: validator, registry, Core/App package discovery, resource requirement declaration, fixture shape, post-check fixture output, and failure vocabulary.
- Recheck condition: Switch to full suite when a later PR adds live runtime execution, Core result envelopes, Harbor evidence schemas, write/precheck behavior, hosted registry behavior, or cross-repo contract ownership changes.

## Acceptance

- `sites/xiaohongshu/search-notes` validates as a read package.
- `sites/xiaohongshu/read-note-detail` validates as a read package.
- Local registry resolves both package refs.
- Failure mapping includes login, readiness, signed-ref, page-change, safety challenge, field-missing, and resource failures.
- Contract docs cite absorbed bb-sites/OpenCLI/SignSrv concepts and explicitly reject copied runtime code and write behavior.
- Real page validation is marked pending human runtime when no logged-in site session is available.
