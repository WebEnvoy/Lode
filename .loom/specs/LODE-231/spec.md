# LODE-231 Spec

## User Story

As WebEnvoy capability authors and downstream Core/App consumers, we need a single Lode truth carrier that says what bb-sites Xiaohongshu/BOSS knowledge can be absorbed, what must only be referenced, what must be rejected, and which first capabilities are frozen before any runtime implementation.

## Suite Path

- Suite path: minimal
- full-path-artifacts not_applicable rationale: This PR adds repo-local Lode docs/light-metadata carriers only; it does not add package schema changes, runtime code, cross-repo API ownership, live evidence storage, or executable browser automation.
- Consumer boundary: review and PR readiness may consume source absorption, field mapping, license/copy boundary, first-batch capability boundary, and user confirmation requirements.
- Recheck condition: Switch to full suite when a later PR changes package schemas, registry, validator/tooling, live runtime execution, Core result envelopes, Harbor evidence schemas, true write behavior, hosted registry behavior, or cross-repo contract ownership.

## Acceptance

- The carrier lists absorb/reference/reject material for bb-sites Xiaohongshu and BOSS.
- It maps search and detail fields from bb-sites source/wiki into existing Lode package inputs, outputs, and follow-up refs.
- It records the license boundary and forbids direct source copy.
- It freezes first read and validate-only write-precheck capabilities.
- It lists user confirmations required before any real browser execution.
- It does not add runtime code or save sensitive/live evidence.

## Non-goals

- No Harbor/Core/App changes.
- No real site run, account login, live evidence, DOM/HAR/screenshot body, cookie/token/profile state, or production payload.
- No publish, upload, send, greet, apply, follow, delete, or CAPTCHA/safety bypass.
