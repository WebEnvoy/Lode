# LODE-262 Spec

## Story Readiness

Lode supplies a mechanically checked, lock-bound admission asset for only `xhs_search_notes` and `boss_job_search`. Harbor #245 and Core #267 may consume it for restricted read-only admission. `proposed` remains proposed; the asset is neither a runtime runner nor evidence of a successful page operation.

## Suite Path

- Suite path: minimal
- full-path-artifacts not_applicable rationale: This Work Item changes only static Lode capability assets, offline validation, and item-specific carriers. It does not add a runtime server, browser automation, Core/Harbor API ownership, live evidence storage, or a write path.
- Consumer boundary: Lode local registry and its two downstream consumers, Harbor #245 and Core #267.
- Recheck condition: Use the full suite when a later Work Item changes a runtime API, browser/session behavior, Core run/result envelope, live evidence shape, or true write behavior.

## Acceptance

- Exactly two unique operation entries bind package ref, lock ref, version, read mode, canonical HTTPS origin, resource requirements, failure taxonomy, refs-only evidence, and post-check.
- Drift, unknown operation, non-HTTPS origin, non-read mode, and missing required assets fail closed.
- No Lode code accesses a browser, production site, account, profile, Cookie, or runtime session.

## Non-Goals

- No active lifecycle promotion, runtime execution, page parsing, Core result envelope, hosted registry, marketplace, or live evidence.
