# Evidence Map

| Evidence id | Type | Source locator | Consumes | Binding | Freshness | Consumer boundary | Remediation direction |
| --- | --- | --- | --- | --- | --- | --- | --- |
| EV-001 | behavior_evidence | .loom/specs/LODE-197/spec.md | 故事就绪度、范围、非目标和 suite path | LODE-197 / 站点知识选择行为 | present | 仅供 review 和 merge-ready 证据消费 | 范围、层级或首批任务边界变化后刷新。 |
| EV-002 | test_evidence | .loom/progress/LODE-197.md | 本地 diff/readability/package-validator/Loom 验证摘要 | LODE-197 / 本地验证检查 | present | 仅供 review 和 merge-ready 证据消费 | 文档或载体编辑后重新运行本地验证。 |
| EV-003 | fresh_verification_input | .loom/progress/LODE-197.md | EV-001 EV-002 | LODE-197 / 最新验证摘要 | present | 仅供 review 和 merge-ready 证据消费 | 验证变化后刷新 progress 摘要。 |
