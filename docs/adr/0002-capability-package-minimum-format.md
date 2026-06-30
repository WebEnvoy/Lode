# 0002 能力包最小格式

## Status

Draft

## Context

Lode 是网站能力资产真相源，不是执行这些资产的 runtime。现有 draft 已经把
站点知识、站点能力、normalizer、fixture、任务封装、版本和失效标记放在
Lode 内，同时划出边界：WebEnvoy Core 负责执行和结果封装，Harbor 提供
runtime session、身份和证据。

research 也收敛到同一方向：capability / workflow 应是带 input/output
schema、fixture 和 post-check 的版本化 package。runtime facts、admission
policy、result envelope 和 evidence storage 不应在本仓库重定义。

## Decision

把 Lode 中一个网站动作的稳定资产单元定义为 site capability package。最小包
合同采用本地文件化形式，必须标识：

- site、supported origins、capability id、operation id、capability family、
  target type、lifecycle 和 version；
- Lode 拥有的 input schema 和 normalized output schema；
- Lode 拥有的 source shape schema，以及 extractor、parser、mapper 或
  normalizer 引用；
- Lode 声明、Core 基于 Harbor runtime facts 匹配的 resource requirement
  profiles；
- Lode 声明、Core 执行的 pre-check 和 post-check；
- failure classification 词表引用、known limitations 和 invalidation marker；
- redacted raw fixtures、normalized fixtures 和 regression checks。

Core admission、Core result envelope 字段、unknown-outcome 语义、Harbor runtime
capability facts、raw payload storage、evidence storage 和 session binding 都是
外部依赖。Lode package 可以用稳定名称或引用字段依赖这些合同，但不在本仓库
重定义它们的 schema。

Task / workflow package 可以组合 site capability。它们必须消费 capability 的
input/output schema 和 normalized result，不直接消费 API、DOM、network 或
Snapshot raw shape。

### Stage 2 v0 Contract

本节是 GH-36 / GH-37 / GH-38 / GH-39 的 docs-only 合同收敛。它冻结最小可引用
字段和失败分类，不创建真实 capability package、schema、fixture、validator 或
registry 代码。

#### Package Minimum Format

| 字段或状态 | Owner | Consumer | 有效性 / 过期规则 | 失败分类 | 非目标 |
|---|---|---|---|---|---|
| package root | Lode | Core admission; App Library | 一个 package root 只能承载一个 `site-capability`；root 由 manifest 所在目录确定。移动 root 或缺 manifest 视为新包或无效包。 | `missing_manifest`; `invalid_contract` | 不定义 repo-level registry 生成方式；不支持一个 root 多能力。 |
| required manifest | Lode | Core admission; App Library | v0 必须有单一 manifest，记录 package identity、capability identity、lifecycle、version、resource requirements、schemas/checks/fixtures 的引用路径。 | `missing_manifest`; `invalid_contract` | 不规定文件名后缀以外的最终 JSON Schema；不生成 manifest。 |
| optional support files | Lode | Core validation; later validator | input/output/source schema、normalizer、fixtures、pre/post-check 可以先以引用路径出现；stable 前必须能解析并通过后续 validator。 | `invalid_contract`; `verification_failed` | 不创建真实 schema、fixture 或 normalizer。 |
| forbidden package contents | Lode | Core admission; security review | v0 包不得保存 Cookie、Token、profile state、完整请求/响应、未脱敏 DOM/HAR/screenshot、用户业务数据或真实运行现场。发现即无效。 | `invalid_contract`; `resource_requirement_changed` | 不替代 Harbor evidence storage 或 Core Run Record。 |
| package type | Lode | Core admission; App Library | v0 只冻结 `site-capability`；workflow package、domain-skill、registry index 继续沿 ADR 0004 后续决策。 | `unsupported_version`; `invalid_contract` | 不把 workflow、benchmark、crawler job 或 marketplace 作为本轮合同。 |

#### Identity, Operation, Family, Tags

