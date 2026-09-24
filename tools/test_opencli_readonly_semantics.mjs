import assert from 'node:assert/strict';
import { execFileSync } from 'node:child_process';
import { readFile } from 'node:fs/promises';
import path from 'node:path';
import vm from 'node:vm';

const root = path.resolve(import.meta.dirname, '..');
const upstream = path.join(root, 'third_party/opencli-1.8.8');
const fixtures = path.join(root, 'tools/fixtures/opencli-readonly');

function toHost(value) {
  if (value === undefined) return undefined;
  return JSON.parse(JSON.stringify(value));
}

// Run the text-only digest/import/hazard audit before creating any VM module.
execFileSync('python3', ['tools/opencli_readonly_candidates.py', '--check'], { cwd: root, stdio: 'inherit' });

const modules = {
  registry: `export const Strategy = Object.freeze({ PUBLIC: 'PUBLIC' });
export function cli(definition) { globalThis.__opencli.register(definition); }`,
  errors: `export class ArgumentError extends Error { constructor(message, ...rest) { super(message, ...rest); this.name = 'ArgumentError'; } }
export class CommandExecutionError extends Error { constructor(message, ...rest) { super(message, ...rest); this.name = 'CommandExecutionError'; } }
export class EmptyResultError extends Error { constructor(message, ...rest) { super(message, ...rest); this.name = 'EmptyResultError'; } }`,
};

async function loadAdapter(entryPath, fetchImpl) {
  let registration;
  const context = vm.createContext({
    URL,
    fetch: fetchImpl,
    __opencli: { register(definition) { registration = definition; } },
  }, { codeGeneration: { strings: false, wasm: false } });
  const cache = new Map();
  const fileModule = async (relativePath) => {
    const identifier = path.posix.normalize(relativePath);
    if (cache.has(identifier)) return cache.get(identifier);
    const source = await readFile(path.join(root, identifier), 'utf8');
    const module = new vm.SourceTextModule(source, {
      context,
      identifier,
      importModuleDynamically() { throw new Error('dynamic imports are denied in this harness'); },
    });
    cache.set(identifier, module);
    return module;
  };
  const builtinModule = (identifier, source) => {
    if (cache.has(identifier)) return cache.get(identifier);
    const module = new vm.SourceTextModule(source, { context, identifier });
    cache.set(identifier, module);
    return module;
  };
  const rootModule = await fileModule(entryPath);
  await rootModule.link(async (specifier, referencingModule) => {
    if (specifier === '@jackwener/opencli/registry') return builtinModule('opencli-shim:registry', modules.registry);
    if (specifier === '@jackwener/opencli/errors') return builtinModule('opencli-shim:errors', modules.errors);
    if (specifier === './utils.js' && referencingModule.identifier.endsWith('/clis/arxiv/recent.js')) {
      return fileModule('third_party/opencli-1.8.8/clis/arxiv/utils.js');
    }
    throw new Error(`denied module import ${specifier} from ${referencingModule.identifier}`);
  });
  await rootModule.evaluate();
  assert.ok(registration, `adapter did not register: ${entryPath}`);
  return registration;
}

function fixtureFetch(expectedOrigin, expectedPath, body, { status = 200, json = false } = {}) {
  const calls = [];
  const fetch = async (urlValue, options = {}) => {
    const url = new URL(String(urlValue));
    assert.equal(url.origin, expectedOrigin, 'adapter requested an unapproved origin');
    assert.equal(url.pathname, expectedPath, 'adapter requested an unapproved path');
    calls.push({ url: url.toString(), options: structuredClone(options) });
    return {
      ok: status >= 200 && status < 300,
      status,
      async text() {
        if (json) throw new Error('text() used for JSON fixture');
        return body;
      },
      async json() {
        if (!json) throw new Error('json() used for text fixture');
        return JSON.parse(body);
      },
    };
  };
  return { fetch, calls };
}

async function textFixture(name) {
  return readFile(path.join(fixtures, name), 'utf8');
}

const packagedAdapters = {
  github: 'sites/github/opencli-trending-repos/scripts/opencli-adapter.mjs',
  devto: 'sites/devto/opencli-latest-articles/scripts/opencli-adapter.mjs',
  arxiv: 'sites/arxiv/opencli-recent-papers/scripts/opencli-adapter.mjs',
};

