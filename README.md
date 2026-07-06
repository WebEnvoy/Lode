# Lode

Lode 是 WebEnvoy 的能力资产仓库。

它把网站经验、站点能力、站点级清洗与归一化规则、任务模板和测试样例沉淀为可安装、可版本管理、可测试、可修复、可复用的能力资产。

WebEnvoy Core 解释并执行 Lode 资产；WebEnvoy App 在 Library（资产库）区域提供浏览、安装、配置、调试、探索、维护和上报入口；Harbor 提供执行身份、浏览器运行环境和运行现场。

## 一句话定位

Lode 是 WebEnvoy 的网站能力资产真相源。

## 仓库角色

Lode 负责沉淀和维护：

- 站点知识；
- 站点能力；
- 原子动作；
- 任务封装；
- 能力输出契约、来源结构定义（`source schema`）、字段映射、归一化器（`normalizer`）和归一化结果结构定义（`normalized result schema`）；
- 官方模板；
- 能力测试样例；
- 能力版本与失效标记。

这些资产可以被 WebEnvoy Core 执行，也可以在 WebEnvoy App 的 Library（资产库）区域中被人类用户浏览、安装、配置、调试和维护。

## 资产边界

Lode 需要同时支持平台资产和用户个人资产。

平台资产是官方或公共分发的站点知识、能力包、任务模板、测试样例、版本和失效标记。用户可以按需安装、更新、锁定和回滚，但不应直接改写官方资产本体。

用户个人资产是用户或团队私有的能力修改、任务模板、覆盖层（overlay）、分叉版本（fork）、探索草稿、修复草稿和私有测试样例。它们应支持版本管理、差异对比、回滚、导出、可选同步和可选提交为公共贡献。

推荐关系：

```text
平台资产
  └── 用户 overlay / fork / draft
```

## 与 App / Core / Harbor 的关系

- WebEnvoy App 负责 Library（资产库）工作台，提供资产浏览、安装、配置、探索、修复和上报入口；
- WebEnvoy Core 负责解释和执行 Lode 资产，并记录任务运行事实；
- Harbor 负责浏览器身份、运行会话、查看器、人工接管和运行证据；
- Lode 负责站点知识、能力包、任务模板、输出契约、归一化器（`normalizer`）、测试样例、版本和失效标记。

Lode 不管理浏览器运行现场，不保存账号凭据、会话状态、具体任务输入、真实生产原始载荷、用户业务客户数据或未脱敏执行现场。它定义并版本化能力结果的公共形态，以及从站点原始来源到公共结果的抽取（extraction）、解析（parsing）、映射（mapping）和归一化（normalization）规则；WebEnvoy Core 负责运行时调用、校验、投影和封装，Harbor 负责提供证据引用（`evidence_ref`）、原始载荷引用（`raw_payload_ref`）和来源轨迹（`source_trace`）。

## 文档

- [愿景](VISION.md)
- [路线图](ROADMAP.md)
- [架构决策记录](docs/adr/0001-record-architecture-decisions.md)
- [小红书与 BOSS 站点知识吸收边界](docs/adr/0006-xhs-boss-site-knowledge-selection.md)
- [小红书只读能力包合同](docs/contracts/xiaohongshu-read-capabilities.md)
- [BOSS 直聘只读能力包合同](docs/contracts/boss-read-capabilities.md)
- [真实页面写前验证能力合同](docs/contracts/write-precheck-capabilities.md)
- [bb-sites 小红书与 BOSS 吸收冻结](docs/contracts/bb-sites-xhs-boss-absorption-freeze.md)

## 本地校验

当前最小校验器命令行使用 Python 标准库，离线校验单个能力包（capability package）的
清单（manifest）、结构定义、固定样本数据、后置检查、失败映射和仓库本地登记表（repo-local registry）
引用，不访问真实账号、
浏览器运行环境、Core、Harbor 或 App：

```bash
python3 tools/lode_validate_package.py sites/example/read-public-page --json
```

仓库内存在 `registry/local-packages.json` 时，校验器会自动检查该本地索引中的
能力包引用（package ref）、版本、清单路径和资产角色解析。也可以显式传入索引：

