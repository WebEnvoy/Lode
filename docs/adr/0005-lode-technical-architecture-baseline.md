# 0005 Lode 技术架构基线

## Status

Accepted for milestone #8 docs-only technical baseline, 2026-07-01.

## Context

本 ADR 收口 GitHub #72-#81：在真实 capability package、JSON Schema、
validator、packer、tester 和 registry tooling 落地前，先冻结 Lode 资产文件和
本地 tooling 的职责边界。

本 ADR 只补充 ADR 0002、0003、0004，不替代它们；不创建 package 文件、schema
文件、fixture、post-check runner、registry、CLI、`package.json` 或依赖。

## Decision

### Asset And Tooling Boundary

| 面 | Accepted boundary | Rejected / forbidden | Deferred |
| --- | --- | --- | --- |
| JSON / YAML assets | manifest、package metadata、schema examples、fixture metadata、post-check requirement 和 local registry index 可用 JSON 或 YAML 表达；稳定可校验合同必须能映射到 JSON Schema。 | 不保存 Cookie、Token、profile state、runtime session、live tab、raw evidence body、完整 DOM/HAR/screenshot、生产 payload 或用户业务数据。 | 真实文件名、目录树和生成规则留给后续 package/schema Work Item。 |
| Markdown assets | 用于 ADR、authoring guidance、known limitations、deferred/rejected 说明和索引；不能替代正式校验合同。 | 不把 Markdown 表格、display columns 或草稿示例当 validator truth。 | 使用教程等到有真实命令或用户流程后再写。 |
| TypeScript tooling | 只允许用于 offline validator、packer、tester 和 local registry tooling。tooling 消费 Lode 文件，输出机器可读报告。 | 不做 runtime runner、不选择 Harbor provider/profile、不执行真实浏览器任务、不写 Core Run Record、不做 App UI。 | 具体 CLI 命令、包管理和依赖选择留到 tooling Work Item。 |
| Local registry | 只做本地 discoverability、version identity、引用检查和 asset_missing / registry_unavailable 诊断。 | 不做 hosted registry、marketplace、team sync、public contribution review 或远程分发。 | Hosted registry / marketplace / sync 等本地闭环后再立项。 |

### Package File Responsibilities

| 文件族 | Owner | Responsibility | Must not become |
| --- | --- | --- | --- |
| package manifest | Lode | 记录 package/capability identity、site/origin、version、lifecycle、operation、family、resource requirement refs、schema refs、fixture refs、post-check refs、known limitations、deprecation 和 invalidation marker。 | runtime binding、profile/provider selection、secret store、live evidence store 或 App display truth。 |
| JSON Schema | Lode | 正式合同载体，描述 input、normalized output、source shape、fixture metadata 和 post-check requirement shape；每个 validator/tester 报告必须引用 schema id/version。 | Markdown 说明、TypeScript 类型副产物、展示列或 sample payload。 |
| fixture | Lode | 保存脱敏 raw fixture、normalized fixture、source/evidence placeholder refs、redaction policy、fixture id/version 和 integrity hint，用于 offline regression。 | live evidence、生产 raw payload、完整截图/HAR/DOM、账号态或长期业务数据集。 |
| post-check | Lode declares; Core executes later | 声明 capability 成功条件、required fields、source/evidence binding 和失败分类；tester 只能对 fixture/dry-run 入口验证声明。 | 浏览器自动化步骤、真实写入、Core result envelope 或 Harbor evidence schema。 |
| normalizer / adapter refs | Lode package internals | 作为 manifest 引用的 implementation component 或后续共享 asset；只有多包复用且有独立版本时进入 local registry。 | 用户 task contract、runtime provider、crawler queue 或通用 browser agent loop。 |

### JSON Schema Authority

JSON Schema 是 Lode 结构化合同的正式载体。Markdown 只能解释字段、作者指南和取舍。
TypeScript 类型可以从 JSON Schema 派生或辅助实现，但不能成为比 JSON Schema 更高的
truth source。

后续 validator、tester 和 registry tooling 的报告必须至少输出：

- package/capability id；
- schema id/version；
- checked file path 或 package-relative locator；
- status；
- severity；
- machine-readable failure code；
- human-readable message；
- recovery hint；
- checked refs。

### Tooling Minimum Boundary

| Tool | Minimum input | Minimum output | Explicit non-goals |
| --- | --- | --- | --- |
| validator | package root、manifest、JSON Schema、fixture、post-check refs、local registry/index refs。 | `status`, `errors[]`, `warnings[]`, `checked_refs[]`，失败码至少覆盖 `missing_manifest`, `invalid_contract`, `unsupported_version`, `deprecated`, `asset_missing`, `fixture_missing`, `fixture_invalid`, `post_check_failed`, `forbidden_field`。 | 不连生产 runtime、不读取真实账号、不匹配 Harbor live facts、不执行 browser steps、不发布 package。 |
| packer | 已通过 validator 的本地 package root。 | 可被本地安装/引用的 package artifact 或 manifest summary。 | 不发布 hosted registry、不做 marketplace、不同步团队资产、不修复合同错误。 |
| tester | 脱敏 fixture、normalized fixture、post-check requirement、normalizer/test hook。 | fixture regression 报告、post-check dry-run 报告、source/evidence placeholder 绑定诊断。 | 不执行真实写入、不访问生产账号、不把 browser step 完成当业务成功。 |
| registry tooling | local package paths、manifest/version/lifecycle/dependency refs。 | local index、引用完整性报告、version/deprecation/invalidation 摘要。 | 不做远程发现、权限系统、公共贡献审核、团队同步或 App marketplace。 |

