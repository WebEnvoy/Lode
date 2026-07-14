# 仓库指南

## 项目结构与模块组织

本仓库是 `WebEnvoy/Lode`，负责站点知识、站点能力、原子动作、任务封装和模板资产。当前文档位于 `README.md` 和 `docs/`；后续资产建议按以下方向组织：`schemas/` 放包格式和能力 Schema，`sites/` 放站点知识与站点能力，`tasks/` 放任务封装，`templates/` 放官方模板，`fixtures/` 放脱敏测试样例，`tools/` 放校验、打包和测试工具。

## 构建、测试与开发命令

当前尚未初始化 `package.json`。新增工具后，优先统一为：`pnpm install` 安装依赖，`pnpm validate` 校验包和 Schema，`pnpm test` 运行测试，`pnpm lint` 检查格式，`pnpm build` 打包资产。新增命令必须写入 `package.json` 并同步 README 或 `docs/`。

当前技术架构基线是 docs-only；不得为了文档基线 PR 初始化 `package.json`、安装依赖、创建 CLI、生成 schema、创建 fixture、写 validator/packer/tester/registry 代码或提交工具输出。

## 代码风格与命名规范

本仓库以 JSON / YAML / Markdown 为主，TypeScript 只用于 validator、packer、tester 和 registry tooling。站点目录使用稳定 slug，例如 `sites/xiaohongshu/`；能力 ID 使用小写短横线，例如 `publish-note`、`read-comments`；任务封装使用业务中性命名，例如 `collect-details`。Markdown 用于说明，正式执行依赖应落到结构化 Schema。

## 技术架构基线约束

- [ADR 0005](docs/adr/0005-lode-technical-architecture-baseline.md) 是当前技术基线入口；后续 package/schema/tooling Work Item 先引用它，再细化真实文件和命令。
- JSON / YAML / Markdown 是 Lode 资产主载体；JSON Schema 是正式结构化合同载体，Markdown 只能说明和索引。
- TypeScript 只用于 offline validator、packer、tester 和 local registry tooling；不得把 Lode tooling 做成 runtime runner、browser automation runner、Core executor 或 App UI。
- validator 只校验 manifest、JSON Schema、fixture、post-check、local registry 和引用完整性；不得连接生产 runtime、读取真实账号、匹配 live Harbor facts 或执行真实写入。
- packer 只打包已通过本地校验的资产；local registry tooling 只做本地索引和引用验证。hosted registry、marketplace、team sync 和 public contribution review 不得提前塞进 v0 tooling。
- manifest 描述身份、版本、生命周期、资源需求和引用；schema 描述 input/output/source/fixture/post-check shape；fixture/post-check 用于验证，不是 live evidence store。
- 任何能力包、fixture、post-check、normalizer 或 registry 文件不得包含 Cookie、Token、profile state、runtime session、live tab、raw evidence body、完整 DOM/HAR/screenshot、生产 payload 或用户业务数据。
- 修改技术基线时只改当前 Work Item 直接需要的 docs / contracts / AGENTS 与宿主 PR 元数据；不要顺带重排路线图、创建代码骨架或扩大到其他仓。

## 测试指南

测试应覆盖 schema validation、package validation、fixture validation、capability dry-run tests 和 Markdown link check。测试样例必须可脱敏复现，不依赖真实账号、真实会话或私有业务数据。新增站点能力至少提供最小 fixture、输入输出示例、前置检查和后置验证说明。

docs-only 基线 PR 的最小验证是 `git diff --check`、Markdown/JSON 可读性检查以及 PR body/head readback；只有引入真实 code/schema/runtime/fixture/tooling 行为时才升级到对应测试命令。

## 提交与 Pull Request 规范

提交信息使用 Conventional Commits，例如 `docs: refine capability model`、`feat: add site package schema`。PR 需要说明新增或修改的站点、能力、任务封装、Schema 版本和验证结果。修改包格式时必须说明兼容性影响；新增能力时必须列出资源需求和已知限制。

