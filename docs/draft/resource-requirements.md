# 资源需求声明

本文档描述 Lode 中能力资源需求声明的初步方向，不代表最终稳定 Schema。

资源需求声明用于表达一个站点能力或任务封装在运行时需要什么资源条件。它不选择 Harbor Profile，不选择 provider，不定义 fallback，也不排序资源。它只声明可被 WebEnvoy Core 匹配的公共需求。

## 核心原则

- 资源需求由 Lode 能力资产声明；
- 当前资源能力事实由 Harbor 返回；
- 是否满足由 WebEnvoy Core 做 one-of matching；
- 多个 profile 表示“任一满足即可”，不是 fallback 顺序；
- 每个 profile 应有 evidence_refs 或 fixture 支撑；
- 资源需求不应包含 Cookie、Token、Session、provider route 或站点私有字段。

## Resource Requirement Profile

建议结构：

```text
ResourceRequirementProfile
  profile_key
  dependency_mode
  required_capabilities
  evidence_refs
```

字段含义：

| 字段 | 含义 |
|---|---|
| `profile_key` | 声明内稳定标识，不代表优先级 |
| `dependency_mode` | 是否需要资源，例如 `none` 或 `required` |
| `required_capabilities` | 所需抽象资源能力 |
| `evidence_refs` | 支撑该 profile 合法性的证据或 fixture 引用 |

## One-of 满足性

同一能力可以声明多个可满足 profile：

```text
resource_requirement_profiles:
  - profile_key: stable_identity_proxy
    required_capabilities:
      - stable_identity
      - persistent_profile
      - proxy
  - profile_key: stable_identity
    required_capabilities:
      - stable_identity
      - persistent_profile
```

运行时只需要满足其中任一 profile。匹配失败表示当前资源不可用，不表示声明非法。声明字段、能力词汇或证据不合法才是 contract invalid。

## 建议资源能力词汇

初始词汇可以从以下抽象能力开始：

```text
account
stable_identity
persistent_profile
browser_context
proxy
viewer
manual_takeover
snapshot
network_summary
write_verification
evidence_capture
raw_payload_reference
```

这些是公共运行资源能力词汇，不是 Harbor 内部字段，也不是 provider 私有参数。`raw_payload_ref` 与 `evidence_ref` 是结果 / 证据引用字段，不应作为资源需求 capability id。

## 与 Harbor 的关系

Harbor 返回 Runtime Capability Facts，例如：

- Profile 是否长期持久；
- Execution Identity 是否绑定站点账号；
- Cookie / storage 是否持久存在；
- proxy 是否绑定；
- CDP 是否可用；
- Viewer 是否可用；
- Snapshot / network summary 是否可用；
- 人工接管是否可用；
- 当前 session 是否健康。

Core 使用这些事实与 Lode 的 resource requirement profiles 做匹配。

## Stage 2 v0 合同

本节把 `Resource Requirements v0` 收敛为可被 Core 准入消费的最小合同。Lode 只声明需求；Harbor 仍是 runtime facts 的 truth source；Core 做匹配、失败归因和 result envelope 映射。

### Harbor facts vocabulary 消费

