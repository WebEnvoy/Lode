# 失效与上报

本文档定义 Lode 能力资产失效标记和上报边界。

## 失效来源

能力资产可能因为以下原因失效：

- 页面结构变化；
- 入口路径变化；
- 字段或按钮变化；
- API / DOM / network source shape 变化；
- source schema 变化；
- normalizer 失败；
- 字段映射不完整；
- 必填字段缺失；
- cursor / continuation shape 变化；
- partial parse 失败；
- 登录状态异常；
- 访问受限；
- 写入后验证失败；
- 用户手动标记；
- 回归测试失败。

## 私有失效标记

私有失效标记只影响用户本地或团队资产。

适用场景：

- 某个能力不适合当前账号；
- 某个任务模板不适合用户自己的流程；
- 用户 overlay 或 fork 出现问题；
- 用户希望暂时禁用某个能力版本。

## 平台失效上报

平台失效上报面向公共能力生态。

它应尽量只包含脱敏事实，例如：

- 能力 ID；
- 能力版本；
- 失败类型；
- 页面状态摘要；
- 元素变化摘要；
- 错误码；
- 验证阶段；
- source shape 类型；
- source schema 版本；
- normalizer 版本；
- 脱敏 raw fixture 引用；
- normalized fixture 引用；
- 证据引用。

平台上报不应包含用户业务内容、账号凭据、完整执行现场、真实生产 raw payload 或未脱敏页面内容。

## 归一化失效类型

站点级归一化可以使用更细的失效类型：

| 失效类型 | 含义 |
|---|---|
| `source_shape_changed` | API、DOM、network 或 Snapshot 的 raw shape 变化 |
| `source_schema_changed` | 已记录 source schema 与实际来源不一致 |
| `normalizer_failed` | normalizer 无法生成合法 normalized output |
| `mapping_incomplete` | 站点字段到公共字段的映射缺失 |
| `required_field_missing` | source 中缺少 output schema 必填字段 |
| `cursor_shape_changed` | continuation / reply cursor 形态变化 |
| `partial_parse_failed` | 部分 item 可解析，部分 item 解析失败 |
| `output_contract_broken` | normalizer 输出不满足 output schema |

这些类型应尽量定位到 source shape 或 normalizer，而不是笼统标记整个站点能力失效。

## 修复流程

推荐流程：

```text
发现失败
  → 标记失效
  → 创建修复草稿
  → 运行测试
  → 保存为个人资产
  → 可选提交为平台贡献
```

## App 中的呈现

WebEnvoy App 的 Library / Reports 应支持：

- 标记能力失效；
- 标记任务模板失效；
- 创建站点变化报告；
- 创建修复请求；
- 附加脱敏证据；
- 管理私有失效标记；
- 提交平台失效上报。
