# 0003 Schema、Fixture 与 Post-Check

## Status

Accepted for Stage 2 docs-only contract, 2026-06-30.

## Context

draft 已要求 stable capability 具备 input/output contract、resource
requirements、pre-check、post-check、failure classification、fixture、test、
version 和 invalidation marker。research 也明确反对把一次跑通、展示列、
CSV 输出或 LLM 生成 workflow 当成稳定合同。

因此 Lode 必须拥有足够的 schema 与回归材料，让 capability 可测试；runtime
execution 和 result envelope 仍留给 Core / Harbor。

## Decision

Lode 拥有以下 package-level asset：

- capability 和 workflow 参数的 input schema；
- capability data 的 normalized output schema；
- 支持的 raw source 对应 source shape schema；
- redacted raw fixtures 及匹配的 normalized fixtures；
- normalizer tests 或等价 regression checks；
- 声明式 pre-check 和 post-check requirements；
- capability-level failure classes 和 known limitations。

site capability 不能标记为 `stable`，除非这些资产存在。唯一例外是能力明确声明
`dependency_mode=none`，并且仍提供适合该操作的 fixture、post-check 和 evidence
policy reference。

post-check 是 Lode asset 的一部分，因为它定义该 capability 的成功条件。Core
决定何时以及如何执行 post-check、记录结果，并把失败映射进 Core result
envelope。Harbor 通过引用提供 screenshot、Snapshot、network summary、raw
payload reference 和其他 runtime evidence。

对 write-like capability，post-check 必须显式声明。浏览器步骤完成不等于业务
成功。

### Stage 2 v0 Contract: Input, Output, And Source Shape

本节是 GH-43 / GH-44 / GH-45 / GH-46 的 docs-only 合同收敛。它只定义文档级
shape、边界和失败映射，不创建真实 JSON Schema、validator、fixture、registry
或 runtime 代码。

#### Input Schema Shape

v0 input schema 只描述能力包可声明的字段类别和示例，不冻结 JSON Schema 文件名
或 validator 行为。

| 字段或状态 | Owner | Consumer | 有效性 / 过期规则 | 失败分类 | 非目标 |
|---|---|---|---|---|---|
| `schema_id` / `schema_version` | Lode | Core input validation; App form/rendering | package 内稳定；破坏字段、required/default 或敏感性声明时需要新 version。 | `input_invalid`; `unsupported_version` | 不定义真实 schema registry。 |
| `fields[]` | Lode | Core input validation; App form/rendering | 每个字段声明 `name`、`type`、`required`、`default`、`description`、`sensitivity`、`constraints`、`example`；缺少 required 输入或类型不符映射为 input failure。 | `input_invalid`; `invalid_contract` | 不收集真实用户业务参数样本。 |
| `sensitivity` | Lode declares; Core/App enforce handling | App consent/copy; Core redaction | v0 候选：`public`、`user_provided`、`sensitive`、`secret_ref`。`secret_ref` 只能引用外部 secret handle，不 inline secret。 | `input_invalid`; `requires_user_action`; `invalid_contract` | 不保存 Cookie、Token、password、profile state 或 live secret。 |
| `resource_requirement_refs` | Lode | Core admission | 输入 schema 可以引用 resource requirement profile，但不选择具体 Harbor profile/provider。 | `resource_unavailable`; `invalid_contract` | 不把 provider_key、profile_id、proxy、local path 写进 input schema。 |
| `examples[]` | Lode | App docs; package review | 示例必须脱敏、可复现、非真实客户数据；示例过期不等于 capability failure，但 stable 前必须有可解释替代。 | `invalid_contract` for sensitive example leakage | 不把示例当 fixture 或 runtime evidence。 |

文档级示例：

```yaml
schema_id: content-detail-input
schema_version: 0.1.0
fields:
  - name: url
    type: url
    required: true
    sensitivity: public
    constraints:
      allowed_origins: ["https://www.example.com"]
    example: "https://www.example.com/items/123"
  - name: requested_fields
    type: string_list
    required: false
    default: ["title", "creator_ref", "published_at"]
    sensitivity: user_provided
```

#### Normalized Output Schema And Result Classification

Lode owns the normalized `data` shape. Core owns the result envelope around it.
The v0 alignment target is:

```yaml
core_result_envelope:
  ok: true
  outcome: success
  data: "<Lode normalized output>"
  source_refs: []
  evidence_refs: []
  failure: null
```

