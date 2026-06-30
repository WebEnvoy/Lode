# Lode Drafts

`docs/draft/` 只保存短期草稿或从旧草稿到正式事实载体的指针。

draft 不能作为实现、测试、schema、validator、runtime 或 generated facts 的依据。实现应读取 [ADR](../adr/) 或 [contracts](../contracts/)。

## 生命周期规则

每个 draft 必须写清：

- status: `promoted`、`pending`、`deferred`、`removed` 或 `pointer`
- owner
- linked issue
- exit condition

状态含义：

| status | 含义 | 退出条件 |
| --- | --- | --- |
| `promoted` | 本文件本身已成为当前正式说明。 | 后续更稳定载体接手后改为 pointer 或删除。 |
| `pointer` | 旧草稿内容已被 ADR 或 contract 接受，本文件只保留跳转。 | 下游引用改到正式载体后删除。 |
| `pending` | 仍需当前 milestone 内决策。 | 决策进入 ADR / contract，或降级为 deferred。 |
| `deferred` | 不阻塞当前 milestone，后续再设计。 | 新 Work Item / ADR 接手后迁移或删除。 |
| `removed` | 已过期或重复。 | 删除，或保留一段短指针说明替代载体。 |

## Draft 归宿盘点

| 文件 | 当前用途 | 状态 | 目标位置 | linked issue | 判断理由 | 处理动作 |
| --- | --- | --- | --- | --- | --- | --- |
| `README.md` | draft 生命周期与盘点入口 | promoted | 本文件 | [#63](https://github.com/WebEnvoy/Lode/issues/63), [#64](https://github.com/WebEnvoy/Lode/issues/64) | 这是本 milestone 的正式目录规则和盘点表，不是旧产品草稿。 | 重写为生命周期规则和归宿表 |
| `asset-sources.md` | 平台资产、个人资产和来源边界 | pointer | [ADR 0004](../adr/0004-asset-types-and-registry.md), [contracts](../contracts/) | 平台/个人资产、overlay/fork/draft 和本地 registry 边界已被 ADR 0004 接受；App 呈现细节未接受，不能作为合同保留。 | 改为短指针 |
| `asset-versioning.md` | asset version、pin、rollback、Run Record 引用 | pointer | [ADR 0004](../adr/0004-asset-types-and-registry.md), [PD-0012](../adr/pending-decisions.md#pd-0012) | version identity、freshness、Run Record 引用已在 ADR 0004；overlay 冲突仍是 PD-0012，不能在 draft 里变成第二份 truth。 | 改为短指针 |
| `capability-lifecycle.md` | capability lifecycle 和 stable 条件 | pointer | [ADR 0002](../adr/0002-capability-package-minimum-format.md), [ADR 0003](../adr/0003-schema-fixtures-and-post-check.md) | lifecycle、stable 条件、fixture/post-check/resource requirement 都已被 ADR 0002/0003 接受；旧文没有剩余独立决策。 | 改为短指针 |
| `capability-model.md` | site knowledge / capability / task 分层 | pointer | [ADR 0002](../adr/0002-capability-package-minimum-format.md), [ADR 0004](../adr/0004-asset-types-and-registry.md) | 分层已收敛为 site-capability、workflow-package、domain-skill、adapter 等正式 asset taxonomy；旧四层说明会制造重复概念。 | 改为短指针 |
| `contribution-model.md` | 公共贡献和审核方向 | deferred | future contribution / marketplace Work Item | [#66](https://github.com/WebEnvoy/Lode/issues/66) | 安全贡献输入已被 ADR 0003/0004 吸收，但公共审核、分发、moderation、团队同步还没有 Stage 2 接受合同，仍有未来独立价值。 | 保留 deferred 草稿，补 owner 和退出条件 |
| `invalidation-reporting.md` | invalidation marker 和 report 边界 | pointer | [ADR 0002](../adr/0002-capability-package-minimum-format.md), [ADR 0003](../adr/0003-schema-fixtures-and-post-check.md), [ADR 0004](../adr/0004-asset-types-and-registry.md) | invalidation marker、failure class、fixture/evidence ref 和敏感数据排除已被正式 ADR 覆盖；App Reports UX 未接受。 | 改为短指针 |
| `personal-assets.md` | overlay / fork / private asset 方向 | deferred | [ADR 0004](../adr/0004-asset-types-and-registry.md), future App Library / overlay Work Item | [#66](https://github.com/WebEnvoy/Lode/issues/66) | platform/personal 边界和 overlay/fork/draft 词汇已接受，但私有资产存储、同步、冲突和 App 操作仍未定，保留为后续入口。 | 保留 deferred 草稿，补 owner 和退出条件 |
| `resource-requirements.md` | resource requirement matching 边界 | pointer | [ADR 0003](../adr/0003-schema-fixtures-and-post-check.md), [contracts](../contracts/) | Harbor facts consumption、matching state 和 operation boundary 已进入 ADR 0003；继续保留正文会形成第二份准入合同。 | 改为短指针 |
| `result-schema.md` | normalized result 和 Core envelope 边界 | pointer | [ADR 0003](../adr/0003-schema-fixtures-and-post-check.md), [contracts](../contracts/) | normalized data shape、Core envelope 分界、source/evidence refs 已进入 ADR 0003；旧候选字段不应被实现直接依赖。 | 改为短指针 |
| `site-normalization.md` | source shape、normalizer、fixture 边界 | pointer | [ADR 0003](../adr/0003-schema-fixtures-and-post-check.md), [contracts](../contracts/) | source shape、normalizer、redacted/normalized fixture 和 regression 边界已进入 ADR 0003；候选目录不应成为事实。 | 改为短指针 |
| `site-package-format.md` | site capability package 目录候选 | pointer | [ADR 0002](../adr/0002-capability-package-minimum-format.md), [ADR 0004](../adr/0004-asset-types-and-registry.md) | manifest/package identity 和 asset taxonomy 已被 ADR 0002/0004 接受；示例目录仍未实现，不能放入 contracts。 | 改为短指针 |
| `task-package-format.md` | workflow / task package 候选 | pointer | [ADR 0004](../adr/0004-asset-types-and-registry.md) | workflow-package 已作为 asset type 和引用边界进入 ADR 0004；runner、visual builder、schedule 等均非 Stage 2。 | 改为短指针 |
