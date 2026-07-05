# Implementation Contract

## Ownership

- Lode owns package refs, version refs, lifecycle metadata, repair draft metadata, overlay/fork metadata, local registry entries, package lock refs, and validator checks.
- Core owns task admission, run records, failure attribution truth, post-check result truth, and result envelopes.
- Harbor owns runtime facts, validation refs, evidence refs, redaction, retention, freshness, and viewer refs.
- App owns local UI intent, display state, report intent, and user navigation.

## Allowed Edits

- `sites/example/read-public-page/repair/**`
- `sites/example/read-public-page/manifest.json`
- `sites/example/read-public-page/package-lock.json`
- `sites/example/read-public-page/catalog-metadata.json`
- `sites/example/read-public-page/failure-mapping.json`
- `registry/local-packages.json`
- `tools/lode_validate_package.py`
- `.loom/**/LODE-156*`
- `.loom/status/current.md`
- `.loom/bootstrap/init-result.json`

## Forbidden Edits

- No App, Core, or Harbor implementation changes in this PR.
- No hosted registry, marketplace, sync, crawler, or runtime implementation.
- No credentials, cookies, tokens, browser profile state, runtime session state, live tab state, raw evidence bodies, full DOM, network archives, production payloads, or user business data.
- No Stage 6 write-side execution behavior.

## Verification

- `python3 -m py_compile tools/lode_validate_package.py`
- `python3 tools/lode_validate_package.py sites/example/read-public-page --registry-index registry/local-packages.json --json`
- `python3 tools/lode_validate_package.py --registry-index registry/local-packages.json --all --json`
- `git diff --check`
- `loom suite validate --target . --item LODE-156 --json`
- `loom suite evidence validate --target . --item LODE-156 --json`
- `loom suite carrier validate --target . --item LODE-156 --json`
- `loom fact-chain --target . --json`
- `loom verify --target . --json`