## 架构与 Agent 专项说明

Lode 只维护资产定义、测试样例、版本和失效标记，不负责运行时执行。WebEnvoy Core 解释并执行 Lode 资产；Harbor 提供 Profile、Execution Identity、Runtime Session、CDP / VNC 和 Evidence。任务封装不应依赖某个具体 Runtime 实现，也不应硬编码 Harbor 内部细节。

## 路线图 / 里程碑 / 功能需求 / 工作项

- 跨仓长期方向以 `WebEnvoy/.github/ROADMAP.md` 为准。
- 当前执行状态以 GitHub Milestones、Project、issues 和 PR 为准，不在仓库文档中复制维护。
- GitHub Milestone 只承载当前 1-3 个可交付阶段，不承载全部远期设想。
- 功能需求（FR）issue 表达用户可见或系统可验证的能力增量。
- 工作项（Work Item）issue 是可由一个 PR 完成的最小执行单元。
- 新建功能需求或工作项前，先确认它属于当前活跃 Milestone；不属于则回到总 ROADMAP 或 backlog。
- 创建或调整 Milestone、功能需求或工作项前，先检查本仓 `docs/adr/pending-decisions.md`；会阻塞当前事项的决策必须链接到 issue，并标明阻塞级别：`Milestone blocker`、`FR blocker`、`Work Item blocker`、`Spec detail` 或 `Deferred`。
- 被决策阻塞的 issue 使用 `status: needs-decision`；决策完成后必须回写对应 ADR 或 `docs/adr/pending-decisions.md`，再继续拆分或实施。
- 仓库级 `ROADMAP.md` 是组织级 ROADMAP 的本仓投影，只能说明本仓如何服务总路线，不能新增跨仓阶段、重定义目标状态或覆盖组织级边界。
- 除仓库级 `ROADMAP.md` 外，单仓 planning 文档只能解释本仓如何服务当前活跃 Milestone，不能新增跨仓 Milestone。
- 不允许在单仓创建与总 ROADMAP 冲突的平行路线图。
- 规格文档只服务当前或下一个活跃 Milestone，不提前铺满远期设计。
- 涉及跨仓方向、阶段阶梯或边界调整时，先更新或评审总 ROADMAP / 跨仓架构，再拆单仓事项。

## 安全与数据处理

不要提交真实凭据、会话状态、未脱敏执行现场、用户私有任务参数或真实业务客户数据。站点能力不应包含账号投放、内容排期、客户运营或广告决策等业务策略；这些属于上游系统。

<!-- LOOM_BOOTSTRAP_START -->
## Loom Execution

本仓库使用 Loom 编排 Work Item、build、review、merge-ready 与 host closeout。Loom
消费 GitHub 与工作现场事实，不用 repo current、progress、review、shadow 或 closeout
carrier 替代宿主真相。

开始改文件前：

1. 用 `loom route --target . --issue <issue> --json` 判断规划或执行入口。
2. 实现必须显式绑定 Work Item 与 issue-scoped branch；PR 创建前可直接运行
   `loom build --target . --issue <work-item> --branch <branch> --json`。
3. 一次只推进一个有界目标；不要创建空提交、空 PR 或治理载体来满足 admission。
4. PR 存在后再运行 `loom pre-review`、`loom review`、`loom merge-ready` 或 `loom ship`；
   这些入口从 GitHub readback 取得 branch、head、review、checks 与 merge 状态。
5. 验证证据记录命令、结果、时间或 head/run id；变更代码或 PR review 输入后重新确认
   current-head attestation 与 gate freshness。
6. merge 不等于产品完成；用 `loom attestation closeout` 消费宿主 closeout，用
   `loom release readback` 消费发布事实，不创建 closeout/current-retire PR。

环境或 provider 问题由 `loom doctor --target . --json` 分类；退役命令返回
`unsupported_command_surface`，不得通过 compatibility flag 恢复。
<!-- LOOM_BOOTSTRAP_END -->
