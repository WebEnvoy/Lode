# Spec: 小红书与 BOSS 站点知识选择

## Story Readiness

- User value: Lode 能在能力包实现前，把既有小红书与 BOSS 站点知识转成清晰资产边界。
- Success experience: 评审者能看到哪些输入被吸收、改造、参考或拒绝；每类知识属于哪个层级；以及下游能力包首批冻结哪些只读任务。
- Failure states: 来源盘点缺失、首批任务范围过大、暗示写入行为、Harbor/Core/App 边界模糊，或直接复制未授权源码。
- Sensitive data boundary: Lode 只保存文档、ADR 事实、来源 locator、字段/路由知识和能力包设计指引；不保存凭据、身份档案状态、运行会话、实时标签页、原始页面结构/网络载荷、生产证据或用户业务数据。
- Non-goals: 实现真实能力包、创建结构定义/固定样本数据/校验器逻辑、执行浏览器运行环境、执行真实写入、编辑 sources/research，或进入 Lode #198/#199/#200。

## Suite Path

- Suite path: minimal
- full-path-artifacts not_applicable rationale: 仅文档的产品与资产边界决策；consumer boundary: suite validation、review、merge-ready 和 closeout 只消费 spec.md、plan.md、evidence-map.md、task-carrier.md 与 ADR 0006；recheck condition: 创建可执行能力包、结构定义、固定样本数据、校验器、运行环境证据合同或跨仓合同所有权变更时，切换到 full suite。
