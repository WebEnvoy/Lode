# Site SKILL Package V1

状态：规范候选（`#563`，待本分支评审与合入）；版本：v1；产品归口：`#563`（parent `#475`）；owner：Lode（包身份、版本、来源、完整性、任务声明及包内知识资产）。

本文件冻结 Lode 提供给 WebEnvoy 的网站 SKILL 包合同。当前候选分支为
[`codex/spec-563-package`](https://github.com/WebEnvoy/Lode/tree/codex/spec-563-package)。WebEnvoy
的配套执行合同在候选分支
[`codex/spec-563-skill`](https://github.com/WebEnvoy/WebEnvoy/tree/codex/spec-563-skill)
的 [Site SKILL Execution V1](https://github.com/WebEnvoy/WebEnvoy/blob/codex/spec-563-skill/docs/specs/site-skill-execution-v1.md)。
这两个链接指向待评审候选，不能用来声称对应文档已经存在于 `main`。

本合同扩展 Lode 已接受的 site-capability 包边界，不替代
[ADR 0002](../adr/0002-capability-package-minimum-format.md)、
[ADR 0003](../adr/0003-schema-fixtures-and-post-check.md)、
[ADR 0004](../adr/0004-asset-types-and-registry.md)、
[ADR 0005](../adr/0005-lode-technical-architecture-baseline.md) 或
[ADR 0007](../adr/0007-capability-action-declaration.md)。这些 ADR 继续拥有既有
capability、schema、fixture、动作声明及本地 tooling 的语义；本文件只拥有
`site-skill` 包这一层。与 WebEnvoy 执行、Grant、Profile、Page、ControlLease、Run、
receipt、ExternalOutcome 或现场恢复有关的语义由配套执行合同及其引用的 WebEnvoy
合同拥有。

## 1. 用户结果与边界

安装一个经过确认的 site SKILL 后，Agent 可以发现包声明的正式任务，按同一版本的
知识、references、scripts 和 assets 运行，并获得可验证的输入、输出、验证和恢复
说明。包能让任务可发现，不让包本身取得授权、浏览器现场或业务成功。

以下事实始终分开判断：

1. 包内容是否完整、来源获准、版本兼容并通过 Lode 离线验证；
2. 包内 script 是否获得可信代码准入；
3. 包是否按现有受管 SKILL 生命周期安装、启用并固定 revision；
4. 当前 Principal、Grant、task scope、Profile ceiling、ControlLease 和 Runtime
   是否允许本次任务；
5. 任务是否被允许把数据交给某个外部主体；
6. 当前页面和业务对象是否满足包声明的 post-check，因此可以报告业务成功。

这六项不能由 `SKILL.md`、包版本、安装结果、API 授权或脚本退出码互相推导。

本合同不创建 Lode registry、网站任务 runner、通用 DSL、通用不受信代码沙箱、
第二个 Run/receipt 状态机或第二个权限系统。Lode 不在 Core/Harbor 进程内加载或
执行第三方代码。Lode 只声明包与其运行所需的引用；WebEnvoy 选择已接受的受管
执行位置并执行现有 Runtime 能力。

## 2. 所有权与术语

| 事实 | 唯一 owner | 其他组件的角色 |
| --- | --- | --- |
| `package_ref`、包版本、来源 commit/path、文件和包 digest、生命周期及兼容声明 | Lode | WebEnvoy 校验并记录已解析的引用，不改写 Lode 身份 |
| `SKILL.md`、references、scripts、assets、任务声明、输入/输出 schema 引用、pre/post-check、限制和 repair guidance | Lode | WebEnvoy 读取受授权的包元数据与已安装内容 |
| 安装、启用、更新、回滚、禁用、选择、历史和 receipt | WebEnvoy Core 的 [Managed SKILL Library Lifecycle V1](https://github.com/WebEnvoy/WebEnvoy/blob/main/docs/specs/skill-library-lifecycle-v1.md) | Plugin 只投影；Lode 不维护第二份安装状态 |
| Principal、Grant、task scope、Profile ceiling、当前连接、ControlLease、Run、idempotency、ExternalOutcome、unknown 和恢复 | WebEnvoy Core/Harbor 既有合同 | Lode 只声明所需 capability、动作和验证条件 |
| Page、Frame、document generation、observation/target ref、Provider 现场、实际文件/网络权限 | Harbor 与既有 Runtime 合同 | Lode 只能引用不透明 ref 和 capability |
| 正式任务执行入口及跨进程结果投影 | WebEnvoy 的配套 [Site SKILL Execution V1](https://github.com/WebEnvoy/WebEnvoy/blob/codex/spec-563-skill/docs/specs/site-skill-execution-v1.md) | Lode 声明任务输入、输出、脚本和验证要求 |

`package_ref` 是 Lode 的稳定逻辑身份；不可变的 `revision_ref` 指向其中一个完整
包版本。WebEnvoy 的受管 `skill_ref` 是生命周期投影，可以引用 `package_ref`，但
不成为包身份或内容摘要的第二 owner。任何 projection 与 Lode 摘要不一致都必须拒绝。

## 3. 包根、文件布局与信任边界

一个包根只能承载一个 `site-skill` 包；包根由单一 manifest 所在目录确定。建议的
最小布局如下，目录是包内相对路径，不代表本次创建这些资产：

```text
<package-root>/
  manifest.json                 # 唯一包 manifest
  SKILL.md                      # 面向 Agent 的路由和知识入口
  tasks/<task-ref>.yaml         # 正式任务声明，可引用已有 schema/check
  references/**                 # 脱敏知识、页面语义、限制和 repair notes
  scripts/**                    # 固定版本、可审查的源文件；不是任意 eval 输入
  assets/**                     # 脱敏静态材料；不是 live evidence 或用户数据
  schemas/**                    # 可选，本包拥有或引用的 JSON Schema
  checks/**                     # 可选，本包拥有或引用的 pre/post-check
```

布局规则如下：

- `manifest.json`、`SKILL.md` 和被 manifest 引用的文件必须是普通文件；禁止 symlink、
  `..` 越界、绝对路径和安装时脚本。未声明的文件不属于包。
- `SKILL.md` 是知识与任务路由文本，不是可信 DSL、权限声明或可执行入口。知识-only
  包可以被授权读取，但不能因此获得正式任务支持。
- `references/`、`assets/` 和示例必须脱敏。它们不能包含 Cookie、Token、密码、
  profile/session state、localStorage、真实账号、用户业务数据、完整请求/响应、
  未脱敏 DOM/HAR/screenshot 或 live tab/provider handle。
- `scripts/` 只能作为显式声明的固定 source asset。包不得携带 install hook、
  post-install command、动态下载、动态 import、任意 shell/JS/CDP/Juggler 文本或
  Provider 私有 endpoint。
- 任务声明可以引用 Lode 已有的 site-capability、schema、fixture、normalizer、
  pre/post-check 和 repair notes；不得复制 Core result envelope、Harbor evidence
  schema、Page/Session 内部结构或既有 capability 的 raw source shape。

### 3.1 Script 执行位置的最低合同

Lode 不提供 runner。凡 WebEnvoy 将一个已准入 script 送入运行时，配套 WebEnvoy 合同
至少要求以下 OS 边界；API 授权不能代替这些边界：

- script 只在 S1/Harbor 批准的受限 Agent-side OS 进程或等价 worker 中运行，且不在
  Core/Harbor 进程内加载或执行。OS identity、owner/control socket、文件和网络的
  role matrix 由 S1/Harbor 合同拥有；本文件不另造一套 Agent/owner 身份或授权系统。
- 包内容以只读方式提供；任务工作目录是受管、任务范围内的临时目录。script 只能
  读取包内声明文件和已有 capability 提供的不透明材料，写入只能经正式的临时材料、
  evidence 或结果引用，不得打开任意用户路径、Profile 目录、Lode checkout 或
  credential store。
- OS 文件权限必须拒绝未声明路径；经代码准入的 script 只能使用 S1/Harbor worker
  已明确允许的本机文件范围和正式 file/material capability。运行时不得把 Cookie、
  Token、profile state 或用户 HOME 作为环境变量或隐式挂载传入。
- 未声明的 raw socket、任意 DNS 和任意出站连接默认拒绝；经代码准入的 script 如需
  本机网络，只能使用 S1/Harbor worker 已明确允许的范围、已接受的 WebEnvoy Network
  capability/Harbor broker，并同时通过现有 Grant、origin 和 task scope。本合同不建立
  Network body/interception/modification 合同。
- script 的进程身份、文件和网络边界由 WebEnvoy 实现和现场证据证明；`grant_id`、
  HTTP/MCP 认证或包内字段单独不能声称 sandbox。具体 OS 技术（例如平台进程隔离或
  既有受管 worker）属于 WebEnvoy 实现合同，不由 Lode 发明新的路径隔离或长期 runner。

如果宿主只能依靠同一 OS 用户下的不同 bearer、路由、环境变量或约定路径来隔离
Agent 与 owner 文件，则不满足本合同；同 UID 进程可读取 owner-controlled 文件，或
Agent-side worker 可读取 owner control socket 时，该 script 必须被拒绝执行。WebEnvoy
的 S1/实现候选必须先记录宿主强制的进程、socket、文件和网络边界；独立 service UID
本身也不足以证明该隔离。没有可验证的拒绝事实时，只能保留包读取和 `knowledge_only`，
不能报告可信代码准入或安全执行就绪。这里的 OS 边界是受限执行前提，不是一个面向
任意不可信代码的通用 sandbox。

上述执行位置只是一项安全前提；它不改变 Lode 的资产 owner，也不把包变成可直接
调用 Browser Provider 的程序。

## 4. Manifest、身份与完整性

`manifest.json` 是包身份的唯一机器可读入口。下列字段名和语义是 v1 合同；实际
JSON Schema 属于后续实现 Work Item，不能用 Markdown 示例代替 validator。

```yaml
manifest_version: lode.site-skill-package.manifest.v1
package_type: site-skill
package_ref: lode://site-skill/<site>/<name>
revision_ref: lode://site-skill/<site>/<name>@<version>#<package-digest>
version: 1.0.0
lifecycle: proposed # proposed | experimental | stable | deprecated
site:
  site_id: example
  supported_origins: [https://www.example.com]
  account_system_ref: lode://account-system/<ref>@<version>
source:
  repository: WebEnvoy/Lode
  package_path: sites/<site>/<name>
  commit: <immutable-commit>
  source_ref: <approved-source-ref>
integrity:
  package_digest: sha256:<digest>
  files: [{path: SKILL.md, role: entrypoint, bytes: 123, sha256: sha256:<digest>}]
compatibility:
  package_contract: lode.site-skill-package/v1
  execution_contract: webenvoy.site-skill-execution/v1
  required_capabilities: []
tasks: []
validation: {}
```

必需语义如下：

- `package_ref` 在站点内稳定；改名、换站点或改变包边界即为新身份。`revision_ref`
  必须同时绑定 `package_ref`、完整 `version` 和不可变 `package_digest`，不能使用
  `latest`、工作树路径或浮动分支。
- `version` 是 Lode 的 package version。破坏任务输入/输出、脚本 ABI、source shape、
  verification 或 repair contract 时必须升版本或显式 `deprecated`；WebEnvoy 只能
  记录和选择 Lode 已声明的版本。
- `source` 至少包含 repository、package path、immutable commit 和获准 source ref。
  source path 是来源元数据，不是 Agent 可访问的本地文件路径。
- `integrity.files[]` 按包内相对路径列出每个普通文件的角色、字节数和 SHA-256。
  `package_digest` 对规范化 manifest（暂时省略 `integrity.package_digest` 字段）
  和按字典序排列的 `(path, bytes, sha256)` tuples 计算；因此 digest 不循环且可在
  不执行代码的情况下复核。manifest 摘要与文件摘要都属于 Lode owner fact。
- `lifecycle` 复用 ADR 0002 的 `proposed`、`experimental`、`stable`、`deprecated`。
  `stable` 只表示包材料满足 Lode 的资产验证门，不表示已安装、已获运行授权或业务
  成功。
- `site.account_system_ref` 只引用同一包兼容的 AccountSystem 资产；不内嵌账户、
  密钥、登录态或 Profile。相同 AccountSystem 仍是唯一来源。
- `compatibility.required_capabilities` 只声明能力引用和版本约束，不选择 Provider、
  Profile、代理、环境、文件路径或网络路线。

缺少 manifest、任一摘要不符、来源未获准、路径越界、禁止内容或未知必需字段时，
包不能进入 executable-ready。Lode 的验证失败不能被 WebEnvoy 改名为业务失败或
运行成功。

## 5. Task declaration 合同

每个可正式发现的任务必须由一个 `task_ref` 唯一标识，并在 `tasks/<task-ref>.*`
或 manifest 的 `tasks[]` 中完整声明。任务声明是受校验的描述，不是可自由组合的
workflow DSL，也不替代 Core 的任务和 Run。

```yaml
task_ref: <stable-task-ref>
version: 1.0.0
title: <short-human-title>
intent: <bounded-user-result>
operation_id: <existing-capability-operation>
action: read # read | prepare | commit | destructive
applicability:
  origins: [https://www.example.com]
  account_system_ref: lode://account-system/<ref>@<version>
  target_type: <business-target-type>
entrypoint:
  script_ref: <script-ref>
  capability_refs: [lode://site-capability/<ref>@<version>]
inputs:
  schema_ref: lode://schema/<ref>@<version>
outputs:
  schema_ref: lode://schema/<ref>@<version>
  result_kind: <bounded-kind>
  completeness: required
preconditions: [<pre-check-ref>]
verification:
  post_check_ref: <post-check-ref>
  required_evidence_refs: [<opaque-evidence-kind>]
known_branches: [<bounded-branch-ref>]
failure_recovery:
  failure_classes: [<accepted-class>]
  repair_ref: <repair-note-ref>
  unknown_policy: query_original_run_only
data_handling:
  output_sensitivity: public
  external_egress: none
```

字段规则：

- `operation_id` 必须引用 WebEnvoy 已有 capability operation 或经配套 WebEnvoy 合同
  接受的新 operation。Lode 不定义 CLI/MCP 路由、工具名、Grant 字段或 Provider endpoint。
- `action` 复用 ADR 0007。它是 Lode 的动作声明，不是授权结果；`commit` 或
  `destructive` 任务仍必须由 Core 按现有授权、确认、ControlLease、idempotency 和
  unknown 合同处理。
- `applicability` 可声明 origin、AccountSystem 和业务 target 类型，不能指定当前
  Profile、账号、Provider、session 或实际 URL。任务必须在运行时重新绑定当前可信
  observation 和 target ref。
- `entrypoint` 至少提供一个 capability ref 或已声明 script ref。`SKILL.md` 的自然
  语言步骤不构成 entrypoint。多个 capability 的顺序若影响结果，必须在任务声明中
  以有限、可验证的分支和 pre/post-check 表达，不能引入通用 block graph。
- `inputs.schema_ref` 和 `outputs.schema_ref` 必须能解析到 Lode JSON Schema。输出中的
  collection 必须声明字段类型、单位、可空/unknown/empty、分页、截断、去重、版本和
  错误映射；缺页、截断未标记或无法核验的结果不能成为 `success_result`。
- `verification.post_check_ref` 拥有业务成功条件。浏览器导航完成、HTTP 2xx、脚本
  退出码、output schema 通过或已有页面文本都不能单独等同业务成功。
- `failure_recovery` 只能引用既有 failure class、repair note 和 WebEnvoy query/
  reconcile。`unknown_policy` 固定为原 Run/operation 对账；不得用新 script、版本、
  idempotency key 或 reload 重做一个已派发且 unknown 的写入。
- `data_handling.external_egress` 只声明包需要什么；是否允许外发由 WebEnvoy 的
  现有模型、Network、文件和 Grant 合同再次决定。包不能通过该字段扩权。

没有 `tasks[]`、只有 references/说明或 task 未通过上述校验的包，`task_support` 是
`knowledge_only`；可读不等于可运行。`task_support=executable_ready` 只表示包和
任务材料经过 Lode 校验，不表示已安装、代码已准入、当前授权存在或 Runtime 可用。

## 6. Script declaration 与可信代码准入

每个 script 必须在 manifest 或任务的 `scripts[]` 中有稳定声明：

| 字段 | 语义 |
| --- | --- |
| `script_ref` / `path` | 包内稳定身份和相对路径；路径不能越界 |
| `source_commit` / `version` / `sha256` | Lode 来源、版本和完整性；改变即新 revision 或新 script version |
| `runtime_kind` / `entrypoint` | 受管执行 host 可识别的固定语言和入口；不等于 Provider API |
| `input_schema_ref` / `output_schema_ref` | 有界输入、输出和单位；禁止隐式环境输入 |
| `capability_refs` / `action` | 只声明允许调用的正式能力和动作类别 |
| `target_binding` | 需要的 Page/Frame/document/observation/业务 target 类型；实际 ref 由 Harbor 当前观察提供 |
| `timeout` / `cancel` | 有界运行和取消要求；取消不回滚已经派发的外部效果 |
| `data_handling` | 敏感等级、脱敏、是否允许外发；默认无外发 |

可信代码准入由 WebEnvoy 的受管 source/admission 过程独立决定。Lode 的 source/hash
和离线验证是准入材料，不是自动信任；安装、enable 或 SKILL 文本出现都不能跳过准入。
未准入的包仍可在获准范围内作为知识/资产读取，但不得作为 executable entrypoint。
准入结果必须可追溯到 `package_ref`、`revision_ref`、`script_ref` 和摘要；不能建立
另一个 Lode trust registry。

获准 script 只能调用已接受的 WebEnvoy Runtime capability。它不能直接调用 CDP、
Juggler、Provider endpoint、任意 JavaScript/eval、任意 shell、Cookie/storage、
文件路径或未声明的网络。需要 fresh observation 时，script 可以请求正式 observation
并获得新的 target ref；旧 ref 失效后不能静默重绑到另一个节点。

## 7. 与既有包和 #508 生命周期的兼容

### 7.1 既有 Lode site-capability

既有 `lode.site-capability.manifest.v0` 包、`capability_id`、`operation_id`、
`operation_mode`、action declaration、input/output/source schema、fixtures、
pre/post-check、resource requirement 和 invalidation marker 继续有效。site SKILL
任务通过 `capability_refs` 消费它们的版本化输出，不复制 manifest 或另造 normalizer。

一个现有 capability 包只有说明、`proposed` 生命周期、缺失任务 entrypoint 或缺少
完整验证材料时，可以作为知识/依赖存在，但不能被推断为 executable-ready site SKILL。
现有包不因本文件而大规模迁移、改名或改变 `operation_mode`。

### 7.2 #508 managed asset lifecycle

安装和选择严格复用 WebEnvoy [Managed SKILL Library Lifecycle V1](https://github.com/WebEnvoy/WebEnvoy/blob/main/docs/specs/skill-library-lifecycle-v1.md)：

1. Core 仅接受批准 manifest 中的完整 `revision_ref`，安装后保持 disabled；
2. `enable` 只选择已安装、兼容、摘要正确且已准入的 revision；
3. `update`/`rollback` 使用明确目标和 CAS；`disable` 保留内容、选择和历史；
4. Core 在同一受管库记录 Lode `package_ref`、`revision_ref`、version 和 digest 的
   projection，并以不一致拒绝，不能另写一份包身份真相；
5. 任务进入 Run 后固定解析出的 revision 和 script digest；后续包更新不能改变
   该 Run。当前本地修改必须报告 `managed_skill_local_modified` 或等价既有错误，
   不能被 update/rollback 静默覆盖；
6. 安装、更新、启用、读取和执行都沿既有 Core Run、receipt、idempotency、query 和
   unknown 语义；本文件不增加 package manager、队列或 durable Run。

当前 #508 文档中登记的 `webenvoy-browser-reference` 是 WebEnvoy 管理/浏览器参考
资产，不能被解释为已有网站业务 SKILL，也不能因为该资产存在就声称 Lode site SKILL
已经安装或可以执行。若实现要把 Lode 包加入批准 manifest，必须在实现 Work Item
中提供精确的 manifest/source/hash/compatibility 证据；本文件不伪造该事实。

### 7.3 局部失败与版本 pin

包损坏、缺失、未准入或不可兼容只阻断该包和依赖它的任务，不能阻断 Profile 管理、
通用浏览器能力或没有网站 SKILL 的任务。包更新只影响未来新 Run；进行中的 Run 继续
使用 admission 时固定的 revision。local overlay、草稿修复和自动合并不在 v1 中，
任何本地修改都保留原文件并要求显式修复或新 revision。

## 8. 验证、修复与结果边界

Lode 离线验证至少检查：manifest 唯一性、路径和普通文件、必填身份、source/hash、
版本兼容、引用可解析性、schema 形状、脱敏 fixture、pre/post-check、任务输入输出、
script 声明、action、known branches、分页/截断语义、禁止内容和 repair reference。
验证结果引用包 revision 和 checked refs，使用 ADR 0005 的结构化 failure code；不运行
真实浏览器、不选择 Provider、不写 Core Run、不读取账号、不外发数据。

repair note 必须说明触发条件、受影响 revision、需要重新观察或重新生成的引用、
需要人工确认的动作、验证入口和是否需要升 version。repair note 不能自动改写用户
本地文件、切换已启用 revision 或重放 unknown 写入。真实页面变化由 Harbor 提供
fresh observation；业务结果由任务 post-check 和 Core result envelope 共同判定。

Lode 输出的是可被 Core 引用的 normalized data、source/evidence ref policy 和
验证分类。Core/Harbor 仍拥有 `{ok, run_id, status, result?, failure?}`、
`ExternalOutcome`、`dispatch_state` 和 `unknown_outcome`。包不能用自己的 `status`
覆盖这些事实。

## 9. 最小场景

| 场景 | 必须成立的合同事实 |
| --- | --- |
| 只导入知识 | `SKILL.md`/references 可读；没有完整 task declaration 或脚本准入时标为 `knowledge_only`，不得出现在正式任务执行入口。 |
| 页面节点被替换 | 旧 observation/target ref 按 Harbor freshness 失效；任务 fresh observe 并获得新 ref；不能按 selector、文本或脚本私自重绑旧节点。 |
| 写入响应丢失 | Core/Harbor 保留原 Run 的 `dispatched`/`unknown_outcome`；只用原 operation/idempotency key 查询或对账，不换 script version、key、页面或提交。 |
| 包更新进行中 | 新 Run 选择新 revision；已经 admission 的 Run 固定旧 revision。更新不会覆盖本地修改，local modified 必须显式修复。 |
| schema 通过但分页遗漏 | post-check 发现 completeness 不满足；结果是 partial/incomplete 或 unknown，不能报告业务成功。 |

## 10. Design Obligation disposition

| Obligation | 本候选判断 | 依据和实施前门槛 |
| --- | --- | --- |
| `DO-PLUGIN-EXPOSURE` | `triggered` | 已安装任务需要新的动态 task/capability discovery 或 task projection；配套执行合同给出 specialist 语义。实现前必须同步 [Plugin Runtime Exposure V1](https://github.com/WebEnvoy/WebEnvoy/blob/main/docs/specs/plugin-runtime-exposure-v1.md) 的入口、过滤、版本、错误和兼容；不能只新增包字段。 |
| `DO-GRANT-WIRE` | `not-triggered` | 本候选只复用既有 `skill_scope`（资产管理）、browser `allowed_operations`/Profile/origin/task scope 和现有 Runtime capability；没有新持久 Grant 维度。若实现增加 script、egress 或 site-task 专属持久字段，必须先把它改为 `triggered` 并更新 Grant 合同。 |
| `DO-NETWORK-CONTRACT` | `conditional` | 本包默认无主动 Network，且不声明 body/interception/modification。若任务实际需要公共 Network payload 或主动外发，先由 S4 接受 [Network Runtime V1](https://github.com/WebEnvoy/WebEnvoy/blob/main/docs/specs/network-runtime-contract-v1.md) 并重判。 |
| `DO-CONSOLE-CONTRACT` | `not-triggered` | 包不新增 console/page-error public payload；只可引用已有诊断结果。 |
| `DO-PROVIDER-PRIVATE-SCHEMA` | `not-triggered` | 包不保存 Provider 环境、启动参数、私有 handle 或 replay bundle。 |
| `DO-APP-IA` | `not-triggered` | 包复用现有 owner/Agent 入口，不新增 Library、Activity、工作台或导航。 |

## 11. 非目标、supersession 与合并顺序

本文件不实现包、schema、validator、packer、runner、sandbox、registry、Marketplace、
站点转换、账号登录、浏览器启动、Profile/Provider 选择、Network/视觉能力、第二权限
系统或真实站点验收。它也不宣称本候选已经 installed、plugin_verified、live 或具有
任何业务成功证据。

本文件在 #563 接受后，仅 supersede 现有规划材料中“site SKILL 包的身份、完整文件
清单、任务声明和脚本边界尚未冻结”的部分；不 supersede #508、ADR 0002–0007 或
WebEnvoy Core/Harbor 的既有授权、Run、unknown 和现场合同。若当前候选与这些已接受
合同冲突，应暂停实现并更新拥有该语义的合同，不能靠包文档覆盖。

跨仓集成顺序为：

1. 评审并接受本分支 `codex/spec-563-package` 的精确提交；
2. 用该提交作为 WebEnvoy `codex/spec-563-skill` 的 Lode package companion，评审
   配套执行合同；
3. 两个候选都接受后，由集成 owner 把两个 `main` 路径写入各自共享索引，并把本文件
   中的候选分支链接替换为合入后的稳定链接；
4. 实现 Work Item 另行提供 source admission、OS worker 文件/网络边界、真实安装、
   Plugin/Grant schema、Run/unknown 和 live site 证据。规格接受不等于这些授权或实现。
