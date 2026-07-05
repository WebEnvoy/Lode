# Spec: Stage 6 Expected Change And Preview Semantics

## Story Readiness

- User value: a caller can see what a write-precheck would change, why it is risky, how preview post-check evaluates it, and why preview failed without mistaking it for a submitted write.
- Success experience: Core/App can consume structured expected change, risk hints, post-check facts, and preview failure classes from Lode package assets.
- Failure states: missing expected change, unknown risk hint, failed preview post-check, page changed, preview unavailable, user cancelled, or evidence unavailable.
- Sensitive data boundary: Lode stores only redacted summaries and refs; no credentials, profile state, runtime session, live tab, raw DOM/network/evidence, production payload, or user business data.
- Non-goals: true write execution, marketplace/hosted sync, generic workflow runtime, Core preview Result Envelope, Harbor evidence bodies, and App UI.

## Suite Path

- Suite path: minimal
- full-path-artifacts not_applicable rationale: bounded package/schema/fixture contract slice; consumer boundary: Core/App consume refs, schemas, and static preview facts only; recheck condition: switch to full suite when adding executable write behavior, hosted registry, runtime execution, or private material handling.
