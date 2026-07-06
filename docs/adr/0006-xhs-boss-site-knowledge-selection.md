# ADR 0006: 小红书与 BOSS 站点知识吸收边界

## 状态

已接受，2026-07-06。

## 背景

Lode #197 需要在 milestone #13「小红书与 BOSS 站点能力产品化」下完成产品和资产边界盘点，覆盖 #201/#202/#203/#204/#217，以及 #197 comment 中的语义故事 #13/#14。

本 ADR 只冻结站点知识、吸收清单和首批真实任务范围。它不创建真实能力包（capability package），不实现小红书或 BOSS 执行代码，不进入 #198/#199/#200 的能力包/结构定义（schema）/固定样本数据（fixture）/校验器实现。

Lode 的边界仍沿用 ADR 0002、ADR 0004、ADR 0005：Lode 是站点知识、能力包、结构定义、归一化器（`normalizer`）、固定样本数据和后置检查（post-check）的事实源；Core 负责执行和结果事实；Harbor 负责浏览器运行环境、身份档案、运行会话和证据引用；App 负责 Library（资产库）展示、配置和人机入口。

## 决策

### 1. 首批真实任务范围

| 站点 | 首批只读能力 | 首批输入边界 | 首批输出边界 | 明确不覆盖 |
| --- | --- | --- | --- | --- |
| 小红书 | 搜索笔记 | `keyword`，后续可扩展排序/筛选；必须记录登录、页面就绪、安全拦截和空结果失败类。 | 笔记行、标题、作者、互动数、`note_id`、`xsec_token` 或带签名笔记 URL、后续引用（follow-up ref）。 | 评论、用户主页、feed、收藏、点赞、下载、关注、删除、发布。 |
| 小红书 | 笔记详情 | 带签名笔记 URL，或 `note_id` + `xsec_token`，优先由搜索结果后续引用传入。 | 标题、正文、作者、互动数、标签、图片引用、发布时间、IP 属地、来源引用。 | 评论分页、用户主页、作者统计、创作者中心。 |
| BOSS 直聘 | 职位搜索 | `query`、城市、经验、学历、薪资、行业等小集合过滤；必须记录账号态、城市解析和分页风险。 | 职位行、薪资、公司、地点、经验、学历、技能、boss 元信息、`securityId`、`encryptJobId`、详情 URL。 | 沟通、打招呼、投递、批量采集、候选人管理。 |
| BOSS 直聘 | 职位详情 | 来自搜索结果的 `securityId`；必要时保留 `encryptJobId` 和来源引用。 | 职位、公司、招聘者、福利、技能、地点、失败类。 | 聊天页、消息发送、简历投递、招聘侧写动作。 |

写前验证只作为未来候选能力：允许 `validate_only`、`draft`、`preview` 语义；禁止上传（upload）、文件选择器（file picker）、`DataTransfer` 注入、提交（submit）、发布（publish）、发送（send）、打招呼（greet）、投递（apply）、关注（follow）、删除（delete）等外部可见动作。首批能力包不实现写前验证，只在后续 #198/#199/#200 设计时消费本 ADR。

### 2. 站点知识层级

| 层级 | Lode 形态 | 内容 | 消费者 | 进入条件 |
| --- | --- | --- | --- | --- |
| 站点知识 | 站点技能（`domain-skill`）或站点知识文档 | 路由、登录态、页面就绪、token、过滤器、页面结构/API 注意点、失败提示、人工操作提示。 | App Library（资产库）、能力作者、智能体、命令行。 | 信息可复核，且不包含运行会话、cookie、原始证据或生产载荷。 |
| 只读能力 | 站点能力包（`site-capability`） | 输入/输出/来源结构定义、归一化器、固定样本数据、资源要求、后置检查、失败映射、后续引用。 | Core、App Library（资产库）、智能体/命令行。 | 有明确只读目标、首批固定样本数据可脱敏、来源到归一化结果可验证。 |
| 写前验证能力 | `site-capability`，操作模式为 `validate_only`、`draft` 或 `preview` | 预检、草稿、预览、风险提示和禁止提交保护（no-submit guard）。 | Core 准入、App 预览、智能体/命令行。 | 明确禁止提交边界，且不执行真实写入、上传、发送或发布。 |
| 未来多步流程 | 流程包（`workflow-package`） | 搜索到详情、详情后评论、创作者中心草稿、BOSS 沟通前检查等步骤编排。 | Core 流程、App 任务入口。 | 依赖的站点能力已经稳定，且失败/恢复点可表示。 |
| 智能体/命令行技能 | `domain-skill` + 能力引用 | 人类可读流程、参数建议、失败解释和命令行复用形态。 | 智能体、命令行、App 辅助面板。 | 不能单独当作可执行合同；必须引用能力包才可进入稳定执行路径。 |

