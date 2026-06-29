# 0002 能力包最小格式

## Status

Proposed

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
- `https://github.com/WebEnvoy/research/blob/main/synthesis.md` 收敛出 capability /
  workflow asset 需要 schema、fixture 和 post-check，runtime facts 必须和
  task policy 拆开。
- `https://github.com/WebEnvoy/research/blob/main/absorability/themes/site-knowledge-and-capability-assets.md`
  支持 adapter/package metadata，但否定把 read-only flag 或 raw adapter 当成
  完整 WebEnvoy 合同。
- `https://github.com/WebEnvoy/research/blob/main/absorability/themes/task-execution-and-admission.md`
  区分 Harbor runtime facts 和 Core admission rules。

## Open Questions

- 第一版稳定 action risk enum 尚未冻结；`read`、`write`、`submit`、
  `destructive` 是当前最小候选集合。
- search-to-detail flow 的 follow-up references 需要稳定字段形态。
- `source_trace`、`raw_payload_ref`、`evidence_ref` 需要 Core/Harbor 先拥有
  schema，Lode 才能做更深层引用校验。