async function executePackagedAdapter(site, input, { body, contentType, status = 200, failAfterDispatch = false }) {
  const source = await readFile(path.join(root, packagedAdapters[site]), 'utf8');
  assert.doesNotMatch(source, /^\s*import\s/m, 'candidate bundles must have no unresolved module loader');
  assert.doesNotMatch(source, /\b(?:eval|Function)\s*\(|\bimport\s*\(|\b(?:require|child_process)\b|process\.env/);
  let output;
  const calls = [];
  // Match the installed worker's context: only the generated module's own
  // globals are present; Node host globals such as URL are not injected.
  const context = vm.createContext(Object.create(null));
  assert.equal(vm.runInContext('typeof URL', context), 'undefined');
  const module = new vm.SourceTextModule(source, { context, identifier: packagedAdapters[site] });
  await module.link(() => { throw new Error('candidate bundle unexpectedly imported a module'); });
  await module.evaluate();
  assert.equal(vm.runInContext('typeof URL', context), site === 'github' ? 'function' : 'undefined');
  const responseRef = `core:public-http:${site}:fixture`;
  const broker = {
    network: {
      async read(request) {
        calls.push(toHost(request));
        assert.equal(request.method, 'GET');
        assert.equal(typeof request.url, 'string');
        assert.equal('body' in request, false);
        assert.equal('credentials' in request, false);
        if (failAfterDispatch) throw new Error('fixture response lost after dispatch');
        return {
          ok: status >= 200 && status < 300,
          status,
          url: request.url,
          body,
          response_ref: responseRef,
          content_type: contentType,
        };
      },
    },
    output: {
      async write(value) {
        output = toHost(value);
        return { accepted: true };
      },
    },
  };
  let result;
  let error;
  try {
    result = await module.namespace.run(input, broker, {});
  } catch (caught) {
    error = caught;
  }
  return { calls, output, result: toHost(result), error };
}

function assertCandidateEvidence(output, responseRef) {
  assert.equal(output.source_refs.length, 1);
  assert.deepEqual(output.source_refs[0], { ref_id: responseRef, source_kind: 'public_http_response' });
  assert.deepEqual(output.evidence_refs[0], {
    ref_id: responseRef,
    evidence_kind: 'public_http_response',
    producer: 'core',
    redaction: 'summary_only',
  });
}

async function testGithubTrending() {
  const html = await textFixture('github-trending.html');
  const network = fixtureFetch('https://github.com', '/trending', html);
  const adapter = await loadAdapter('third_party/opencli-1.8.8/clis/github-trending/repos.js', network.fetch);
  assert.deepEqual(toHost(adapter.args.map(({ name, default: value }) => [name, value])), [
    ['since', 'daily'], ['language', ''], ['limit', 25],
  ]);
  const rows = await adapter.func({});
  assert.deepEqual(toHost(rows), [
    { rank: 1, repo: 'acme/alpha', description: 'A & B core', language: 'TypeScript', stars: 12345, forks: 1234, starsSince: 456, url: 'https://github.com/acme/alpha' },
    { rank: 2, repo: 'acme/beta', description: '', language: null, stars: 90, forks: 8, starsSince: 7, url: 'https://github.com/acme/beta' },
  ]);
  assert.equal(network.calls[0].url, 'https://github.com/trending?since=daily');
  assert.equal(network.calls[0].options.headers.Accept, 'text/html');
  assert.equal(network.calls[0].options.headers['User-Agent'], 'Mozilla/5.0 (compatible; opencli/github-trending)');

  const filteredNetwork = fixtureFetch('https://github.com', '/trending/c%2B%2B', html);
  const filtered = await loadAdapter('third_party/opencli-1.8.8/clis/github-trending/repos.js', filteredNetwork.fetch);
  assert.equal((await filtered.func({ since: 'weekly', language: 'c++', limit: 1 })).length, 1);
  assert.equal(filteredNetwork.calls[0].url, 'https://github.com/trending/c%2B%2B?since=weekly');

  const emptyNetwork = fixtureFetch('https://github.com', '/trending', await textFixture('github-trending-empty.html'));
  const empty = await loadAdapter('third_party/opencli-1.8.8/clis/github-trending/repos.js', emptyNetwork.fetch);
  await assert.rejects(empty.func({}), { name: 'EmptyResultError' });

  const truncatedNetwork = fixtureFetch('https://github.com', '/trending', await textFixture('github-trending-truncated.html'));
  const truncated = await loadAdapter('third_party/opencli-1.8.8/clis/github-trending/repos.js', truncatedNetwork.fetch);
  await assert.rejects(truncated.func({}), { name: 'CommandExecutionError' });

  const invalidNetwork = fixtureFetch('https://github.com', '/trending', html);
  const invalid = await loadAdapter('third_party/opencli-1.8.8/clis/github-trending/repos.js', invalidNetwork.fetch);
  await assert.rejects(invalid.func({ since: 'yearly' }), { name: 'ArgumentError' });
  await assert.rejects(invalid.func({ limit: 26 }), { name: 'ArgumentError' });
  assert.equal(invalidNetwork.calls.length, 0, 'invalid inputs must fail before fetch');

  const limitedNetwork = fixtureFetch('https://github.com', '/trending', html, { status: 429 });
  const limited = await loadAdapter('third_party/opencli-1.8.8/clis/github-trending/repos.js', limitedNetwork.fetch);
  await assert.rejects(limited.func({}), { name: 'CommandExecutionError' });
}

async function testDevtoLatest() {
  const body = await textFixture('devto-latest.json');
  const network = fixtureFetch('https://dev.to', '/api/articles/latest', body, { json: true });
  const adapter = await loadAdapter('third_party/opencli-1.8.8/clis/devto/latest.js', network.fetch);
  assert.deepEqual(toHost(adapter.args.map(({ name, default: value }) => [name, value])), [['limit', 20], ['page', 1]]);
  const rows = await adapter.func({ page: 2, limit: 20 });
  assert.deepEqual(toHost(rows), [
    { rank: 21, id: '123', title: 'Hello & world', author: 'alice', tags: 'node, ai', reactions: 4, comments: 2, published: '2026-09-25', url: 'https://dev.to/alice/hello-world' },
    { rank: 22, id: '', title: '', author: '', tags: '', reactions: null, comments: 3, published: 'bad', url: '' },
  ]);
  const request = new URL(network.calls[0].url);
  assert.equal(request.origin, 'https://dev.to');
  assert.equal(request.pathname, '/api/articles/latest');
  assert.equal(request.searchParams.get('per_page'), '20');
  assert.equal(request.searchParams.get('page'), '2');
  assert.equal(network.calls[0].options.headers.accept, 'application/json');

  const completeBody = await textFixture('devto-latest-complete.json');
  const completeNetwork = fixtureFetch('https://dev.to', '/api/articles/latest', completeBody, { json: true });
  const completeAdapter = await loadAdapter('third_party/opencli-1.8.8/clis/devto/latest.js', completeNetwork.fetch);
  const completeRows = await completeAdapter.func({ page: 2, limit: 20 });

  for (const fixture of ['devto-empty.json', 'devto-not-array.json']) {
    const emptyNetwork = fixtureFetch('https://dev.to', '/api/articles/latest', await textFixture(fixture), { json: true });
    const empty = await loadAdapter('third_party/opencli-1.8.8/clis/devto/latest.js', emptyNetwork.fetch);
    await assert.rejects(empty.func({}), { name: 'EmptyResultError' });
  }

  const malformedNetwork = fixtureFetch('https://dev.to', '/api/articles/latest', await textFixture('devto-invalid-json.txt'), { json: true });
  const malformed = await loadAdapter('third_party/opencli-1.8.8/clis/devto/latest.js', malformedNetwork.fetch);
  await assert.rejects(malformed.func({}), { name: 'CommandExecutionError' });

  const invalidNetwork = fixtureFetch('https://dev.to', '/api/articles/latest', body, { json: true });
  const invalid = await loadAdapter('third_party/opencli-1.8.8/clis/devto/latest.js', invalidNetwork.fetch);
  await assert.rejects(invalid.func({ limit: 101 }), { name: 'ArgumentError' });
  await assert.rejects(invalid.func({ page: 0 }), { name: 'ArgumentError' });
  assert.equal(invalidNetwork.calls.length, 0, 'invalid inputs must fail before fetch');

  const limitedNetwork = fixtureFetch('https://dev.to', '/api/articles/latest', body, { status: 429, json: true });
  const limited = await loadAdapter('third_party/opencli-1.8.8/clis/devto/latest.js', limitedNetwork.fetch);
  await assert.rejects(limited.func({}), { name: 'CommandExecutionError' });
  return { incomplete: toHost(rows), complete: toHost(completeRows) };
}

async function testArxivRecent() {
  const body = await textFixture('arxiv-recent.atom');
  const network = fixtureFetch('https://export.arxiv.org', '/api/query', body);
  const adapter = await loadAdapter('third_party/opencli-1.8.8/clis/arxiv/recent.js', network.fetch);
  assert.deepEqual(toHost(adapter.args.map(({ name, required, positional, default: value }) => [name, required ?? false, positional ?? false, value])), [
    ['category', true, true, null], ['limit', false, false, 10],
  ]);
  assert.deepEqual(toHost(await adapter.func({ category: 'cs.CL' })), [
    { id: '2609.12345', title: 'A & B Parser', authors: 'Alice Example, Bob Example', published: '2026-09-25', primary_category: 'cs.CL', url: 'https://arxiv.org/abs/2609.12345' },
    { id: '2609.12346', title: 'Missing fields', authors: '', published: '', primary_category: '', url: 'https://arxiv.org/abs/2609.12346' },
  ]);
  const request = new URL(network.calls[0].url);
  assert.equal(request.origin, 'https://export.arxiv.org');
  assert.equal(request.pathname, '/api/query');
  assert.equal(request.searchParams.get('search_query'), 'cat:cs.CL');
  assert.equal(request.searchParams.get('max_results'), '10');
  assert.equal(request.searchParams.get('sortBy'), 'submittedDate');
  assert.equal(request.searchParams.get('sortOrder'), 'descending');

  const truncatedNetwork = fixtureFetch('https://export.arxiv.org', '/api/query', await textFixture('arxiv-truncated.atom'));
  const truncated = await loadAdapter('third_party/opencli-1.8.8/clis/arxiv/recent.js', truncatedNetwork.fetch);
  const truncatedRows = await truncated.func({ category: 'cs.CL' });
  assert.equal(truncatedRows.length, 1, 'the source parser returns prior entries when trailing XML is truncated');
  assert.equal(truncatedRows[0].id, '2609.12345');

  for (const fixture of ['arxiv-empty.atom', 'arxiv-truncated.atom']) {
    const emptyBody = fixture === 'arxiv-empty.atom' ? await textFixture(fixture) : '<feed><entry';
    const emptyNetwork = fixtureFetch('https://export.arxiv.org', '/api/query', emptyBody);
    const empty = await loadAdapter('third_party/opencli-1.8.8/clis/arxiv/recent.js', emptyNetwork.fetch);
    if (fixture === 'arxiv-empty.atom') await assert.rejects(empty.func({ category: 'cs.CL' }), { name: 'EmptyResultError' });
    else await assert.rejects(empty.func({ category: 'cs.CL' }), { name: 'EmptyResultError' });
  }

  const invalidNetwork = fixtureFetch('https://export.arxiv.org', '/api/query', body);
  const invalid = await loadAdapter('third_party/opencli-1.8.8/clis/arxiv/recent.js', invalidNetwork.fetch);
  await assert.rejects(invalid.func({ category: '../cs.CL' }), { name: 'ArgumentError' });
  await assert.rejects(invalid.func({ category: 'cs.CL', limit: 51 }), { name: 'ArgumentError' });
  assert.equal(invalidNetwork.calls.length, 0, 'invalid inputs must fail before fetch');

  const limitedNetwork = fixtureFetch('https://export.arxiv.org', '/api/query', body, { status: 503 });
  const limited = await loadAdapter('third_party/opencli-1.8.8/clis/arxiv/recent.js', limitedNetwork.fetch);
  await assert.rejects(limited.func({ category: 'cs.CL' }), { name: 'CommandExecutionError' });
  return { complete: toHost(await adapter.func({ category: 'cs.CL' })), truncated: toHost(truncatedRows) };
}

async function testPackagedAdapterCandidates(sourceSemantics) {
  const responseRef = 'core:public-http:github:fixture';
  const github = await executePackagedAdapter('github', { since: 'daily', language: '', limit: 3 }, {
    body: await textFixture('github-trending.html'), contentType: 'text/html; charset=utf-8',
  });
  assert.equal(github.error, undefined);
  assert.equal(github.output.status, 'available');
  assert.deepEqual(github.output.normalized.records, [
    { rank: 1, repo: 'acme/alpha', description: 'A & B core', language: 'TypeScript', stars: 12345, forks: 1234, starsSince: 456, url: 'https://github.com/acme/alpha' },
    { rank: 2, repo: 'acme/beta', description: '', language: null, stars: 90, forks: 8, starsSince: 7, url: 'https://github.com/acme/beta' },
  ]);
  assert.equal(github.calls.length, 1);
  assert.equal(github.calls[0].url, 'https://github.com/trending?since=daily');
  assert.deepEqual(github.calls[0].headers, {
    'user-agent': 'Mozilla/5.0 (compatible; opencli/github-trending)',
    accept: 'text/html',
  });
  assert.equal(github.output.normalized.parameters.limit, 3);
  assert.equal(github.output.normalized.records.length, 2, 'limit is an upper bound; a complete shorter page remains available');
  assertCandidateEvidence(github.output, responseRef);

  const githubLanguage = await executePackagedAdapter('github', { since: 'weekly', language: 'c++', limit: 1 }, {
    body: await textFixture('github-trending.html'), contentType: 'text/html; charset=utf-8',
  });
  assert.equal(githubLanguage.error, undefined);
  assert.equal(githubLanguage.calls[0].url, 'https://github.com/trending/c%2B%2B?since=weekly',
    'the in-VM URL interface preserves the adapter’s encoded path and query behavior');
  assert.equal(githubLanguage.output.normalized.parameters.language, 'c++');

  const githubEmpty = await executePackagedAdapter('github', { limit: 3 }, {
    body: await textFixture('github-trending-empty.html'), contentType: 'text/html',
  });
  assert.equal(githubEmpty.error, undefined);
  assert.equal(githubEmpty.output.status, 'available');
  assert.deepEqual(githubEmpty.output.normalized.records, [], 'explicit source empty signal normalizes to a valid empty collection');

  const githubUnknownEmpty = await executePackagedAdapter('github', { limit: 3 }, {
    body: '<html><body><main></main></body></html>', contentType: 'text/html',
  });
  assert.equal(githubUnknownEmpty.output, undefined, 'empty HTML without the explicit upstream empty signal must not become success');
  assert.equal(githubUnknownEmpty.error?.name, 'CommandExecutionError');

  const devto = await executePackagedAdapter('devto', { limit: 20, page: 2 }, {
    body: await textFixture('devto-latest-complete.json'), contentType: 'application/json; charset=utf-8',
  });
  assert.equal(devto.error, undefined);
  assert.equal(devto.output.status, 'available');
  assert.equal(devto.output.normalized.records[0].rank, 21);
  assert.equal(devto.output.normalized.records[0].author, 'sample-author');
  assert.deepEqual(devto.output.normalized.records, sourceSemantics.devto.complete, 'the packaged adapter preserves the same fixed complete-page fixture result');
  assert.equal(devto.calls.length, 1);
  const devtoUrl = new URL(devto.calls[0].url);
  assert.equal(devtoUrl.origin, 'https://dev.to');
  assert.equal(devtoUrl.pathname, '/api/articles/latest');
  assert.equal(devtoUrl.searchParams.get('per_page'), '20');
  assert.equal(devtoUrl.searchParams.get('page'), '2');
  assert.deepEqual(devto.calls[0].headers, { accept: 'application/json' });
  assertCandidateEvidence(devto.output, 'core:public-http:devto:fixture');

  const devtoEmpty = await executePackagedAdapter('devto', {}, {
    body: await textFixture('devto-empty.json'), contentType: 'application/json',
  });
  assert.equal(devtoEmpty.error, undefined);
  assert.equal(devtoEmpty.output.status, 'available');
  assert.deepEqual(devtoEmpty.output.normalized.records, [], 'a valid empty JSON page is distinguishable from malformed or missing data');
  assertCandidateEvidence(devtoEmpty.output, 'core:public-http:devto:fixture');

  const devtoNotArray = await executePackagedAdapter('devto', {}, {
    body: await textFixture('devto-not-array.json'), contentType: 'application/json',
  });
  assert.equal(devtoNotArray.output, undefined);
  assert.ok(devtoNotArray.error, 'an object response cannot be normalized as an empty page');

  const devtoMissing = await executePackagedAdapter('devto', { limit: 20, page: 2 }, {
    body: await textFixture('devto-latest.json'), contentType: 'application/json',
  });
  assert.equal(devtoMissing.error, undefined);
  assert.equal(devtoMissing.output.status, 'partial', 'missing key identity/title/URL cannot be accepted as a complete result');
  assert.equal(devtoMissing.output.normalized.completeness, 'unknown');
  assert.deepEqual(devtoMissing.output.normalized.records, sourceSemantics.devto.incomplete, 'partial classification does not rewrite the original field mapping');

  const devtoNaN = await executePackagedAdapter('devto', {}, {
    body: JSON.stringify([{ id: 1, title: 'nan', user: { username: 'a' }, tag_list: '', public_reactions_count: 'NaN', comments_count: 0, published_at: '2026-09-25', url: 'https://dev.to/a/nan' }]),
    contentType: 'application/json',
  });
  assert.equal(devtoNaN.output, undefined, 'non-finite values cannot be persisted as success');
  assert.equal(devtoNaN.error?.name, 'CommandExecutionError');

  const arxiv = await executePackagedAdapter('arxiv', { category: 'cs.CL', limit: 10 }, {
    body: await textFixture('arxiv-recent.atom'), contentType: 'application/atom+xml; charset=utf-8',
  });
  assert.equal(arxiv.error, undefined);
  assert.equal(arxiv.output.status, 'available');
  assert.deepEqual(arxiv.output.normalized.records.map(({ id, title, url }) => ({ id, title, url })), [
    { id: '2609.12345', title: 'A & B Parser', url: 'https://arxiv.org/abs/2609.12345' },
    { id: '2609.12346', title: 'Missing fields', url: 'https://arxiv.org/abs/2609.12346' },
  ]);
  assert.equal(arxiv.calls.length, 1);
  const arxivUrl = new URL(arxiv.calls[0].url);
  assert.equal(arxivUrl.origin, 'https://export.arxiv.org');
  assert.equal(arxivUrl.pathname, '/api/query');
  assert.equal(arxivUrl.searchParams.get('search_query'), 'cat:cs.CL');
  assert.equal(arxivUrl.searchParams.get('max_results'), '10');
  assert.equal(arxivUrl.searchParams.get('sortBy'), 'submittedDate');
  assert.equal(arxivUrl.searchParams.get('sortOrder'), 'descending');
  assert.deepEqual(arxiv.calls[0].headers, {});
  assertCandidateEvidence(arxiv.output, 'core:public-http:arxiv:fixture');

  const arxivEmpty = await executePackagedAdapter('arxiv', { category: 'cs.CL', limit: 10 }, {
    body: await textFixture('arxiv-zero.atom'), contentType: 'application/atom+xml',
  });
  assert.equal(arxivEmpty.error, undefined);
  assert.equal(arxivEmpty.output.status, 'available');
  assert.deepEqual(arxivEmpty.output.normalized.records, [], 'a complete Atom feed with totalResults=0 is a valid empty result');
  assertCandidateEvidence(arxivEmpty.output, 'core:public-http:arxiv:fixture');

  const arxivNoTotal = await executePackagedAdapter('arxiv', { category: 'cs.CL', limit: 10 }, {
    body: await textFixture('arxiv-empty.atom'), contentType: 'application/atom+xml',
  });
  assert.equal(arxivNoTotal.output, undefined, 'an empty feed without an explicit total remains unverified');
  assert.equal(arxivNoTotal.error?.name, 'EmptyResultError');

  const arxivTruncated = await executePackagedAdapter('arxiv', { category: 'cs.CL' }, {
    body: await textFixture('arxiv-truncated.atom'), contentType: 'application/atom+xml',
  });
  assert.equal(arxivTruncated.error, undefined);
  assert.equal(arxivTruncated.output.status, 'partial', 'the original parser can yield prior entries from a truncated Atom body');
  assert.equal(arxivTruncated.output.normalized.completeness, 'unknown');
  assert.deepEqual(arxivTruncated.output.normalized.records, sourceSemantics.arxiv.truncated, 'truncation is marked partial while retaining the original parser rows');
  assert.deepEqual(arxiv.output.normalized.records, sourceSemantics.arxiv.complete, 'the packaged adapter preserves the same fixed Atom fixture result');

  const refused = await executePackagedAdapter('github', { limit: 2 }, {
    body: await textFixture('github-trending.html'), contentType: 'text/html', status: 429,
  });
  assert.equal(refused.output, undefined);
  assert.equal(refused.error?.name, 'CommandExecutionError');
  assert.equal(refused.calls.length, 1);

  const unknown = await executePackagedAdapter('github', { limit: 2 }, {
    body: '', contentType: 'text/html', failAfterDispatch: true,
  });
  assert.equal(unknown.output, undefined);
  assert.equal(unknown.error?.name, 'CommandExecutionError');
  assert.equal(unknown.calls.length, 1, 'a lost dispatched response is not retried');
}

await testGithubTrending();
const devtoSemantics = await testDevtoLatest();
const arxivSemantics = await testArxivRecent();
await testPackagedAdapterCandidates({ devto: devtoSemantics, arxiv: arxivSemantics });
console.log('OpenCLI fixed-source and packaged candidate offline semantics: PASS (fixtures only; no network)');