| fact vocabulary | Owner | Lode consumer boundary | 有效性 / 过期规则 | 失败分类 | 非目标 |
|---|---|---|---|---|---|
| `profile_persistence` | Harbor | Lode 可声明需要 `persistent_profile` 或 `ephemeral_profile_allowed`。 | 事实随 Harbor profile/session 状态刷新；过期事实不能用于 admission。 | `resource_unavailable` | 不保存 profile id、路径、Cookie 或 storage。 |
| `identity_binding` | Harbor | Lode 可声明需要 `account_bound`、`anonymous_allowed` 或 `user_login_required`。 | 登录墙、账号切换、登出或风险页会使事实过期。 | `resource_unavailable`; `requires_user_action` | 不保存账号名、手机号、cookie 或 token。 |
| `browser_context` | Harbor | Lode 可声明需要 browser context、CDP、viewer 或 manual takeover。 | session close、provider restart 或 tab loss 会使事实过期。 | `resource_unavailable` | 不选择 provider、tab 或 driver 参数。 |
| `network_context` | Harbor | Lode 可声明是否需要 proxy、稳定出口或允许无代理。 | proxy 轮换、健康检查失败或站点封禁会使事实过期。 | `resource_unavailable` | 不保存 proxy endpoint、供应商或路由。 |
| `evidence_capability` | Harbor | Lode 可声明需要 Snapshot、network summary、screenshot summary、raw payload ref 或 evidence capture。 | evidence policy、retention 或 capture failure 变化会使匹配失效。 | `evidence_unavailable`; `resource_unavailable` | 不 inline screenshot、HAR、DOM 或完整响应。 |
| `write_safety_capability` | Harbor/Core boundary | Stage 2 只允许声明 write-like validation 需要未来 write target binding、completion evidence 和 user confirmation。 | 真实写侧合同未稳定前只能 `deferred`。 | `invalid_contract` when used for real write in Stage 2 | 不执行 submit/publish/delete/pay/send/follow 等真实写入。 |

### 匹配状态

| 状态 | 含义 | Owner | Consumer | 失败分类 | 非目标 |
|---|---|---|---|---|---|
| `matched` | 声明合法，且至少一个 resource requirement profile 被当前 Harbor facts 满足。 | Core | Core admission; App explainability | not_applicable | 不表示业务结果成功。 |
| `unmatched` | 声明合法，但当前 Harbor facts 不满足任一 profile。 | Core | App repair/login/runtime setup | `resource_unavailable`; `requires_user_action` | 不把资源不足误报为 package 无效。 |
| `invalid_contract` | profile 字段、词汇、引用、证据或 operation/resource 边界非法。 | Lode validator / Core admission | Package repair | `invalid_contract` | 不尝试 fallback 或硬跑 runtime。 |

### read / validate-only / write-like 边界

| operation boundary | Stage 2 允许声明 | 必须 deferred | 失败分类 | 非目标 |
|---|---|---|---|---|
| `read` | 读取页面、列表、详情、评论或公开/用户已授权可见内容；可要求 Snapshot、network summary、manual takeover 或 raw payload ref。 | 长队列 crawler、账号池调度、后台采集和未脱敏存储。 | `resource_unavailable`; `source_unavailable`; `output_invalid` | 不做真实写入或 provider 选择。 |
| `validate-only` | 在不提交外部变更的前提下校验目标页面、输入、资源、风险和预期变更可解释性。 | 保存到真实外部系统、点击提交、发送、发布、支付、删除。 | `input_invalid`; `requires_user_action`; `verification_failed` | 不把验证通过当写入成功。 |
| `write-like` | 只记录未来真实写能力需要的资源和证据条件。 | action boundary、idempotency key、write operation ref、completion evidence、rollback/repair hint 未定稿前的真实写 package。 | `invalid_contract` when claimed as executable | 不把 Stage 2 提前扩成真实写闭环。 |

## 与能力生命周期的关系

稳定能力必须声明资源需求。没有资源需求的能力可以处于 proposed 或 experimental，但不应进入 stable execution，除非它明确声明 `dependency_mode=none` 并有对应 evidence_refs。

## 禁止字段

资源需求声明不应包含：

- provider_key；
- provider_selector；
- provider_routing；
- fallback；
- priority；
- preferred_profile；
- Cookie；
- Token；
- Session；
- local path；
- storage URL；
- platform private object；
- browser driver 参数；
- business strategy。

这些字段属于 Harbor 内部事实、站点能力内部实现或上游业务策略，不应进入 Lode 的公共资源需求契约。

## 失败语义

Core 匹配资源需求时应区分：

| 状态 | 含义 |
|---|---|
| `matched` | 至少一个 profile 被当前 Harbor 能力事实满足 |
| `unmatched` | 声明合法，但当前资源能力不足 |
| `invalid_contract` | 声明字段、能力词汇、证据或引用不合法 |

这种区分能避免把“当前资源不足”误报成“能力资产无效”，也能避免资源声明非法时继续硬跑。
