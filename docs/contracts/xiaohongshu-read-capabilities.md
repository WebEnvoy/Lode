# Xiaohongshu Read Capability Packages

Status: proposed, refreshed for LODE-236 / milestone #14 on 2026-07-06 UTC.

## Scope

This contract originally covered Lode #198 and Work Items #205, #206, #207, and #208.
LODE-236 refreshes the same package refs for FR #235 and Work Items #236, #237,
and #239 without changing package identity or claiming live account execution.
It implements two repo-local read packages:

- `lode://site-capability/xiaohongshu/search-notes@0.1.0`
- `lode://site-capability/xiaohongshu/read-note-detail@0.1.0`

Covered semantic stories: #15, #16, #17 from
https://github.com/WebEnvoy/Lode/issues/198#issuecomment-4888807384.

## Runtime Boundary

Lode declares package contracts, resource requirements, fixtures, post-checks,
and failure classes. Core owns execution and result envelopes. Harbor owns the
browser identity, runtime session, source refs, and evidence refs.

LODE-236 declares the real site entrypoints, evidence requirements, and failure
classification that Core/App/Harbor can consume. Live Xiaohongshu validation is
not attempted here because this execution is forbidden from accessing a real
account; later runtime evidence must use a user-authorized logged-in browser and
refs-only evidence capture.

## Site Readiness

The packages require:

- `https://www.xiaohongshu.com` browser surface.
- User is already logged in in the bound browser.
- Xiaohongshu Vue app and Pinia store are hydrated.
- The target route is `/explore`, `/search_result`, or a signed `/explore/<note_id>` URL.
- Source refs and evidence refs are available from Harbor/Core.
- No visible verification, login wall, or safety challenge is blocking the page.
- Evidence is refs-only: no cookie, token, raw DOM, HAR, network response body,
  screenshot body, production payload, profile state, or runtime session state.

## Search Package

Input:

- `url`: Xiaohongshu entry or search result URL.
- `keyword`: required search keyword.
- `sort`: `general`, `latest`, `likes`, `comments`, or `collects`.
- `limit`: fixture-bounded result count hint.

Output:

- keyword, sort, result count, note cards, note URL, author, interaction
  metrics, and `follow_up_ref`.
- `follow_up_ref` preserves the signed note URL or `xsec_token` value needed by
  the detail package.

## Detail Package

Input:

- `url`: signed note URL, preferably emitted by the search package.
- optional `note_id` and `xsec_token` when Core already resolved them.

Output:

- title, author, body summary, interaction metrics, tags, published hint,
  IP-location hint, and source citation.

## Failure Classes

Both packages declare these Xiaohongshu-specific classes in addition to the
base Lode validator classes:

- `not_logged_in`
- `login_expired`
- `page_not_ready`
- `signed_ref_missing`
- `safety_challenge`
- `field_missing`
- `network_resource_unavailable`

Core/App can map these to user recovery prompts without Lode storing account
state or runtime evidence.

## Source Absorption

Referenced locators:

- `sources/epiral/bb-sites/xiaohongshu/search.js`
- `sources/epiral/bb-sites/xiaohongshu/note.js`
- `sources/epiral/bb-sites/xiaohongshu/comments.js`
- `sources/epiral/bb-sites/xiaohongshu/user_posts.js`
- `sources/epiral/bb-sites/xiaohongshu/feed.js`
- `sources/epiral/bb-sites/xiaohongshu/me.js`
- `research/subjects/epiral/bb-sites/wiki/versions/9aba7d0d/index.md`
- `research/subjects/epiral/bb-sites/wiki/versions/9aba7d0d/pages/4.1-xiaohongshu-suite.md`
- `research/subjects/epiral/bb-sites/wiki/versions/9aba7d0d/pages/3.2-adapter-patterns-and-approaches.md`
- `research/subjects/epiral/bb-sites/wiki/versions/9aba7d0d/pages/3.3-authentication-and-browser-sessions.md`
- `research/subjects/jackwener/OpenCLI/wiki/versions/09a0af7a/pages/5.6-site-sitemaps.md`
- `research/subjects/MediaCrawlPro/MediaCrawlerPro-SignSrv/wiki/versions/2026-06-09-114042/18-xiao-hong-shu-qian-ming-shi-xian-chun-suan-fa-liu-lan-qi-mo-shi-yu-xhshow-xiu-fu.md`

Absorbed:

- Same-origin logged-in browser requirement.
- Vue/Pinia readiness and page hydration probes.
- Search-to-detail signed follow-up reference.
- `xsec_token` preservation as an input/output contract, not as stored account
  state.
- Structured failure hints for login, readiness, signed-ref, safety challenge,
  field drift, and runtime resource failures.

Not absorbed:

- bb-sites adapter source code or runtime interception code.
- Sign service implementation, browser automation runner, or request signing.
- Comments, feed, user profile, creator center, write actions, batch crawling,
  or any safety-control bypass.

## LODE-236 Package Readiness

- `sites/xiaohongshu/search-notes/manifest.json` now binds FR #235/#236/#239,
  real site entrypoints, absorbed source locators, and refs-only evidence policy.
- `sites/xiaohongshu/read-note-detail/manifest.json` now binds FR #235/#237/#239,
  signed detail ref requirements, absorbed source locators, and refs-only
  evidence policy.
- `registry/local-query.fixture.json` exposes the LODE-236 Xiaohongshu batch for
  Core/App discovery while marking live account validation as not attempted.
