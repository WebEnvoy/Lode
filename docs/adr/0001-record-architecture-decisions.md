# 0001 记录架构决策

## Status

Draft

## Context

Lode 已经在 `docs/draft/` 下保存规划草稿，但仓库还没有稳定位置记录
比完整 spec 更轻、又比草稿更持久的架构决策。

当前 capability package 工作需要一个精简 ADR 约定，后续 schema、包格式和
registry 变更可以引用决策记录，而不是重复背景说明。

## Decision

架构决策记录在 `docs/adr/`，使用递增编号 Markdown 文件：

```text
docs/adr/0001-record-architecture-decisions.md
docs/adr/0002-capability-package-minimum-format.md
```

每个 ADR 使用以下最小章节：

- `Status`
- `Context`
- `Decision`
- `Consequences`
- `Alternatives Considered`
- `Research Evidence`
- `Open Questions`

ADR 编号只追加。后续 ADR 可以 supersede 旧 ADR，不直接改写历史决策。

## Consequences

- 决策可以保持简短，并回链到 draft 或 research。
- 草稿文档可以继续演进，不需要假装每条说明都已定稿。
- 推翻或替换决策需要新 ADR，设计漂移会更容易被看见。

## Alternatives Considered

- 只把决策留在 `docs/draft/`：不采用，因为 draft 已明确不是稳定 spec 或实现承诺。
- 引入更重的 RFC 模板：暂不采用，因为当前需要的是轻量记录，不是评审流程框架。

## Research Evidence

- `docs/draft/README.md` 说明当前 draft 只是规划候选，不代表最终 spec。
- `AGENTS.md` 说明正式执行依赖应落到结构化 Schema，Markdown 主要用于说明。

## Open Questions

- [PD-0001](pending-decisions.md#pd-0001)：已接受 ADR 是否需要进入后续生成的
  reference docs。
- [PD-0002](pending-decisions.md#pd-0002)：schema-breaking change 是否需要单独的
  migration note 模板。
