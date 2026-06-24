# 资产版本管理

本文档定义 Lode 能力资产的版本管理原则。

## 版本对象

需要版本管理的对象包括：

- 站点知识；
- 能力包；
- source schema；
- normalizer；
- output schema；
- 原子动作；
- 任务模板；
- 测试样例；
- 用户 overlay；
- fork；
- draft。

## 平台资产版本

平台资产应支持：

- install：安装指定版本；
- update：更新到新版本；
- pin：锁定版本；
- rollback：回滚版本；
- disable：禁用版本；
- changelog：查看变更记录。

平台资产版本应可被 Core 运行记录引用，用于解释一次任务使用了哪个能力版本、哪个 source schema、哪个 normalizer 和哪个 output schema。

## 个人资产版本

用户个人资产应支持：

- 本地版本历史；
- diff；
- 回滚；
- 标记 active 版本；
- 标记 deprecated；
- 导出；
- 可选提交为平台贡献。

## 与 Run Record 的关系

Core Run Record 应引用能力资产版本。

对于含归一化逻辑的站点能力，Run Record 或 result envelope 还应能引用：

- capability version；
- source schema version；
- normalizer version；
- output schema version；
- fixture / regression version；
- compatibility 或 migration note。

这样失败后可以判断：

- 是平台资产版本问题；
- 是用户 overlay / fork 的问题；
- 是网站变化；
- 是资源或账号状态问题；
- 是业务输入问题；
- 是 source shape 变化；
- 是 normalizer 版本问题；
- 是 output schema 兼容性问题。

API 字段变化、DOM 结构变化、network response shape 变化，可能只需要升级 source schema 或 normalizer，不一定改变整个能力语义。

## App 中的呈现

WebEnvoy App 的 Library 区域应显示：

- 已安装版本；
- 可更新版本；
- 锁定状态；
- 回滚入口；
- 私有修改是否存在；
- 当前任务使用的能力版本。
