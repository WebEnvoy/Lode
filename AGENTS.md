# Lode 执行指南

Lode 是独立的 MIT 资产仓，维护网站 SKILL、AccountSystem 模板、共享知识、必要脚本和脱敏验证资产。产品方向与 V1 约束以组织级 [canonical v1 规范](https://github.com/WebEnvoy/.github/blob/main/docs/product-architecture-v1.md) 为准。

## 边界与实施原则

- SKILL 是网站知识的主要载体，围绕用户目标组织；AccountSystem 是可被多个 SKILL 引用的独立资产，运行时以用户本地定义为准。
- Lode 不运行浏览器、不授予权限、不保存 Profile 或生产现场，也不复制 Core 的 Run、授权、幂等或结果状态机。
- capability package、Schema、fixture、post-check 和脚本只在真实消费者需要时补充；不为未来站点、媒体或形态横向铺满合同。
- 页面事实未知时保持 unknown；fixture、validator 或资产合并不证明 Runtime、App 或 live 业务能力完成。
- BOSS 资产保留但退出近期交付。首个小红书消费者只推进图片上传、必要字段回读和页面实际证明支持的一种 commit；文字配图与其他形态后置。
- 复用现有可消费资产；临时兼容层必须写明消费者和退出条件。不得建立 runner、hosted registry、marketplace、同步服务或通用执行 DSL。

## 数据与验证

- 不得提交 Cookie、Token、凭据、Profile/Instance state、raw DOM/HAR、未脱敏截图、生产 payload 或用户私有业务内容。
- 资产变更运行 package-specific validator 和必要全仓 validator；Python 使用 `make py-compile`；所有变更运行 `git diff --check`。
- 新的非平凡解析、校验或脚本至少留下一个最小正向、必要拒绝和恢复/unknown 检查；docs-only 不冒充 live 验收。

## GitHub-native 交付

- 当前状态只以 GitHub Issue、原生关系、Milestone、Project、PR、checks、review 和 `main` 回读为准；不创建 carrier 或第二状态机。
- 普通工作可直接使用 Work Item；只细化当前和下一批，只有真实技术或验收阻塞才建 dependency。
- PR 绑定真实 Work Item，在 exact head 上完成独立 review 和 `py-compile`、`lode-ci` 等 required checks。
- `completed` 只表示该资产 Issue 的原验收有证据，且必须说明不代表产品 live；延期保持 open、移出活跃 Milestone并进入 Backlog；替代关闭使用 `not_planned`/Won’t Do。
