# 任务包格式

任务包用于将多个站点能力组合成可复用流程。

## 建议目录

```text
tasks/
  publish-content/
    task.json
    README.md
    examples/
    tests/
```

## task.json 可能包含

```json
{
  "task_id": "publish-content",
  "name": "发布内容",
  "inputs": [],
  "steps": [],
  "resource_requirements": [],
  "verification": []
}
```

## 设计要求

- 任务封装应声明输入、步骤、资源需求和验证方式；
- 写入类任务必须包含写入前检查和写入后验证；
- 任务不应保存用户私有业务参数；
- 任务可以引用站点能力，但不应依赖 Harbor 内部实现。
