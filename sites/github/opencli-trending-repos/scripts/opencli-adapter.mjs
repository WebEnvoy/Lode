// Fixed compatibility shim for OpenCLI 1.8.8 PUBLIC read adapters.
// Generated from reviewed source text; all reads use this run's WebEnvoy broker.
const __opencliSpec = Object.freeze({"result_kind":"opencli_github_trending_repositories","mode":"top_n","media_type":"text/html","headers":{"accept":"text/html","user-agent":"Mozilla/5.0 (compatible; opencli/github-trending)"}});
const __completenessProfile = Object.freeze({"kind":"html-requested-count","default_limit":25,"open_pattern":"<article\\b[^>]*class=\"[^\"]*\\bBox-row\\b[^\"]*\"[^>]*>","close_pattern":"</article>","required_non_empty_fields":["repo","url"],"safe_integer_fields":["stars","forks","starsSince"],"url_field":"url","url_prefix":"https://github.com/"});
let __opencliRegistration;
let __opencliBroker;
let __opencliResponse;
let __opencliReadCount = 0;
let __opencliRunning = false;

const Strategy = Object.freeze({ PUBLIC: 'PUBLIC' });
class ArgumentError extends Error { constructor(message, ...rest) { super(message, ...rest); this.name = 'ArgumentError'; } }
class CommandExecutionError extends Error { constructor(message, ...rest) { super(message, ...rest); this.name = 'CommandExecutionError'; } }
class EmptyResultError extends Error { constructor(message, ...rest) { super(message, ...rest); this.name = 'EmptyResultError'; } }
function cli(definition) {
  if (__opencliRegistration) throw new Error('multiple adapter registrations are unsupported');
  __opencliRegistration = definition;
}

function __checkCompleteness(input, records, body) {
  const profile = __completenessProfile;
  const requiredValues = (row) => profile.required_non_empty_fields.every((key) => typeof row[key] === 'string' && row[key].length > 0);
  if (profile.kind === 'html-requested-count') {
    const requested = Number(input?.limit ?? profile.default_limit);
    const opened = (body.match(new RegExp(profile.open_pattern, 'gi')) ?? []).length;
    const closed = (body.match(new RegExp(profile.close_pattern, 'gi')) ?? []).length;
    const safeCounts = profile.safe_integer_fields.every((key) => records.every((row) => Number.isSafeInteger(row[key]) && row[key] >= 0));
    const urlsMatch = records.every((row) => row[profile.url_field] === profile.url_prefix + row.repo);
    const expectedCount = Math.min(requested, opened);
    const explicitEmpty = opened === 0 && typeof hasExplicitEmptyTrending === 'function' && hasExplicitEmptyTrending(body);
    const complete = Number.isInteger(requested) && opened === closed && records.length === expectedCount && (opened > 0 || explicitEmpty) && records.every(requiredValues) && safeCounts && urlsMatch;
    return { state: complete ? 'complete' : 'unknown', hasMore: null };
  }
  if (profile.kind === 'json-page-required-fields') {
    const countersFinite = profile.finite_nullable_number_fields.every((key) => records.every((row) => row[key] === null || Number.isFinite(row[key])));
    if (!countersFinite) throw new CommandExecutionError('adapter produced a non-finite numeric value');
    const urlsMatch = records.every((row) => typeof row.url === 'string' && row.url.startsWith(profile.url_prefix));
    const complete = records.every(requiredValues) && urlsMatch;
    return { state: complete ? 'complete' : 'unknown', hasMore: null };
  }
  if (profile.kind === 'atom-feed-count-and-total') {
    const requested = Number(input?.limit ?? profile.default_limit);
    const totalMatch = body.match(new RegExp(profile.total_pattern));
    const total = totalMatch ? Number(totalMatch[1]) : NaN;
    const opened = (body.match(new RegExp(profile.entry_open_pattern, 'g')) ?? []).length;
    const closed = (body.match(new RegExp(profile.entry_close_pattern, 'g')) ?? []).length;
    const feedOpen = new RegExp(profile.feed_open_pattern, 'i').test(body);
    const feedClosed = new RegExp(profile.feed_close_pattern, 'i').test(body);
    const urlsMatch = records.every((row) => row.url === profile.url_template.replace('{id}', row.id));
    const complete = feedOpen && feedClosed && opened === closed && opened === records.length && Number.isSafeInteger(total) && records.length === Math.min(requested, total) && records.every(requiredValues) && urlsMatch;
    return { state: complete ? 'complete' : 'unknown', hasMore: null };
  }
  throw new CommandExecutionError('unsupported pinned completeness profile');
}

