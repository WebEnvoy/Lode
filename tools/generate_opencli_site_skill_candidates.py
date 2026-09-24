#!/usr/bin/env python3
"""Materialize proposed Lode package candidates from pinned OpenCLI sources.

This is a deterministic text transformation only. It never imports, executes,
installs, or fetches the fixed upstream adapters.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]


class CandidateError(ValueError):
    pass


def read_utf8(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as error:
        raise CandidateError(f"cannot read UTF-8 source {path}: {error}") from error


SOURCE_COMMIT_PATTERN = re.compile(r"^[0-9a-f]{40}$")
UPSTREAM_COMMIT = "8271afc67e8504bda94c147f446ee29775d08274"
UPSTREAM_ROOT = ROOT / "third_party/opencli-1.8.8"
LICENSE_BYTES = (UPSTREAM_ROOT / "LICENSE").read_bytes()
LICENSE_SHA256 = hashlib.sha256(LICENSE_BYTES).hexdigest()


def pretty(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + "\n").encode("utf-8")


def digest(data: bytes) -> str:
    return "sha256:" + hashlib.sha256(data).hexdigest()


def canonical(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("utf-8")


SAMPLES: list[dict[str, Any]] = [
    {
        "candidate_id": "github-trending-html",
        "site": "github",
        "name": "opencli-trending-repos",
        "task": "read-trending-repositories",
        "display": "GitHub Trending repositories",
        "origin": "https://github.com",
        "upstream_site": "github-trending",
        "upstream_name": "repos",
        "entrypoint": "third_party/opencli-1.8.8/clis/github-trending/repos.js",
        "source_files": ["third_party/opencli-1.8.8/clis/github-trending/repos.js"],
        "source_functions": ["parseTrendingHtml"],
        "accept": "text/html",
        "user_agent": "Mozilla/5.0 (compatible; opencli/github-trending)",
        "effective_user_agent": "Mozilla/5.0 (compatible; opencli/github-trending)",
        "user_agent_source": "adapter_explicit",
        "path": "/trending",
        "allow_one_path_segment": True,
        "query_keys": ["since"],
        "content_types": ["text/html"],
        "max_response_bytes": 2 * 1024 * 1024,
        "timeout_ms": 10000,
        "result_kind": "opencli_github_trending_repositories",
        "completeness_profile": {"kind": "html-requested-count", "default_limit": 25, "open_pattern": "<article\\b[^>]*class=\"[^\"]*\\bBox-row\\b[^\"]*\"[^>]*>", "close_pattern": "</article>", "required_non_empty_fields": ["repo", "url"], "safe_integer_fields": ["stars", "forks", "starsSince"], "url_field": "url", "url_prefix": "https://github.com/"},
        "empty_fixture": "github-trending-empty.html",
        "selection_reason": "Preselected to test reuse of the fixed upstream HTML parser and its since/language/limit semantics behind the managed anonymous response body. It is a distinct package from the existing daily-top5 snapshot task.",
        "compatibility_note": "The body is an actual HTTP response, not a rendered browser snapshot. Completeness compares the parsed records with min(requested limit, complete matching Box-row blocks); a valid zero-row result requires the original parser's explicit empty-site text.",
    },
    {
        "candidate_id": "devto-latest-json",
        "site": "devto",
        "name": "opencli-latest-articles",
        "task": "read-latest-articles-page",
        "display": "DEV.to latest articles",
        "origin": "https://dev.to",
        "upstream_site": "devto",
        "upstream_name": "latest",
        "entrypoint": "third_party/opencli-1.8.8/clis/devto/latest.js",
        "source_files": ["third_party/opencli-1.8.8/clis/devto/latest.js"],
        "source_functions": [],
        "accept": "application/json",
        "user_agent": None,
        "effective_user_agent": "node",
        "user_agent_source": "node_fetch_default",
        "path": "/api/articles/latest",
        "allow_one_path_segment": False,
        "query_keys": ["per_page", "page"],
        "content_types": ["application/json"],
        "max_response_bytes": 4 * 1024 * 1024,
        "timeout_ms": 10000,
        "result_kind": "opencli_devto_latest_articles",
        "completeness_profile": {"kind": "json-page-required-fields", "required_non_empty_fields": ["id", "title", "url"], "url_prefix": "https://dev.to/", "finite_nullable_number_fields": ["reactions", "comments"]},
        "empty_fixture": "devto-empty.json",
        "selection_reason": "Preselected to exercise a public JSON adapter on a second site while retaining the upstream limit/page validation, request construction, and field mapping.",
        "compatibility_note": "Completeness is scoped to the requested page response. It does not claim that the entire latest-article feed was fetched; the adapter does not consume a continuation link or total count.",
    },
    {
        "candidate_id": "arxiv-recent-atom",
        "site": "arxiv",
        "name": "opencli-recent-papers",
        "task": "read-recent-category-papers",
        "display": "arXiv recent papers by category",
        "origin": "https://export.arxiv.org",
        "upstream_site": "arxiv",
        "upstream_name": "recent",
        "entrypoint": "third_party/opencli-1.8.8/clis/arxiv/recent.js",
        "source_files": [
            "third_party/opencli-1.8.8/clis/arxiv/recent.js",
            "third_party/opencli-1.8.8/clis/arxiv/utils.js",
        ],
        "source_functions": ["parseEntries"],
        "accept": None,
        "user_agent": None,
        "effective_user_agent": "node",
        "user_agent_source": "node_fetch_default",
        "path": "/api/query",
        "allow_one_path_segment": False,
        "query_keys": ["search_query", "max_results", "sortBy", "sortOrder"],
        "content_types": ["application/atom+xml"],
        "max_response_bytes": 4 * 1024 * 1024,
        "timeout_ms": 20000,
        "result_kind": "opencli_arxiv_recent_papers",
        "completeness_profile": {"kind": "atom-feed-count-and-total", "default_limit": 10, "entry_open_pattern": "<entry\\b[^>]*>", "entry_close_pattern": "</entry>", "total_pattern": "<opensearch:totalResults\\b[^>]*>\\s*(\\d+)\\s*</opensearch:totalResults>", "feed_open_pattern": "<feed\\b", "feed_close_pattern": "</feed>\\s*$", "required_non_empty_fields": ["id", "title", "url"], "url_template": "https://arxiv.org/abs/{id}"},
        "empty_fixture": "arxiv-zero.atom",
        "selection_reason": "Chosen before shared-layer implementation to exercise a third site and Atom/XML parsing, and to expose the cost of the source adapter's statically imported local helper.",
        "compatibility_note": "A deterministic bundle preserves the helper/parser bodies but removes ESM export/import syntax. The source parser can return earlier entries from truncated XML; the wrapper reports `partial` unless the feed envelope, entry count, and totalResults agree with the requested limit. No page-completeness claim is inferred from HTTP 2xx.",
    },
]


def input_schema(sample: dict[str, Any]) -> dict[str, Any]:
    schema_id = f"lode://schema/site-skill/{sample['site']}/{sample['name']}/input@0.1.0"
    if sample["site"] == "github":
        properties = {
            "since": {"type": "string", "default": "daily", "pattern": "^([dD][aA][iI][lL][yY]|[wW][eE][eE][kK][lL][yY]|[mM][oO][nN][tT][hH][lL][yY])$"},
            "language": {"type": "string", "default": "", "maxLength": 64, "pattern": "^[^/?#\\\\\\u0000-\\u001f]*$"},
            "limit": {"anyOf": [{"type": "integer", "minimum": 1, "maximum": 25}, {"type": "string", "pattern": "^([1-9]|1[0-9]|2[0-5])$"}], "default": 25},
        }
        required: list[str] = []
    elif sample["site"] == "devto":
        properties = {
            "limit": {"anyOf": [{"type": "integer", "minimum": 1, "maximum": 100}, {"type": "string", "pattern": "^([1-9]|[1-9][0-9]|100)$"}], "default": 20},
            "page": {"anyOf": [{"type": "integer", "minimum": 1, "maximum": 1000}, {"type": "string", "pattern": "^(?:[1-9][0-9]{0,2}|1000)$"}], "default": 1},
        }
        required = []
    else:
        properties = {
            "category": {"type": "string", "minLength": 1, "maxLength": 64, "pattern": "^[a-z]+(?:-[a-z]+)*(?:\\.[A-Za-z0-9]+(?:-[A-Za-z0-9]+)*)?$"},
            "limit": {"anyOf": [{"type": "integer", "minimum": 1, "maximum": 50}, {"type": "string", "pattern": "^([1-9]|[1-4][0-9]|50)$"}], "default": 10},
        }
        required = ["category"]
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": schema_id,
        "type": "object",
        "required": required,
        "properties": properties,
        "additionalProperties": False,
    }


def field_schema(sample: dict[str, Any]) -> dict[str, Any]:
    if sample["site"] == "github":
        return {
            "rank": {"type": "integer", "minimum": 1, "maximum": 25},
            "repo": {"type": "string", "pattern": "^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$"},
            "description": {"type": "string"},
            "language": {"type": ["string", "null"]},
            "stars": {"type": "integer", "minimum": 0, "maximum": 9007199254740991},
            "forks": {"type": "integer", "minimum": 0, "maximum": 9007199254740991},
            "starsSince": {"type": "integer", "minimum": 0, "maximum": 9007199254740991},
            "url": {"type": "string", "pattern": "^https://github\\.com/[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$"},
        }
    if sample["site"] == "devto":
        return {
            "rank": {"type": "integer", "minimum": 1},
            "id": {"type": "string"},
            "title": {"type": "string"},
            "author": {"type": "string"},
            "tags": {"type": "string"},
            "reactions": {"type": ["number", "null"], "minimum": 0, "maximum": 9007199254740991},
            "comments": {"type": ["number", "null"], "minimum": 0, "maximum": 9007199254740991},
            "published": {"type": "string"},
            "url": {"type": "string"},
        }
    return {
        "id": {"type": "string"},
        "title": {"type": "string"},
        "authors": {"type": "string"},
        "published": {"type": "string"},
        "primary_category": {"type": "string"},
        "url": {"type": "string"},
    }


def output_schema(sample: dict[str, Any]) -> dict[str, Any]:
    schema_id = f"lode://schema/site-skill/{sample['site']}/{sample['name']}/output@0.1.0"
    fields = field_schema(sample)
    parameters = {"type": "object", "properties": {key: value for key, value in input_schema(sample)["properties"].items()}, "additionalProperties": False}
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": schema_id,
        "type": "object",
        "required": ["result_kind", "status", "normalized", "source_refs", "evidence_refs"],
        "properties": {
            "result_kind": {"const": sample["result_kind"]},
            "status": {"enum": ["available", "partial"]},
            "normalized": {
                "type": "object",
                "required": ["parameters", "records", "completeness", "pagination"],
                "properties": {
                    "parameters": parameters,
                    "records": {"type": "array", "items": {"type": "object", "required": list(fields), "properties": fields, "additionalProperties": False}},
                    "completeness": {"enum": ["complete", "unknown"]},
                    "pagination": {
                        "type": "object",
                        "required": ["mode", "has_more", "completeness"],
                        "properties": {
                            "mode": {"enum": ["top_n", "requested_page", "max_results"]},
                            "has_more": {"type": ["boolean", "null"]},
                            "completeness": {"enum": ["complete", "unknown"]},
                        },
                        "additionalProperties": False,
                    },
                },
                "additionalProperties": False,
                "allOf": [
                    {
                        "if": {"properties": {"completeness": {"const": "complete"}}, "required": ["completeness"]},
                        "then": {"properties": {"pagination": {"properties": {"completeness": {"const": "complete"}}}}},
                    }
                ],
            },
            "source_refs": {
                "type": "array",
                "minItems": 1,
                "maxItems": 1,
                "items": {"type": "object", "required": ["ref_id", "source_kind"], "properties": {"ref_id": {"type": "string", "minLength": 1}, "source_kind": {"const": "public_http_response"}}, "additionalProperties": False},
            },
            "evidence_refs": {
                "type": "array",
                "minItems": 1,
                "maxItems": 1,
                "items": {
                    "type": "object",
                    "required": ["ref_id", "evidence_kind", "producer", "redaction"],
                    "properties": {
                        "ref_id": {"type": "string", "minLength": 1},
                        "evidence_kind": {"const": "public_http_response"},
                        "producer": {"const": "core"},
                        "redaction": {"const": "summary_only"},
                    },
                    "additionalProperties": False,
                },
            },
        },
        "additionalProperties": False,
        "allOf": [
                {
                    "if": {"properties": {"status": {"const": "available"}}, "required": ["status"]},
                "then": {
                    "properties": {
                        "normalized": {
                            "properties": {
                                "completeness": {"const": "complete"},
                                "pagination": {"properties": {"completeness": {"const": "complete"}}},
                            }
                        }
                    }
                },
            },
            {
                "if": {"properties": {"status": {"const": "partial"}}, "required": ["status"]},
                "then": {
                    "properties": {
                        "normalized": {
                            "properties": {
                                "completeness": {"const": "unknown"},
                                "pagination": {"properties": {"completeness": {"const": "unknown"}}},
                            }
                        }
                    }
                },
            },
        ],
    }


def policy(sample: dict[str, Any]) -> dict[str, Any]:
    headers: dict[str, str] = {}
    if sample["accept"] is not None:
        headers["accept"] = sample["accept"]
    if sample["effective_user_agent"] is not None:
        headers["user-agent"] = sample["effective_user_agent"]
    return {
        "transport": "program_anonymous_https",
        "origin": sample["origin"],
        "pathname": sample["path"],
        "allow_one_path_segment": sample["allow_one_path_segment"],
        "query_keys": sample["query_keys"],
        "headers": headers,
        "content_types": sample["content_types"],
        "max_response_bytes": sample["max_response_bytes"],
        "max_redirects": 2,
        "timeout_ms": sample["timeout_ms"],
    }


def network_wrapper(sample: dict[str, Any]) -> str:
    spec = {
        "result_kind": sample["result_kind"],
        "mode": {"github": "top_n", "devto": "requested_page", "arxiv": "max_results"}[sample["site"]],
        "media_type": sample["content_types"][0],
        "headers": policy(sample)["headers"],
        "fetch_default_headers": (
            {"user-agent": sample["effective_user_agent"]}
            if sample["user_agent_source"] == "node_fetch_default" else {}
        ),
    }
    completeness_profile = sample["completeness_profile"]
    url_shim = ""
    if requires_url_compat(sample):
        url_policy = {
            "origin": sample["origin"],
            "pathname": sample["path"],
            "allow_one_path_segment": sample["allow_one_path_segment"],
            "query_keys": sample["query_keys"],
        }
        url_shim = f"""
