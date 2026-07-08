# Lode Runtime Boundary And Closeout Evidence

Status: proposed for Lode #252/#253/#254/#255/#256/#257, 2026-07-08 UTC.

## Scope

This contract corrects the closeout language for the current real-runtime loop.
Lode owns capability assets, schemas, fixtures, post-check declarations,
resource requirements, failure taxonomy, lifecycle metadata, and the repo-local
registry. Lode is not a runtime runner.

## Core Registry Consumption

Core may consume `registry/local-packages.json` and
`registry/local-query.fixture.json` for local admission and reference checks:

- package identity: `package_ref`, `version`, `lock_ref`, `lifecycle`;
- local locators: `package_path`, `manifest_path`, `lock_path`;
- routing facts: `site_slug`, `task_kind`, `capability_id`, `operation_id`,
  `operation_mode`;
- boundary facts: `runtime_execution: out_of_scope`,
  `required_browser_session`, `identity_profile_requirements`,
  `evidence_requirements`, `write_precheck_boundary`, and
  `failure_taxonomy_refs`;
- write-precheck guard facts: `no_submit_guard: active`, `submitted: false`,
  and `true_write_execution: blocked`.

Core must not infer hosted registry behavior, package installation, runtime
execution, profile/provider selection, browser session ownership, live source
lookup, live evidence lookup, write permission, or user-visible task success
from those files. If a required locator, schema, guardrail, Harbor runtime fact,
or evidence ref is absent, Core must fail closed instead of treating a fixture
as a live run.

## Capability Boundary

The Xiaohongshu packages under `sites/xiaohongshu/**` and the BOSS packages
under `sites/boss/**` are static capability assets. They can prove that Lode
has repo-local package refs, schemas, fixtures, post-check declarations,
resource requirements, failure classes, and registry locators.

They cannot prove that a user has a working browser profile, an authenticated
session, a live page, current site access, a completed Core run, or accepted
Harbor evidence. Real read validation belongs to Core plus Harbor with an
explicitly authorized user-controlled browser session.

## Write-Precheck No-Submit Boundary

`sites/xiaohongshu/publish-note-precheck` and `sites/boss/greet-precheck` are
`validate_only` packages. Their only current write-side claim is no-submit
precheck:

- allowed: target/input validation, expected-change preview, risk hints,
  refs-only source/evidence requirements, and no-submit guard checks;
- blocked: publish, save, upload, submit, greet, chat, send, apply, schedule,
  external draft persistence, and write-success evidence.

The active guardrail is a consumer fail-closed input, not permission to click a
site button or mutate an external page.

## Closeout Evidence

Any Lode closeout for these Work Items must include:

- Work Item and covered issue list;
- PR URL, head SHA, and target branch;
- validation commands and conclusions;
- changed Lode locators in `docs/`, `registry/`, `sites/`, `tools/`, or
  `.loom/`;
- explicit statement that fixture/demo/contract evidence is not live runtime
  evidence and does not prove user-visible availability;
- explicit non-goals: no runtime server, no production page access, no real
  account access, no publish/send/submit/apply, no hosted registry or
  marketplace.

Post-merge evidence must be marked as post-merge and must not be presented as a
pre-merge runtime gate.