function __confirmedEmpty(body) {
  const profile = __completenessProfile;
  if (profile.kind === 'html-requested-count') {
    const opened = (body.match(new RegExp(profile.open_pattern, 'gi')) ?? []).length;
    const closed = (body.match(new RegExp(profile.close_pattern, 'gi')) ?? []).length;
    return opened === 0 && closed === 0 && typeof hasExplicitEmptyTrending === 'function' && hasExplicitEmptyTrending(body);
  }
  if (profile.kind === 'json-page-required-fields') {
    try { const parsed = JSON.parse(body); return Array.isArray(parsed) && parsed.length === 0; } catch { return false; }
  }
  if (profile.kind === 'atom-feed-count-and-total') {
    const totalMatch = body.match(new RegExp(profile.total_pattern));
    const openCount = (body.match(new RegExp(profile.entry_open_pattern, 'g')) ?? []).length;
    const closeCount = (body.match(new RegExp(profile.entry_close_pattern, 'g')) ?? []).length;
    return new RegExp(profile.feed_open_pattern, 'i').test(body)
      && new RegExp(profile.feed_close_pattern, 'i').test(body)
      && totalMatch !== null && Number(totalMatch[1]) === 0 && openCount === 0 && closeCount === 0;
  }
  return false;
}

async function __brokerFetch(value, options = {}) {
  if (!__opencliBroker?.network?.read || __opencliReadCount !== 0) throw new CommandExecutionError('managed public read unavailable or request budget exceeded');
  const method = String(options.method ?? 'GET').toUpperCase();
  if (method !== 'GET' || options.body != null || options.credentials != null || options.redirect != null) throw new CommandExecutionError('only the fixed anonymous GET contract is supported');
  const headers = {};
  for (const [rawName, headerValue] of Object.entries(options.headers ?? {})) {
    const name = rawName.toLowerCase();
    if (Object.hasOwn(headers, name) || !Object.hasOwn(__opencliSpec.headers, name) || typeof headerValue !== 'string' || headerValue !== __opencliSpec.headers[name]) throw new CommandExecutionError('adapter request header differs from its pinned policy');
    headers[name] = headerValue;
  }
  if (Object.keys(headers).length !== Object.keys(__opencliSpec.headers).length) throw new CommandExecutionError('adapter omitted a pinned request header');
  __opencliReadCount += 1;
  const response = await __opencliBroker.network.read({ url: String(value), method: 'GET', headers });
  if (!response || typeof response.ok !== 'boolean' || !Number.isInteger(response.status) || typeof response.url !== 'string' || typeof response.body !== 'string' || typeof response.response_ref !== 'string' || !response.response_ref || typeof response.content_type !== 'string') throw new CommandExecutionError('managed public read returned an incomplete response');
  const mediaType = response.content_type.split(';', 1)[0].trim().toLowerCase();
  if (mediaType !== __opencliSpec.media_type) throw new CommandExecutionError('managed public read returned an unexpected media type');
  __opencliResponse = response;
  return {
    ok: response.ok,
    status: response.status,
    async text() { return response.body; },
    async json() { return JSON.parse(response.body); },
  };
}

