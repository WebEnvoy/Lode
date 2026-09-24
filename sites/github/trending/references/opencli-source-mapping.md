# OpenCLI GitHub Trending conversion

## Fixed source and license

- Repository: `jackwener/OpenCLI`
- Commit: `8271afc67e8504bda94c147f446ee29775d08274`
- Release version: `@jackwener/opencli` `1.8.8`
- Source path: `clis/github-trending/repos.js`
- Source SHA-256: `0efc684322b8a70cac358ea3cdccc24bebf105a8d09e7fb6aa6c170e1fd72a32`
- `package.json` SHA-256: `f151c56b14d1a240855ba2330ba2885b5777f4bd45797142c8f719c325c600f0`
- License: Apache-2.0; fixed `LICENSE` SHA-256 `0210b8b66cf00358242cb921ba2be3a46dfe0190159b1b952388a3880ce1ff54`
- The fixed upstream Apache-2.0 license text is included as [`OpenCLI-Apache-2.0-LICENSE.txt`](OpenCLI-Apache-2.0-LICENSE.txt); its bytes match that pinned hash.
- Source references: [adapter at the fixed commit](https://github.com/jackwener/OpenCLI/blob/8271afc67e8504bda94c147f446ee29775d08274/clis/github-trending/repos.js), [package metadata](https://github.com/jackwener/OpenCLI/blob/8271afc67e8504bda94c147f446ee29775d08274/package.json), [license](https://github.com/jackwener/OpenCLI/blob/8271afc67e8504bda94c147f446ee29775d08274/LICENSE).

No upstream executable code is copied. `scripts/read-daily-trending-top5.mjs` is a broker-only rewrite of the selected read result into this package's output contract. The source adapter itself is read-only, public, unauthenticated, and declares `since` (daily/weekly/monthly, default daily), optional language slug, and `limit` (default and maximum 25). It calls raw `fetch()` for GitHub HTML and parses HTML with regular expressions. That network and HTML parser are excluded from this package.

## Accepted task subset

The task is fixed to the daily, unfiltered GitHub Trending page and the first five visible repository rows. It has no caller-provided URL or filter input. The owner or agent opens the page in the currently authorized GitHub Runtime, and the task calls only broker `runtime.invoke` for `instance.snapshot` and `output.write`.

| OpenCLI output | Lode output | Conversion |
| --- | --- | --- |
| Array order / `rank` | `normalized.rows[0..4]` order | The first five valid row headings retain their page order; rank is implicit in array position. |
| `repo` (`owner/name`) | `rows[].name` | Accept only a bounded GitHub owner/repository token; reject malformed names. |
| Derived `https://github.com/${repo}` | `rows[].url` | Construct from the validated `name`; never accept a URL from page text or an input value. |
| `language` string or `null` | `rows[].language` and `language_state` | The page text must contain one row metadata line shaped as `<language> <lifetime-stars> <forks> Built by`; an explicit `Language:` label is also accepted. Missing or unmarked text remains `null`/`unknown`; it is not inferred from description text. |
| `starsSince` for `since=daily` | `rows[].today_stars` | Accept decimal digits with commas only from an explicit `N stars today` line. Abbreviated, missing, or ambiguous counts remain unknown. |
| `description`, lifetime `stars`, `forks` | Not returned | Intentionally outside the #476 result. They are not silently repurposed as accepted fields. |
| `since`, `language`, `limit` inputs | No task input | Narrowed to daily, no language filter, and exactly five requested rows. Weekly/monthly and language-filtered results are not supported by this task. |

The result is `available` only when the snapshot's text coverage is complete and not truncated and all five requested rows have an unambiguous name, URL, language state, and daily star count. The language metadata pattern requires two correctly grouped decimal counts and the exact `Built by` row marker; a lone language-looking token is not enough. Today-stars accepts a decimal count with valid thousands grouping followed by the exact `stars today` marker. Otherwise the result is `partial`; an incomplete result cannot pass the task's post-check. No cursor or pagination is declared. The task does not claim the whole Trending collection is exhausted: completeness is scoped to the requested top five.

## Remaining live compatibility check

An authorized early page-shape spike used Camoufox `0.5.6`, browser `152.0.4-beta.30`, and Playwright `1.60.0`. It observed HTTP 200, the expected title, 17 `article.Box-row` entries, and 3,170 characters from `main.innerText`. Sampled row text placed the repository heading before a metadata line with language, lifetime stars, forks, and `Built by`, followed by an explicit `N stars today` line. There was no per-row `Language:` label. The spike independently checked that sampled `article.Box-row h2 a` links matched the owner/repository path. The current script uses only the bounded snapshot text, parses the fixed metadata marker, and derives URL from the validated name; it does not read DOM attributes, anchors, raw HTML, or raw network data. The live spike established page shape only: it did not execute this package script, authenticate, or persist the page text.

The synthetic fixture models the observed row metadata shape and contains five rows to prove the mapping path. Its unmarked-language negative case proves the script does not misclassify an arbitrary description as a language. It does not preserve or reproduce the live page text.
