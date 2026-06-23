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
- 风控页、验证码页、登录失效页等应作为可识别状态建模。
