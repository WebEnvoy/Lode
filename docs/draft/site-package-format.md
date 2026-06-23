# 站点包格式

本文档描述 Lode 中站点包的初步方向，不代表最终 Schema。

## 建议目录

```text
sites/
  example-site/
    site.json
    states/
    pages/
    apis/
    selectors/
    results/
    fixtures/
    tests/
```

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

## 原则

- 站点知识应尽量结构化；
- 不保存账号、Cookie、Token 或用户私有数据；
- 页面变化应能形成摘要；
- 风控页、验证码页、登录失效页等应作为可识别状态建模；
- 站点能力输出应声明公共 normalized schema，而不是让 Core 或上游系统理解平台 raw 字段；
- raw payload、截图、network 摘要和执行现场应通过引用进入结果，不应直接保存到站点包。
