# Lode Contracts

本目录是已接受合同的索引，不复制 ADR 正文。

| 合同 | 权威载体 |
| --- | --- |
| 能力包最小格式、生命周期、资源需求边界 | [ADR 0002](../adr/0002-capability-package-minimum-format.md) |
| input/output/source schema、fixture、post-check、validator 报告边界 | [ADR 0003](../adr/0003-schema-fixtures-and-post-check.md) |
| asset taxonomy、workflow package、registry / version / invalidation 边界 | [ADR 0004](../adr/0004-asset-types-and-registry.md) |
| Lode 技术栈、资产文件责任、JSON Schema 权威、tooling 最小边界、deferred / rejected 禁线 | [ADR 0005](../adr/0005-lode-technical-architecture-baseline.md) |
| 小红书真实只读能力包 | [Xiaohongshu read capability packages](xiaohongshu-read-capabilities.md) |
| implementation-time / external-contract 未决项 | [pending decisions](../adr/pending-decisions.md) |

实现、测试、schema、validator、runtime 或 generated facts 不应引用 `docs/draft/` 作为权威合同。

未纳入 contracts：public contribution review / marketplace distribution、personal asset storage / sync / overlay conflict policy、App Library UX、Reports UX、真实 package 文件布局、runner、schedule、visual builder、hosted registry。这些内容尚未被 Stage 2 接受。

## 后续 Tooling 骨架入口

后续 package/schema/fixture/post-check/validator/packer/tester/local registry Work Item
必须先引用 [ADR 0005](../adr/0005-lode-technical-architecture-baseline.md)。真实文件、
命令和依赖尚未创建；实现前不得从 `docs/draft/` 或 research locator 直接派生第二套
合同。

Hosted registry、marketplace、team sync、public contribution review、crawler queue
和 benchmark harness 仍是 deferred，不属于本地 validator / packer / registry v0。

## Draft 分析吸收账本

