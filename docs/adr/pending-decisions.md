# Pending Decisions

本文件是 Lode ADR 的唯一待决策索引。ADR 正文中的 `Open Questions` 必须链接到
这里的 ID。

## 第一阶段边界决策

本节是 #6、#7、#8、#9、#10、#11 的第一阶段仓库内事实载体；不新增包格式、
validator 或 registry 实现承诺。依据读取时间为 2026-06-30，来源包括 GitHub
issues #6/#7/#8/#9/#10/#11、`README.md`、`ROADMAP.md`、ADR 0002/0003/0004、
`WebEnvoy/.github/ROADMAP.md` 和 research synthesis / absorability themes。

| 对象/事实 | 本仓归属 | 非本仓归属 | 消费方 | 依据 | 状态 |
|---|---|---|---|---|---|
| capability package | Lode 拥有站点能力包的资产身份、site/origin、capability id、operation id、lifecycle、version、resource requirement 声明、known limitations 和 invalidation marker。 | Core 拥有 admission、执行、Run Record、result envelope；Harbor 拥有 Profile、Runtime Session、provider facts 和 evidence refs。 | Core admission / execution，App Library。 | `README.md`、`ROADMAP.md`、ADR 0002、research synthesis 1.3。 | accepted |
| input / output / source schema | Lode 拥有 capability / workflow input schema、normalized output schema、source shape schema、field mapper / normalizer 引用和 schema 版本。 | Core 只校验、投影并封装运行结果；Harbor 只提供 raw/evidence/source trace 引用，不定义业务 schema。 | Core result validation，App Library schema display，后续 package validator。 | ADR 0002、ADR 0003、`docs/draft/result-schema.md`。 | accepted |
| fixtures | Lode 拥有 redacted raw fixtures、normalized fixtures、normalizer tests 或等价 regression checks。 | 真实生产 raw payload、完整请求/响应、未脱敏 DOM、截图、账号态和用户业务数据不归 Lode 保存。 | package validation，capability regression，repair draft。 | ADR 0003、`docs/draft/site-package-format.md`、`docs/draft/result-schema.md`。 | accepted |
| post-check | Lode 拥有声明式 post-check requirements 和 capability 成功条件；write-like capability 必须显式声明 post-check。 | Core 决定何时/如何执行 post-check 并映射结果；Harbor 提供截图、Snapshot、network summary、raw payload ref 等证据引用。 | Core execution / reconciliation，App result display。 | ADR 0003、research result-normalization / evidence themes。 | accepted |
| registry | Lode 拥有本地 discoverability 和 version identity：asset id、type、path、lifecycle、version、package ownership。 | hosted marketplace、sync service、crawler queue、runtime registry 和 provider registry 不属于第一阶段 Lode 交付。 | App Library，Core package lookup，后续 validator / registry tooling。 | ADR 0004、`ROADMAP.md`。 | accepted；repo-level registry 文件形态见 PD-0010 |
| version / rollback / deprecation / invalidation | Lode 拥有能力资产、schema、normalizer、fixture、workflow、overlay、fork、draft 的版本、失效标记、deprecation 标记和 rollback 语义边界。 | Core Run Record 只引用使用到的版本；App 提供 install / pin / update / rollback 操作入口；外部同步和贡献流后续再定。 | Core run attribution，App Library，repair / invalidation flow。 | ADR 0004、`docs/draft/asset-versioning.md`、`docs/draft/invalidation-reporting.md`。 | accepted；overlay 冲突规则见 PD-0012 |
| `site-capability` | 一等 Lode asset，表达单站点动作、schema、normalizer、fixtures、checks、version 和失效标记。 | 不直接保存运行现场或 provider 选择。 | Core，App Library。 | ADR 0004、research site-knowledge-and-capability-assets。 | accepted |
| `workflow-package` | 一等 Lode asset，组合 site capability，拥有 workflow input、step、resource requirement 和 verification requirement。 | Core 执行 workflow 并记录步骤事实；Harbor 提供运行现场。 | Core workflow execution，App Work / Library。 | ADR 0004、`docs/draft/task-package-format.md`、research workflow-and-task-package。 | accepted |
| supporting asset / `domain-skill` | typed supporting asset，可保存站点知识、notes、selectors、examples、authoring guidance；它本身不是 stable executable capability。 | 不作为 Core 可准入能力，也不替代 schema / fixture / post-check。 | capability authoring，App Explorer / Library。 | ADR 0004、research site-knowledge-and-capability-assets。 | accepted；子结构见 PD-0011 |
| `site-adapter` / helper asset | 默认是 capability package 内部组件；只有被多个 capability 复用时才需要独立索引。 | 不作为用户 task contract，不拥有 runtime/provider 选择权。 | capability package，后续 validator。 | ADR 0004、Syvert / OpenCLI / bb-sites research 输入。 | accepted |
| `benchmark-task` | 暂不作为用户 workflow contract；未来 benchmark harness 成立后再评估独立 eval package。 | 不进入第一阶段包合同或 Core admission。 | 后续 eval / research。 | ADR 0004、research synthesis 明确不吸收 benchmark task 作为产品 task contract。 | deferred；见 PD-0013 |
| `crawler-job` | 暂不作为 Lode MVP 合同；长时间 crawl 未来可转成 workflow profile。 | queue、storage、proxy、scaling runtime、crawler scheduler 不归 Lode。 | 后续 crawler / workflow 规划。 | ADR 0004、`ROADMAP.md`、research workflow-and-task-package。 | deferred |
| 首批只读能力与写侧 validate-only / draft / preview 内容 | 本轮只把它们作为后续 #18/#21 的输入边界：需要 Lode 提供 schema、fixtures、resource requirement 和 post-check。 | 本轮不创建具体能力包、不实现写侧资产、不运行真实提交。 | 后续 #18/#21、Core/App/Harbor 对齐。 | 当前委派边界、`ROADMAP.md` 阶段四/六。 | deferred |

