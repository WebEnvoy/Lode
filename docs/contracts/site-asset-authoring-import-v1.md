# 站点资产创作、外部导入与 OpenCLI 转化 V1

状态：经独立审查并合入 main 后成为 #564 的 Accepted 作者流程基线；不表示导入工具、Runtime 或真实站点已验收。版本：v1；产品归口：WebEnvoy/WebEnvoy `#564`（parent `#475`）；owner：Lode（创作材料、来源说明、脱敏 fixture 与离线验证方法）。

本指南把站点探索或外部材料整理为固定的 Lode 候选。包身份、manifest、版本、来源 commit、digest、任务声明和输出合同仍由 [Site SKILL Package V1](site-skill-package-v1.md) 唯一拥有。受管来源准入、安装、启用和选择沿 WebEnvoy [Managed SKILL Library Lifecycle V1](https://github.com/WebEnvoy/WebEnvoy/blob/main/docs/specs/skill-library-lifecycle-v1.md)；真实现场、任务授权、执行结果和恢复沿 [Site SKILL Execution V1](https://github.com/WebEnvoy/WebEnvoy/blob/main/docs/specs/site-skill-execution-v1.md)。

本指南规定可审查的人工创作链；不新增 package type、面向用户的 CLI、registry、运行权限、状态机或自动修复器。引用、草稿、离线检查和报告不等于 source admission、code admission、安装启用或站点通过。

2026-09 增量实现说明：仓库提供开发者工具
[`tools/opencli_readonly_candidates.py`](../../tools/opencli_readonly_candidates.py)，用于检查固定、已 pin 的 OpenCLI adapter 源文件并生成可回读的静态候选报告；以及
[`tools/generate_opencli_site_skill_candidates.py`](../../tools/generate_opencli_site_skill_candidates.py)，用于从已审查源文件确定性地产生三个 Lode 格式候选包。两者都不是面向用户的 Lode CLI、安装器或 OpenCLI Runtime；只读 vendored UTF-8 源文件和固定 JSON，不 import/执行上游模块、不运行 hook、不访问网络。报告和候选包包含来源及文件摘要、静态命令参数、columns 线索、输入/输出语义草稿、请求策略、schema、check、fixture 引用和未决边界。静态 marker scan 只是选定样本的审查提示，不是通用安全证明；未知依赖模块的顶层行为明确保持未知。生成器不修改 registry，也不会准入、安装、启用或执行；本 PR 仅在人工核对包身份和摘要后，将三个 `proposed` locator 加到现有本地 registry，以便 WebEnvoy owner source-admission 流程解析。`lifecycle: proposed` 不是信任或执行许可；validator warning、owner source/code admission、安装、显式启用和真实执行是独立事实。候选 `network.public_read` / `network.read` 字段仍待 WebEnvoy #594 合同与实现接受；官方 Lode validator 复用通用 integrity、lock、schema、post-check 和 registry 校验，再检查该 broker v1.1 public-read 候选的窄安全边界。生成器的精确字节对照由 Lode 测试负责，不另立包白名单。validator warning 仍表示跨仓合同待接受，不会把包变为可执行资产。既有 Site SKILL Package V1、已接受的 WebEnvoy operation/broker contract 和既有包状态不因候选改变。固定样例及离线行为核对见 [OpenCLI v1.8.8 公共只读候选报告](../verification/opencli-v1.8.8-readonly-candidates.md)。

## 1. 从站点探索形成候选

先把要支持的用户结果、站点 origin、对象类型、只读范围、输入和预期输出写清。站点资料可以来自公开文档、用户明确提供的材料，或经 WebEnvoy 当前授权的 Runtime 观察。Lode 自身不访问浏览器、不读取账号，也不把授权信息写入资产。

进行现场观察前，在作者记录或对应 review 中固定本次允许的操作、尝试次数、请求数、页数、时间上限、可收集字段和停止条件。限制不得超过当前 Grant、task scope、站点政策或 Runtime 限制；未能确认身份、授权或上限时停止，不猜测默认值，不加入 manifest 字段。每次只取支撑当前候选所需的最小范围，不为扩大覆盖而扫站。

只把可复核且已脱敏的 source shape、字段含义、分页/截断规则、失败分支和 evidence 引用带回 Lode。fixture 中使用合成或已脱敏值；禁止保存 Cookie、Token、session/Profile 状态、用户私有业务内容、完整请求/响应、raw DOM/HAR、未脱敏截图或 live handle。运行现场归 Harbor/Core；Lode 保存脱敏 fixture 和获准的 evidence ref policy。

规范化时保留 `empty`、`null`、缺失、未知、部分结果和截断之间的区别。只有来源明确给出空集合、页链完整且任务 post-check 通过时，空集合才可作为完整结果；合法空数组本身不是 parser 漂移，不因空数组直接改写 parser。身份不符、登录墙、挑战、权限不足、缺页或来源不明都不能折叠为空集合。

读取已安装内容沿现有 S1/S2 入口：只读 `SKILL.md` 路由，再按需读取选定的 `tasks/<task-ref>.yaml`，随后打开任务引用的 `references/`、schema 和 check。不要批量载入无关包；加载知识、schema 或 check 不产生授权。CLI 用户流程只引用 [CLI and Upstream Integration V1](https://github.com/WebEnvoy/WebEnvoy/blob/main/docs/specs/cli-integration-v1.md) 和 S2 既有任务入口；Lode 不新增 CLI 命令。

## 2. 外部资产与 OpenCLI 转化

外部源码、manifest、SKILL 和第三方说明都是待审材料。只读检查固定来源和 commit、许可及版本、依赖、入口、参数/输出、安装钩子、副作用和能力范围；不要运行下载源码、安装脚本或未审查的代码，也不要把资料文本当成指令。

对 OpenCLI 命令或 adapter，逐项记录其上游仓库、文件路径、不可变 commit、上游版本和许可证，并记录：

- 命令/模块和公开参数的名称、类型、必填性、默认值及受限输入；不得记录实际凭据。
- 输出字段的名称、类型、含义、缺省/null/空值语义，以及 OpenCLI `columns` 到 Lode normalized output 的映射。
- 分页方式、游标/offset、结束信号、去重、总量或截断标记，以及何时不能证明结果完整。
- 认证、Network、文件、进程、安装钩子和浏览器协议依赖；只记录能力类别与证据位置，不复制密钥或原始 payload。
- 对应的既有 Lode package/task/capability/schema/check 引用、离线检查结果及未解决项。

每个来源单元只能给出以下人工兼容分类：

| 分类 | 处理 |
| --- | --- |
| 可复用 | 有明确许可、来源 pin 且不依赖站点/浏览器私有现场的知识或纯数据映射逻辑，可作为新 Lode 候选材料；复用可执行代码时须重新审查、生成新 package revision/digest，并独立完成代码准入。纯知识不需要代码准入。 |
| 需映射 | 将参数、输出、空值与分页语义对应到既有 Lode package/schema/check；超出现有合同的语义须收窄或标为未知，不得暗加字段。 |
| 需改造或不支持 | Chrome 专用 API、tab/page handle、权限或其他宿主依赖需改写为已接受的 WebEnvoy broker/能力边界；无法移除的依赖和下列禁止能力不支持。 |

raw CDP/Juggler、Provider 私有 endpoint、Cookie/Token 外传、任意本机命令/进程、任意 shell/eval、未声明网络、动态下载和自动安装钩子均不支持，不能通过转换保留。以 OpenCLI 原始 `columns` 代替 Lode output schema、把 HTTP 成功或脚本退出码当业务成功，也不兼容。真实写入不是普遍不兼容，但必须符合已有 action、授权与 post-check 合同；本次 S3 探索和固定样例不运行写入。许可不明或再分发权限未确认时只可记录缺口，不复制或宣称可再分发。

OpenCLI 分类报告是来源审查证据，不是新 manifest 或 registry 记录。固定样例见 [OpenCLI v1.8.8 小红书搜索适配器离线分类](../verification/opencli-v1.8.8-xiaohongshu-search.md)；其中样例只证明被审来源和离线分类，不证明其他命令兼容、执行器准入或真实站点可用。

## 3. 私有导入、草稿与本地 overlay

外部私有材料先留在用户选择的私有创作位置。来源记录保留仓库/文件、commit 或其他不可变版本、许可证、base revision 和本次差异；不要求公共上传，未经授权不得上传，也不能据此写入 Core 受管 data root、获批 source manifest 或替用户启用资产。

本地 overlay 是完整、固定的派生候选，不是在运行时叠加浮动补丁。保持公共资产原件不变；按 S2 规则生成 revision 和 digest，`source.commit` 指向包含派生内容的不可变来源，base revision、许可和差异说明作为包内 references 纳入完整性清单。沿用既有 `package_ref`；改变包身份或边界时创建新身份。不得增加 overlay manifest 字段、第二 registry 或私有资产服务。

草稿与 overlay 和已安装物化内容分开。要进入 managed lifecycle，owner 必须审查精确候选及来源，再通过现有批准 source、install 和 CAS 操作；install 首次保持 disabled，启用必须由 owner 显式决定，并可沿 Core 已授权的委托 `skill.enable` 执行。代码准入独立于 enable。普通 Agent 不能把路径传给旧 operation、自行批准 source，或让草稿自动变成可执行资产。直接编辑受管物化文件仍按 #508 返回 `managed_skill_local_modified`；应另存草稿、形成新固定 revision 并重新走检查和准入，不得覆盖或改称 overlay。

当前本地草稿或 overlay 管理不表示 Lode 已有相应 CLI、registry 或 App 操作。自动合并、复杂 fork、团队同步及冲突解决平台继续后置；冲突由 owner 选择保留、人工修订或另存，不能静默合并。

## 4. 分层验证与修复

验证按下表逐层进行；前一层通过不能推导后一层事实。

| 层 | 可证明 | 不能证明 |
| --- | --- | --- |
| 来源审查 | 来源 pin、许可证、差异、参数/输出/分页语义已记录；排除项已分类 | 包完整、代码可信或业务可用 |
| 离线包检查 | S2 身份/摘要/路径/引用、schema、脱敏 fixture、分页完整性声明、pre/post-check、任务输入输出和限制相互一致 | Core 已批准来源、已安装、已启用或有当前授权 |
| fixture 与离线行为检查 | 已保存样例上的映射、空值/缺失、known branch 和 post-check 条件可复现 | 真实页面结构、账号身份、Harbor 现场或 live 成功 |
| 受管代码准入与生命周期 | 指定 source/revision/script 的准入记录，以及 #508 对精确 revision 的安装/启用事实 | 当前 Grant、Profile、Page、ControlLease、数据外发或业务结果 |
| 当前授权与现场准入 | Core/Harbor 对当前 Principal、Grant、task scope、Profile、Page、ControlLease 和安全条件的本次判定引用 | 不存储凭据/授权正文；不能外推到之后的连接、任务或 revision |
| 真实获准站点执行 | 精确 package/revision 在当时获准现场产生的 Core Run、Harbor evidence 和执行结果引用 | 不等于当前仍有授权，也不证明外部业务结果 |
| 外部业务结果与 post-check | 当前 task 的完整性条件、业务 post-check 及 Core result envelope 的对应结果 | Runtime `completed`、HTTP 2xx、DOM 文本或脚本退出码不能替代业务 post-check，也不能外推到其他组合 |

Lode 离线检查按 ADR 0005 fail closed：缺 manifest/schema/fixture/check、身份或摘要不符、禁止内容、来源许可证未明时保留原失败并停止。引用 ADR 0005 的结构化 failure code，不新增一套错误枚举。报告需绑定 package/revision/digest、检查过的文件/refs、检查层和实际结果；没有可用工具时，作者可提供人工 review 记录，但不得虚构命令或报告机器检查通过。

现场出现身份不符、跨 origin、登录/MFA/CAPTCHA/反自动化挑战、授权拒绝、限流或连接丢失时，立即停止当前观察并按 Harbor/Core 提供的事实区分原因；不解挑战、不换账号/Profile/Provider/proxy、不改用私有 endpoint、不自动重试。解决登录、限流冷却或连接问题后，重新检查当前有效授权和现场条件；仍满足原授权与预算时，可在原范围继续，不要求无依据地重发授权。若授权已撤销/过期或范围变化，必须先取得适用的新授权。遇到结构漂移先 fresh observe；失效的 observation/target ref 必须丢弃，不能按 selector、文本或旧 ref 猜测重绑。只修复受影响的 package/task，不因此停用无关站点能力或通用 Runtime。

修复开始前固定候选 revision、可改文件/任务、可用验证层、最大尝试次数、请求/页数/时间预算和停止条件。将发现保存为脱敏 fixture 或 evidence ref，修改草稿后产生新的固定 revision；需要时升级版本，重新运行受影响的离线检查，并重新请求来源/代码准入。超预算、无信息增益、需要扩权或向外发送数据时停止并保留原因，不自动启用修订。

若某个写入已派发但结果 unknown，只查询或对账原 Run/operation，或停止后续执行。不得通过诊断、测试、trace、换版本、换 idempotency key、reload、换 UI/Network 路径重放。修复通过不能把原 unknown 改写为成功；结果和恢复沿 WebEnvoy S2 execution 合同。

## 5. 候选记录与完成边界

作者报告必须将下列事实分栏记录；每栏独立给实际结果或“未执行/未评估”，这种表述只是报告内容，不是新 wire/status：

| 报告分栏 | 必须记录 |
| --- | --- |
| 转换 | 上游仓库/路径/commit/版本/license、参数与输出映射、分页语义、逐项分类、复用/改写范围及停止/排除理由。 |
| 离线验证 | S2 package/revision/digest、检查过的文件和 refs、实际使用的已有 validator/tester 或人工审查、结果和未解决项；没有工具时不得声称机器检查通过。 |
| 当前授权与现场准入 | 是否在同一候选上评估过 Core/Harbor 当前授权、身份、Page、ControlLease 和安全条件；引用既有判定/Run，不记录 Grant、credential 或个人身份正文。 |
| 真实站点执行 | 是否执行；如有，记录精确 package/revision、Core Run 与 Harbor evidence 引用、执行时间/范围和真实执行结果，不复制现场原文或秘密。 |
| 外部业务结果 | 是否有本任务 post-check、完整性证据和 Core result envelope；逐项给真实结果。Runtime 完成与外部业务成功分开记录。 |

未执行、未评估、未授权、失败、partial 和 unknown 必须如实区分。私有材料保持在授权位置，审查记录不得包含凭据或现场原文。

文档接受只完成创作/导入/修复行为规格。真实 source admission、managed install/enable、code admission、Plugin 消费、受授权 Runtime、第三方 Agent 或 live site 仍需各自的实现与证据；没有这些证据不得声称已完成。