| draft | 是否仍有有效分析 | 已吸收到哪里 | rejected / deferred |
| --- | --- | --- | --- |
| `docs/draft/asset-sources.md` | 有。platform asset 作为公共基线、用户 overlay / fork / draft 不直接改写平台资产、source schema / normalizer / redacted fixture / normalized fixture / tests 才是可沉淀资产，这些判断仍有效。 | [ADR 0004](../adr/0004-asset-types-and-registry.md) 吸收 platform / personal asset 共用 type vocabulary、overlay/fork/draft、本地 registry、version identity；[ADR 0003](../adr/0003-schema-fixtures-and-post-check.md) 吸收 redacted raw fixture、normalized fixture、normalizer regression 和敏感数据排除。 | App Library 的 Platform Assets / My Assets / Explorer / Reports 呈现是 App UX，deferred 到 App Library / marketplace / reports Work Item；真实 hosted distribution 未进入 Stage 2。 |
| `docs/draft/asset-versioning.md` | 有。capability、source schema、normalizer、output schema、fixture、overlay/fork/draft 都需要可引用版本；Run Record 要能说明一次运行消费的资产版本，这些判断仍有效。 | [ADR 0004](../adr/0004-asset-types-and-registry.md) 吸收 version lock、freshness rule、dependency boundary、Core Run Record 版本引用；[ADR 0002](../adr/0002-capability-package-minimum-format.md) 吸收 capability lifecycle/version/deprecation/invalidation。 | install/update/pin/rollback UI、hosted sync、lockfile、个人资产版本历史和 overlay 冲突处理 deferred；overlay/fork 冲突由 [PD-0012](../adr/pending-decisions.md#pd-0012) 承接。 |
| `docs/draft/capability-lifecycle.md` | 有。`proposed` / `experimental` / `stable` / `deprecated`、stable 不能只看一次跑通、stable 需要 schema/fixture/post-check/resource/version/invalidation，这些判断仍有效。 | [ADR 0002](../adr/0002-capability-package-minimum-format.md) 吸收 lifecycle、capability identity、package minimum format、version/deprecation/invalidation；[ADR 0003](../adr/0003-schema-fixtures-and-post-check.md) 吸收 stable 所需 input/output/source schema、fixture、post-check、validator 边界。 | provider routing、fallback priority、业务 workflow、账号运营、Cookie/Token/Session、Harbor Runtime Session 状态明确 rejected as Lode contract。 |
| `docs/draft/capability-model.md` | 有。Lode 拥有站点知识、站点能力、normalizer 和任务封装边界；Core 执行并封装结果；任务封装组合站点能力，这些判断仍有效。 | [ADR 0002](../adr/0002-capability-package-minimum-format.md) 吸收 site capability package 和 normalized output ownership；[ADR 0004](../adr/0004-asset-types-and-registry.md) 吸收 `site-capability`、`workflow-package`、`domain-skill`、`site-adapter` asset taxonomy。 | 旧“四层模型”不再作为实现 taxonomy；“原子动作”未被 Stage 2 接受为独立 Lode asset，deferred 到未来 package/runtime 设计。 |
| `docs/draft/contribution-model.md` | 有。可贡献内容必须是站点结构变化摘要、source schema/normalizer patch、脱敏 fixture、regression test、错误类型和资源需求变化；账号、Cookie、Token、完整 DOM/请求响应、真实业务参数不能贡献，这些判断仍有效。 | [ADR 0003](../adr/0003-schema-fixtures-and-post-check.md) 吸收 redacted fixture、normalized fixture、validator/reporting 的安全输入；[ADR 0004](../adr/0004-asset-types-and-registry.md) 吸收 asset / fixture / package 引用边界。 | 公共贡献审核、moderation、hosted distribution、team/private visibility、rejection/appeal 没有 Stage 2 accepted contract，保留为 deferred draft，由 future contribution / marketplace owner 接手。 |
| `docs/draft/invalidation-reporting.md` | 有。页面/API/DOM/network/source shape 变化、normalizer failure、mapping incomplete、resource requirement changed、verification failed 等失效分类，以及 report 不含敏感现场，这些判断仍有效。 | [ADR 0002](../adr/0002-capability-package-minimum-format.md) 吸收 invalidation marker；[ADR 0003](../adr/0003-schema-fixtures-and-post-check.md) 吸收 failure classes、fixture/evidence ref、post-check failure；[ADR 0004](../adr/0004-asset-types-and-registry.md) 吸收 asset freshness/invalidation boundary。 | App Reports、repair request UX、hosted reporting workflow、真实 evidence storage deferred；Lode 不保存完整执行现场或生产 raw payload。 |
| `docs/draft/personal-assets.md` | 有。个人资产不应覆盖平台资产本体，应通过 overlay/fork/draft；私有 normalizer patch / source schema patch / private fixture 有独立需求，这些判断仍有效。 | [ADR 0004](../adr/0004-asset-types-and-registry.md) 吸收 platform/personal asset 共用 type vocabulary、overlay/fork/draft 和 local registry version identity。 | 私有资产存储、team sync、active/deprecated/archive 状态、App 操作、导出/提交贡献、overlay conflict policy deferred；overlay/fork 冲突由 [PD-0012](../adr/pending-decisions.md#pd-0012) 承接。 |
| `docs/draft/resource-requirements.md` | 有。Lode 只声明抽象资源需求，Harbor 提供 runtime facts，Core 做 one-of matching；`matched` / `unmatched` / `invalid_contract` 必须区分；不得写 provider/profile/cookie/token/fallback，这些判断仍有效。 | [ADR 0003](../adr/0003-schema-fixtures-and-post-check.md) 吸收 Harbor facts vocabulary consumption、matching states、read / validate-only / write-like resource boundary；[ADR 0002](../adr/0002-capability-package-minimum-format.md) 吸收 package resource requirement profiles。 | provider routing、fallback priority、preferred profile、真实 profile/provider/session 字段 rejected as Lode contract；write-like executable resource contract deferred 到 Core/App/Harbor write contracts。 |
| `docs/draft/result-schema.md` | 有。Lode owns normalized `data` shape，Core owns result envelope，Harbor/Core own raw/evidence refs；normalized result 不能泄漏 raw payload、provider route、storage URL、业务私密字段，这些判断仍有效。 | [ADR 0003](../adr/0003-schema-fixtures-and-post-check.md) 吸收 input/output/source shape、normalized output schema、Core envelope boundary、source/evidence refs、fixture/post-check/validator reporting。 | 旧候选字段不作为最终 JSON Schema；Core envelope schema、Harbor evidence schema、dataset sink/长期存储 deferred 到对应 Core/Harbor/App contracts。 |
| `docs/draft/site-normalization.md` | 有。同一能力可有 API/DOM/network/Snapshot/manual evidence 多种 source shape，但必须 normalizer 到同一 public output；Core 不硬编码站点 raw 字段；fixture 必须脱敏，这些判断仍有效。 | [ADR 0003](../adr/0003-schema-fixtures-and-post-check.md) 吸收 source shape schema、extractor/parser/mapper/normalizer ownership、redacted raw fixture、normalized fixture、post-check 和 regression boundary。 | 旧示例目录不是文件布局合同；extractor/parser/mapper 是否拆文件 deferred 到真实 package/schema/validator Work Item。 |
| `docs/draft/site-package-format.md` | 有。site package 应包含 site metadata、capability manifest、input/output/source schemas、normalizers、fixtures/tests，且不保存账号、Cookie、Token、真实 raw payload，这些判断仍有效。 | [ADR 0002](../adr/0002-capability-package-minimum-format.md) 吸收 package root、manifest、capability identity、resource/schema/check/fixture refs；[ADR 0004](../adr/0004-asset-types-and-registry.md) 吸收 local registry、asset locator 和 dependency boundary。 | 具体目录树、文件名、真实 schema/fixture/validator/registry 代码 deferred 到 package implementation Work Item；站点包不拥有 Harbor provider/profile/runtime。 |
| `docs/draft/task-package-format.md` | 有。task/workflow package 组合 site capability，声明输入、步骤、资源需求和 verification，不能直接解析 API/DOM/network/Snapshot raw payload，这些判断仍有效。 | [ADR 0004](../adr/0004-asset-types-and-registry.md) 吸收 `workflow-package` asset type、site capability dependency、normalized output dependency、verification requirement boundary。 | workflow runner、record/replay、visual builder、schedule、queue、marketplace solution catalog deferred；workflow package 不拥有 runtime execution。 |