| 字段或状态 | Owner | Consumer | 有效性 / 过期规则 | 失败分类 | 非目标 |
|---|---|---|---|---|---|
| `capability_id` | Lode | Core admission; App Library | package 内稳定、小写短横线、站点内唯一；重命名视为新 capability identity。 | `invalid_contract` | 不承诺跨站全局唯一。 |
| `operation_id` | Lode owns declaration; Core owns execution semantics | Core admission / routing | 表示公共可调用操作，如 `content_detail_by_url`；语义破坏需要新 version 或 deprecation path。 | `invalid_contract`; `deprecated` | 不定义 Core API surface。 |
| `capability_family` | Lode | App filtering; Core policy grouping | v0 使用小集合：`content_detail`、`content_search`、`content_list`、`comment_collection`、`creator_profile`、`media_asset_fetch`、`media_upload`、`content_publish`；不在集合内先标 experimental。 | `invalid_contract` | 不把 Syvert 全量 taxonomy 一次迁入。 |
| `operation_mode` | Lode declares; Core enforces | Core admission; App risk copy | v0 候选：`read`、`validate_only`、`draft`、`preview`、`write`。稳定写入仍受 PD-0003 阻塞。 | `invalid_contract`; `deprecated` | 不用 `readOnly` 布尔值替代风险语义。 |
| `tags` | Lode | App Library search/filter | 标签只用于展示和过滤，例如 site, target type, risk hint, source shape；不得改变 admission 结果。 | `invalid_contract` when used as policy | 不把 tag 当权限、资源或 runtime policy。 |

#### Lifecycle, Version, Deprecation, Invalidation

| 字段或状态 | Owner | Consumer | 有效性 / 过期规则 | 失败分类 | 非目标 |
|---|---|---|---|---|---|
| `lifecycle` | Lode | Core admission; App Library | v0 采用 `proposed`、`experimental`、`stable`、`deprecated`。只有 `stable` 可进入默认稳定执行路径。 | `deprecated`; `invalid_contract` | 不用一次运行成功升格 stable。 |
| `version` | Lode | Core Run Record; App install/pin | package version 必须可被 Core 运行记录和 App lock 引用；破坏 input/output/source contract 需要新 version。 | `unsupported_version`; `invalid_contract` | 不实现 install/update/rollback UI。 |
| version lock | App owns user choice; Core records use; Lode supplies version identity | App Library; Core Run Record | App 可展示 installed/pinned/latest；Core 只执行被引用的版本并记录 capability/schema/normalizer/output/fixture 版本。 | `unsupported_version`; `invalid_contract` | 不实现 hosted sync 或 marketplace lockfile。 |
| deprecation | Lode | App Library; Core admission | `deprecated` 保留历史语义但不进入新稳定任务；manifest 应提供替代版本或修复提示（如果已知）。 | `deprecated` | 不自动迁移用户任务。 |
| invalidation marker | Lode | Core admission; App repair flow | 可标记 `temporarily_invalid`、`input_contract_broken`、`output_contract_broken`、`source_shape_changed`、`source_schema_changed`、`normalizer_failed`、`mapping_incomplete`、`resource_requirement_changed`、`verification_failed`。 | listed invalidation class; `invalid_contract` | 不保存 live evidence；只保存可脱敏引用或 fixture 线索。 |

#### Consumer Fields

| Consumer | v0 可引用字段 | 不可依赖字段 |
|---|---|---|
| App Library | package type, display name/description, site/origins, capability id, operation id, family, operation mode, tags, lifecycle, version, known limitations, deprecation status, invalidation marker, resource requirement summary, schema/check/fixture presence. | runtime session, profile, provider route, Cookie/Token, live tab, raw evidence body, hosted marketplace state. |
| Core admission | package type, manifest version, capability id, operation id, family, operation mode, lifecycle, version, resource requirements, schema/check/fixture references, known limitations, invalidation/deprecation markers. | App display order, tags as policy, Harbor provider choice, raw payload storage, result envelope schema not owned by Lode. |

#### Research Absorption Record

