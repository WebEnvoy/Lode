# 仓库指南

## 项目结构与模块组织

本仓库是 `WebEnvoy/Lode`，负责站点知识、站点能力、原子动作、任务封装和模板资产。当前文档位于 `README.md` 和 `docs/`；后续资产建议按以下方向组织：`schemas/` 放包格式和能力 Schema，`sites/` 放站点知识与站点能力，`tasks/` 放任务封装，`templates/` 放官方模板，`fixtures/` 放脱敏测试样例，`tools/` 放校验、打包和测试工具。

## 构建、测试与开发命令

当前尚未初始化 `package.json`。新增工具后，优先统一为：`pnpm install` 安装依赖，`pnpm validate` 校验包和 Schema，`pnpm test` 运行测试，`pnpm lint` 检查格式，`pnpm build` 打包资产。新增命令必须写入 `package.json` 并同步 README 或 `docs/`。

## 代码风格与命名规范

本仓库以 JSON / YAML / Markdown 为主，TypeScript 只用于 validator、packer、tester 和 registry tooling。站点目录使用稳定 slug，例如 `sites/xiaohongshu/`；能力 ID 使用小写短横线，例如 `publish-note`、`read-comments`；任务封装使用业务中性命名，例如 `collect-details`。Markdown 用于说明，正式执行依赖应落到结构化 Schema。

## 测试指南

测试应覆盖 schema validation、package validation、fixture validation、capability dry-run tests 和 Markdown link check。测试样例必须可脱敏复现，不依赖真实账号、真实会话或私有业务数据。新增站点能力至少提供最小 fixture、输入输出示例、前置检查和后置验证说明。

## 提交与 Pull Request 规范

提交信息使用 Conventional Commits，例如 `docs: refine capability model`、`feat: add site package schema`。PR 需要说明新增或修改的站点、能力、任务封装、Schema 版本和验证结果。修改包格式时必须说明兼容性影响；新增能力时必须列出资源需求和已知限制。

## 架构与 Agent 专项说明

Lode 只维护资产定义、测试样例、版本和失效标记，不负责运行时执行。WebEnvoy Core 解释并执行 Lode 资产；Harbor 提供 Profile、Execution Identity、Runtime Session、CDP / VNC 和 Evidence。任务封装不应依赖某个具体 Runtime 实现，也不应硬编码 Harbor 内部细节。

## 安全与数据处理

不要提交真实凭据、会话状态、未脱敏执行现场、用户私有任务参数或真实业务客户数据。站点能力不应包含账号投放、内容排期、客户运营或广告决策等业务策略；这些属于上游系统。
