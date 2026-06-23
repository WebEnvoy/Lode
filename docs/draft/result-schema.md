# 结果 Schema 与归一化契约

本文档描述 Lode 中站点能力输出契约的初步方向，不代表最终 Schema。

Lode 不只保存站点入口、页面状态和操作步骤，也应保存站点能力的输出契约。能力包应声明结果如何被公共化表达，让 WebEnvoy Core 可以在运行时校验、投影和封装结果。

## 定位

结果 Schema 是能力资产的一部分。

```text
Lode
  定义 output schema / normalized schema / fixture

WebEnvoy Core
  消费 Lode schema，校验并封装 public result envelope

Harbor
  提供 raw_payload_ref、evidence_ref、source_trace 和运行现场
```

这意味着 Lode 定义“结果应该长什么样”，但不执行归一化，也不保存真实 raw payload。

## 能力输出契约

每个进入稳定执行路径的站点能力都应声明输出契约。最小内容包括：

- 输出类型，例如 detail、collection、comment_collection、profile、media_asset、write_result、dataset_record；
- normalized result schema；
- raw payload 引用策略；
- evidence 引用策略；
- source trace 要求；
- failure classification 词表；
- cursor / continuation 契约；
- 脱敏 fixture 和示例结果。

能力输出契约应服务于 Core 的运行时校验，而不是作为说明性 Markdown 停留在文档中。

## Normalized Result

`normalized` 是平台无关的公共结果投影。它不应暴露平台私有 raw shape，也不应包含 Cookie、Token、完整请求响应、本地路径、storage handle、provider route 或用户业务私有字段。

常见字段候选：

```text
source_platform
source_type
source_id
canonical_ref
title_or_text_hint
body_text_hint
creator_ref
author_ref
media_refs
published_at
```

具体能力可以只声明自己需要的字段，不必强制所有能力共用一个巨大实体模型。

## Collection Item

集合类能力应把平台 item 投影为公共 item envelope。候选结构：

```text
dedup_key
source_ref
normalized
raw_payload_ref
evidence_ref
source_trace
```

`dedup_key` 用于同一结果集或 dataset sink 内去重。`raw_payload_ref` 只指向可审计的原始载荷引用，不应 inline 原始载荷。

## Comment Item

评论能力应在普通集合语义上增加评论关系和可见性约束。候选字段：

```text
dedup_key
source_ref
normalized
visibility_status
reply_cursor
raw_payload_ref
evidence_ref
source_trace
```

`normalized` 中可包含：

```text
source_platform
source_type
source_id
canonical_ref
body_text_hint
root_comment_ref
author_ref
parent_comment_ref
target_comment_ref
published_at
```

评论层级关系应围绕 public `canonical_ref` 建立，而不是围绕平台私有 thread id 或 raw comment object 建立。

## Dataset Record

Dataset record 是结果落地后的最小公共记录，不是产品数据库或内容仓库。候选字段：

```text
dataset_record_id
dataset_id
source_operation
adapter_key
target_ref
raw_payload_ref
normalized_payload
evidence_ref
source_trace
dedup_key
recorded_at
origin_kind
```

`normalized_payload` 必须是 JSON-safe public payload。`raw_payload_ref` 只能是引用或 null，不允许把 raw payload 直接写入 dataset sink。

## Source Trace 与 Evidence Reference

`source_trace` 用来说明公共结果来自哪个 adapter、哪类执行路径和哪些脱敏证据。它不应泄漏真实 provider route、账号池、代理池、本地路径、storage URL 或私密凭据。

`evidence_ref` 指向 Harbor 或 Core 记录的运行证据，例如截图摘要、Snapshot、network 摘要、验证结果或站点变化摘要。

## 边界

Lode 应定义：

- output schema；
- normalized schema；
- collection / comment / dataset schema；
- cursor / continuation schema；
- 脱敏 fixture；
- 版本和失效标记。

Lode 不应保存：

- 真实账号；
- Cookie；
- Token；
- 完整 raw payload；
- 完整 DOM；
- 完整请求 / 响应；
- 用户业务客户数据；
- 未脱敏执行现场。

归一化契约的目标，是让不同网站能力返回稳定、可校验、可记录、可复用的公共结果，而不是把 Lode 扩张成通用 ETL、爬虫数据清洗平台或业务数据仓库。
