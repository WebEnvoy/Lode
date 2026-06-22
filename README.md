# Lode

Lode 是 WebEnvoy 的站点知识、站点能力、任务封装与模板资产库。

它为 WebEnvoy Core 提供可复用的网站能力资产；WebEnvoy Core 解释这些资产，并通过 Harbor 获取执行身份与浏览器 Runtime 来完成真实网站读写任务。

## 仓库角色

Lode 负责沉淀和维护：

- 站点知识；
- 站点能力；
- 原子动作；
- 任务封装；
- 官方模板；
- 能力测试样例；
- 能力版本与失效标记。

## 文档

- [定位](docs/positioning.md)
- [能力模型](docs/capability-model.md)
- [站点包格式](docs/site-package-format.md)
- [任务包格式](docs/task-package-format.md)
- [贡献模型](docs/contribution-model.md)

## 相关仓库

- `WebEnvoy/WebEnvoy`：站点能力执行与编排层，包含 Core、API Server、SDK、CLI、MCP 和 Console；
- `WebEnvoy/Harbor`：Agent-ready 指纹浏览器 / Profile Runtime / 执行身份浏览器；
- `WebEnvoy/research`：组织级研究、调研、对比和决策候选仓库；
- `WebEnvoy/.github`：组织主页、issue 模板、PR 模板和社区配置。

## 状态

项目处于初始化阶段，Schema、目录结构和能力描述格式仍在收敛中。

## 许可证

本仓库采用 MIT License。
