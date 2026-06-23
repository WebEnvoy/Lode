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
raw_payload_ref
evidence_ref
```

这些是公共能力词汇，不是 Harbor 内部字段，也不是 provider 私有参数。

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
