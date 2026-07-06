# Lode Docs

本目录只保留三类文档：

| 目录 | 语义 | 进入条件 |
| --- | --- | --- |
| `adr/` | 架构决策、取舍、accepted / rejected / deferred / pending 记录。 | 需要长期解释为什么这样做，或需要保留未决决策时。 |
| `contracts/` | 后续实现、测试或跨仓消费必须遵守的稳定合同索引。 | 合同已被 ADR 接受，且不应继续只从 draft 读取。 |
| `draft/` | 短期规划草稿和迁移指针。 | 必须有状态、owner、linked issue 和退出条件；不能作为实现依据。 |

现在不创建 `guides/`。等仓库有真实可运行流程、命令或用户操作需要说明时再建。

当前已接受的站点吸收基线包括
[ADR 0006: 小红书与 BOSS 站点知识吸收边界](adr/0006-xhs-boss-site-knowledge-selection.md)。
