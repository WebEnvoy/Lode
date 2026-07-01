# Current Status

## Derived Fact Chain View

- Item ID: GH-90
- Goal: Define the first sample read package manifest instance with package identity, operation, family, tags, and entrypoint/ref.
- Scope: Add the minimum proposed `site-capability` manifest for the reserved-domain sample read package and record item-specific GH-90 Loom carrier evidence.
- Execution Path: milestone-9/read-package-manifest
- Workspace Entry: .
- Recovery Entry: .loom/progress/GH-90.md
- Review Entry: .loom/reviews/GH-90.json
- Validation Entry: `jq empty sites/example/read-public-page/manifest.json`; `git diff --check`; `loom fact-chain --target . --json`; `loom suite validate --target . --item GH-90 --json`; `loom suite carrier validate --target . --item GH-90 --json`; PR body/head readback.
- Closing Condition: PR for GH-90 is merged, hosted checks are recorded, issue #90 closeout evidence is posted, and the branch/head/PR metadata agree with this carrier.
- Current Checkpoint: closed_out
- Current Stop: PR #104 merged into `main` at merge commit `ec4ef6d2b664646958f677f47ee320f18af87cb3`; closeout PR #106 merged at `a31a5091a1f0a40629a336143579edcbfd38a073`; closeout evidence was posted to issue #90 and the issue was closed at 2026-07-01T16:56:40Z.
- Next Step: None for GH-90; continue milestone #9 with GH-91 through GH-103.
- Blockers: None recorded.
- Latest Validation Summary: Post-merge closeout validation on 2026-07-01: local `jq empty sites/example/read-public-page/manifest.json .loom/bootstrap/init-result.json .loom/specs/GH-90/build-evidence.json .loom/reviews/GH-90.json .loom/reviews/GH-90.spec.json`, `git diff --check`, `loom fact-chain --target . --json`, `loom suite validate --target . --item GH-90 --json`, `loom suite carrier validate --target . --item GH-90 --json`, and `loom review read --target . --item GH-90 --json` passed at closeout head `11768e9546435f80378e785d58f2deb822332ca7`; PR #106 metadata readback passed for branch `work/GH-90-closeout`; hosted run `28533610439` passed `py-compile`, `demo-bootstrap`, `repo-local-cli`, and `loom-check`, and failed `loom-pr-merge-gate` only because retained review pointed to deleted branch head `20e3b111922cb3054214970209aaafad82239443`; this update repins retained review to merge commit `ec4ef6d2b664646958f677f47ee320f18af87cb3` for terminal closeout comparison.
- Recovery Boundary: Re-check if this PR adds schema files, fixtures, validator code, registry behavior, runtime behavior, external writes, or changes outside GH-90 manifest/carrier scope.
- Current Lane: closeout

## Runtime Evidence

- Run Entry: not_applicable
- Logs Entry: not_applicable
- Diagnostics Entry: not_applicable
- Verification Entry: .loom/progress/GH-90.md
- Lane Entry: milestone-9/read-package-manifest

## Sources

- Static Truth: .loom/work-items/GH-90.md
- Dynamic Truth: .loom/progress/GH-90.md
- Locator Truth: .loom/bootstrap/init-result.json
- Fact Chain CLI: loom fact-chain --target . --json

## Notes

- 2026-07-01: GH-90 became the active item for the first milestone #9 implementation PR.
- 2026-07-01: Hosted run `28532434367` failed only `loom-pr-merge-gate`; failure was classified as review evidence stale because `.loom/work-items/GH-90.md` changed after reviewed head `8560e142aba8ca732ea3d8e38a5f55111ecd974f`.
- 2026-07-01: Hosted run `28532869991` consumed GH-90 review approval and carrier-only head binding; remaining fallback was recovery checkpoint `build`, so checkpoint is advanced to `merge`.
- 2026-07-01: PR #104 merged to `main` at `ec4ef6d2b664646958f677f47ee320f18af87cb3`; closeout branch records post-merge evidence before closing issue #90.
- 2026-07-01: Hosted run `28533610439` proved PR #106 metadata readback and non-gate checks, then failed only because retained review pointed to deleted branch-only commit `20e3b111922cb3054214970209aaafad82239443`; retained review is repinned to merge commit `ec4ef6d2b664646958f677f47ee320f18af87cb3` for closeout-only gate consumption.
- 2026-07-01: Closeout PR #106 merged into `main` at `a31a5091a1f0a40629a336143579edcbfd38a073`; closeout evidence was posted to issue #90 and the issue closed at 2026-07-01T16:56:40Z.
