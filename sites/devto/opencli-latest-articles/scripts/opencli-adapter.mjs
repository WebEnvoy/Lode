// Fixed compatibility shim for OpenCLI 1.8.8 PUBLIC read adapters.
// Generated from reviewed source text; all reads use this run's WebEnvoy broker.
const __opencliSpec = Object.freeze({"result_kind":"opencli_devto_latest_articles","mode":"requested_page","media_type":"application/json","headers":{"accept":"application/json"}});
const __completenessProfile = Object.freeze({"kind":"json-page-required-fields","required_non_empty_fields":["id","title","url"],"url_prefix":"https://dev.to/","finite_nullable_number_fields":["reactions","comments"]});
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

// Retained source: third_party/opencli-1.8.8/clis/devto/latest.js
// devto latest — newest dev.to articles, regardless of tag.
//
// Hits the public `/api/articles/latest` endpoint. Complements the existing
// `devto top` (most-reactioned) and `devto tag` (filtered) commands by
// surfacing the firehose of brand-new posts.
function requireBoundedInt(value, defaultValue, maxValue) {
    const raw = value ?? defaultValue;
    const n = typeof raw === 'number' ? raw : Number(raw);
    if (!Number.isInteger(n) || n <= 0) {
        throw new ArgumentError('devto limit must be a positive integer');
    }
    if (n > maxValue) {
        throw new ArgumentError(`devto limit must be <= ${maxValue}`);
    }
    return n;
}

cli({
    site: 'devto',
    name: 'latest',
    access: 'read',
    description: 'Newest dev.to articles (firehose, all tags)',
    domain: 'dev.to',
    strategy: Strategy.PUBLIC,
    browser: false,
    args: [
        { name: 'limit', type: 'int', default: 20, help: 'Articles per page (1-100)' },
        { name: 'page', type: 'int', default: 1, help: 'Page number (1-based)' },
    ],
    columns: ['rank', 'id', 'title', 'author', 'tags', 'reactions', 'comments', 'published', 'url'],
    func: async (args) => {
        const limit = requireBoundedInt(args.limit, 20, 100);
        const page = requireBoundedInt(args.page, 1, 1000);
        const url = `https://dev.to/api/articles/latest?per_page=${limit}&page=${page}`;
        let resp;
        try {
            resp = await __brokerFetch(url, { headers: { accept: 'application/json' } });
        }
        catch (err) {
            throw new CommandExecutionError(
                `devto latest request failed: ${err?.message ?? err}`,
                'Check that dev.to is reachable from this network.',
            );
        }
        if (!resp.ok) {
            throw new CommandExecutionError(`devto latest returned HTTP ${resp.status}`);
        }
        let body;
        try {
            body = await resp.json();
        }
        catch (err) {
            throw new CommandExecutionError(`devto latest returned malformed JSON: ${err?.message ?? err}`);
        }
        const list = Array.isArray(body) ? body : [];
        if (!list.length) {
            throw new EmptyResultError('devto latest', `dev.to /articles/latest returned no items at page ${page}.`);
        }
        return list.map((item, i) => ({
            rank: (page - 1) * limit + i + 1,
            id: item.id != null ? String(item.id) : '',
            title: String(item.title ?? ''),
            author: String(item?.user?.username ?? ''),
            tags: String(item.tag_list ?? '').replace(/,\s*/g, ', '),
            reactions: item.public_reactions_count != null ? Number(item.public_reactions_count) : null,
            comments: item.comments_count != null ? Number(item.comments_count) : null,
            published: String(item.published_at ?? '').slice(0, 10),
            url: String(item.url ?? ''),
        }));
    },
});

export async function run(input, broker, context) { return __run(input, broker, context); }