Fixture / post-check 的验证入口必须 fail closed：缺少 manifest、schema、fixture、
post-check ref 或禁止字段时输出结构化错误，不猜测默认资源或临时跳过。

### Deferred And Rejected

| Topic | Decision | Reason |
| --- | --- | --- |
| hosted registry, marketplace, team sync, public contribution review | Deferred | ADR 0004 已接受本地 registry 足以支撑近期验证；远程分发会扩大权限、审核和同步范围。 |
| crawler queue, benchmark task contract, visual builder, schedule | Deferred | 不是 capability package v0 的本地校验边界。 |
| true write capability execution | Deferred | 需要 Core action risk、App confirmation、Harbor target binding、completion evidence、idempotency 和 unknown-outcome 合同先稳定。 |
| validator as runtime runner | Rejected | Lode tooling 只校验资产合同；runtime execution 属于 Core/Harbor。 |
| Markdown as contract truth | Rejected | Admission、regression、failure output 和版本引用需要机器可校验合同。 |
| live profile / credential / raw evidence in Lode package | Rejected | 这些是 Harbor/Core runtime facts 或 evidence refs，不是 Lode asset。 |

## Input Absorption Record

| locator | 判断 | 吸收 / 裁剪 / 拒绝 |
| --- | --- | --- |
| `WebEnvoy/.github/ROADMAP.md` | 吸收 | 吸收 Lode 只提供 capability package、schema、fixtures、post-check、asset registry、版本和失效标记；拒绝把 hosted marketplace、crawler queue 和完整生态协作前置。 |
| `Lode/ROADMAP.md` | 吸收 | 吸收阶段二“Core 可准入、可校验、可版本引用”的最小能力包合同；裁剪掉阶段五以后的 hosted registry、marketplace 和 sync。 |
| `Lode/AGENTS.md` | 吸收 | 吸收 JSON/YAML/Markdown 为主、TypeScript 只用于 validator/packer/tester/registry tooling、Lode 不保存 runtime session/profile/credential/raw evidence 的约束，并在本 PR 补强禁线。 |
| `Lode/docs/adr/0002-capability-package-minimum-format.md` | 吸收 | 保留 manifest、capability identity、lifecycle、version、resource requirement、schema/check/fixture refs 和 forbidden contents；本 ADR 只把文件责任表明文化。 |
| `Lode/docs/adr/0003-schema-fixtures-and-post-check.md` | 吸收 | 保留 input/output/source schema、redacted fixture、post-check、failure mapping 和 validator v0 报告边界；本 ADR 明确 JSON Schema 是正式载体。 |
| `Lode/docs/adr/0004-asset-types-and-registry.md` | 吸收 | 保留 typed assets、local registry、locator/dependency boundary、version/deprecation/invalidation；本 ADR 明确 hosted registry/marketplace/sync deferred。 |
| `research/absorability/themes/site-knowledge-and-capability-assets.md` | 裁剪复用 | 吸收 OpenCLI manifest seeds、Syvert taxonomy/lifecycle、旧 WebEnvoy XHS capability 素材、MediaCrawler 字段组织和 domain skill 分层；拒绝 `readOnly` 布尔作为唯一安全分类、直接迁入站点 adapter、把 OpenCLI columns 当 output schema、把 crawler runtime/账号池/代理池/存储放进 Lode。 |
| `WebEnvoy/docs/adr/0007-reference-version-ownership-v0.md` | 吸收 | 吸收 Lode owns `capability_ref` / `package_ref` / schema/resource/post-check 版本，Core 只记录引用；拒绝 Lode 复制 Run Record、evidence body、runtime/session/profile 内部状态。 |
| `App/docs/contracts/README.md` | 吸收 | 吸收 App Library 只是 Lode/Core/Harbor facts 的展示投影；拒绝把 App 本地 cache、installer/update UX 或 marketplace 操作写成本轮 Lode 合同。 |

## Consequences

- 后续 package/schema/tooling Work Item 可以引用同一个基线，不再从 draft 或 research
  重新解释边界。
- Lode 可以先用本地文件和 offline tooling 验证资产质量，不等待 hosted registry。
- Core、Harbor、App 的 runtime、evidence、display 和 execution truth 不会被 Lode
  tooling 偷偷复制。

## Non-Goals

- 不创建能力包、schema、fixture、post-check、registry、validator、packer、tester、
  package manager 配置或依赖。
- 不规划完整 marketplace、public contribution review、team sync、crawler queue、
  benchmark harness、visual builder 或 true write execution。
- 不 merge PR，不关闭 issue。
