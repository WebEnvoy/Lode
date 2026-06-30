# Spec

## Goal

Record the minimum docs-only decision surface for the first low-risk read capability candidate class, package shape, fixture/post-check evidence, research absorption, and write-side non-goals.

## Scope

- In scope: `docs/adr/pending-decisions.md` and GH-19 item-specific Loom carrier.
- Out of scope: full schema, validator, package directory, real capability implementation, marketplace, crawler queue, benchmark task contract, generic browser agent loop, live write capability, issue closeout, and merge.

## Required Behavior

- Prefer low-risk read capability candidates: single-page structured extraction, page state summary, and bounded list field extraction.
- Define Lode's minimum package responsibility: metadata, input shape, result shape, evidence requirements, fixture/post-check, version/deprecation.
- Absorb OpenCLI/Syvert/old WebEnvoy/MediaCrawler only as asset model and field seeds.
- Keep validate-only/draft/preview as future write-side asset shapes; true write capability remains deferred.

## Suite Path

- Suite path: minimal
- Full suite artifacts not_applicable: rationale: this PR changes repository docs and item-specific Loom carriers only; consumer boundary: GH issues, ADR readers, Loom review, and merge gate consume the decision table and carrier metadata, not executable schemas or runtime behavior; recheck condition: require full suite if the PR adds schema/API/runtime code, package directories, fixtures, generated assets, real capability implementations, workflow logic, external writes, or user-facing behavior.