| 字段或状态 | Owner | Consumer | 有效性 / 过期规则 | 失败分类 | 非目标 |
|---|---|---|---|---|---|
| `output_schema_id` / `output_schema_version` | Lode | Core output validation; App rendering | package 内稳定；破坏 public data shape 需要新 version 或 deprecation. | `output_invalid`; `unsupported_version` | 不定义 Core envelope schema。 |
| `result_kind` | Lode | Core result projection; App display | v0 候选：`content_detail`、`collection`、`comment_collection`、`creator_profile`、`media_asset`、`write_result`、`workflow_result`。 | `invalid_contract`; `output_invalid` | 不把 CSV/table/display columns 当 schema。 |
| `classification` | Lode declares data class; Core declares run outcome | Core/App | v0 normalized result class：`success_result`、`partial_result`、`empty_result`、`not_normalizable`。Core maps these into envelope outcome. | `empty_result`; `normalization_failed`; `output_invalid` | 不用 browser step status 代表业务成功。 |
| `normalized` | Lode | Core validation; App display | JSON-safe public payload；不得包含 raw source body、Cookie、Token、provider route、本地路径、storage URL、用户业务私密字段。 | `output_invalid`; `invalid_contract` | 不保存长期 dataset 或业务数据库记录。 |
| `dedup_key` / `canonical_ref` | Lode | Core reconciliation; App display | 对 collection/comment/dataset-like result 应稳定可重复；生成规则变化需要 output schema version bump。 | `normalization_failed`; `output_invalid` | 不要求所有 detail result 都有全局唯一 ID。 |
| `source_refs[]` / `evidence_refs[]` | Lode declares reference policy; Core/Harbor own referenced records | Core/App evidence display | 输出可携带引用，但不 inline heavy evidence。缺引用本身不必使 `data` invalid，除非 post-check 或 schema 声明 required。 | `source_unavailable`; `verification_failed`; `output_invalid` | 不重定义 Core/Harbor ref schema；只声明 Lode 依赖边界。 |

#### Source Payload / Source Ref Shape

| 字段或状态 | Owner | Consumer | 有效性 / 过期规则 | 失败分类 | 非目标 |
|---|---|---|---|---|---|
| `source_shape_id` / `source_shape_version` | Lode | normalizer; fixture review; Core validation hook | 每个 source shape 绑定 source kind、schema version 和 normalizer version；source shape 变化需要 invalidation 或 version bump。 | `source_schema_changed`; `source_shape_changed`; `source_unavailable` | 不保存 live raw payload schema from production without redaction. |
| `source_payload` | Harbor/Core runtime owns live payload; Lode owns redacted fixture shape | normalizer; package tests | Lode 只可保存 redacted fixture payload 或 minimal fixture sample；runtime payload must stay by ref. | `invalid_contract` if inline sensitive live data | 不保存完整生产请求/响应、未脱敏 DOM/HAR/screenshot。 |
| `source_ref` | Core/Harbor owns record; Lode declares required reference fields | Core/App evidence display; post-check | v0 文档级字段：`ref_id`、`source_kind`、`producer`、`captured_at`、`redaction`、`retention`、`schema_hint`、`integrity_hint`。Lode 只能校验引用存在性和 declared kind until Core/Harbor contract stabilizes. | `source_unavailable`; `evidence_unavailable`; `invalid_contract` | 不把 local file path、storage URL 或 profile route 暴露给 capability output。 |
| `source_trace` | Lode declares trace shape; Core fills runtime provenance | Core run record; App diagnostics | 可说明 source kind、normalizer id/version、field mapping summary 和 source_refs used；不得泄漏 provider route、账号池、代理池或 secret。 | `normalization_failed`; `mapping_incomplete`; `output_invalid` | 不替代 Core Run Record。 |

文档级 source ref 示例：

```yaml
source_ref:
  ref_id: "run-source-1"
  source_kind: "network_response_summary"
  producer: "harbor"
  captured_at: "2026-06-30T00:00:00Z"
  redaction: "summary_only"
  retention: "core_run_record"
  schema_hint: "content-detail-web-api-source@0.1.0"
  integrity_hint: "sha256:<redacted-fixture-or-summary-hash>"
```

#### Failure Mapping To Core / App

| Lode failure class | Trigger | Core mapping expectation | App mapping expectation | Notes |
|---|---|---|---|---|
| `input_invalid` | Missing required input, type mismatch, origin not allowed, sensitivity violation. | envelope `ok=false`, outcome `failed`, category `user_or_contract_input`. | Show user-fixable input message when safe. | Does not start runtime execution. |
| `resource_unavailable` | Resource requirement not matched by Harbor facts. | envelope `ok=false`, outcome `blocked`, category `resource_unavailable`. | Ask for profile/login/runtime setup when appropriate. | Lode only declares requirement. |
| `source_unavailable` | Declared source ref missing, unavailable, expired, or inaccessible. | envelope `ok=false` or `partial`, category `source_unavailable`. | Show retry/repair or missing evidence. | Core/Harbor own actual ref lookup. |
| `output_invalid` | Normalized data fails declared output shape. | envelope `ok=false`, outcome `failed`, category `contract_violation`. | Mark package needs repair. | Usually package/normalizer bug. |
| `normalization_failed` | Parser/mapper/normalizer cannot produce public data from available source. | envelope `ok=false` or `partial`, category `normalization_failed`. | Show package repair or source changed. | Includes parse failure and mapping errors. |
| `mapping_incomplete` | Required public field cannot be mapped but source exists. | envelope `ok=true` with `partial_result` or `ok=false`, based on requiredness. | Display partial-result warning. | Requiredness belongs to Lode schema. |
| `empty_result` | Valid execution returns no items/content. | envelope `ok=true`, outcome `empty`. | Show empty state, not error. | Not a contract failure. |
| `evidence_unavailable` | Evidence ref required by policy/post-check is missing. | envelope `ok=false` or `unknown_outcome`, based on Core policy. | Show unverifiable result. | Core/Harbor own evidence store. |
| `requires_user_action` | User must login, confirm, solve challenge, or provide missing safe input. | envelope outcome `requires_user_action`. | Prompt user at App boundary. | Lode only declares possible requirement. |

