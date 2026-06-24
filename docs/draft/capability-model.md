# 能力模型

Lode 的知识与能力可以分为四层。

## 1. 站点知识

站点知识回答：这个网站是什么结构？有哪些页面、入口、接口和状态？

典型内容：

- 页面结构；
- API 路径；
- 入口路径；
- 字段结构；
- 页面状态；
- 登录态判断；
- 风控页特征；
- 站点变化记录。

## 2. 站点能力

站点能力回答两个问题：如何完成一个标准网站动作，以及如何把来自 API、DOM、network、Snapshot 等不同来源的数据归一到同一个公共输出。

例如：

- 读取详情；
- 搜索内容；
- 搜索用户；
- 读取评论；
- 检查账号状态；
- 上传媒体；
- 发布内容；
- 修改内容；
- 删除内容；
- 提交表单。

站点能力还应声明并维护输出契约和站点级归一化资产。输出契约包括 normalized result schema、collection item schema、comment item schema、dataset record schema、dedup_key、raw_payload_ref、evidence_ref、source_trace、失败分类和脱敏 fixture。站点级归一化资产包括 source schema、extractor、parser、field mapper、normalizer、脱敏 raw fixture、normalized fixture 和 normalizer tests。

normalizer 是能力资产的一部分，不是 Core 的站点私有逻辑。WebEnvoy Core 在运行时调用能力和 normalizer，负责校验、投影和封装公共结果。

## 3. 原子动作

原子动作回答：完成站点能力时底层有哪些可复用小动作？

例如：

- 打开页面；
- 等待；
- 点击；
- 填写；
- 上传；
- 提取字段；
- 调用接口；
- 识别页面状态；
- 验证结果。

## 4. 任务封装

任务封装回答：用户如何把多个站点能力组合成自己的业务流程？

例如：

- 发布内容并回收链接；
- 批量采集详情；
- 检查账号后发布内容；
- 上传素材并保存草稿。
