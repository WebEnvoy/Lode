# 0003 Schema、Fixture 与 Post-Check

## Status

Proposed

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

- 是否每个 read capability 都需要 post-check，还是部分 read-only capability 可先用
  schema validation 加 fixture test。
- 第一版 failure classification 词表尚未冻结。
- Lode failure class 到 Core `unknown_outcome` / `requires_user_action` 的映射
  仍是 Core 决策。
- evidence type enum 应先由 Core/Harbor 拥有，Lode 再做超出引用存在性的校验。
