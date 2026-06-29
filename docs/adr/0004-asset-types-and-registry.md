# 0004 资产类型与 Registry

## Status

Proposed

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

- 第一版 repo-level registry file 应立即强制存在，还是从 package manifest 生成。
- `domain-skill` 后续是否需要拆成 notes、selectors、examples 和 authoring
  guidance。
- overlay / fork 在 update 和 rollback 时如何处理冲突。
- benchmark harness 存在后，benchmark task 应留在本仓库还是拆到独立 eval
  package。