#### Research Absorption Record

| locator | 判断 | 机制吸收 / 裁剪 / 拒绝理由 | 落点 |
|---|---|---|---|
| `Lode/ROADMAP.md` | 吸收 | 吸收阶段二 input/output/source schema 和 resource requirement v0；裁剪掉真实 runtime、完整站点字段全集和写侧完整合同。 | Input Schema Shape; Normalized Output Schema |
| `docs/adr/pending-decisions.md` | 吸收 | 吸收 Lode 拥有 input/output/source schema、fixture/post-check 和 failure class 声明；保留 PD-0005/PD-0007/PD-0008/PD-0009 为 Core/Harbor 外部合同或 validator 后续决策。 | Failure Mapping; Open Questions |
| `research/synthesis.md` | 吸收 | 吸收 schema 化 capability/workflow、Run Record/evidence 统一归 Core/Harbor/App、runtime facts 与 task policy 拆分；拒绝把 raw payload storage 或 agent loop 写进 Lode schema。 | Source Payload / Source Ref Shape |
| `research/absorability/README.md` | 只参考 | 只采用其吸收记录方法，不从该文提取字段。 | Research Absorption Record |
| `research/absorability/themes/result-normalization-and-reconciliation.md` | 裁剪复用 | 吸收低噪音 result、typed error/hint、schema-first extraction、heavy evidence by reference、平台字段 mapping；裁剪为 Lode normalized data + Core envelope 分工；拒绝 adapter 自定义 JSON、OpenCLI columns、Stagehand 临时 schema、Automa table、EasySpider output file 作为稳定 schema。 | Normalized Output Schema; Failure Mapping |
| `research/absorability/themes/task-execution-and-admission.md` | 裁剪复用 | 吸收 resource matching、post-check、unknown outcome、requires user action、write fail-closed 语义；裁剪为 Lode failure mapping；拒绝 BrowserUse agent loop、workflow-use/Skyvern 执行器、旧 XHS gate 全量字段进入本 ADR。 | Failure Mapping To Core / App |

## Consequences

- stable capability 可以在不依赖真实账号或生产 payload 的情况下回放和回归测试。
- Lode 可以在不启动 live browser 的情况下校验 package 质量。
- Core 可以区分 invalid contract、runtime resource failure 和 unknown outcome。
- 站点 source shape 变化时，fixture 维护成为必要工作。

## Alternatives Considered

- 只要求 schema，不要求 fixture：不采用，因为 schema 无法证明 source-specific
  normalizer 仍可工作。
- 让 Core 从 run status 推断 post-check：不采用，因为浏览器动作完成时业务结果
  仍可能 unknown。
- 在 Lode fixture 内 inline raw payload 或 evidence：不采用，因为 Lode 只能保存
  已脱敏、可复现样例。
- 对所有 draft asset 都要求同样重的 fixture 集：不采用，因为 `proposed` 和
  `experimental` 需要在 stable gate 前存在。

## Research Evidence

- `docs/draft/capability-lifecycle.md` 列出 stable capability 的要求：schema、
  normalizer、resource requirement、pre/post check、failure classification、
  fixture、test、version 和 invalidation marker。
- `docs/draft/resource-requirements.md` 定义 Lode resource declaration，以及
  Core 基于 Harbor facts 做 one-of matching。
- `docs/draft/result-schema.md` 把 output schema、source schema、normalizer、
  fixture 和 test 归属给 Lode，把 public result wrapping 留给 Core。
- <https://github.com/WebEnvoy/research/blob/main/absorability/themes/result-normalization-and-reconciliation.md>
  否定把 adapter-specific JSON、display columns 和文件格式当稳定 result schema。
- <https://github.com/WebEnvoy/research/blob/main/absorability/themes/workflow-and-task-package.md>
  支持 workflow input schema、verification checks 和 expected outcome。
- <https://github.com/WebEnvoy/research/blob/main/absorability/themes/task-execution-and-admission.md>
  说明 deterministic step completion 需要 post-check 和 unknown-outcome handling。

## Open Questions

- [PD-0006](pending-decisions.md#pd-0006)：是否每个 read capability 都需要
  post-check，还是部分 read-only capability 可先用 schema validation 加 fixture
  test。
- [PD-0007](pending-decisions.md#pd-0007)：第一版 failure classification 词表尚未冻结。
- [PD-0008](pending-decisions.md#pd-0008)：Lode failure class 到 Core
  `unknown_outcome` / `requires_user_action` 的映射仍是 Core 决策。
- [PD-0009](pending-decisions.md#pd-0009)：evidence type enum 应先由 Core/Harbor
  拥有，Lode 再做超出引用存在性的校验。
