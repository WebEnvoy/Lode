# GitHub Trending

This package contains a fixed read-only task for the first five repositories on GitHub's daily Trending page. The current task page must already be open at `https://github.com/trending` or `https://github.com/trending?since=daily`; the script does not navigate.

The task obtains one fresh, bounded `instance.snapshot` through WebEnvoy's managed broker, maps visible page text to repository name, URL, language, and stars today, and writes only schema-constrained output. Language is accepted only from GitHub's row metadata pattern (`<language> <lifetime-stars> <forks> Built by`) or an explicit `Language:` label. The URL is derived from a validated `owner/repository` heading, as OpenCLI's adapter does; no raw HTML, direct network request, cookie, browser handle, or OpenCLI code is used.

Plain text without the accepted row marker is ambiguous with a description and stays `unknown`; the task reports partial instead of guessing. The task reports complete only when five rows and every required field are observed on a complete, untruncated snapshot.

See [`opencli-source-mapping.md`](references/opencli-source-mapping.md) for fixed upstream provenance, the field map, exclusions, and current validation limits. This public task does not require or consume an AccountSystem definition.
