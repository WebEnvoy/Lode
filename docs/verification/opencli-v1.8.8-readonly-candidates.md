# OpenCLI v1.8.8 公共只读兼容候选

状态：固定源码静态审查、离线 adapter 语义候选和三个 proposed Lode 包文件已形成；**未完成代码准入、正式安装、live 执行或独立业务结果核验**。

## 来源与检查边界

- 上游：[`jackwener/OpenCLI` 1.8.8](https://github.com/jackwener/OpenCLI/tree/8271afc67e8504bda94c147f446ee29775d08274)，固定 commit `8271afc67e8504bda94c147f446ee29775d08274`。
- 许可：`Apache-2.0`；`NOTICE`: `未发现`；保留副本 `third_party/opencli-1.8.8/LICENSE`，SHA-256 `0210b8b66cf00358242cb921ba2be3a46dfe0190159b1b952388a3880ce1ff54`。
- package.json SHA-256：`f151c56b14d1a240855ba2330ba2885b5777f4bd45797142c8f719c325c600f0`。
- 上游 package lifecycle hooks 存在：`postinstall`, `prepare`, `prepublishOnly`, `preuninstall`；检查期间未运行。
- 检查器只读固定源文件，不导入/执行上游模块，不运行安装钩子，不访问网站；拒绝样本也只做静态文本检查。
- 三个候选包分别进入现有本地 registry，lifecycle 保持 proposed；候选可发现不等于信任、代码准入、安装或启用。官方 Lode validator 的 warning 继续标示 WebEnvoy #594 合同尚待接受。
- `Strategy.PUBLIC`、`access: read` 和 GET 本身不授予权限，也不证明 URL 安全。每个 task 仍需 WebEnvoy 授权及受管匿名 HTTP broker。

## 固定正向样本

### `github-trending-html` — `github-trending repos`

The first sample checks whether the existing raw HTML parser and parameter semantics can be retained behind a managed anonymous response body. It is a new OpenCLI candidate and does not replace the existing daily-top5 snapshot package.

- 源文件：`clis/github-trending/repos.js` (`0efc684322b8a70cac358ea3cdccc24bebf105a8d09e7fb6aa6c170e1fd72a32`)。
- 源 imports：`@jackwener/opencli/registry`, `@jackwener/opencli/errors`。
- parser：`parseTrendingHtml`；响应候选 `text/html`；分页：One page; `limit` slices returned rows and the source provides no continuation token or completeness signal.
- 请求：`GET https://github.com/trending/{encoded-language?}`；query `{"since": "daily|weekly|monthly"}`；Accept `text/html`；User-Agent `Mozilla/5.0 (compatible; opencli/github-trending)`。
- 参数来自静态注册及参数校验源码：

  | 参数 | 类型 | 必需/默认值/范围 | 证据 |
  | --- | --- | --- | --- |
  | `since` | `string` | 默认 `daily`; 枚举 `daily`, `weekly`, `monthly` | `const SINCE = {` |
  | `language` | `string` | 默认 `` | `const language = String(args.language ?? '').trim()` |
  | `limit` | `integer` | 默认 `25`; 范围 1–25 | `if (n > 25)` |

- 输出字段是人工按映射表达式核对的 schema 草稿；`columns` 只作为字段名线索：

  | 字段 | 类型 | 缺失/空值语义 | 源码锚点 |
  | --- | --- | --- | --- |
  | `rank` | `"integer"` | Computed from returned array index. | `third_party/opencli-1.8.8/clis/github-trending/repos.js:158` |
  | `repo` | `"string"` | Missing or malformed repository link throws parser-drift error. | `third_party/opencli-1.8.8/clis/github-trending/repos.js:67` |
  | `description` | `"string"` | Absent paragraph becomes empty string; present empty paragraph is also empty string. | `third_party/opencli-1.8.8/clis/github-trending/repos.js:73` |
  | `language` | `["string", "null"]` | Missing span becomes null; empty span becomes empty string. | `third_party/opencli-1.8.8/clis/github-trending/repos.js:78` |
  | `stars` | `"integer"` | Missing or nonnumeric count throws parser-drift error. | `third_party/opencli-1.8.8/clis/github-trending/repos.js:89` |
  | `forks` | `"integer"` | Missing or nonnumeric count throws parser-drift error. | `third_party/opencli-1.8.8/clis/github-trending/repos.js:90` |
  | `starsSince` | `"integer"` | Missing or nonnumeric count throws parser-drift error. | `third_party/opencli-1.8.8/clis/github-trending/repos.js:91` |
  | `url` | `"string"` | Derived from a validated repository identity. | `third_party/opencli-1.8.8/clis/github-trending/repos.js:92` |

- 未决边界：
  - OpenCLI columns are treated only as field-name clues; field types and missing-value behavior above are separately tied to parser expressions.
  - The source does not expose response truncation or page-completeness facts; a managed broker must fail closed when body completeness is unknown.
  - `Strategy.PUBLIC` and `access: read` are declarations, not authorization or network-safety evidence.

### `devto-latest-json` — `devto latest`

This second positive sample exercises public JSON parsing and user-controlled pagination on a different site, without page/browser state.

- 源文件：`clis/devto/latest.js` (`6b7290772a6f0c22bcbfc3b6da1f331c42d0c58bbb636ab9e1840b274f527302`)。
- 源 imports：`@jackwener/opencli/registry`, `@jackwener/opencli/errors`。
- parser：`inline JSON mapping in cli.func`；响应候选 `application/json`；分页：One requested page; `rank` is offset by `(page - 1) * limit`; no next-page or total-count signal is consumed.
- 请求：`GET https://dev.to/api/articles/latest`；query `{"per_page": "limit (1..100)", "page": "page (1..1000)"}`；Accept `application/json`；User-Agent `未由 adapter 显式设置；Node 24 `fetch` 有效默认 `node``。
- 参数来自静态注册及参数校验源码：

  | 参数 | 类型 | 必需/默认值/范围 | 证据 |
  | --- | --- | --- | --- |
  | `limit` | `integer` | 默认 `20`; 范围 1–100 | `requireBoundedInt(args.limit, 20, 100)` |
  | `page` | `integer` | 默认 `1`; 范围 1–1000 | `requireBoundedInt(args.page, 1, 1000)` |

- 输出字段是人工按映射表达式核对的 schema 草稿；`columns` 只作为字段名线索：

  | 字段 | 类型 | 缺失/空值语义 | 源码锚点 |
  | --- | --- | --- | --- |
  | `rank` | `"integer"` | Computed from input page/limit and array index. | `third_party/opencli-1.8.8/clis/devto/latest.js:63` |
  | `id` | `"string"` | Nullish id becomes empty string. | `third_party/opencli-1.8.8/clis/devto/latest.js:64` |
  | `title` | `"string"` | Nullish title becomes empty string. | `third_party/opencli-1.8.8/clis/devto/latest.js:65` |
  | `author` | `"string"` | Missing nested user/username becomes empty string. | `third_party/opencli-1.8.8/clis/devto/latest.js:66` |
  | `tags` | `"string"` | Nullish tag_list becomes empty string; arrays stringify then commas normalize. | `third_party/opencli-1.8.8/clis/devto/latest.js:67` |
  | `reactions` | `["number", "null"]` | Nullish becomes null; nonnumeric present values can produce NaN and need result validation. | `third_party/opencli-1.8.8/clis/devto/latest.js:68` |
  | `comments` | `["number", "null"]` | Nullish becomes null; nonnumeric present values can produce NaN and need result validation. | `third_party/opencli-1.8.8/clis/devto/latest.js:69` |
  | `published` | `"string"` | Nullish becomes empty string; malformed but present strings are sliced without date validation. | `third_party/opencli-1.8.8/clis/devto/latest.js:70` |
  | `url` | `"string"` | Nullish becomes empty string. | `third_party/opencli-1.8.8/clis/devto/latest.js:71` |

- 未决边界：
  - A non-array JSON body becomes an empty list and then EmptyResultError; it is not evidence of a valid empty page.
  - The source does not consume a continuation link or total; one-page output cannot claim the full feed is complete.
  - `Strategy.PUBLIC` and `access: read` are declarations, not authorization or network-safety evidence.

### `arxiv-recent-atom` — `arxiv recent`

Selected before shared implementation to test a third site and an Atom/XML parser with a statically imported local helper; it reveals module-packaging cost without requiring a site-specific Runtime branch.

- 源文件：`clis/arxiv/recent.js` (`59e2b9efb159ee7277ba284beaaae4119b8cd931967ad328499ced6bb9deafaa`), `clis/arxiv/utils.js` (`08518cd096e6c127bd1cebe83e6d1d6551bc3de2d1781bd1b7d9249f31e74708`)。
- 源 imports：`@jackwener/opencli/registry`, `@jackwener/opencli/errors`, `./utils.js`, `@jackwener/opencli/errors`。
- parser：`parseEntries in arxiv/utils.js`；响应候选 `application/atom+xml`；分页：One query with max_results and descending submitted date; no start offset or continuation token is consumed.
- 请求：`GET https://export.arxiv.org/api/query`；query `{"search_query": "cat:{validated-category}", "max_results": "limit (1..50)", "sortBy": "submittedDate", "sortOrder": "descending"}`；Accept `上游未设置`；User-Agent `未由 adapter 显式设置；Node 24 `fetch` 有效默认 `node``。
- 参数来自静态注册及参数校验源码：

  | 参数 | 类型 | 必需/默认值/范围 | 证据 |
  | --- | --- | --- | --- |
  | `category` | `string` | 必需; 位置参数; 格式 `^[a-z]+(?:-[a-z]+)*(?:\.[A-Za-z0-9]+(?:-[A-Za-z0-9]+)*)?$` | `ARXIV_CATEGORY_PATTERN` |
  | `limit` | `integer` | 默认 `10`; 范围 1–50 | `normalizeArxivLimit(args.limit, 10, 50)` |

- 输出字段是人工按映射表达式核对的 schema 草稿；`columns` 只作为字段名线索：

  | 字段 | 类型 | 缺失/空值语义 | 源码锚点 |
  | --- | --- | --- | --- |
  | `id` | `"string"` | Missing id becomes empty string and then yields an abs URL with an empty id. | `third_party/opencli-1.8.8/clis/arxiv/utils.js:98` |
  | `title` | `"string"` | Missing title becomes empty string. | `third_party/opencli-1.8.8/clis/arxiv/utils.js:99` |
  | `authors` | `"string"` | No authors becomes empty string. | `third_party/opencli-1.8.8/clis/arxiv/utils.js:100` |
  | `published` | `"string"` | Missing published becomes empty string; date syntax is not validated. | `third_party/opencli-1.8.8/clis/arxiv/utils.js:102` |
  | `primary_category` | `"string"` | Missing attribute becomes empty string. | `third_party/opencli-1.8.8/clis/arxiv/utils.js:104` |
  | `url` | `"string"` | Derived even when the normalized id is empty. | `third_party/opencli-1.8.8/clis/arxiv/utils.js:108` |

- 未决边界：
  - The candidate deterministically bundles the two pinned source files and preserves the helper/parser bodies; external errors-module top-level behavior remains unknown, and no general importer or arbitrary-module execution is claimed.
  - The regex parser can return earlier complete entries from truncated XML and does not report truncation; no completeness claim is safe without broker/body completeness evidence.
  - Malformed XML without entries and a valid empty feed both become EmptyResultError at the adapter boundary.
  - The adapter does not explicitly set Accept or User-Agent; Node 24 built-in fetch supplies the effective User-Agent `node`, which the managed wrapper now pins explicitly. No additional Accept header is added.
  - `Strategy.PUBLIC` and `access: read` are declarations, not authorization or network-safety evidence.

## 固定拒绝样本

| 来源 | 分类 | 静态锚点 | 执行 |
| --- | --- | --- | --- |
| `clis/1688/download.js` (`b3a0c69c32b557a7b1dd00b93eb466752d5ffbc6da40065dfebc1d6d27b25795`) | reject_cookie_and_local_download_dependency | `clis/1688/download.js:63`, `clis/1688/download.js:2`, `clis/1688/download.js:3` | 未执行 |
| `src/browser/cdp.ts` (`7771ad8fe31e208cc751cdf02b09ef2dc2a5fb75336b8129ed677c4bdf2f0f7f`) | reject_raw_cdp_method_dispatch | `src/browser/cdp.ts:456`, `src/browser/cdp.ts:457` | 未执行 |
| `clis/spotify/spotify.js` (`4f2ecef8a7b67598b7b4a21e451a649e3e0fcd7e2c8aaab9e6913f90a335a0ab`) | reject_credentials_local_files_and_process_execution | `clis/spotify/spotify.js:7`, `clis/spotify/spotify.js:103`, `clis/spotify/spotify.js:18`, `clis/spotify/spotify.js:43`, `clis/spotify/spotify.js:83` | 未执行 |

## 复用结果与待补合同

三个正向样本覆盖 GitHub HTML、DEV.to JSON、arXiv Atom/XML。上游参数处理和 parser 函数体保持原样，wrapper 将原 fetch 映射到候选 broker，并补有界完整性检查。第三个样本没有新增 WebEnvoy 站点专属 Runtime 分支，但确实需要改动 Lode 生成器：支持 arXiv 两文件静态 bundle，并加入 Atom envelope、totalResults、entry 数量及明确空集检查。因此“第三样本只需声明/schema/check/fixture”的复用目标未达到；没有记录耗时或成本，不能据此声称接入提效。

任何正式 Lode task 包都还需固定：任务绑定的 HTTPS origin/path/query/header、匿名请求策略、重定向逐跳复核、响应 MIME 与解压体积、预算/超时/取消、完整性事实和失败结果。脚本不能通过 Node `fetch` 自行访问网络；HTTP 2xx 不代表业务成功。

## 离线行为验证

`tools/test_opencli_readonly_semantics.mjs` 在静态摘要验证成功后，用 Node 内置 VM 和合成 fixture 分别运行固定上游源码及实际生成的三份候选脚本。测试禁止额外 module imports，并禁用 VM 字符串代码生成；覆盖正常值、合法空集、无证据空集、缺失字段、异常/截断正文、分页、参数错误和响应丢失。它只证明离线语义与包装行为，不代表 WebEnvoy broker、安装、真实网站、业务结果或 Plugin 验收。

候选阶段边界：本报告证明固定源码静态可分析；候选包的结构校验由 Lode 官方 validator/CI 单独执行。代码准入、正式安装、真实站点执行、业务结果独立核验均不由本报告证明。

重复检查：`python3 tools/opencli_readonly_candidates.py --check`；离线行为：`node --experimental-vm-modules tools/test_opencli_readonly_semantics.mjs`。
