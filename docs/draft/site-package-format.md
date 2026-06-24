# 站点包格式

本文档描述 Lode 中站点包的初步方向，不代表最终 Schema。

站点包不仅保存站点结构、页面状态和能力定义，也可以保存站点级 extraction、parsing、mapping、normalization 规则、脱敏 fixture 和 normalizer tests。它的目标是把站点来源差异吸收到能力资产里，而不是让 WebEnvoy Core 或上游系统理解小红书、抖音等站点的 raw 字段。

## 建议目录

```text
sites/
  example-site/
    site.json
    states/
    pages/
    apis/
    selectors/
    capabilities/
      read-content-detail/
        capability.json
        input.schema.json
        output.schema.json
        sources/
          web-api.schema.json
          dom.schema.json
          network.schema.json
        extractors/
        parsers/
        mappers/
        normalizers/
        fixtures/
          web-api.raw.redacted.json
          dom.raw.redacted.json
          network.raw.redacted.json
          content-detail.normalized.json
        tests/
          normalize.test.ts
    fixtures/
    tests/
```

`capabilities/*/sources` 描述不同 raw source shape；`extractors`、`parsers`、`mappers` 和 `normalizers` 描述如何把这些来源归一到同一个 output schema；`fixtures` 和 `tests` 用于回归验证。

## site.json 可能包含

```json
{
  "site_id": "example-site",
  "name": "Example Site",
  "domains": ["example.com"],
  "login": {
    "required_for": ["publish", "account_status"],
    "state_detectors": []
  },
  "risk_states": [],
  "resource_defaults": {}
}
```

## capability.json 可能包含

```json
{
  "capability_id": "read-content-detail",
  "operation_id": "content_detail_by_url",
  "lifecycle": "experimental",
  "input_schema": "input.schema.json",
  "output_schema": "output.schema.json",
  "source_shapes": ["web-api", "dom", "network"],
  "normalizers": {
    "web-api": "normalizers/web-api-to-content-detail.ts",
    "dom": "normalizers/dom-to-content-detail.ts",
    "network": "normalizers/network-to-content-detail.ts"
  }
}
```

## 原则

- 站点知识应尽量结构化；
- 站点包可以保存站点级清洗和归一化逻辑；
- 同一能力可以支持多个 source shape，但应输出同一个 normalized schema；
- 不保存账号、Cookie、Token 或用户私有数据；
- 只保存脱敏 raw fixture，不保存真实生产 raw payload；
- 页面变化应能形成摘要；
- API、DOM、network、Snapshot 等 source shape 变化应能形成失效标记；
- 风控页、验证码页、登录失效页等应作为可识别状态建模；
- 站点能力输出应声明公共 normalized schema，而不是让 Core 或上游系统理解平台 raw 字段；
- raw payload、截图、network 摘要和执行现场应通过引用进入结果，不应直接保存到站点包。
