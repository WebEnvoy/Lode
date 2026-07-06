# Spec: BOSS Real Read and Write-Precheck Capability Batch

## Story Readiness

- User value: Core/App/Harbor can discover and consume BOSS real-site package definitions for job search, job detail, and greet write-precheck without relying on bb-sites runtime code.
- Success experience: Core/App can resolve all three package refs, validate their schemas and fixtures, understand real page entrypoints, bind source/evidence requirements to Harbor-owned refs, preserve `securityId` and `encryptJobId` search-to-detail refs, and enforce no-submit for greet precheck.
- Failure states: not logged in, identity insufficient, CAPTCHA or safety challenge, page not ready, missing query, unresolved city/filter, missing `securityId`, pagination limited, job expired, permission denied, target not writable, page changed, preview unavailable, field missing, empty result, resource unavailable, evidence expired, user cancelled, or invalid package contract.
- Sensitive data boundary: Lode stores only package contracts, public field names, source/evidence reference policies, placeholder refs, and redacted fixtures. Lode does not store cookies, tokens, profile state, runtime session, raw DOM, HAR, network bodies, screenshot bodies, production payloads, candidate/customer data, or user business data.
- Non-goals: No real account access, no live site execution, no login automation, no candidate management, no batch pagination, no apply/greet/chat/send/save/upload action, no safety-control bypass, no Harbor/Core/App changes, no `sources/` or `research/` edits, no merge, and no issue closeout.

## Suite Path

- Suite path: minimal
- full-path-artifacts not_applicable rationale: This PR changes repo-local Lode assets, fixtures, registry entries, docs, and item-specific carriers only. It does not add runtime code, cross-repo API ownership, live evidence storage, true write execution, hosted registry behavior, or browser automation.
- Consumer boundary: Lode validator, local registry, Core/App package discovery, Harbor/Core refs-only evidence requirements, fixture shape, post-check fixture output, source absorption record, and failure vocabulary.
- Recheck condition: Upgrade to full suite when a later PR adds live runtime execution, Core result envelopes, Harbor evidence schemas, true write behavior, hosted registry behavior, or cross-repo contract ownership changes.

## Acceptance

- `sites/boss/job-search` validates as a read package for #241/#244.
- `sites/boss/read-job-detail` validates as a read package for #242/#244.
- `sites/boss/greet-precheck` validates as a `validate_only` package for #243/#244.
- Local registry resolves all three package refs and exposes a FR #240 BOSS package query.
- Package assets declare real page entrypoints, input/output fields, evidence requirements, failure classes, and post-check plans.
- Greet precheck declares expected change, risk hints, active no-submit guard, true write blocked, and no external submit.
- bb-sites and research mechanisms are absorbed as field/route/failure/evidence knowledge only; source code and runtime adapters are rejected.
- Live account validation is explicitly not attempted under this worker's forbidden-action boundary.
