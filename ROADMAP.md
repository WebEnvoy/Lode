# Lode 路线图

本文是 `WebEnvoy/.github/ROADMAP.md` 的 Lode 仓库级投影。若本文与组织级 ROADMAP 冲突，以组织级 ROADMAP 为准。

本文用于指导 Lode GitHub Milestone 的创建和排序，不维护当前 issue、PR 或执行看板。

## 本仓职责

Lode 负责站点知识、capability package、workflow package、schema、fixtures、post-check、asset registry、版本、失效标记和平台/用户资产边界。

Lode 不选择 Runtime Session，不保存真实账号状态或生产运行现场。

## 路线原则

- GitHub Milestone 必须能映射到本文的阶段路线和组织级 ROADMAP。
- Lode 的 milestone 优先形成可被 Core 准入和校验的能力资产合同。
- 资产格式可以先本地化和包级化，不提前承诺 hosted marketplace 或 sync service。
- 平台资产和用户 overlay / fork / draft 必须保持边界清楚。
- 涉及当前 milestone 的 pending decision 必须先在 `docs/adr/pending-decisions.md` 标明阻塞级别。

## 阶段路线

### 组织阶段一投影：边界清晰

Lode 明确自己是能力资产 truth source，不是浏览器 runtime、Core 执行器或 App Shell。

可创建 milestone 的主题：

- Lode 边界和 ADR 治理。
- capability / workflow / supporting asset 类型边界。

### 组织阶段二投影：合同可执行

Lode 的第一优先级是提供 Core 可准入、可校验、可版本引用的最小能力包合同。

可创建 milestone 的主题：

- capability package minimum format v0。
- input / output schema 和 resource requirements v0。
- fixtures、post-check 和 failure classification v0。
- package validator v0。

阶段二完成前，不应创建依赖完整 registry、marketplace 或 hosted sync 的 milestone。

### 组织阶段三投影：能力可复用

Lode 让网站经验变成可安装、可版本化、可测试、可失效、可修复的能力资产。

可创建 milestone 的主题：

- asset registry local v0。
- version / invalidation / rollback semantics。
- platform asset 与 user overlay / fork / draft。
- starter site packages 和脱敏 fixtures。

### 组织阶段四投影：运行可恢复

Lode 为 Core 和 App 提供 post-check、failure classification、repair hint 和失效标记。

可创建 milestone 的主题：

- failure-to-repair mapping。
- private invalidation 和 platform report boundary。
- repair draft lifecycle。

### 组织阶段五投影：产品可操作

Lode 支撑 App Library 的浏览、安装、锁定、更新、草稿、修复和上报体验。

可创建 milestone 的主题：

- catalog metadata for App filtering/search。
- asset install / lock / update semantics。
- Explorer draft to asset flow。

### 组织阶段六投影：生态可扩展

Lode 支持更多资产来源、团队协作、可选同步和公共贡献，但不破坏本地资产边界。

可创建 milestone 的主题：

- platform contribution review flow。
- optional sync / export。
- marketplace readiness，不作为默认 MVP 合同。

## 不进入 Lode 路线图

- Harbor Profile、Runtime Session、Viewer、CDP、VNC 和 provider driver。
- Core Run Record、Admission、Action Risk 和执行状态机。
- App Shell 和 UI truth。
- 真实账号、Cookie、token、完整请求响应、用户业务数据或未脱敏执行现场。

## Milestone 创建检查

创建 Lode milestone 前必须确认：

- 对应组织级 ROADMAP 阶段。
- 对应的 Lode 阶段路线主题。
- 是否改变 Core 可消费的 package/schema 合同。
- 是否有 `Milestone blocker` 或 `FR blocker` pending decision。
- 是否维护平台资产与用户个人资产边界。