async function __run(input, broker, _context) {
  if (!__opencliRegistration || typeof __opencliRegistration.func !== 'function') throw new Error('static OpenCLI registration missing');
  if (__opencliRunning) throw new Error('concurrent invocation is unsupported');
  __opencliRunning = true;
  __opencliBroker = broker;
  __opencliResponse = undefined;
  __opencliReadCount = 0;
  try {
    let records;
    try {
      records = await __opencliRegistration.func(input ?? {});
    } catch (error) {
      if (error?.name === 'EmptyResultError' && __opencliResponse && __confirmedEmpty(__opencliResponse.body)) records = [];
      else throw error;
    }
    if (!Array.isArray(records) || !__opencliResponse || __opencliReadCount !== 1) throw new CommandExecutionError('adapter returned no verified response records');
    const completeness = __checkCompleteness(input, records, __opencliResponse.body);
    const result = {
      result_kind: __opencliSpec.result_kind,
      status: completeness.state === 'complete' ? 'available' : 'partial',
      normalized: {
        parameters: input ?? {},
        records,
        completeness: completeness.state,
        pagination: { mode: __opencliSpec.mode, has_more: completeness.hasMore, completeness: completeness.state },
      },
      source_refs: [{ ref_id: __opencliResponse.response_ref, source_kind: 'public_http_response' }],
      evidence_refs: [{ ref_id: __opencliResponse.response_ref, evidence_kind: 'public_http_response', producer: 'core', redaction: 'summary_only' }],
    };
    return await broker.output.write(result);
  } finally {
    __opencliBroker = undefined;
    __opencliResponse = undefined;
    __opencliReadCount = 0;
    __opencliRunning = false;
  }
}

// Retained source: third_party/opencli-1.8.8/clis/github-trending/repos.js
// github-trending — repositories from https://github.com/trending (public HTML, no auth).
const SINCE = {
    daily: 'daily',
    weekly: 'weekly',
    monthly: 'monthly',
};

