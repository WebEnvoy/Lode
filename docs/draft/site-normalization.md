# 站点级清洗与归一化

本文档描述 Lode 中站点级 extraction、parsing、mapping 与 normalization 的初步方向，不代表最终稳定 Schema。

Lode 不只是定义 normalized output schema。对于小红书、抖音等具体站点，同一个读能力可能来自 API、页面 DOM、network response、移动端接口或浏览器 Snapshot。不同来源的 raw shape 不同，但它们应被站点包中的规则和代码归一到同一个能力输出契约。

## 定位

站点级归一化是能力资产的一部分。

```text
Harbor
  提供 raw_payload_ref、evidence_ref、source_trace、Snapshot、network summary 和运行现场引用

Lode
  保存 source schema、extractor、parser、mapper、normalizer、fixture 和 tests

WebEnvoy Core
  调用 Lode 能力和 normalizer，校验 output schema，封装 result envelope，写入 Run Record
```

Lode 可以保存“如何把某站点 raw source 转成公共结果”的知识和代码，但不保存真实生产 raw 数据，也不做长期数据存储或通用 ETL 调度。

## Source Shape

同一站点能力可以支持多个 source shape：

- `web_api`：页面内接口或公开 Web API 返回；
- `network_response`：浏览器运行时被动拦截到的响应；
- `dom`：页面 DOM、可见文本或结构化 DOM 摘要；
- `snapshot`：Harbor 生成的页面 Snapshot / RefMap；
- `mobile_api`：移动端或第三方 provider 后方返回的结构；
- `manual_evidence`：人工接管或诊断产生的脱敏证据。

每个 source shape 可以有自己的 schema、fixture 和 normalizer，但同一能力最终应输出同一个 normalized result schema。

## 归一化流水线

站点能力内部的归一化可以分为四步：

```text
raw source reference
  → extraction
  → parsing
  → mapping
  → normalization
  → output schema validation
```

| 阶段 | 职责 | 示例 |
|---|---|---|
| extraction | 从 Harbor 引用或运行证据中取得可处理的脱敏输入 | network response summary、Snapshot、DOM 摘要 |
| parsing | 把 source shape 解析为站点内部中间结构 | 小红书 note API payload、抖音 comment response |
| mapping | 把站点字段映射到公共语义 | `note_id` → `source_id`，`authorInfo.id` → `author_ref` |
| normalization | 生成 Lode output schema 定义的公共结果 | `ContentDetail`、`CommentItem`、`CollectionItem` |

Core 不应硬编码小红书、抖音等站点字段映射。字段映射和 normalizer 应归属于 Lode 站点包。

## 建议目录

```text
sites/
  xiaohongshu/
    capabilities/
      read-note-detail/
        capability.json
        input.schema.json
        output.schema.json
        sources/
          web-api.schema.json
          dom.schema.json
          network.schema.json
        extractors/
          network-response.extractor.ts
          snapshot.extractor.ts
        parsers/
          web-api.parser.ts
          dom.parser.ts
          network.parser.ts
        mappers/
          web-api.mapper.ts
          dom.mapper.ts
          network.mapper.ts
        normalizers/
          web-api-to-content-detail.ts
          dom-to-content-detail.ts
          network-to-content-detail.ts
        fixtures/
          web-api.raw.redacted.json
          dom.raw.redacted.json
          network.raw.redacted.json
          content-detail.normalized.json
        tests/
          normalize.test.ts
```

这个结构只是候选方向。最终实现可以合并 extractor / parser / mapper / normalizer，但语义边界应保留。

## Fixture 要求

归一化测试需要两类 fixture：

- 脱敏 raw fixture：来自 API、DOM、network、Snapshot 等 source shape；
- normalized fixture：期望输出的公共结果。

脱敏 raw fixture 必须移除或替换：

- Cookie；
- Token；
- Session；
- 完整请求 / 响应中的私密字段；
- 账号信息；
- 用户业务内容；
- 本地路径；
- storage URL；
- provider route。

如果某字段对归一化测试必要，应使用公共 placeholder 或 redacted value，而不是提交真实值。

## Normalizer 测试

每个 stable 能力的 normalizer 应至少覆盖：

- 每个已声明 source shape 的 happy path；
- 必填字段缺失；
- 可选字段缺失；
- source shape 轻微变化；
- partial parse；
- cursor / continuation shape；
- raw payload 不允许泄漏到 normalized result；
- normalized fixture 与 output schema 匹配。

测试失败应能区分 source shape 变化、parser 失败、mapping 缺失、output schema 失败和 fixture 失效。

## 失效类型

站点级归一化应支持更细的失效标记：

- `source_shape_changed`；
- `source_schema_changed`；
- `normalizer_failed`；
- `parser_failed`；
- `mapping_incomplete`；
- `required_field_missing`；
- `cursor_shape_changed`；
- `partial_parse_failed`；
- `output_contract_broken`。

这样，小红书或抖音 API 字段变化时，不必笼统标记整个能力失效，可以定位到具体 source shape 或 normalizer。

## 边界

Lode 应保存：

- source schema；
- extractor / parser / mapper / normalizer；
- output schema；
- 脱敏 raw fixture；
- normalized fixture；
- regression tests；
- normalizer version；
- source shape invalidation marker。

Lode 不应保存：

- 真实生产 raw 数据；
- 未脱敏请求 / 响应；
- Cookie、Token、Session；
- 真实账号材料；
- 用户业务数据集；
- 长期采集数据；
- 通用 ETL 调度任务。

站点级清洗与归一化的目标，是把站点来源差异吸收到能力资产里，让 Core 和上游系统看到稳定的公共结果。
