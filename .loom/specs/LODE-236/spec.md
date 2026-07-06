# Spec: Xiaohongshu Real Read and Write-Precheck Capability Batch

## Story Readiness

- User value: Core/App/Harbor can discover and consume Xiaohongshu real-site package definitions for search results, note detail, and publish draft write-precheck without relying on bb-sites runtime code.
- Success experience: Core/App can resolve all three package refs, validate their schemas and fixtures, understand real page entrypoints, bind source/evidence requirements to Harbor-owned refs, preserve search-to-detail signed refs, and enforce no-submit for publish precheck.
- Failure states: not logged in, login expired, page not ready, signed detail ref missing, page changed, permission insufficient, target not writable, safety challenge, preview unavailable, field missing, empty result, resource unavailable, evidence expired, user cancelled, or invalid package contract.
- Sensitive data boundary: Lode stores only package contracts, public field names, source/evidence reference policies, placeholder refs, and redacted fixtures. Lode does not store cookies, tokens, profile state, runtime session, raw DOM, HAR, network bodies, screenshot bodies, production payloads, or user business data.
- Non-goals: No real account access, no live site execution, no login automation, no comments/feed/user profile capabilities, no publish/upload/save/comment/like/collect/follow/delete/message action, no safety-control bypass, no Harbor/Core/App changes, no `sources/` or `research/` edits, no merge, and no issue closeout.

## Suite Path

- Suite path: minimal
- full-path-artifacts not_applicable rationale: This PR changes repo-local Lode assets, fixtures, registry entries, docs, and item-specific carriers only. It does not add runtime code, cross-repo API ownership, live evidence storage, true write execution, hosted registry behavior, or browser automation.
- Consumer boundary: Lode validator, local registry, Core/App package discovery, Harbor/Core refs-only evidence requirements, fixture shape, post-check fixture output, source absorption record, and failure vocabulary.
- Recheck condition: Upgrade to full suite when a later PR adds live runtime execution, Core result envelopes, Harbor evidence schemas, true write behavior, hosted registry behavior, or cross-repo contract ownership changes.

## Acceptance

- `sites/xiaohongshu/search-notes` validates as a read package for #236/#239.
- `sites/xiaohongshu/read-note-detail` validates as a read package for #237/#239.
- `sites/xiaohongshu/publish-note-precheck` validates as a `validate_only` package for #238/#239.
- Local registry resolves all three package refs and exposes a FR #235 Xiaohongshu package query.
- Package assets declare real page entrypoints, input/output fields, evidence requirements, failure classes, and post-check plans.
- Publish precheck declares expected change, risk hints, active no-submit guard, true write blocked, and no external submit.
- bb-sites and wiki mechanisms are absorbed as field/route/failure/evidence knowledge only; source code and runtime interception are rejected.
- Live account validation is explicitly not attempted under this worker's forbidden-action boundary.
