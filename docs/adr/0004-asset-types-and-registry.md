# 0004 资产类型与 Registry

## Status

Draft

## Context

Lode 需要描述多类可复用资产。research 明确反对把 site capability、workflow、
benchmark task、crawler job 和 agent plugin 混成一种 package type。现有 draft
也已经区分 site knowledge、site capability、atomic action、task package、
platform asset、personal overlay、fork、draft、version 和 invalidation marker。

当前决策只保留本地、包级 registry。hosted marketplace、sync service 或 runtime
registry 不在本 ADR 范围内。

## Decision

Lode 使用 typed assets。最小 registry surface 是 local manifest 或 repo-level
index，记录 asset id、type、path、lifecycle、version 和 package ownership。它
不执行 asset，也不选择 runtime。

资产类型决策：

| Asset | Decision |
|---|---|
| `site-capability` | 一等 Lode asset。拥有站点动作 metadata、schema、normalizer、fixture、check、version 和 invalidation marker。 |
| `workflow-package` | 一等 Lode asset。把 site capability 组合成可复用任务，并拥有 workflow input、step 和 verification requirement。 |
| `domain-skill` | typed supporting asset。保存 site knowledge 或 agent-readable guidance，但本身不是 stable executable capability。 |
| `site-adapter` | site capability 内的 typed implementation component；只有被多个 capability 复用时才需要独立索引。它不是单独的产品 task contract。 |
| `benchmark-task` | deferred separate asset type。未来可用于 evaluation 索引，但不能当用户 workflow contract。 |
| `crawler-job` | deferred separate asset type。长时间 crawl 行为未来可转成 workflow profile，但 Lode 不拥有 queue、storage、proxy 或 scaling runtime。 |

platform asset 和 personal asset 共用同一 type vocabulary。公共 platform asset
作为 baseline；用户 overlay、fork 和 draft 可以覆盖或扩展它们，但不原地改写
platform asset body。

registry 只记录本地 discoverability 和 version identity。Core Run Record 或
result envelope 应在相关合同存在时引用 capability version、source schema
version、normalizer version、output schema version，以及 fixture / regression
version。

### Stage 2 v0 Contract: Asset / Workflow Reference Boundary

本节是 GH-40 / GH-41 / GH-42 的 docs-only 合同收敛。它只冻结资产分型、引用边界
和失败映射，不创建真实 package、registry、schema、fixture、validator 或 runtime
代码。

#### Taxonomy Boundary

| 字段或状态 | Owner | Consumer | 有效性 / 过期规则 | 失败分类 | 非目标 |
|---|---|---|---|---|---|
| `site-capability` | Lode | Core admission; App Library; workflow package | 进入 Lode package 语义。必须有 package identity、site/origin、operation、version、schema/check/fixture 引用和 resource requirement 声明；破坏 input/output/source contract 需要新 version 或失效标记。 | `invalid_contract`; `unsupported_version`; `deprecated`; `asset_missing` | 不保存 runtime secret/profile/live data；不选择 Harbor provider。 |
| `workflow-package` | Lode owns static workflow asset; Core owns execution and run record | Core workflow admission; App Library | 进入 Lode package 语义，但 v0 只定义引用边界。workflow 只能引用 versioned `site-capability` 和其 normalized output，不直接消费 API、DOM、network、Snapshot raw shape。 | `invalid_contract`; `unsupported_asset_kind`; `dependency_unavailable` | 不实现 workflow runner、record/replay、visual builder、schedule、queue 或 marketplace。 |
| `domain-skill` | Lode | capability authoring; App Explorer / Library | 作为 supporting asset 进入 Lode 语义。可保存 notes、selectors、examples、authoring guidance 等站点经验；必须标明适用 site/origin、版本和过期条件。 | `unsupported_asset_kind`; `asset_missing`; `invalid_contract` | 不作为 Core stable executable capability；不替代 schema、fixture、post-check。 |
| `site-adapter` | Lode package internals | capability package; later validator | 默认是 capability 内部 implementation component。只有被多个 package 复用并有独立 version/owner 时才可进入 local registry index。 | `asset_missing`; `invalid_contract`; `dependency_unavailable` | 不作为用户 task contract；不拥有 runtime/provider/profile 选择权。 |
| `benchmark-task` | future eval owner | future eval tooling | deferred。只保留评测语义参考，不进入 Stage 2 Lode package 语义。 | `unsupported_asset_kind` | 不用 benchmark episode 代表用户 workflow 或 product success。 |
| `crawler-job` | future workflow/crawler owner | future long-running read flow | deferred。长任务可未来映射为 workflow profile 或 resume token，但 Stage 2 不定义 queue/storage/proxy/scaling。 | `unsupported_asset_kind`; `dependency_unavailable` | 不把 crawler runtime、账号池、代理池、存储或调度放入 Lode。 |
| hosted registry / marketplace | future App/Lode service owner | future install/update flow | deferred。v0 只允许本地 manifest、包内引用或 repo-level index 草案。 | `registry_unavailable` | 不承诺 hosted sync、公共市场、团队同步或贡献审核流。 |

