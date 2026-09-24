# OpenCLI 来源与兼容映射候选：GitHub Trending repositories

状态：**候选材料**。这不是代码准入、安装、启用、正式执行或 live 验收结论。

## 固定来源

- 上游：[`jackwener/OpenCLI`](https://github.com/jackwener/OpenCLI)，版本 `1.8.8`，commit `8271afc67e8504bda94c147f446ee29775d08274`。
- 许可证：Apache-2.0，来源文件 `third_party/opencli-1.8.8/LICENSE`，SHA-256 `0210b8b66cf00358242cb921ba2be3a46dfe0190159b1b952388a3880ce1ff54`；候选包附同一许可证全文。
- 选中命令：`github-trending repos`；注册 `columns` 仅作字段线索。
- `third_party/opencli-1.8.8/clis/github-trending/repos.js` — upstream SHA-256 `0efc684322b8a70cac358ea3cdccc24bebf105a8d09e7fb6aa6c170e1fd72a32`

## 保留与包装

- 保留 parser/业务映射：`parseTrendingHtml`；输入参数校验和 URL/query 构造保留上游逻辑。
- 入口包装只替换 OpenCLI 注册/error import，并将原始 `fetch` 名称解析到固定兼容 shim；shim 校验上游显式请求头，并只补入 Node 24 `fetch` 的固定默认 `User-Agent: node`（适用于未显式指定该头的样本）；arXiv 两个审查源以确定性文本 bundle 合并，移除静态 ESM import/export 标记，不改变工具/解析函数体。
- GitHub 源调用 `new URL()`。受管 VM 不注入 Node `URL` 或其他宿主全局，因此候选在包内提供只支持已固定 origin/path、至多一个声明路径段和声明 query key 的小型 URL 字符串接口；它不提供网络请求、DNS 或宿主运行时能力。
- 兼容 shim 限制每个 Run 一次匿名 GET，将上游 Response 使用到的 `ok/status/text()/json()` 映射到 `network.read`；禁止未声明 method/body/credentials/redirect 参数。响应只在 worker 内存使用，结果只写 normalized records 与 opaque ref。
- 不使用浏览器 snapshot/DOM、原生网络、浏览器 Cookie/登录态、代理或任何凭据。HTTP 2xx 不等于业务成功。

## 固定匿名读取策略候选

```json
{
  "transport": "program_anonymous_https",
  "origin": "https://github.com",
  "pathname": "/trending",
  "allow_one_path_segment": true,
  "query_keys": [
    "since"
  ],
  "headers": {
    "accept": "text/html",
    "user-agent": "Mozilla/5.0 (compatible; opencli/github-trending)"
  },
  "content_types": [
    "text/html"
  ],
  "max_response_bytes": 2097152,
  "max_redirects": 2,
  "timeout_ms": 10000
}
```

上游显式请求头：`{"accept": "text/html", "user-agent": "Mozilla/5.0 (compatible; opencli/github-trending)"}`。有效 broker 策略：Accept=`text/html`；User-Agent=`上游显式设置 `Mozilla/5.0 (compatible; opencli/github-trending)``。跳转最多 2 次同策略内；响应正文体积限制为 `2097152` 字节，超时 `10000` ms。该声明待 WebEnvoy #594 合同/实现接受后才可能执行。

## 输出语义与限制

- schema 显式类型化上游列出的每个公开输出字段；源字段缺失、可空、空文本和有限数值按上游表达式保留。DEV.to 非数字计数可产生 NaN，在 JSON/Schema 边界拒绝，不伪装为 `null`。
- 输出保留本次所请求的参数和分页范围；不能据单页数据声称整个站点集合完整。`available` 只在包装层给出本合同内的完整性证据时使用，无法证明时返回 `partial` / `unknown`。
- The body is an actual HTTP response, not a rendered browser snapshot. Completeness compares the parsed records with min(requested limit, complete matching Box-row blocks); a valid zero-row result requires the original parser's explicit empty-site text.
- `source_refs` 与 `evidence_refs` 指向同一 `public_http_response` opaque ref；不输出响应正文、headers、Cookie 或真实 URL。
- `unknown` 按原 Run 查询/对账，不生成新 key 重放。导入和候选生成本身不信任、安装或启用资产。
- 上游 adapter 对零条记录会抛 `EmptyResultError`；候选 wrapper 只在可复核信号明确时归一为 `available` 且 `records: []`：GitHub 需 explicit-empty 文案及零个完整 Box-row，DEV.to 需正文严格解析为 JSON 数组 `[]`，arXiv 需完整 Atom feed、`totalResults=0` 且零 entry。没有这些信号的空结果继续失败；截断/缺字段不归为合法空集合。
- GitHub `limit` 是上限；完整页少于 limit 时，只有 `min(limit, matched Box-row count)` 个 parsed row 与完整正文一致才判 available。

## 离线验证入口

- 静态核验：`python3 tools/opencli_readonly_candidates.py --check`
- 同一组离线 HTML/JSON/Atom fixture 调用固定 OpenCLI 源码：`node --experimental-vm-modules tools/test_opencli_readonly_semantics.mjs`
- 固定测试材料列于 `tools/fixtures/opencli-readonly/`；测试不连接网站。
- 候选包 schema/check 由包级测试校验；正式网络 broker、代码准入、安装、现场执行和业务结果仍未验收。