function decodeHtmlEntities(value) {
    return String(value ?? '')
        .replace(/&amp;/g, '&')
        .replace(/&lt;/g, '<')
        .replace(/&gt;/g, '>')
        .replace(/&quot;/g, '"')
        .replace(/&#0?39;/g, "'")
        .replace(/&#x27;/gi, "'")
        .replace(/&nbsp;/g, ' ');
}

function stripTags(value) {
    return String(value ?? '').replace(/<[^>]*>/g, '');
}

function parseCount(value) {
    if (value == null) return null;
    const digits = String(value).replace(/[,\s]/g, '');
    if (!/^\d+$/.test(digits)) return null;
    return Number(digits);
}

function escapeRegExp(value) {
    return String(value).replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

function assertCount(value, field, repo) {
    const count = parseCount(value);
    if (count == null) {
        throw new CommandExecutionError(`github-trending parser drift: missing ${field} for ${repo}`);
    }
    return count;
}

function hasExplicitEmptyTrending(html) {
    return /don.t have any trending repositories/i.test(stripTags(html))
        || /no trending repositories/i.test(stripTags(html));
}

function parseTrendingHtml(html, limit) {
    const blocks = Array.from(String(html ?? '').matchAll(/<article\b[^>]*class="[^"]*\bBox-row\b[^"]*"[^>]*>([\s\S]*?)<\/article>/g))
        .map((match) => match[1]);
    const rows = [];

    if (blocks.length === 0) {
        if (hasExplicitEmptyTrending(html)) return rows;
        throw new CommandExecutionError('github-trending parser drift: no repository rows found');
    }

    for (const raw of blocks) {
        const block = raw;

        const nameMatch = block.match(/<h2\b[\s\S]*?href="\/([^"/?#]+\/[^"/?#]+)"/);
        if (!nameMatch) {
            throw new CommandExecutionError('github-trending parser drift: missing repository link');
        }
        const repo = decodeHtmlEntities(nameMatch[1]).trim();
        if (!/^[A-Za-z0-9_.-]+\/[A-Za-z0-9_.-]+$/.test(repo)) {
            throw new CommandExecutionError(`github-trending parser drift: invalid repository identity "${repo}"`);
        }

        const descMatch = block.match(/<p class="col-9 color-fg-muted[^"]*">([\s\S]*?)<\/p>/);
        const description = descMatch
            ? decodeHtmlEntities(stripTags(descMatch[1]).replace(/\s+/g, ' ')).trim()
            : '';

        const langMatch = block.match(/<span itemprop="programmingLanguage">([\s\S]*?)<\/span>/);
        const language = langMatch ? decodeHtmlEntities(stripTags(langMatch[1])).trim() : null;

        const escapedRepo = escapeRegExp(repo);
        const starsMatch = block.match(new RegExp(`<a\\b[^>]*href="/${escapedRepo}/stargazers"[^>]*>([\\s\\S]*?)</a>`));
        const forksMatch = block.match(new RegExp(`<a\\b[^>]*href="/${escapedRepo}/forks"[^>]*>([\\s\\S]*?)</a>`));
        const sinceMatch = block.match(/([\d,]+)\s+stars\s+(?:today|this week|this month)/i);

        rows.push({
            repo,
            description,
            language,
            stars: assertCount(starsMatch ? stripTags(starsMatch[1]) : null, 'stars', repo),
            forks: assertCount(forksMatch ? stripTags(forksMatch[1]) : null, 'forks', repo),
            starsSince: assertCount(sinceMatch?.[1], 'period stars', repo),
            url: `https://github.com/${repo}`,
        });
        if (rows.length >= limit) break;
    }
    return rows;
}

cli({
    site: 'github-trending',
    name: 'repos',
    access: 'read',
    description: 'GitHub Trending repositories (public, no login). Filter by --language and --since.',
    domain: 'github.com',
    strategy: Strategy.PUBLIC,
    browser: false,
    args: [
        { name: 'since', type: 'string', default: 'daily', help: 'Time range: daily / weekly / monthly' },
        { name: 'language', type: 'string', default: '', help: 'Filter by programming language slug, e.g. python, rust, "c++"' },
        { name: 'limit', type: 'int', default: 25, help: 'Number of repositories to return (max 25)' },
    ],
    columns: ['rank', 'repo', 'description', 'language', 'stars', 'forks', 'starsSince', 'url'],
    func: async (args) => {
        const sinceKey = String(args.since ?? 'daily').toLowerCase();
        const since = SINCE[sinceKey];
        if (!since) {
            throw new ArgumentError(`Unknown --since "${sinceKey}". Valid: ${Object.keys(SINCE).join(', ')}`);
        }

        const n = Number(args.limit ?? 25);
        if (!Number.isInteger(n) || n <= 0) {
            throw new ArgumentError('--limit must be a positive integer');
        }
        if (n > 25) {
            throw new ArgumentError('--limit must be <= 25 (GitHub Trending lists at most 25 repositories)');
        }
        const limit = n;

        const language = String(args.language ?? '').trim();
        const path = language ? `/trending/${encodeURIComponent(language)}` : '/trending';
        const url = new URL(`https://github.com${path}`);
        url.searchParams.set('since', since);

        let resp;
        try {
            resp = await __brokerFetch(url, {
                headers: {
                    'User-Agent': 'Mozilla/5.0 (compatible; opencli/github-trending)',
                    Accept: 'text/html',
                },
            });
        } catch (error) {
            throw new CommandExecutionError(`github-trending request failed: ${error?.message || error}`);
        }
        if (!resp.ok) {
            throw new CommandExecutionError(`github-trending request failed: HTTP ${resp.status}`);
        }

        const html = await resp.text();
        const rows = parseTrendingHtml(html, limit);
        if (rows.length === 0) {
            throw new EmptyResultError('github-trending', language
                ? `no trending repositories for language "${language}" (${since})`
                : `no trending repositories (${since})`);
        }

        return rows.map((row, index) => ({
            rank: index + 1,
            repo: row.repo,
            description: row.description,
            language: row.language,
            stars: row.stars,
            forks: row.forks,
            starsSince: row.starsSince,
            url: row.url,
        }));
    },
});

export async function run(input, broker, context) { return __run(input, broker, context); }