#### Asset Locator And Dependency Boundary

| 字段或状态 | Owner | Consumer | 有效性 / 过期规则 | 失败分类 | 非目标 |
|---|---|---|---|---|---|
| package-internal locator | Lode package | package validator; Core admission | 相对 package root，必须指向同一 package 内的 schema、normalizer、fixture、check、domain-skill 或 adapter 文件；移动或删除后必须更新 manifest/version。 | `asset_missing`; `invalid_contract` | 不允许绝对本地路径、用户 home 路径或临时目录。 |
| package-external locator | Lode package declares; dependency owner owns target | Core admission; App install/lock | 只能引用 versioned package、versioned local registry entry 或 documented external contract。必须有 dependency id、version/range、owner、freshness rule 和 failure mapping。 | `dependency_unavailable`; `unsupported_version`; `registry_unavailable` | 不引用 live tab、profile、Cookie、Token、storage handle、provider route 或生产 payload。 |
| version lock | Lode supplies asset versions; App/User chooses install/pin; Core records use | App Library; Core Run Record | capability、workflow、domain-skill、adapter、source schema、output schema、normalizer、fixture 和 post-check 都必须可被版本引用；破坏性变化需要新 version、deprecation 或 invalidation marker。 | `unsupported_version`; `deprecated`; `invalid_contract` | 不实现 lockfile、update UI、rollback UI 或 hosted sync。 |
| freshness rule | Lode | Core admission; App repair flow | 每个 package-external dependency 和 source-shape-sensitive locator 必须写清何时 stale：version drift、source shape changed、normalizer failed、fixture failed、resource requirement changed、registry unavailable。 | `source_shape_changed`; `normalizer_failed`; `verification_failed`; `registry_unavailable` | 不用实时站点探测替代 package freshness。 |
| invalidation marker | Lode | Core admission; App repair flow | 失效只标记资产或引用，不保存 live evidence。允许指向脱敏 fixture、review note 或 Core/Harbor evidence ref。 | `temporarily_invalid`; `input_contract_broken`; `output_contract_broken`; `source_schema_changed`; `mapping_incomplete` | 不把完整请求/响应、未脱敏 DOM/HAR/screenshot 或账号态写入 Lode。 |
| secret / profile / live data boundary | Harbor/Core own runtime facts; Lode owns only abstract requirements | Core admission; security review | Lode package 可声明 `resource_requirement_profiles` 和 evidence ref policy；不得保存 Cookie、Token、session storage、profile state、localStorage、live tab id、provider secret、真实账号或用户业务数据。 | `invalid_contract`; `resource_requirement_changed` | 不替代 Harbor evidence store、Core Run Record 或 runtime session binding。 |

#### Consumer Fields

| Consumer | v0 可引用字段 | 不可依赖字段 |
|---|---|---|
| Core admission | package type, asset id, package root, version, lifecycle, dependencies, resource requirements, schema/check/fixture locators, invalidation marker, failure class mapping. | App display order, runtime profile/session/provider choice, Cookie/Token, live data, raw evidence body, hosted marketplace state. |
| Core workflow execution | workflow package id/version, step capability refs, normalized output refs, dependency lock, verification requirement refs. | Source payload body, DOM/network/Snapshot raw shape, browser automation internals, visual builder graph UI state. |
| App Library | package type, display metadata, site/origin, lifecycle, version, dependency summary, freshness/invalidation summary, limitations. | runtime secrets, profile status, live tabs, raw evidence body, user business inputs. |

#### Research Absorption Record

