# Lode

Lode 是 WebEnvoy 的能力资产仓库。

它把网站经验、站点能力、站点级清洗与归一化规则、任务模板和测试样例沉淀为可安装、可版本管理、可测试、可修复、可复用的能力资产。

WebEnvoy Core 解释并执行 Lode 资产；WebEnvoy App 在 Library 区域提供浏览、安装、配置、调试、探索、维护和上报入口；Harbor 提供执行身份、浏览器 Runtime 和运行现场。

## 一句话定位

Lode 是 WebEnvoy 的网站能力资产真相源。

## 仓库角色

Lode 负责沉淀和维护：

- 站点知识；
- 站点能力；
- 原子动作；
- 任务封装；
- 能力输出契约、source schema、字段映射、normalizer 和 normalized result schema；
- 官方模板；
- 能力测试样例；
- 能力版本与失效标记。

这些资产可以被 WebEnvoy Core 执行，也可以在 WebEnvoy App 的 Library 区域中被人类用户浏览、安装、配置、调试和维护。

## 资产边界

Lode 需要同时支持平台资产和用户个人资产。

平台资产是官方或公共分发的站点知识、能力包、任务模板、测试样例、版本和失效标记。用户可以按需安装、更新、锁定和回滚，但不应直接改写官方资产本体。

用户个人资产是用户或团队私有的能力修改、任务模板、overlay、fork、探索草稿、修复草稿和私有测试样例。它们应支持版本管理、diff、回滚、导出、可选同步和可选提交为公共贡献。

推荐关系：

```text
平台资产
  └── 用户 overlay / fork / draft
```

## 与 App / Core / Harbor 的关系

- WebEnvoy App 负责 Library 工作台，提供资产浏览、安装、配置、探索、修复和上报入口；
- WebEnvoy Core 负责解释和执行 Lode 资产，并记录任务运行事实；
- Harbor 负责浏览器身份、Runtime Session、Viewer、人工接管和运行证据；
- Lode 负责站点知识、能力包、任务模板、输出契约、normalizer、测试样例、版本和失效标记。

Lode 不管理浏览器运行现场，不保存账号凭据、会话状态、具体任务输入、真实生产 raw payload、用户业务客户数据或未脱敏执行现场。它定义并版本化能力结果的公共形态，以及从站点 raw source 到公共结果的 extraction、parsing、mapping 和 normalization 规则；WebEnvoy Core 负责运行时调用、校验、投影和封装，Harbor 负责提供 evidence_ref、raw_payload_ref 和 source_trace。

## 文档

- [愿景](VISION.md)
- [路线图](ROADMAP.md)
- [架构决策记录](docs/adr/0001-record-architecture-decisions.md)

## 本地校验

当前最小 validator CLI 使用 Python 标准库，离线校验单个 capability package 的
manifest、schema、fixture、post-check、failure mapping 和 repo-local registry
引用，不访问真实账号、
浏览器 runtime、Core、Harbor 或 App：

```bash
python3 tools/lode_validate_package.py sites/example/read-public-page --json
```

仓库内存在 `registry/local-packages.json` 时，validator 会自动检查该本地索引中的
package ref、version、manifest path 和 asset role 解析。也可以显式传入索引：

```bash
python3 tools/lode_validate_package.py sites/example/read-public-page --registry-index registry/local-packages.json --json
```

sample package 还包含 `package-lock.json`，用于固定 package ref、capability id、
version、锁定资产版本和失效触发条件。该文件只是本地可校验合同，不表示 App
安装/更新、hosted registry、Core Run Record 或 runtime 执行已经实现。

## 首个 sample read package

当前首个低风险只读样例是
`sites/example/read-public-page`，对应 package ref
`lode://site-capability/example/read-public-page@0.1.0`。它使用 reserved
public Example Domain 内容和 summary-only 脱敏 fixture，manifest 中的
`sample_read_package` 记录选择理由、fixture 绑定和 Core 后续可消费入口。
该选择只表示 Lode 中已有离线可校验样例，不表示 Core fixture consumption、
runtime execution、stable admission 或任何写能力已经实现。

报告输出 `status`、`errors[]`、`warnings[]` 和 `checked_refs[]`。在 GH-97
交付后，sample package 的 post-check asset 只声明输出格式、成功条件和
source/evidence ref 绑定；validator 不执行浏览器 runtime，也不生成 Core 运行结果。

## 许可证

本仓库采用 [MIT License](LICENSE)。
