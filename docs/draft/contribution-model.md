# 贡献模型

Lode 未来可以支持公共能力贡献、审核和分发。

## 默认可以贡献的内容

- 站点结构变化摘要；
- 页面状态识别规则；
- 接口形状摘要；
- source schema 变更摘要；
- normalizer patch；
- 脱敏 raw fixture；
- normalized fixture；
- normalizer regression test；
- 能力失败步骤；
- 错误类型；
- 风控状态类型；
- 资源需求变化；
- 不含私密数据的测试样例。

## 默认不应提交的内容

- 账号；
- Cookie；
- Token；
- 发布内容；
- 完整截图；
- 完整 DOM；
- 完整请求 / 响应；
- 真实生产 raw payload；
- 未脱敏 raw fixture；
- 用户私有任务封装；
- 用户业务参数。

## 公共与私有

公共能力需要审核后分发。

用户私有能力和私有任务封装可以长期运行，但不应默认进入公共库。

## Normalizer 贡献要求

提交站点级 normalizer 贡献时，至少应满足：

- 声明适用的站点、能力和 source shape；
- 提供 source schema 或 source schema diff；
- 提供 normalizer 或 mapping patch；
- 提供脱敏 raw fixture；
- 提供 normalized fixture；
- 提供 regression test；
- 不包含 Cookie、Token、Session、本地路径、storage URL 或 provider route；
- 不包含用户业务内容或真实生产 raw 数据。

公共审核应重点确认 normalizer 不把平台私有 raw shape 泄漏到公共 normalized result。
