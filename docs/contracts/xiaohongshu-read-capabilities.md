# Xiaohongshu Read Capability Packages

Status: proposed, 2026-07-06.

## Scope

This contract covers Lode #198 and Work Items #205, #206, #207, and #208.
It implements two repo-local read packages:

- `lode://site-capability/xiaohongshu/search-notes@0.1.0`
- `lode://site-capability/xiaohongshu/read-note-detail@0.1.0`

Covered semantic stories: #15, #16, #17 from
https://github.com/WebEnvoy/Lode/issues/198#issuecomment-4888807384.

## Runtime Boundary

Lode declares package contracts, resource requirements, fixtures, post-checks,
and failure classes. Core owns execution and result envelopes. Harbor owns the
browser identity, runtime session, source refs, and evidence refs.

Real Xiaohongshu validation is pending a human-owned logged-in browser session.
This PR does not fabricate live evidence.

## Site Readiness

The packages require:

- `https://www.xiaohongshu.com` browser surface.
- User is already logged in in the bound browser.
- Xiaohongshu Vue app and Pinia store are hydrated.
- The target route is `/explore`, `/search_result`, or a signed `/explore/<note_id>` URL.
- Source refs and evidence refs are available from Harbor/Core.
- No visible verification, login wall, or safety challenge is blocking the page.

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
- `sources/epiral/bb-sites/xiaohongshu/me.js`
- `research/subjects/epiral/bb-sites/wiki/versions/9aba7d0d/pages/4.1-xiaohongshu-suite.md`
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