### 3. bb-sites 盘点与选择

| 来源 | 结论 | 理由 |
| --- | --- | --- |
| `bb-sites` 设计原则 | 吸收 | 同源浏览器身份（same-origin）、domain 作为执行边界、直接请求（direct fetch）/请求头求值（header eval）/Pinia store 分层、结构化 `{error,hint,action}`、搜索到详情的后续引用，都适合作为 Lode 能力包设计输入。 |
| `xiaohongshu/search.js` | 改造后吸收 | 使用页面路由、Pinia search store、fetch/XHR 拦截和 `xsec_token` 缓存，适合作为搜索能力的来源/引用机制；需要重写为结构定义、固定样本数据、后置检查和失败映射。 |
| `xiaohongshu/note.js` | 改造后吸收 | 确认详情依赖带签名 URL 或 `note_id + xsec_token`，字段形态可作为详情归一化结果种子；不能直接复制代码。 |
| `xiaohongshu/comments.js` | 参考 | 评论是后续流程/能力候选，不在首批真实任务范围。 |
| `xiaohongshu/user_posts.js` | 参考 | 用户主页和 SSR `__INITIAL_STATE__` 解析可作为后续用户能力知识，不进入首批。 |
| `xiaohongshu/feed.js` | 参考 | feed store 可辅助发现 token 和首页笔记，但不是首批明确任务。 |
| `xiaohongshu/me.js` | 参考 | 登录态和用户 store 检测可沉淀为站点就绪知识，不作为用户数据能力首批交付。 |
| `boss/search.js` | 改造后吸收 | `/wapi/zpgeek/search/joblist.json`、城市/经验/学历过滤、`securityId`、`encryptJobId` 和职位字段是 BOSS 搜索能力种子。 |
| `boss/detail.js` | 改造后吸收 | `/wapi/zpgeek/job/detail.json?securityId=...` 和职位/公司/招聘者字段是详情能力种子。 |

`sources/epiral/bb-sites` 未发现仓库级 LICENSE 文件。Lode 不直接复制 bb-sites 适配脚本源码；只吸收可复核机制、字段、失败类和设计结论，并在后续能力包中重写实现与固定样本数据。

### 4. OpenCLI、浏览器技能、旧 WebEnvoy 盘点与选择

