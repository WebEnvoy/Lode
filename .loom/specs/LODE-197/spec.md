# Spec: Xiaohongshu and BOSS Site Knowledge Selection

## Story Readiness

- User value: Lode can turn existing Xiaohongshu and BOSS site knowledge into a clear asset boundary before package implementation starts.
- Success experience: reviewers can see which inputs are absorbed, remodeled, referenced, or rejected; what hierarchy each knowledge item belongs to; and which first read-only tasks are frozen for downstream package work.
- Failure states: source inventory missing, first task scope too broad, write behavior implied, Harbor/Core/App boundaries blurred, or direct unlicensed source copying.
- Sensitive data boundary: Lode stores only docs, ADR facts, source locators, field/route knowledge, and package design guidance; no credentials, profile state, runtime session, live tab, raw DOM/network payload, production evidence, or user business data.
- Non-goals: implement real capability packages, create schema/fixtures/validator logic, execute browser runtime, perform live write, edit sources/research, or enter Lode #198/#199/#200.

## Suite Path

- Suite path: minimal
- full-path-artifacts not_applicable rationale: docs-only product and asset boundary decision; consumer boundary: suite validation, review, merge-ready, and closeout consume spec.md, plan.md, evidence-map.md, task-carrier.md, and ADR 0006 only; recheck condition: switch to full suite when creating executable packages, schemas, fixtures, validators, runtime evidence contracts, or cross-repo contract ownership changes.
