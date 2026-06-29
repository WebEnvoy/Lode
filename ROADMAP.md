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
- 能力成熟度按只读、写前验证、受控写入和多步 workflow 递进，不把完整生态能力前置。
- 涉及当前 milestone 的 pending decision 必须先在 `docs/adr/pending-decisions.md` 标明阻塞级别。

## 阶段路线

### 组织阶段一投影：用户任务与吸收边界

Lode 明确自己是能力资产 truth source，不是浏览器 runtime、Core 执行器或 App Shell；同时明确首批只读能力和写前验证边界。

可创建 milestone 的主题：

- Lode 边界和 ADR 治理。
- capability / workflow / supporting asset 类型边界。
- 首个低风险只读能力候选。
- validate-only、draft、preview 与真实写能力的资产边界。
- OpenCLI manifest、Syvert registry、旧 WebEnvoy XHS 能力、MediaCrawler 字段模型的裁剪吸收评估。
- marketplace、crawler queue 和 benchmark task contract 不作为 Lode MVP 合同。

### 组织阶段二投影：最小统一协议

Lode 的第一优先级是提供 Core 可准入、可校验、可版本引用的最小能力包合同。

可创建 milestone 的主题：

- capability package minimum format v0。
- input / output schema 和 resource requirements v0。
- fixtures、post-check 和 failure classification v0。
- package validator v0。

阶段二完成前，不应创建依赖完整 registry、marketplace 或 hosted sync 的 milestone。

### 组织阶段三投影：可信可引用运行现场

Lode 声明能力对 Harbor 运行现场和页面上下文的需求，但不保存真实账号状态或生产运行现场。

可创建 milestone 的主题：

- Snapshot / RefMap / evidence refs requirement。
- runtime facts 和 resource requirements 表达。
- locator fallback 与 post-check 引用边界。
- fixture 脱敏规则和现场数据禁止保存规则。

### 组织阶段四投影：最小只读任务闭环

Lode 提供首个低风险只读 capability package，让 Core 能准入、执行、校验并返回结构化结果。

可创建 milestone 的主题：

- low-risk read capability package v0。
- read input / output schema。
- read fixtures 和 post-check。
- failure classification v0。

### 组织阶段五投影：只读能力产品化

Lode 让只读网站经验变成可安装、可版本化、可测试、可失效、可修复的能力资产。

可创建 milestone 的主题：

- asset registry local v0。
- version / invalidation / rollback semantics。
- platform asset 与 user overlay / fork / draft。
- starter read packages 和脱敏 fixtures。
- failure-to-repair mapping 和 repair draft lifecycle。

### 组织阶段六投影：写前验证闭环

Lode 提供 validate-only、draft 或 preview 写能力包，表达预期变更、风险提示、资源需求和 post-check。

可创建 milestone 的主题：

- validate-only / draft / preview capability package。
- expected change schema。
- write-precheck resource requirements。
- preview post-check 和 failure classification。

### 组织阶段七投影：受控写入闭环

Lode 提供首批低风险真实写能力包，明确动作边界、幂等、写操作引用、post-check 和修复线索。

可创建 milestone 的主题：

- write capability action boundary。
- idempotency key requirement。
- write operation ref schema。
- post-check 和 repair hint。
- private invalidation 和 platform report boundary。

### 组织阶段八投影：可恢复多步读写工作流

Lode 提供多步 workflow package，让 Core 能在 step 级别记录、恢复、对账和归因。

可创建 milestone 的主题：

- workflow package v0。
- step-level post-check。
- step failure classification。
- recovery / repair hint mapping。

### 组织阶段九投影：日常产品与多入口稳定

Lode 支撑 App Library 的浏览、安装、锁定、更新、草稿、修复、上报和版本策略体验。

可创建 milestone 的主题：

- catalog metadata for App filtering/search。
- asset install / lock / update semantics。
- Explorer draft to asset flow。
- App / API 一致的 package metadata 查询。

### 组织阶段十投影：生态与协作扩展

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
- 是否服务当前组织阶段的纵向闭环，而不是只完成 Lode 横向资产格式。
- 是否改变 Core 可消费的 package/schema 合同。
- 是否有 `Milestone blocker` 或 `FR blocker` pending decision。
- 是否维护平台资产与用户个人资产边界。
