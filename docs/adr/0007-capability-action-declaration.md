# 0007. Capability 动作类别与授权需求声明

## 状态

Accepted for Lode #282; package/schema implementation remains in #281, 2026-07-14.

本 ADR 扩展 ADR 0002 的 `operation_mode`。Lode 声明能力可能执行的动作和目标范围，
但不拥有用户授权策略、approval workflow 或 runtime 决定。

## 背景

旧模型使用 `read`、`validate_only`、`draft`、`preview`、`write` 和 risk hints 混合
表达能力行为、UI 文案和授权需求。App/Core 由此形成散落的 risk/approval 状态。

Capability asset 只需要如实声明可能发生的动作。Core 根据用户全局默认、当前任务
覆盖和单次授权计算是否允许；Harbor 执行有效授权；App 投影同一决定。

## 决策

Capability package 从以下四类中声明非空集合：

| 类别 | Lode 声明含义 |
| --- | --- |
| `read` | 导航、搜索或读取，不产生目标网站外部变化 |
| `prepare` | 只在本机或页面内准备，不向外部系统传输材料或产生持久变化 |
| `commit` | 上传、发布、发送、提交、创建、修改或其他外部传输/变化 |
| `destructive` | 删除、撤销或其他破坏性变化 |

`environment` 是共享授权词汇中的第五类，但只由 Harbor provider/session operation
catalog 声明；Lode site capability 不得声明它。

声明还必须包含：

- 动作适用的目标类型或 target scope；
- capability 是否可能产生外部变化；
- 需要的 resource requirements；
- 用于能力验证的 pre/post-check 和运行记录 requirements。

`operation_mode` 继续描述产品形态，例如 `validate_only` 或 `preview`，但不再充当
授权决策。当前小红书只读能力声明 `read`；发布前 validate-only 能力只有在合同保证
不上传、不自动保存、不向外部传输材料时才能只声明 `prepare`。一旦包含上传、自动保存
或其他外部传输，就必须声明 `commit`，即使最终发布按钮没有点击。

Evidence、fixture 和 post-check 继续用于资产验证、来源追溯和运行记录。Lode 不要求
App 默认展示 evidence refs、截图或 trace。

## 消费边界

- Core 验证声明并计算有效授权；
- App/CLI/MCP/API/SDK 展示业务动作和授权结果，不解释 Lode 私有字段；
- Harbor 为 provider/session operation 声明 `environment` 动作，并只消费 Core 已允许的
  请求；直接用户意图也是 Core evaluator 的输入，不是 Harbor 绕过授权的许可；
- Lode 不保存用户全局策略、任务 grant、单次决定或审批记录。

## 兼容性

现有 `operation_mode` 不立即删除。Current packages 在 #281 的实现 PR 中补充动作声明；
Core 在新字段缺失时不得从 `write` 等旧值静默扩大授权。兼容读取的移除时间由后续
schema version Work Item 决定。

## 非目标

- 不建立 RBAC、组织审批、provider policy 或 App UI。
- 不定义 Core Run Record、authorization API 或 Harbor session schema。
- 不把当前 no-submit 验收范围写成 WebEnvoy 永久产品限制。
