# 资产来源

本文档定义 Lode 中平台资产和用户个人资产的来源边界。

## 平台资产

平台资产是官方或公共分发的能力资产，包括站点知识、能力包、source schema、normalizer、任务模板、测试样例、版本和失效标记。

平台资产应支持：

- 按需安装；
- 更新；
- 版本锁定；
- 回滚；
- 校验；
- 禁用；
- 查看变更记录。

用户不应直接改写平台资产本体。需要调整时，应通过 overlay、fork、draft 或贡献流程完成。

## 用户个人资产

用户个人资产是用户或团队私有的能力资产，包括能力修改、私有任务模板、私有站点知识补丁、normalizer patch、source schema patch、探索草稿、修复草稿和私有测试样例。

用户个人资产默认不进入公共能力库。

## 推荐关系

```text
平台资产
  └── 用户 overlay / fork / draft
```

平台资产提供公共基线；用户个人资产承载用户自己的修改、私有流程和探索结果。

## 归一化资产来源

站点级清洗与归一化资产可以来自：

- API payload 观察；
- DOM / Snapshot 观察；
- network response 观察；
- Harbor evidence summary；
- 用户提交的脱敏 raw fixture；
- failed run 的脱敏 source shape 摘要；
- normalizer regression fixture；
- 人工修复草稿。

这些来源应沉淀为 source schema、normalizer、脱敏 raw fixture、normalized fixture 和 tests，而不是保存真实生产 raw 数据。

## App 中的呈现

在 WebEnvoy App 的 Library 区域中：

- Platform Assets 用于安装、更新、锁定和回滚平台资产；
- My Assets 用于管理个人资产、overlay、fork、draft 和私有测试样例；
- Explorer 用于生成个人资产草稿；
- Reports 用于反馈失效或修复信息。
