# 能力生命周期

本文档描述 Lode 中站点能力生命周期的初步方向，不代表最终稳定 Schema。

能力生命周期用于区分探索草稿、实验能力、稳定能力和废弃能力。它的目标是让 WebEnvoy Core 在执行前知道一个能力是否可以进入稳定运行路径，而不是让 Agent 或调用方临场判断。

## 生命周期状态

建议使用四类状态：

| 生命周期 | 语义 | 是否稳定执行 |
|---|---|---|
| `proposed` | 候选能力、命名占位、探索方向或设计草稿 | 否 |
| `experimental` | 可在受控场景试用，但契约、fixture 或失效处理未完全冻结 | 默认否 |
| `stable` | 已具备稳定输入输出、资源需求、测试样例、版本和失效处理 | 是 |
| `deprecated` | 保留历史语义，但不应进入新的稳定任务 | 否 |

`proposed` 不是弱稳定能力。`experimental` 即使可运行，也不应默认被 WebEnvoy Core 当成 stable capability。

## Stable 能力的最低条件

一个能力进入 `stable` 前，至少应具备：

- operation id；
- capability family；
- target type；
- input schema；
- source schema；
- extraction / parsing / mapping / normalization 规则；
- output schema / normalized schema；
- resource requirement profiles；
- pre-check；
- post-check / verification；
- failure classification；
- evidence policy；
- redacted raw fixtures；
- normalized fixtures；
- normalizer tests；
- version；
- invalidation marker；
- known limitations。

稳定能力的判断不应只看“能跑通一次”。它应能被验证、回放、失效标记和版本锁定。

## Operation 与 Capability 的关系

建议区分：

```text
operation_id
  外部可调用的公共操作，例如 content_search_by_keyword

capability_family
  能力族，例如 content_search

site capability
  某个站点包内对该能力族的具体实现
```

这种区分可以让不同站点能力共享公共 operation 语义，同时保留站点内部的执行细节和版本。

## 生命周期与输出契约

稳定能力必须有输出契约和 source-specific normalizer。输出契约包括：

- source schema；
- extractor / parser / mapper / normalizer；
- normalized result schema；
- collection item schema；
- comment item schema；
- dataset record schema；
- cursor / continuation schema；
- raw_payload_ref policy；
- evidence_ref policy；
- source_trace policy；
- redacted raw fixture；
- normalized fixture；
- normalizer tests。

没有输出契约和 normalizer 测试的能力可以作为探索草稿或 experimental 能力，但不应进入稳定任务路径。

## 生命周期与资源需求

稳定能力必须声明资源需求。资源需求不应是简单布尔值，而应支持多个可满足 profile，例如：

```text
stable_identity + persistent_profile + proxy
stable_identity + persistent_profile
public_no_account
```

Core 执行时根据 Lode 声明和 Harbor 能力事实做 one-of matching。

## 失效与废弃

网站变化后，能力可以被标记为：

- temporarily_invalid；
- output_contract_broken；
- input_contract_broken；
- selector_or_flow_changed；
- source_shape_changed；
- source_schema_changed；
- normalizer_failed；
- mapping_incomplete；
- resource_requirement_changed；
- verification_failed；
- deprecated。

失效标记应能关联到能力版本、fixture、失败证据和可选修复草稿。

## 不应做的事

能力生命周期不应承载：

- provider routing；
- fallback priority；
- 业务 workflow；
- 内容策略；
- 账号运营策略；
- Cookie / Token / Session；
- 平台 raw payload；
- Harbor Runtime Session 状态。

能力生命周期的价值，是让 Lode 资产在被 Core 执行前具备明确状态和稳定边界。