// The approved worker intentionally has no Node host globals. Keep the
// adapter's URL construction inside this bounded, package-local interface.
const __opencliUrlPolicy = Object.freeze({json.dumps(url_policy, ensure_ascii=False, separators=(',', ':'))});
function __opencliPathAllowed(pathname) {{
  if (pathname === __opencliUrlPolicy.pathname) return true;
  if (!__opencliUrlPolicy.allow_one_path_segment || !pathname.startsWith(__opencliUrlPolicy.pathname + '/')) return false;
  const segment = pathname.slice(__opencliUrlPolicy.pathname.length + 1);
  if (!segment || segment.includes('/')) return false;
  let decoded;
  try {{ decoded = decodeURIComponent(segment); }} catch {{ return false; }}
  return Boolean(decoded && decoded !== '.' && decoded !== '..' && !/[\\\\/\\u0000-\\u001f\\u007f-\\u009f]/.test(decoded) && !/%(?:2f|5c|2e|00)/i.test(decoded));
}}
class __OpenCliURL {{
  constructor(value) {{
    if (typeof value !== 'string' || value.length > 2048 || /[?#\\\\\\u0000-\\u001f\\u007f-\\u009f]/.test(value) || !value.startsWith(__opencliUrlPolicy.origin)) throw new TypeError('URL is outside the pinned adapter interface');
    const pathname = value.slice(__opencliUrlPolicy.origin.length);
    if (!__opencliPathAllowed(pathname)) throw new TypeError('URL path is outside the pinned adapter interface');
    this.__pathname = pathname;
    this.__query = new Map();
    this.searchParams = Object.freeze({{ set: (name, rawValue) => {{
      if (typeof name !== 'string' || !__opencliUrlPolicy.query_keys.includes(name)) throw new TypeError('URL query key is outside the pinned adapter interface');
      const item = String(rawValue);
      if (item.length > 512 || /[\\u0000-\\u001f\\u007f-\\u009f]/.test(item)) throw new TypeError('URL query value is outside the pinned adapter interface');
      this.__query.set(name, item);
    }} }});
  }}
  toString() {{
    const query = [...this.__query].map(([name, value]) => encodeURIComponent(name) + '=' + encodeURIComponent(value).replace(/%20/g, '+')).join('&');
    return __opencliUrlPolicy.origin + this.__pathname + (query ? '?' + query : '');
  }}
}}
Object.defineProperty(globalThis, 'URL', {{ value: __OpenCliURL, writable: false, configurable: false }});
"""
    return f"""// Fixed compatibility shim for OpenCLI 1.8.8 PUBLIC read adapters.
// Generated from reviewed source text; all reads use this run's WebEnvoy broker.
const __opencliSpec = Object.freeze({json.dumps(spec, ensure_ascii=False, separators=(',', ':'))});
const __completenessProfile = Object.freeze({json.dumps(completeness_profile, ensure_ascii=False, separators=(',', ':'))});
let __opencliRegistration;
let __opencliBroker;
let __opencliResponse;
let __opencliReadCount = 0;
let __opencliRunning = false;

const Strategy = Object.freeze({{ PUBLIC: 'PUBLIC' }});
class ArgumentError extends Error {{ constructor(message, ...rest) {{ super(message, ...rest); this.name = 'ArgumentError'; }} }}
class CommandExecutionError extends Error {{ constructor(message, ...rest) {{ super(message, ...rest); this.name = 'CommandExecutionError'; }} }}
class EmptyResultError extends Error {{ constructor(message, ...rest) {{ super(message, ...rest); this.name = 'EmptyResultError'; }} }}
function cli(definition) {{
  if (__opencliRegistration) throw new Error('multiple adapter registrations are unsupported');
  __opencliRegistration = definition;
}}
{url_shim}

function __checkCompleteness(input, records, body) {{
  const profile = __completenessProfile;
  const requiredValues = (row) => profile.required_non_empty_fields.every((key) => typeof row[key] === 'string' && row[key].length > 0);
  if (profile.kind === 'html-requested-count') {{
    const requested = Number(input?.limit ?? profile.default_limit);
    const opened = (body.match(new RegExp(profile.open_pattern, 'gi')) ?? []).length;
    const closed = (body.match(new RegExp(profile.close_pattern, 'gi')) ?? []).length;
    const safeCounts = profile.safe_integer_fields.every((key) => records.every((row) => Number.isSafeInteger(row[key]) && row[key] >= 0));
    const urlsMatch = records.every((row) => row[profile.url_field] === profile.url_prefix + row.repo);
    const expectedCount = Math.min(requested, opened);
    const explicitEmpty = opened === 0 && typeof hasExplicitEmptyTrending === 'function' && hasExplicitEmptyTrending(body);
    const complete = Number.isInteger(requested) && opened === closed && records.length === expectedCount && (opened > 0 || explicitEmpty) && records.every(requiredValues) && safeCounts && urlsMatch;
    return {{ state: complete ? 'complete' : 'unknown', hasMore: null }};
  }}
  if (profile.kind === 'json-page-required-fields') {{
    const countersFinite = profile.finite_nullable_number_fields.every((key) => records.every((row) => row[key] === null || Number.isFinite(row[key])));
    if (!countersFinite) throw new CommandExecutionError('adapter produced a non-finite numeric value');
    const urlsMatch = records.every((row) => typeof row.url === 'string' && row.url.startsWith(profile.url_prefix));
    const complete = records.every(requiredValues) && urlsMatch;
    return {{ state: complete ? 'complete' : 'unknown', hasMore: null }};
  }}
  if (profile.kind === 'atom-feed-count-and-total') {{
    const requested = Number(input?.limit ?? profile.default_limit);
    const totalMatch = body.match(new RegExp(profile.total_pattern));
    const total = totalMatch ? Number(totalMatch[1]) : NaN;
    const opened = (body.match(new RegExp(profile.entry_open_pattern, 'g')) ?? []).length;
    const closed = (body.match(new RegExp(profile.entry_close_pattern, 'g')) ?? []).length;
    const feedOpen = new RegExp(profile.feed_open_pattern, 'i').test(body);
    const feedClosed = new RegExp(profile.feed_close_pattern, 'i').test(body);
    const urlsMatch = records.every((row) => row.url === profile.url_template.replace('{{id}}', row.id));
    const complete = feedOpen && feedClosed && opened === closed && opened === records.length && Number.isSafeInteger(total) && records.length === Math.min(requested, total) && records.every(requiredValues) && urlsMatch;
    return {{ state: complete ? 'complete' : 'unknown', hasMore: null }};
  }}
  throw new CommandExecutionError('unsupported pinned completeness profile');
}}

function __confirmedEmpty(body) {{
  const profile = __completenessProfile;
  if (profile.kind === 'html-requested-count') {{
    const opened = (body.match(new RegExp(profile.open_pattern, 'gi')) ?? []).length;
    const closed = (body.match(new RegExp(profile.close_pattern, 'gi')) ?? []).length;
    return opened === 0 && closed === 0 && typeof hasExplicitEmptyTrending === 'function' && hasExplicitEmptyTrending(body);
  }}
  if (profile.kind === 'json-page-required-fields') {{
    try {{ const parsed = JSON.parse(body); return Array.isArray(parsed) && parsed.length === 0; }} catch {{ return false; }}
  }}
  if (profile.kind === 'atom-feed-count-and-total') {{
    const totalMatch = body.match(new RegExp(profile.total_pattern));
    const openCount = (body.match(new RegExp(profile.entry_open_pattern, 'g')) ?? []).length;
    const closeCount = (body.match(new RegExp(profile.entry_close_pattern, 'g')) ?? []).length;
    return new RegExp(profile.feed_open_pattern, 'i').test(body)
      && new RegExp(profile.feed_close_pattern, 'i').test(body)
      && totalMatch !== null && Number(totalMatch[1]) === 0 && openCount === 0 && closeCount === 0;
  }}
  return false;
}}

async function __brokerFetch(value, options = {{}}) {{
  if (!__opencliBroker?.network?.read || __opencliReadCount !== 0) throw new CommandExecutionError('managed public read unavailable or request budget exceeded');
  const method = String(options.method ?? 'GET').toUpperCase();
  if (method !== 'GET' || options.body != null || options.credentials != null || options.redirect != null) throw new CommandExecutionError('only the fixed anonymous GET contract is supported');
  const headers = {{}};
  for (const [rawName, headerValue] of Object.entries(options.headers ?? {{}})) {{
    const name = rawName.toLowerCase();
    if (Object.hasOwn(headers, name) || !Object.hasOwn(__opencliSpec.headers, name) || typeof headerValue !== 'string' || headerValue !== __opencliSpec.headers[name]) throw new CommandExecutionError('adapter request header differs from its pinned policy');
    headers[name] = headerValue;
  }}
  for (const [name, headerValue] of Object.entries(__opencliSpec.fetch_default_headers)) {{
    if (Object.hasOwn(headers, name) && headers[name] !== headerValue) throw new CommandExecutionError('adapter request header differs from its pinned fetch default');
    headers[name] = headerValue;
  }}
  if (Object.keys(headers).length !== Object.keys(__opencliSpec.headers).length) throw new CommandExecutionError('adapter omitted a pinned request header');
  __opencliReadCount += 1;
  const response = await __opencliBroker.network.read({{ url: String(value), method: 'GET', headers }});
  if (!response || typeof response.ok !== 'boolean' || !Number.isInteger(response.status) || typeof response.url !== 'string' || typeof response.body !== 'string' || typeof response.response_ref !== 'string' || !response.response_ref || typeof response.content_type !== 'string') throw new CommandExecutionError('managed public read returned an incomplete response');
  const mediaType = response.content_type.split(';', 1)[0].trim().toLowerCase();
  if (mediaType !== __opencliSpec.media_type) throw new CommandExecutionError('managed public read returned an unexpected media type');
  __opencliResponse = response;
  return {{
    ok: response.ok,
    status: response.status,
    async text() {{ return response.body; }},
    async json() {{ return JSON.parse(response.body); }},
  }};
}}

async function __run(input, broker, _context) {{
  if (!__opencliRegistration || typeof __opencliRegistration.func !== 'function') throw new Error('static OpenCLI registration missing');
  if (__opencliRunning) throw new Error('concurrent invocation is unsupported');
  __opencliRunning = true;
  __opencliBroker = broker;
  __opencliResponse = undefined;
  __opencliReadCount = 0;
  try {{
    let records;
    try {{
      records = await __opencliRegistration.func(input ?? {{}});
    }} catch (error) {{
      if (error?.name === 'EmptyResultError' && __opencliResponse && __confirmedEmpty(__opencliResponse.body)) records = [];
      else throw error;
    }}
    if (!Array.isArray(records) || !__opencliResponse || __opencliReadCount !== 1) throw new CommandExecutionError('adapter returned no verified response records');
    const completeness = __checkCompleteness(input, records, __opencliResponse.body);
    const result = {{
      result_kind: __opencliSpec.result_kind,
      status: completeness.state === 'complete' ? 'available' : 'partial',
      normalized: {{
        parameters: input ?? {{}},
        records,
        completeness: completeness.state,
        pagination: {{ mode: __opencliSpec.mode, has_more: completeness.hasMore, completeness: completeness.state }},
      }},
      source_refs: [{{ ref_id: __opencliResponse.response_ref, source_kind: 'public_http_response' }}],
      evidence_refs: [{{ ref_id: __opencliResponse.response_ref, evidence_kind: 'public_http_response', producer: 'core', redaction: 'summary_only' }}],
    }};
    return await broker.output.write(result);
  }} finally {{
    __opencliBroker = undefined;
    __opencliResponse = undefined;
    __opencliReadCount = 0;
    __opencliRunning = false;
  }}
}}
"""


def requires_url_compat(sample: dict[str, Any]) -> bool:
    """Detect the narrow URL constructor surface used by a fixed source set."""
    return any(re.search(r"\bnew\s+URL\s*\(", read_utf8(ROOT / relative)) for relative in sample["source_files"])


def source_script(sample: dict[str, Any]) -> bytes:
    segments: list[str] = []
    for relative in sample["source_files"]:
        source = read_utf8(ROOT / relative)
        source = re.sub(r"^\s*import\s+[^;]+;\s*\n", "", source, flags=re.MULTILINE)
        if relative.endswith("utils.js"):
            source = re.sub(r"^export\s+", "", source, flags=re.MULTILINE)
        calls = len(re.findall(r"\bfetch\s*\(", source))
        if calls != (1 if relative.endswith(("repos.js", "latest.js", "utils.js")) else 0):
            raise CandidateError(f"expected one reviewed network call site in {relative}, found {calls}")
        source = re.sub(r"\bfetch\s*\(", "__brokerFetch(", source)
        segments.append(f"\n// Retained source: {relative}\n{source.rstrip()}\n")
    return (network_wrapper(sample) + "".join(segments) + "\nexport async function run(input, broker, context) { return __run(input, broker, context); }\n").encode("utf-8")


def task_data(sample: dict[str, Any], package_ref: str, revision: str, source_ref: str, capability_ref: str, script_ref: str, script_sha: str) -> dict[str, Any]:
    schema_root = f"lode://schema/site-skill/{sample['site']}/{sample['name']}"
    post_check_ref = f"lode://check/site-skill/{sample['site']}/{sample['name']}/post-check@0.1.0"
    recovery_ref = f"lode://reference/site-skill/{sample['site']}/{sample['name']}/recovery@0.1.0"
    return {
        "task_ref": sample["task"],
        "version": "0.1.0",
        "title": sample["display"],
        "intent": f"Read public {sample['display']} data using the pinned OpenCLI 1.8.8 adapter semantics.",
        "operation_id": "network.public_read",
        "action": "read",
        "applicability": {"origins": [sample["origin"]], "target_type": "public_http_origin"},
        "entrypoint": {
            "script_ref": script_ref,
            "script_version": "0.1.0",
            "script_sha256": script_sha,
            "runtime_kind": "webenvoy.site-skill-script-abi/v1",
            "broker": "webenvoy.site-skill-broker/v1.1",
            "capability_refs": [capability_ref],
        },
        "network_read": policy(sample),
        "inputs": {"schema_ref": f"{schema_root}/input@0.1.0", "carrier": "webenvoy.managed-task-inline/v1", "max_bytes": 4096, "content_type": "application/json", "sensitivity": "public"},
        "outputs": {"schema_ref": f"{schema_root}/output@0.1.0", "result_kind": sample["result_kind"], "completeness": "required"},
        "preconditions": ["anonymous_https_origin_allowed", "pinned_adapter_code_admitted"],
        "verification": {"post_check_ref": post_check_ref, "required_evidence_refs": ["public_http_response"]},
        "known_branches": ["invalid_input", "not_dispatched", "redirect_refused", "http_non_2xx", "response_too_large", "unexpected_content_type", "empty_result", "partial_result", "unknown_outcome"],
        "failure_recovery": {"failure_classes": ["invalid_contract", "resource_unavailable", "site_changed", "empty_result", "post_check_failed", "evidence_expired"], "repair_ref": recovery_ref, "unknown_policy": "query_original_run_only"},
        "data_handling": {"input_sensitivity": "public", "output_sensitivity": "public", "external_egress": "declared"},
    }


def markdown_mapping(sample: dict[str, Any], report: dict[str, Any], policy_value: dict[str, Any]) -> str:
    candidate = next(item for item in report["positive_candidates"] if item["id"] == sample["candidate_id"])
    source_files = {item["path"]: item for item in candidate["files"]}
    file_lines = "\n".join(
        f"- `{relative}` — upstream SHA-256 `{source_files[relative.removeprefix('third_party/opencli-1.8.8/')]['sha256']}`"
        for relative in sample["source_files"]
    )
    parser_text = ", ".join(f"`{item}`" for item in sample["source_functions"]) or "adapter 内联记录映射"
    accept_text = sample["accept"] if sample["accept"] is not None else "未声明；兼容层不添加 Accept"
    if sample["user_agent_source"] == "node_fetch_default":
        ua_text = "上游未显式设置；Node 24 `fetch` 默认 `node`，兼容层将这个有效默认值固定为 broker 请求头"
    else:
        ua_text = f"上游显式设置 `{sample['user_agent']}`"
    explicit_headers = {key: value for key, value in (("accept", sample["accept"]), ("user-agent", sample["user_agent"])) if value is not None}
    url_compat_text = (
        "- GitHub 源调用 `new URL()`。受管 VM 不注入 Node `URL` 或其他宿主全局，因此候选在包内提供只支持已固定 origin/path、至多一个声明路径段和声明 query key 的小型 URL 字符串接口；它不提供网络请求、DNS 或宿主运行时能力。\n"
        if requires_url_compat(sample) else ""
    )
    return f"""# OpenCLI 来源与兼容映射候选：{sample['display']}

状态：**候选材料**。这不是代码准入、安装、启用、正式执行或 live 验收结论。

## 固定来源

- 上游：[`jackwener/OpenCLI`](https://github.com/jackwener/OpenCLI)，版本 `1.8.8`，commit `{UPSTREAM_COMMIT}`。
- 许可证：Apache-2.0，来源文件 `third_party/opencli-1.8.8/LICENSE`，SHA-256 `{LICENSE_SHA256}`；候选包附同一许可证全文。
- 选中命令：`{sample['upstream_site']} {sample['upstream_name']}`；注册 `columns` 仅作字段线索。
{file_lines}

## 保留与包装

- 保留 parser/业务映射：{parser_text}；输入参数校验和 URL/query 构造保留上游逻辑。
- 入口包装只替换 OpenCLI 注册/error import，并将原始 `fetch` 名称解析到固定兼容 shim；shim 校验上游显式请求头，并只补入 Node 24 `fetch` 的固定默认 `User-Agent: node`（适用于未显式指定该头的样本）；arXiv 两个审查源以确定性文本 bundle 合并，移除静态 ESM import/export 标记，不改变工具/解析函数体。
{url_compat_text}- 兼容 shim 限制每个 Run 一次匿名 GET，将上游 Response 使用到的 `ok/status/text()/json()` 映射到 `network.read`；禁止未声明 method/body/credentials/redirect 参数。响应只在 worker 内存使用，结果只写 normalized records 与 opaque ref。
- 不使用浏览器 snapshot/DOM、原生网络、浏览器 Cookie/登录态、代理或任何凭据。HTTP 2xx 不等于业务成功。

## 固定匿名读取策略候选

```json
{json.dumps(policy_value, ensure_ascii=False, indent=2)}
```

上游显式请求头：`{json.dumps(explicit_headers, ensure_ascii=False) or '无'}`。有效 broker 策略：Accept=`{accept_text}`；User-Agent=`{ua_text}`。跳转最多 2 次同策略内；响应正文体积限制为 `{policy_value['max_response_bytes']}` 字节，超时 `{policy_value['timeout_ms']}` ms。该声明待 WebEnvoy #594 合同/实现接受后才可能执行。

## 输出语义与限制

- schema 显式类型化上游列出的每个公开输出字段；源字段缺失、可空、空文本和有限数值按上游表达式保留。DEV.to 非数字计数可产生 NaN，在 JSON/Schema 边界拒绝，不伪装为 `null`。
- 输出保留本次所请求的参数和分页范围；不能据单页数据声称整个站点集合完整。`available` 只在包装层给出本合同内的完整性证据时使用，无法证明时返回 `partial` / `unknown`。
- {sample['compatibility_note']}
- `source_refs` 与 `evidence_refs` 指向同一 `public_http_response` opaque ref；不输出响应正文、headers、Cookie 或真实 URL。
- `unknown` 按原 Run 查询/对账，不生成新 key 重放。导入和候选生成本身不信任、安装或启用资产。
- 上游 adapter 对零条记录会抛 `EmptyResultError`；候选 wrapper 只在可复核信号明确时归一为 `available` 且 `records: []`：GitHub 需 explicit-empty 文案及零个完整 Box-row，DEV.to 需正文严格解析为 JSON 数组 `[]`，arXiv 需完整 Atom feed、`totalResults=0` 且零 entry。没有这些信号的空结果继续失败；截断/缺字段不归为合法空集合。
- GitHub `limit` 是上限；完整页少于 limit 时，只有 `min(limit, matched Box-row count)` 个 parsed row 与完整正文一致才判 available。

## 离线验证入口

- 静态核验：`python3 tools/opencli_readonly_candidates.py --check`
- 同一组离线 HTML/JSON/Atom fixture 调用固定 OpenCLI 源码：`node --experimental-vm-modules tools/test_opencli_readonly_semantics.mjs`
- 固定测试材料列于 `tools/fixtures/opencli-readonly/`；测试不连接网站。
- 候选包 schema/check 由包级测试校验；正式网络 broker、代码准入、安装、现场执行和业务结果仍未验收。
"""


def package_files(sample: dict[str, Any], source_commit: str, source_record: dict[str, Any]) -> dict[str, bytes]:
    site, name = sample["site"], sample["name"]
    package_ref = f"lode://site-skill/{site}/{name}"
    revision = f"{package_ref}@0.1.0#{source_commit}"
    source_ref = f"lode://source/site-skill/{site}/{name}@0.1.0#{source_commit}"
    lock_ref = f"lode://lock/site-skill/{site}/{name}@0.1.0"
    capability_ref = f"lode://site-capability/{site}/{name}@0.1.0"
    script_ref = f"lode://script/site-skill/{site}/{name}/{sample['task']}@0.1.0"
    input_ref = f"lode://schema/site-skill/{site}/{name}/input@0.1.0"
    output_ref = f"lode://schema/site-skill/{site}/{name}/output@0.1.0"
    post_check_ref = f"lode://check/site-skill/{site}/{name}/post-check@0.1.0"
    recovery_ref = f"lode://reference/site-skill/{site}/{name}/recovery@0.1.0"
    script = source_script(sample)
    script_sha = digest(script)
    input_data = input_schema(sample)
    output_data = output_schema(sample)
    task = task_data(sample, package_ref, revision, source_ref, capability_ref, script_ref, script_sha)
    capability = {
        "capability_ref": capability_ref,
        "capability_id": name,
        "version": "0.1.0",
        "source_ref": source_ref,
        "lock_ref": lock_ref,
        "operation_id": "network.public_read",
        "action": "read",
    }
    post_check = {
        "schema_version": "lode.post-check.v0",
        "check_ref": post_check_ref,
        "requirements": [{
            "requirement_id": "public-response-and-complete-request-scope",
            "required_status": "available",
            "required_normalized_fields": ["parameters", "records", "completeness", "pagination"],
            "expected_normalized_fields": {"completeness": "complete"},
            "required_evidence_refs": ["public_http_response"],
        }],
    }
    recovery = f"""# Recovery: {sample['display']}

This candidate is a public anonymous read and performs no write. On authorization, target, rate-limit, content-type, response-size, parser, or completeness failure, retain the original Run and query its result. Do not switch origin, provider, browser, account, proxy, or network route; do not retry a dispatched unknown request under a new idempotency key. An owner may explicitly create and review a new task attempt only after querying/reconciling the original Run.
"""
    source_map = markdown_mapping(sample, source_record, policy(sample))
    skill = f"""# {sample['display']}

This proposed package retains OpenCLI `1.8.8` `{sample['upstream_site']} {sample['upstream_name']}` input and parser/mapping semantics behind a WebEnvoy-managed anonymous HTTPS read. Do not treat source indexing or installation as code admission or execution authorization.

Task: `{sample['task']}`. It accepts only the pinned fields in `schemas/input.schema.json`, is bound to `{sample['origin']}`, and emits the pinned output schema. The candidate target type is `public_http_origin`, so `task.submit` must omit `target`; WebEnvoy binds the task to the exact task origin and authorized Profile. It never uses browser state, account credentials, cookies, local files, a proxy, raw sockets, or arbitrary code loading. Query the original Run after unknown or missing results; do not replay.

The script broker v1.1 and `network_read` are pending cross-repository contract acceptance and implementation. Use this package only as review material until those gates are satisfied.
"""
    package_lock = {
        "schema_version": "lode.site-skill-package.lock.v1",
        "lock_ref": lock_ref,
        "package_ref": package_ref,
        "revision_ref": revision,
        "version": "0.1.0",
        "source_ref": source_ref,
        "capability_ref": capability_ref,
    }
    files: dict[str, bytes] = {
        "SKILL.md": skill.encode(),
        "capabilities/public-read.json": pretty(capability),
        "checks/post-check.json": pretty(post_check),
        "fixtures/README.md": ("# Offline fixture map\n\nAll fixtures are synthetic and live under `tools/fixtures/opencli-readonly/`; no site response or account material is included in this package candidate.\n" + "\n".join(f"- `{path}`" for path in _fixtures_for_sample(sample)) + "\n").encode(),
        "package-lock.json": pretty(package_lock),
        "references/OpenCLI-Apache-2.0-LICENSE.txt": LICENSE_BYTES,
        "references/opencli-source-mapping.md": source_map.encode(),
        "references/recovery.md": recovery.encode(),
        "schemas/input.schema.json": pretty(input_data),
        "schemas/output.schema.json": pretty(output_data),
        "scripts/opencli-adapter.mjs": script,
        f"tasks/{sample['task']}.json": pretty(task),
    }
    role_for_path = {
        "SKILL.md": "entrypoint",
        "capabilities/public-read.json": "capability_declaration",
        "checks/post-check.json": "post_check",
        "fixtures/README.md": "fixture_index",
        "package-lock.json": "package_lock",
        "references/OpenCLI-Apache-2.0-LICENSE.txt": "license_notice",
        "references/opencli-source-mapping.md": "source_mapping",
        "references/recovery.md": "repair_guidance",
        "schemas/input.schema.json": "input_schema",
        "schemas/output.schema.json": "output_schema",
        "scripts/opencli-adapter.mjs": "script_source",
        f"tasks/{sample['task']}.json": "task_declaration",
    }
    integrity_files = [
        {"path": path, "role": role_for_path[path], "bytes": len(data), "sha256": digest(data)}
        for path, data in sorted(files.items())
    ]
    manifest: dict[str, Any] = {
        "manifest_version": "lode.site-skill-package.manifest.v1",
        "package_type": "site-skill",
        "package_ref": package_ref,
        "revision_ref": revision,
        "version": "0.1.0",
        "lifecycle": "proposed",
        "site": {"site_id": site, "supported_origins": [sample["origin"]]},
        "source": {"repository": "WebEnvoy/Lode", "package_path": f"sites/{site}/{name}", "commit": source_commit, "source_ref": source_ref},
        "package_lock": {"path": "package-lock.json", "lock_ref": lock_ref},
        "integrity": {"files": integrity_files},
        "compatibility": {"package_contract": "lode.site-skill-package/v1", "execution_contract": "webenvoy.site-skill-execution/v1", "required_capabilities": [{"ref": capability_ref, "version": "0.1.0"}]},
        "assets": [
            {"role": "capability_declaration", "path": "capabilities/public-read.json", "capability_ref": capability_ref},
            {"role": "input_schema", "path": "schemas/input.schema.json", "schema_ref": input_ref},
            {"role": "output_schema", "path": "schemas/output.schema.json", "schema_ref": output_ref},
            {"role": "post_check", "path": "checks/post-check.json", "check_ref": post_check_ref},
            {"role": "repair_guidance", "path": "references/recovery.md", "reference_ref": recovery_ref},
        ],
        "scripts": [{
            "script_ref": script_ref,
            "path": "scripts/opencli-adapter.mjs",
            "source_commit": source_commit,
            "version": "0.1.0",
            "sha256": script_sha,
            "runtime_kind": "webenvoy.site-skill-script-abi/v1",
            "entrypoint": "run",
            "input_schema_ref": input_ref,
            "output_schema_ref": output_ref,
            "capability_refs": [capability_ref],
            "action": "read",
            "broker": "webenvoy.site-skill-broker/v1.1",
            "broker_capabilities": ["network.read", "output.write"],
            "target_binding": {"target_type": "public_http_origin", "requires_profile_origin_grant": True},
            "timeout_ms": sample["timeout_ms"],
            "cancel": "cooperative",
            "data_handling": {"input_sensitivity": "public", "output_sensitivity": "public", "external_egress": "declared"},
        }],
        "tasks": [{"task_ref": sample["task"], "path": f"tasks/{sample['task']}.json"}],
        "validation": {"runtime_execution": "not_claimed", "live_evidence": "not_claimed"},
    }
    digest_input = b"lode.site-skill-package/v1\n" + canonical(manifest) + b"\n" + "".join(
        f"{record['path']}\t{record['bytes']}\t{record['sha256']}\n" for record in integrity_files
    ).encode()
    manifest["integrity"]["package_digest"] = digest(digest_input)
    files["manifest.json"] = pretty(manifest)
    return files


def _fixtures_for_sample(sample: dict[str, Any]) -> list[str]:
    if sample["site"] == "github":
        return ["github-trending.html", "github-trending-empty.html", "github-trending-truncated.html"]
    if sample["site"] == "devto":
        return ["devto-latest-complete.json", "devto-latest.json", "devto-empty.json", "devto-not-array.json", "devto-invalid-json.txt"]
    return ["arxiv-recent.atom", "arxiv-empty.atom", "arxiv-zero.atom", "arxiv-truncated.atom"]


def source_record() -> dict[str, Any]:
    return json.loads((ROOT / "docs/verification/opencli-v1.8.8-readonly-candidates.json").read_text(encoding="utf-8"))


def run(source_commit: str, check: bool) -> int:
    if not SOURCE_COMMIT_PATTERN.fullmatch(source_commit):
        raise CandidateError("--source-commit must be a full lowercase Git SHA-1")
    source = source_record()
    mismatches: list[str] = []
    for sample in SAMPLES:
        package_root = ROOT / "sites" / sample["site"] / sample["name"]
        expected = package_files(sample, source_commit, source)
        for relative, data in expected.items():
            destination = package_root / relative
            if check:
                if not destination.is_file() or destination.read_bytes() != data:
                    mismatches.append(str(destination.relative_to(ROOT)))
            else:
                destination.parent.mkdir(parents=True, exist_ok=True)
                destination.write_bytes(data)
    if check and mismatches:
        raise CandidateError("generated package candidate bytes differ: " + ", ".join(mismatches))
    print("OpenCLI Lode package candidates match fixed source and pins" if check else "Generated three proposed Lode package candidates; execution remains unclaimed")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-commit", help="immutable Lode source commit recorded in each package")
    parser.add_argument("--check", action="store_true", help="verify exact generated candidate bytes without writing")
    args = parser.parse_args()
    source_commit = args.source_commit
    if args.check and source_commit is None:
        manifests = [ROOT / "sites" / sample["site"] / sample["name"] / "manifest.json" for sample in SAMPLES]
        commits = {json.loads(path.read_text(encoding="utf-8"))["source"]["commit"] for path in manifests if path.is_file()}
        if len(commits) != 1:
            raise CandidateError("candidate packages must exist and share one source.commit for --check")
        source_commit = next(iter(commits))
    if source_commit is None:
        parser.error("--source-commit is required unless --check reads it from existing manifests")
    try:
        return run(source_commit, args.check)
    except (CandidateError, OSError, json.JSONDecodeError, KeyError, TypeError, ValueError) as error:
        print(f"candidate package generation failed: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
