# BOSS Zhipin Read Capability Packages

Status: proposed, refreshed for LODE-241 / milestone #14 on 2026-07-06 UTC.

## Scope

This contract originally covered Lode #199 and Work Items #209, #210, #211,
and #212. LODE-241 refreshes the BOSS portion for FR #240 and Work Items
#241, #242, and #244 without claiming live account execution. It covers two
repo-local read packages:

- `lode://site-capability/boss/job-search@0.1.0`
- `lode://site-capability/boss/read-job-detail@0.1.0`

Covered milestone #14 issues: #240, #241, #242, and #244.

## Runtime Boundary

Lode declares package contracts, resource requirements, fixtures, post-checks,
and failure classes. Core owns execution and result envelopes. Harbor owns the
browser identity, runtime session, source refs, and evidence refs.

Real BOSS validation requires a user-owned logged-in browser session and was
not attempted under LODE-241 because this worker is forbidden to access real
accounts or real sites. This PR does not fabricate live evidence.

## Site Readiness

The packages require:

- `https://www.zhipin.com` browser surface.
- User is already logged in as a job seeker in the bound browser.
- The BOSS web app is hydrated enough for read-only extraction.
- The current origin can read `/wapi/zpgeek/*` through the existing browser identity.
- Source refs and evidence refs are available from Harbor/Core.
- No visible verification, login wall, CAPTCHA, or safety challenge is blocking the page.

## Search Package

Input:

- `url`: BOSS job search URL on `www.zhipin.com`.
- `query`: required job search keyword.
- optional city, experience, degree, salary, and industry filter codes.
- `page`: first page only; batch pagination is out of scope.

Output:

- query, city, filters, result count, job cards, salary, company, location,
  experience, degree, skills, welfare, recruiter summary, and `detail_ref`.
- `detail_ref` preserves `securityId`, `encryptJobId`, and detail URL for the
  detail package.

## Detail Package

Input:

- `url`: BOSS job detail URL, preferably emitted by the search package.
- `securityId`: required detail reference from search results.
- optional `encryptJobId` when Core already resolved it from the URL.

Output:

- job description, salary, experience, degree, location, address, skills,
  company information, recruiter summary, and source citation.

## Failure Classes

Both packages declare these BOSS-specific classes in addition to base Lode
validator classes:

- `not_logged_in`
- `identity_insufficient`
- `captcha_required`
- `page_not_ready`
- `input_missing_security_id`
- `query_missing`
- `city_unresolved`
- `pagination_limited`
- `job_expired`
- `permission_denied`
- `field_missing`
- `network_resource_unavailable`

Core/App can map these to user recovery prompts without Lode storing account
state or runtime evidence.

## Source Absorption

Referenced locators:

- `sources/epiral/bb-sites/boss/search.js`
- `sources/epiral/bb-sites/boss/detail.js`
- `research/subjects/epiral/bb-sites/wiki/versions/9aba7d0d/pages/5.2-boss-zhipin-adapters.md`
- `research/subjects/epiral/bb-sites/wiki/versions/9aba7d0d/pages/3.2-adapter-patterns-and-approaches.md`
- `research/subjects/epiral/bb-sites/wiki/versions/9aba7d0d/pages/3.3-authentication-and-browser-sessions.md`
- `research/subjects/jackwener/OpenCLI/wiki/versions/09a0af7a/pages/3.1-built-in-commands-reference.md`
- `research/subjects/Panniantong/Agent-Reach/wiki/versions/ca2e8552/pages/3.9-instagram-linkedin-and-boss-channels.md`
- `docs/adr/0006-xhs-boss-site-knowledge-selection.md`

Absorbed:

- Same-origin logged-in browser requirement for `www.zhipin.com`.
- Search source shape from `/wapi/zpgeek/search/joblist.json`.
- Detail source shape from `/wapi/zpgeek/job/detail.json?securityId=...`.
- `securityId` and `encryptJobId` as search-to-detail references.
- Public job, company, recruiter, city, salary, experience, degree, skill,
  welfare, and status fields.
- HTTP/API error, login, permission, job-expired, and manual verification
  failure classes.

Cut or rewritten:

- bb-sites adapter functions were rewritten as manifest/schema/fixture/post-check
  contracts.
- OpenCLI command inventory was used only to distinguish read commands from
  greet, send, chat, and batch-greet surfaces.
- Browser domain-skill material was used only for page readiness and risk
  vocabulary.
- Same-origin fetch remains Core/Harbor runtime behavior, not Lode code.

Rejected:

- Source code copy from bb-sites or research locators.
- Login automation, QR login automation, CAPTCHA solving, or safety-control bypass.
- Greet, batch-greet, send, chat, apply, resume upload, candidate management,
  recruiter-side automation, or other external-visible writes.
- Bulk scraping, crawler queue, or batch pagination.
- Raw API responses, full DOM, screenshots, account state, runtime state, or
  production payloads.
