# Pending Decisions

本文件是 Lode ADR 的唯一待决策索引。ADR 正文中的 `Open Questions` 必须链接到
这里的 ID。

## PD-0001

- ID: `PD-0001`
- 问题: 已接受 ADR 是否需要进入后续生成的 reference docs。
- 来源 ADR: [0001](0001-record-architecture-decisions.md)
- 阻塞什么: 不阻塞 0001 的 ADR 流程约定；阻塞后续文档发布策略。
- 当前状态: pending
- 后续归属/下一步: docs/reference 文档生成方案确定时处理。

## PD-0002

- ID: `PD-0002`
- 问题: schema-breaking change 是否需要单独的 migration note 模板。
- 来源 ADR: [0001](0001-record-architecture-decisions.md)
- 阻塞什么: 不阻塞 0001 的 ADR 流程约定；阻塞 schema 迁移记录格式。
- 当前状态: pending
- 后续归属/下一步: 第一条 schema-breaking change 出现前补决策。

## PD-0003

- ID: `PD-0003`
- 问题: 第一版稳定 action risk enum 是否采用 `read`、`write`、`submit`、`destructive`。
- 来源 ADR: [0002](0002-capability-package-minimum-format.md)
- 阻塞什么: 不阻塞 0002 的能力包边界；阻塞 stable write capability 的具体枚举校验。
- 当前状态: pending
- 后续归属/下一步: Core admission / App confirmation 决策中定稿。

## PD-0004

- ID: `PD-0004`
- 问题: search-to-detail flow 的 follow-up references 字段形态。
- 来源 ADR: [0002](0002-capability-package-minimum-format.md)
- 阻塞什么: 不阻塞 0002 的最小包边界；阻塞 search/detail 类能力 schema 定稿。
- 当前状态: pending
- 后续归属/下一步: 第一批 search/detail capability schema 设计时定稿。

## PD-0005

- ID: `PD-0005`
- 问题: `source_trace`、`raw_payload_ref`、`evidence_ref` 的 Core/Harbor schema。
- 来源 ADR: [0002](0002-capability-package-minimum-format.md)
- 阻塞什么: 不阻塞 0002 的依赖边界；阻塞 Lode 对这些引用做深层校验。
- 当前状态: pending-external-contract
- 后续归属/下一步: Core result envelope 与 Harbor evidence contract 定稿后回填 Lode 校验。

## PD-0006

- ID: `PD-0006`
- 问题: 是否每个 read capability 都需要 post-check。
- 来源 ADR: [0003](0003-schema-fixtures-and-post-check.md)
- 阻塞什么: 不阻塞 0003 的 fixture/post-check 归属；阻塞 read-only stable gate 的细化规则。
- 当前状态: pending
- 后续归属/下一步: 第一批 read capability 进入 stable 前决定。

## PD-0007

- ID: `PD-0007`
- 问题: 第一版 failure classification 词表。
- 来源 ADR: [0003](0003-schema-fixtures-and-post-check.md)
- 阻塞什么: 不阻塞 0003 的 Lode 归属边界；阻塞 package validator 的枚举校验。
- 当前状态: pending
- 后续归属/下一步: validator/schema 第一版中定稿。

## PD-0008

- ID: `PD-0008`
- 问题: Lode failure class 到 Core `unknown_outcome` / `requires_user_action` 的映射。
- 来源 ADR: [0003](0003-schema-fixtures-and-post-check.md)
- 阻塞什么: 不阻塞 0003 的 failure class 声明；阻塞 Core result mapping 兼容性校验。
- 当前状态: pending-external-contract
- 后续归属/下一步: Core result envelope 决策中定稿。

## PD-0009

- ID: `PD-0009`
- 问题: evidence type enum 的 Core/Harbor 所有权与 Lode 校验边界。
- 来源 ADR: [0003](0003-schema-fixtures-and-post-check.md)
- 阻塞什么: 不阻塞 0003 的 evidence reference 依赖；阻塞 Lode 对 evidence type 的枚举校验。
- 当前状态: pending-external-contract
- 后续归属/下一步: Harbor evidence contract 定稿后决定 Lode 引用校验范围。

## PD-0010

- ID: `PD-0010`
- 问题: 第一版 repo-level registry file 是强制存在，还是从 package manifest 生成。
- 来源 ADR: [0004](0004-asset-types-and-registry.md)
- 阻塞什么: 不阻塞 0004 的资产分型；阻塞 registry 文件落地方式。
- 当前状态: pending
- 后续归属/下一步: 第一个 package validator / registry tool 实现前决定。

## PD-0011

- ID: `PD-0011`
- 问题: `domain-skill` 是否拆成 notes、selectors、examples 和 authoring guidance。
- 来源 ADR: [0004](0004-asset-types-and-registry.md)
- 阻塞什么: 不阻塞 0004 的 typed supporting asset 决策；阻塞 domain-skill 子结构。
- 当前状态: pending
- 后续归属/下一步: 第一个 domain-skill package 草案中决定。

## PD-0012

- ID: `PD-0012`
- 问题: overlay / fork 在 update 和 rollback 时如何处理冲突。
- 来源 ADR: [0004](0004-asset-types-and-registry.md)
- 阻塞什么: 不阻塞 0004 的 platform/personal asset 分层；阻塞 overlay/fork 管理规则。
- 当前状态: pending
- 后续归属/下一步: App Library 或 asset versioning 规则设计时决定。

## PD-0013

- ID: `PD-0013`
- 问题: benchmark harness 存在后，benchmark task 留在本仓库还是拆到独立 eval package。
- 来源 ADR: [0004](0004-asset-types-and-registry.md)
- 阻塞什么: 不阻塞 0004 对 benchmark-task 的 deferred 分型；阻塞 benchmark 资产归属。
- 当前状态: deferred
- 后续归属/下一步: benchmark harness 立项时再做 ADR。