| locator | 判断 | 机制吸收 / 裁剪 / 拒绝理由 | 落点 |
|---|---|---|---|
| `Lode/ROADMAP.md` | 吸收 | 阶段二要求 Core 可准入、可校验、可版本引用的最小能力包合同；本 ADR 只冻结 package v0，不提前做 registry、marketplace 或 runtime。 | Stage 2 v0 Contract |
| `docs/adr/pending-decisions.md` | 吸收 | 采用已接受的 capability metadata、schema/fixture/post-check、version/invalidation 归属；PD-0003/PD-0005/PD-0010 等仍保留为后续阻塞，不在本轮伪定。 | Stage 2 v0 Contract; Open Questions |
| `research/synthesis.md` | 吸收 | 吸收“版本化 package + input/output schema + fixtures/post-check”和 runtime facts 与 task policy 拆分；拒绝把 hosted platform、crawler queue、benchmark task 或 browser agent loop 当前置合同。 | Package Minimum Format; Non-goals |
| `research/absorability/README.md` | 只参考 | 该文定义 research 分层和“机制吸收 / 源码复用分开记录”的方法，不直接提供包字段。 | Research Absorption Record |
| `research/absorability/themes/site-knowledge-and-capability-assets.md` | 裁剪复用 | 裁剪吸收 OpenCLI manifest、Syvert taxonomy/lifecycle、旧 WebEnvoy XHS contract、MediaCrawler 字段组织；拒绝 `readOnly` 布尔值、直接迁入站点 adapter、把 columns 当 output schema。 | Identity/Operation/Family/Tags; Package Minimum Format |
| `research/absorability/themes/workflow-and-task-package.md` | 只参考 | workflow package、record/replay、visual builder 和 solution catalog 对后续有价值；本轮只冻结 `site-capability`，不把 workflow/block graph 放进 package minimum v0。 | Package type non-goals |

## Consequences

- normalizer 是 capability asset，站点字段映射不会变成 Core 私有逻辑。
- stable execution 可以基于包元数据 gate，而不是依赖调用方临场判断。
- Lode package 不命名 Harbor provider、profile、Cookie、Token、storage path 或
  fallback route，因此保持可移植。
- capability package 可以先从本地小目录开始；本决策不需要 registry service。

## Alternatives Considered

- 只用 Markdown instruction 表达 capability asset：不采用，因为 admission、
  validation、regression 和 result reconciliation 需要结构化合同。
- 让 Core 拥有站点私有 parsing / normalization：不采用，因为这会要求 Core
  理解每个平台 raw shape。
- 把 Harbor profile selection 和 provider routing 写进 Lode package：不采用，
  因为它们是 runtime fact 和 admission decision，不是资产定义。
- 先设计 hosted registry contract：延后，因为本地 package metadata 已足够验证
  资产边界。

## Research Evidence

- `docs/draft/capability-model.md` 把 site capability、source-specific
  normalization 和 task package 定义为 Lode asset。
- `docs/draft/site-package-format.md` 提出包含 schema、normalizer、fixture 和
  test 的 capability 目录。
- `docs/draft/task-package-format.md` 说明 task package 引用 site capability，
  不应解析 raw site source。
- `docs/draft/result-schema.md` 说明 Lode 拥有 result shape 和 normalizer，
  Core 封装 public result，Harbor 提供 evidence reference。
- <https://github.com/WebEnvoy/research/blob/main/synthesis.md> 收敛出 capability /
  workflow asset 需要 schema、fixture 和 post-check，runtime facts 必须和
  task policy 拆开。
- <https://github.com/WebEnvoy/research/blob/main/absorability/themes/site-knowledge-and-capability-assets.md>
  支持 adapter/package metadata，但否定把 read-only flag 或 raw adapter 当成
  完整 WebEnvoy 合同。
- <https://github.com/WebEnvoy/research/blob/main/absorability/themes/task-execution-and-admission.md>
  区分 Harbor runtime facts 和 Core admission rules。

## Open Questions

- [PD-0003](pending-decisions.md#pd-0003)：第一版稳定 action risk enum 尚未冻结；
  `read`、`write`、`submit`、
  `destructive` 是当前最小候选集合。
- [PD-0004](pending-decisions.md#pd-0004)：search-to-detail flow 的 follow-up
  references 需要稳定字段形态。
- [PD-0005](pending-decisions.md#pd-0005)：`source_trace`、`raw_payload_ref`、
  `evidence_ref` 需要 Core/Harbor 先拥有 schema，Lode 才能做更深层引用校验。