## 第一阶段排除的运行时事实

| 非目标 | 排除原因 | 可重新评估条件 | 影响阶段 | 状态 |
|---|---|---|---|---|
| 真实账号、Cookie、Token、session storage、localStorage、Profile 状态 | 这些是 Harbor / runtime identity facts，包含高度敏感账号状态；Lode 只能声明抽象 resource requirement 或保存脱敏 fixture。 | Harbor facts / Core admission 合同稳定后，Lode 可增加引用字段或校验引用存在性。 | 阶段三以后 | rejected (Lode storage) |
| Runtime Session、provider、CDP / VNC / Viewer、profile lock、live tab state | 这些是执行现场和运行资源，不是能力资产定义。 | Harbor Runtime Session API 与 Core Run Record 稳定后，Lode 可声明所需 runtime capability 词汇。 | 阶段三以后 | rejected (Lode ownership) |
| 真实生产 raw payload、完整请求/响应、未脱敏 DOM、未脱敏截图 / HAR / trace | 可能包含账号、业务内容、私信、表单、路径或凭据；Lode 只能保存脱敏 raw fixture、normalized fixture 或 evidence_ref。 | Evidence policy、redaction 和 retention 策略稳定后，只允许通过引用消费。 | 阶段三/四以后 | rejected (inline storage) |
| 用户具体任务输入、客户数据、业务运营策略、投放/联系/发布决策 | Lode 只维护可复用能力资产，不是业务策略系统或用户数据仓库。 | 上游业务系统定义可脱敏、可复用模板时，Lode 只接收公共 task package 边界。 | 阶段四以后 | rejected |
| hosted marketplace、团队同步、公共贡献审核流 | 第一阶段只需要本地包和边界；提前做 hosted service 会扩大范围。 | 本地 install / lock / update / report 闭环跑通后再评估。 | 阶段九/十 | deferred |

当前阶段无 Milestone / FR / Work Item blocker。剩余 PD-0003 至 PD-0013 均为
implementation-time 或 external-contract 决策，不阻塞 #6 / #9 的第一阶段边界收敛。

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