| 来源 | 结论 | Lode 使用方式 |
| --- | --- | --- |
| OpenCLI 小红书站点地图/风险提示/流程文档 | 吸收 | 路由、登录探针、`xsec_token` 要求、创作者中心域名区分、搜索 API 不稳定、页面结构兜底、发布风险说明进入站点知识。 |
| OpenCLI 小红书 `search` / `note` | 改造后吸收 | 页面结构搜索、带签名笔记 URL、详情字段和安全/登录失败类可补充小红书只读能力；OpenCLI Apache-2.0，但后续仍应按 Lode 结构定义重写。 |
| OpenCLI 小红书 `drafts` / `draft-open` | 参考 | 可作为未来草稿/预览写前验证知识，不进入首批。 |
| OpenCLI 小红书 `publish` / `follow` / `delete` 类写动作 | 拒绝进入首批 | 涉及真实发布、关注或删除；只可作为未来强治理写侧研究材料。 |
| OpenCLI BOSS `search` / `detail` / `utils` | 改造后吸收 | BOSS 城市/筛选映射、类型化鉴权错误、带凭据 XHR、分页/去重规则可补强 BOSS 只读能力。 |
| 浏览器技能小红书抓取说明 | 吸收 | 直接搜索 URL、筛选面板、重复页面节点、状态里的 `xsecToken`、不要剥离带 token URL，进入站点技能。 |
| 浏览器技能 BOSS 导航/职位搜索说明 | 吸收 | 单页应用水合、根路径跳转、求职者/招聘者身份、`/wapi` 需要浏览器会话、API 薪资比页面结构更可信，进入站点技能。 |
| 浏览器技能 BOSS 聊天说明 | 参考/拒绝首批 | 只保留“未经明确许可不发送消息”的风险边界；聊天、打招呼、发送消息不进入首批。 |
| 旧 WebEnvoy 小红书读取试验 | 改造后吸收 | 能力信封（ability envelope）、页面目标、准入/失败分类和 detail/user_home 合同可帮助 Lode 输出能力合同；运行桥接属于 Core/Harbor。 |
| 旧 WebEnvoy 小红书写入/真实写入准入 | 参考/拒绝首批 | 默认失败关闭（fail-closed）、身份绑定、操作者确认和禁止不可逆动作约束进入写前验证边界；真实写入不进入首批。 |

### 5. 吸收 / 改造 / 参考 / 拒绝清单

| 类别 | 条目 |
| --- | --- |
| 吸收 | 同源 domain 身份；结构化错误和提示；小红书 `xsec_token` 后续引用；BOSS `securityId` 详情引用；BOSS 城市/筛选/鉴权错误映射；浏览器技能中的页面就绪和选择器注意点；旧 WebEnvoy 读取准入/失败分类。 |
| 改造 | bb-sites 和 OpenCLI 具体适配脚本必须改造成 Lode 结构定义、固定样本数据、后置检查、资源要求、失败映射；OpenCLI 展示列不能直接当输出结构定义；bb-sites `readOnly` 不能替代操作模式/风险分类；旧 WebEnvoy FR 字段需要拆分为 Lode 资产引用、Core 运行引用、Harbor 证据引用。 |
| 参考 | 小红书 comments、user_posts、feed、me；OpenCLI drafts/draft-open/publish 流程；MediaCrawler 字段命名和归一化经验；BOSS 聊天/读取导航；旧 WebEnvoy 真实写入准入。 |
| 拒绝 | 无 license 的源码直拷；把原始页面结构/网络载荷、运行会话或 cookie 存入 Lode；通用浏览器循环作为正式能力；批量 crawler queue；真实发布/提交/上传/发送/打招呼/投递/关注/删除；绕过登录、安全拦截或风控。 |

### 6. 首批能力包的后续实现提示

后续 #198/#199/#200 若创建能力包，应把本 ADR 作为范围载体，并至少产出：

- 每个只读能力的输入结构定义、来源结构定义（source schema）、归一化输出结构定义、归一化器、脱敏固定样本数据、后置检查和失败映射。
- 搜索到详情的后续引用，尤其是小红书带签名笔记 URL / `xsec_token` 和 BOSS `securityId`。
- 资源要求：目标 domain、是否需要已登录浏览器会话、页面就绪探针、账号态失败类、禁止动作。
- 禁写保护：明确只读能力不允许触发提交、发送、发布、上传、关注、删除、投递。

## 影响

本 ADR 让 #197 的产品/资产边界可以被 #198/#199/#200 消费，但不会制造伪能力包或提前承诺运行环境行为。

小红书首批能力被压缩到 search/detail，因为带 token 的后续引用是核心不确定性。评论、用户主页和创作者中心延后，避免在首批混入多步流程和写侧风险。

BOSS 首批能力被压缩到 job search/detail，因为搜索到详情的 `securityId` 链路清晰。聊天、打招呼、投递和候选人管理是外部可见动作，必须等待单独的写前验证或强治理故事。

## 已考虑的替代方案

