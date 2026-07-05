# Spec: Stage 6 Write-Pre Candidate Fixture

## Story Readiness

- User value: Core/App can discover a low-risk write-precheck capability fixture that proves draft/preview shape without implying a submitted write.
- Success experience: the local registry returns the preview-contact-form validate-only package with candidate metadata, draft/preview fixture pointers, Core admission fields, active no-submit guard, and true-write blocked facts.
- Failure states: missing candidate metadata, missing draft/preview fixture pointer, absent no-submit guard, validator failure, sensitive material detected, or registry query not resolving.
- Sensitive data boundary: Lode stores only schemas, refs, redacted fixture summaries, package metadata, and no-submit facts; no credentials, profile state, runtime session, live tab, raw DOM/network/evidence, production payload, or user business data.
- Non-goals: true write execution, marketplace, hosted sync, crawler queue, full workflow runtime, Core result envelopes, Harbor capture, and App UI.

## Suite Path

- Suite path: minimal
- full-path-artifacts not_applicable rationale: bounded package/fixture/catalog contract slice; consumer boundary: Core/App consume package refs, schema refs, candidate metadata, and redacted fixture pointers only; recheck condition: switch to full suite when adding executable write behavior, hosted registry, runtime execution, or private material handling.
