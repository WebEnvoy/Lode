// Fixed compatibility shim for OpenCLI 1.8.8 PUBLIC read adapters.
// Generated from reviewed source text; all reads use this run's WebEnvoy broker.
const __opencliSpec = Object.freeze({"result_kind":"opencli_arxiv_recent_papers","mode":"max_results","media_type":"application/atom+xml","headers":{}});
const __completenessProfile = Object.freeze({"kind":"atom-feed-count-and-total","default_limit":10,"entry_open_pattern":"<entry\\b[^>]*>","entry_close_pattern":"</entry>","total_pattern":"<opensearch:totalResults\\b[^>]*>\\s*(\\d+)\\s*</opensearch:totalResults>","feed_open_pattern":"<feed\\b","feed_close_pattern":"</feed>\\s*$","required_non_empty_fields":["id","title","url"],"url_template":"https://arxiv.org/abs/{id}"});
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

// Retained source: third_party/opencli-1.8.8/clis/arxiv/recent.js
cli({
    site: 'arxiv',
    name: 'recent',
    access: 'read',
    description: 'List recent arXiv submissions in a category',
    strategy: Strategy.PUBLIC,
    browser: false,
    args: [
        { name: 'category', positional: true, required: true, help: 'arXiv category (e.g. cs.CL, cs.LG, math.PR, q-bio.NC)' },
        { name: 'limit', type: 'int', default: 10, help: 'Max results (max 50)' },
    ],
    columns: ['id', 'title', 'authors', 'published', 'primary_category', 'url'],
    func: async (args) => {
        const category = normalizeArxivCategory(args.category);
        const limit = normalizeArxivLimit(args.limit, 10, 50);
        const query = encodeURIComponent(`cat:${category}`);
        const xml = await arxivFetch(`search_query=${query}&max_results=${limit}&sortBy=submittedDate&sortOrder=descending`);
        const entries = parseEntries(xml);
        if (!entries.length)
            throw new EmptyResultError('arxiv', `No recent papers in ${category}. Check the category name.`);
        return entries.map(e => ({
            id: e.id,
            title: e.title,
            authors: e.authors,
            published: e.published,
            primary_category: e.primary_category,
            url: e.url,
        }));
    },
});

// Retained source: third_party/opencli-1.8.8/clis/arxiv/utils.js
/**
 * arXiv adapter utilities.
 *
 * arXiv exposes a public Atom/XML API — no key required.
 * https://info.arxiv.org/help/api/index.html
 */
const ARXIV_BASE = 'https://export.arxiv.org/api/query';
const ARXIV_CATEGORY_PATTERN = /^[a-z]+(?:-[a-z]+)*(?:\.[A-Za-z0-9]+(?:-[A-Za-z0-9]+)*)?$/;
async function arxivFetch(params) {
    const resp = await __brokerFetch(`${ARXIV_BASE}?${params}`);
    if (!resp.ok) {
        throw new CommandExecutionError(`arXiv API HTTP ${resp.status}`, 'Check your search term or paper ID');
    }
    return resp.text();
}
function normalizeArxivLimit(value, defaultValue, maxValue, label = 'limit') {
    const raw = value ?? defaultValue;
    const limit = Number(raw);
    if (!Number.isInteger(limit) || limit <= 0) {
        throw new ArgumentError(`arxiv ${label} must be a positive integer`);
    }
    if (limit > maxValue) {
        throw new ArgumentError(`arxiv ${label} must be <= ${maxValue}`);
    }
    return limit;
}
function normalizeArxivCategory(value) {
    const category = String(value || '').trim();
    if (!ARXIV_CATEGORY_PATTERN.test(category)) {
        throw new ArgumentError(`Invalid arXiv category "${value}". Examples: cs.CL, cs.LG, math.PR, q-bio.NC, physics.comp-ph`);
    }
    return category;
}
/** Decode the small set of XML entities arXiv emits in text fields. */
function decodeEntities(s) {
    return s
        .replace(/&amp;/g, '&')
        .replace(/&lt;/g, '<')
        .replace(/&gt;/g, '>')
        .replace(/&quot;/g, '"')
        .replace(/&apos;/g, "'")
        .replace(/&#39;/g, "'");
}
/** Extract the text content of the first matching XML tag. */
function extract(xml, tag) {
    const m = xml.match(new RegExp(`<${tag}[^>]*>([\\s\\S]*?)<\\/${tag}>`));
    return m ? m[1].trim() : '';
}
/** Extract all text contents of a repeated XML tag. */
function extractAll(xml, tag) {
    const re = new RegExp(`<${tag}[^>]*>([\\s\\S]*?)<\\/${tag}>`, 'g');
    const results = [];
    let m;
    while ((m = re.exec(xml)) !== null)
        results.push(m[1].trim());
    return results;
}
/** Extract the value of a named attribute from the first matching tag (open or self-closing). */
function extractAttr(xml, tag, attr) {
    const m = xml.match(new RegExp(`<${tag}\\b[^>]*?\\b${attr}="([^"]*)"`));
    return m ? m[1] : '';
}
/** Extract all values of a named attribute across repeated tags. */
function extractAllAttr(xml, tag, attr) {
    const re = new RegExp(`<${tag}\\b[^>]*?\\b${attr}="([^"]*)"`, 'g');
    const out = [];
    let m;
    while ((m = re.exec(xml)) !== null)
        out.push(m[1]);
    return out;
}
/** Find the href of the first <link> tag matching a given rel. */
function findLinkHref(xml, rel) {
    const re = /<link\b([^>]*)\/?>/g;
    let m;
    while ((m = re.exec(xml)) !== null) {
        const attrs = m[1];
        if (new RegExp(`\\brel="${rel}"`).test(attrs)) {
            const h = attrs.match(/\bhref="([^"]*)"/);
            if (h)
                return h[1];
        }
    }
    return '';
}
/** Parse Atom XML feed into structured entries. */
function parseEntries(xml) {
    const entryRe = /<entry>([\s\S]*?)<\/entry>/g;
    const entries = [];
    let m;
    while ((m = entryRe.exec(xml)) !== null) {
        const e = m[1];
        const rawId = extract(e, 'id');
        const arxivId = rawId.replace(/^https?:\/\/arxiv\.org\/abs\//, '').replace(/v\d+$/, '');
        const pdf = findLinkHref(e, 'related') || `https://arxiv.org/pdf/${arxivId}`;
        entries.push({
            id: arxivId,
            title: decodeEntities(extract(e, 'title').replace(/\s+/g, ' ')),
            authors: decodeEntities(extractAll(e, 'name').join(', ')),
            abstract: decodeEntities(extract(e, 'summary').replace(/\s+/g, ' ')),
            published: extract(e, 'published').slice(0, 10),
            updated: extract(e, 'updated').slice(0, 10),
            primary_category: extractAttr(e, 'arxiv:primary_category', 'term'),
            categories: extractAllAttr(e, 'category', 'term').join(', '),
            comment: decodeEntities(extract(e, 'arxiv:comment').replace(/\s+/g, ' ')),
            pdf,
            url: `https://arxiv.org/abs/${arxivId}`,
        });
    }
    return entries;
}

export async function run(input, broker, context) { return __run(input, broker, context); }