- 直接迁移 bb-sites 适配脚本代码。拒绝：bb-sites license 不明确，且 Lode 需要结构定义、固定样本数据、后置检查、版本和失败映射，而不是浏览器脚本源码本体。
- 把 OpenCLI 命令列直接作为 Lode 输出结构定义。拒绝：展示列适合命令行展示，不等于稳定归一化结果合同。
- 首批同时包含评论、用户主页、feed、发布草稿和 BOSS 聊天。拒绝：范围扩大到多步流程和写侧交互，会遮蔽 #197 的核心目标。
- 用通用浏览器智能体技能替代能力包。拒绝：技能可以辅助人类和智能体，但没有稳定结构定义、固定样本数据、版本和后置检查，不能成为 Lode 执行事实源。

## 调研证据

以下为 `/Volumes/2T/dev/WebEnvoy` 外层工作区输入 locator；`sources/` 和 `research/` 在本批中只读，不进入 Lode PR 变更。

- `sources/epiral/bb-sites/README.zh-CN.md`, `README.md`, `SKILL.md`, `DESIGN.md`
- `sources/epiral/bb-sites/xiaohongshu/search.js`, `note.js`, `comments.js`, `user_posts.js`, `feed.js`, `me.js`
- `sources/epiral/bb-sites/boss/search.js`, `detail.js`
- `research/synthesis.md`
- `research/absorability/themes/site-knowledge-and-capability-assets.md`
- `research/OpenCLI/wiki/docs/adapters/browser/xiaohongshu.md`, `boss.md`
- `research/OpenCLI/source/sitemaps/xiaohongshu/SITE.md`, `apis.md`, `pitfalls.md`, `pages/explore.md`, `pages/note.md`, `workflows/search.md`, `workflows/publish.md`
- `research/OpenCLI/source/clis/xiaohongshu/search.js`, `note.js`, `drafts.js`, `draft-open.js`, `publish.js`
- `research/OpenCLI/source/clis/boss/search.js`, `detail.js`, `utils.js`
- `research/browser-use/agent-workspace/domain-skills/xiaohongshu/scraping.md`
- `research/browser-use/agent-workspace/domain-skills/BOSS-zhipin/navigation.md`, `job-search.md`, `chat.md`
- `research/lodcel-WebEnvoy/wiki/7-xiao-hong-shu-du-qu-yu-zui-xiao-jiao-hu-shi-li.md`
- `research/lodcel-WebEnvoy/wiki/21-xiao-hong-shu-ming-ling-fang-an-yu-shi-xian-lan-tu-zhong-qi-ji-ci-shou-kong-qian-ti.md`
- `research/lodcel-WebEnvoy/wiki/22-shou-kong-xiao-hong-shu-fa-bu-zui-xiao-bi-huan-fang-an.md`
- `research/lodcel-WebEnvoy/wiki/23-feng-xian-yu-li-wai-kou-jing.md`
- `research/lodcel-WebEnvoy/wiki/25-hou-xuan-neng-li-ji-zhu-fang-an-package-mvp.md`
- `research/lodcel-WebEnvoy/source/work_items/FR-0005-xhs-read-spike/contracts/xhs-read-spike.md`
- `research/lodcel-WebEnvoy/source/work_items/FR-0025-xhs-detail-user-home-commercialization/contracts/detail-user-home-command-surface.md`
- `research/lodcel-WebEnvoy/source/work_items/FR-0008-xhs-write-spike/contracts/xhs-write-spike.md`
- `research/lodcel-WebEnvoy/source/work_items/FR-0031-xhs-creator-live-write-admission/contracts/xhs-creator-live-write-admission.md`

## 实现时待决

- #198/#199/#200 必须决定具体能力包 ID、结构定义文件、固定样本数据格式和后置检查。
- ADR 0002 pending decisions PD-0003、PD-0004、PD-0011 仍然有效，分别对应操作风险枚举、搜索到详情引用和站点技能子结构。
- 如果后续工作要包含 BOSS 沟通，必须先创建独立写前验证故事，并在任何运行环境实现前明确禁止发送保护。