| locator | 判断 | 机制吸收 / 裁剪 / 拒绝理由 | 落点 |
|---|---|---|---|
| `Lode/ROADMAP.md` | 吸收 | 吸收阶段二“Core 可准入、可校验、可版本引用”的本地包优先原则；裁剪掉阶段五以后 registry、marketplace、sync 和团队贡献流。 | Taxonomy Boundary; Asset Locator And Dependency Boundary |
| `docs/adr/pending-decisions.md` | 吸收 | 吸收已接受的 typed asset、registry local、version/invalidation、platform/personal asset 边界；保留 PD-0010/PD-0011/PD-0012/PD-0013 为后续决策，不在本轮定实现形态。 | Taxonomy Boundary; Open Questions |
| `research/synthesis.md` | 吸收 | 吸收 capability/workflow schema 化、runtime facts 与 task policy 拆分、Run Record/evidence 不归 Lode 重定义；拒绝把 hosted platform、crawler queue、benchmark task 或 browser agent loop 当前置合同。 | Taxonomy Boundary; Asset Locator And Dependency Boundary |
| `research/absorability/README.md` | 只参考 | 该文提供“机制吸收与源码复用分开记录”的方法，不提供字段合同。 | Research Absorption Record |
| `research/absorability/themes/site-knowledge-and-capability-assets.md` | 裁剪复用 | 吸收 OpenCLI manifest、Syvert taxonomy/lifecycle、旧 WebEnvoy capability、MediaCrawler 字段组织；裁剪为 Lode asset taxonomy；拒绝 `readOnly` 布尔、raw adapter、columns、站点私有 API/header/token 逻辑作为稳定合同。 | Taxonomy Boundary |
| `research/absorability/themes/workflow-and-task-package.md` | 裁剪复用 | 吸收 workflow input_schema、steps、verification_checks、expected_outcome、record/replay 参考；裁剪为 workflow 引用边界；拒绝 AGPL workflow-use/Skyvern/Automa/EasySpider 源码、全量 block graph、visual builder、solution catalog 进入 Stage 2。 | Taxonomy Boundary; Consumer Fields |

## Consequences

- capability package 和 workflow package 可以独立演进。
- domain note 和 adapter 不会伪装成 stable executable contract。
- benchmark / crawler 关注点保持可见，但不会现在就把 queue、storage、eval
  harness 或 scaling design 拉进 Lode。
- local package validation 可以早于任何 registry service 落地。

## Alternatives Considered

- 所有内容共用一个泛化 `package` type：不采用，因为它会隐藏 runtime、
  evaluation、workflow 和 capability 边界。
- 把每个 supporting file 都做成 first-class registry asset：不采用，因为这会在
  package validation 前过度索引 selector、note、fixture 和实现细节。
- 现在设计 hosted registry service：不采用，因为当前需要的是本地 asset
  identity，不是网络分发。
- 立即把 crawler job 当 workflow：延后，因为 crawler queue、proxy pool、
  resume storage 和 scaling 都是 runtime concern。

## Research Evidence

- `README.md` 区分 Lode asset、Core execution 和 Harbor runtime。
- `docs/draft/asset-sources.md` 定义 platform asset 与用户 overlay/fork/draft，
  并避免直接改写官方资产。
- `docs/draft/asset-versioning.md` 要求 capability、source schema、normalizer、
  output schema、fixture、task、overlay、fork 和 draft 具备版本引用。
- <https://github.com/WebEnvoy/research/blob/main/synthesis.md> 说明 site capability、
  workflow、benchmark task、crawler job 和 agent plugin 不应混成一种 asset。
- <https://github.com/WebEnvoy/research/blob/main/absorability/themes/site-knowledge-and-capability-assets.md>
  区分 domain skill、adapter、package metadata、private override 和 capability
  taxonomy。
- <https://github.com/WebEnvoy/research/blob/main/absorability/themes/workflow-and-task-package.md>
  说明 workflow package 是不同于 atomic site capability 的问题域。
- <https://github.com/WebEnvoy/research/blob/main/absorability/themes/task-execution-and-admission.md>
  否定把 benchmark loop 和 crawler runtime 当成产品 admission contract。

## Open Questions

- [PD-0010](pending-decisions.md#pd-0010)：第一版 repo-level registry file 应立即
  强制存在，还是从 package manifest 生成。
- [PD-0011](pending-decisions.md#pd-0011)：`domain-skill` 后续是否需要拆成 notes、
  selectors、examples 和 authoring guidance。
- [PD-0012](pending-decisions.md#pd-0012)：overlay / fork 在 update 和 rollback
  时如何处理冲突。
- [PD-0013](pending-decisions.md#pd-0013)：benchmark harness 存在后，benchmark
  task 应留在本仓库还是拆到独立 eval package。
