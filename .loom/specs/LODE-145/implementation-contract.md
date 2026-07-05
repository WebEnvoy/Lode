# Implementation Contract

## Ownership

- Lode owns lifecycle state, version identity, package lock, rollback refs, registry package facts, and validator checks.
- Core may consume these facts for admission and run/result attribution, but owns run record and result envelope truth.
- App may display these facts and store local UI intent only, but does not save package truth.
- Harbor owns runtime/session/evidence refs and private capture status; Lode does not store those payloads.

## Required Behavior

- Lifecycle states are limited to `proposed`, `active`, `suspected_broken`, `broken`, and `deprecated`.
- Rollback and previous-known-good values are refs only: package ref, version, and lock ref.
- Registry batch validation reads repo-local package paths from `registry/local-packages.json`.
- Validator remains offline and does not access accounts, browser runtime, Core, Harbor, App, network, hosted registry, or production pages.

## Forbidden Behavior

- No marketplace, hosted sync, crawler queue, live write, Stage 6 write-precheck, or Browser management console.
- No cookies, tokens, profile state, runtime session state, raw DOM, raw network, screenshot/video body, production payload, user business data, or private local browser material.