```bash
python3 tools/lode_validate_package.py sites/example/read-public-page --registry-index registry/local-packages.json --json
```

也可以从仓库本地登记表批量校验所有能力包条目：

```bash
python3 tools/lode_validate_package.py --registry-index registry/local-packages.json --all --json
```

样例能力包还包含 `package-lock.json`，用于固定能力包引用、能力 ID、
版本、锁定资产版本和失效触发条件。该文件只是本地可校验合同，不表示 App
安装/更新、托管登记表、Core 运行记录或运行环境执行已经实现。

## 小红书只读能力包

当前小红书真实站点只读包包括：

- `sites/xiaohongshu/search-notes`：声明登录态、页面就绪、搜索输入/输出、
  搜索结果字段来源、笔记链接和后续详情引用。
- `sites/xiaohongshu/read-note-detail`：声明签名笔记 URL 输入、详情输出、
  标题、作者、正文摘要、互动指标和来源引用。

这两个包只提供 Lode 可校验资产、脱敏固定样本、post-check 和失败分类。真实
页面验证需要人工拥有的已登录小红书浏览器现场，当前标记为
`pending_human_runtime`；本仓不保存账号状态、运行会话、原始页面、网络载荷或
生产证据。

## BOSS 直聘只读能力包

当前 BOSS 直聘真实站点只读包包括：

- `sites/boss/job-search`：声明已登录求职者身份、页面就绪、搜索输入/输出、
  职位列表字段来源、`securityId` 和后续详情引用。
- `sites/boss/read-job-detail`：声明详情 URL 与 `securityId` 输入、职位详情输出、
  职位描述、薪资、地点、公司和招聘者摘要。

这两个包只提供 Lode 可校验资产、脱敏固定样本、post-check 和失败分类。真实
页面验证需要人工拥有的已登录 BOSS 直聘浏览器现场，当前标记为
`pending_human_runtime`；本仓不保存账号状态、运行会话、原始页面、网络载荷或
生产证据。

## 真实页面写前验证能力包

当前真实页面写前验证包包括：

- `sites/xiaohongshu/publish-note-precheck`：声明小红书创作中心发布页和内容编辑目标，
  输出预期变更、风险提示、页面要求和不发布边界。
- `sites/boss/greet-precheck`：声明 BOSS 职位或招聘者沟通目标，输出打招呼内容预览、
  目标引用、风险提示和不发送边界。

这两个包只做 `validate_only` 写前验证，支持 Core/App 消费静态结构定义、脱敏固定样本、
post-check、失败分类和仓库本地登记表结果。它们不执行保存、上传、发布、投递、
打招呼或发送消息；真实页面验证仍需要人工拥有的已登录浏览器现场。

## 首个样例只读能力包

当前首个低风险只读样例是
`sites/example/read-public-page`，对应能力包引用
`lode://site-capability/example/read-public-page@0.1.0`。它使用保留的
public Example Domain 内容和仅摘要脱敏固定样本数据，清单中的
`sample_read_package` 记录选择理由、固定样本数据绑定和 Core 后续可消费入口。
GH-102 补充了
`sites/example/read-public-page/fixtures/core-consumption.fixture.json`，作为 Core
准入/结构定义校验可直接读取的仓库本地固定样本数据。它只绑定
能力包引用、锁定文件、结构定义、固定样本数据、后置检查和失败映射路径，不表示
Core 运行环境执行、Core 结果信封、稳定准入或任何写能力已经实现。
GH-103 补充了 `sites/example/read-public-page/write-deferred-guardrail.json`，
用于声明 `validate_only`、`draft`、`preview` 和 `write` 仍处于 deferred/blocked 边界；
校验器只做离线形态与默认失败关闭检查，不执行或授权任何写侧动作。

报告输出 `status`、`errors[]`、`warnings[]` 和 `checked_refs[]`。在 GH-97
交付后，样例能力包的后置检查资产只声明输出格式、成功条件和
来源/证据引用绑定；校验器不执行浏览器运行环境，也不生成 Core 运行结果。

## 许可证

本仓库采用 [MIT License](LICENSE)。
