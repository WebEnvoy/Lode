# ADR 0006: 小红书与 BOSS 站点知识吸收边界

## Status

Accepted, 2026-07-06.

## Context

Lode #197 需要在 milestone #13「小红书与 BOSS 站点能力产品化」下完成产品和资产边界盘点，覆盖 #201/#202/#203/#204/#217，以及 #197 comment 中的语义故事 #13/#14。

本 ADR 只冻结站点知识、吸收清单和首批真实任务范围。它不创建真实 capability package，不实现小红书或 BOSS 执行代码，不进入 #198/#199/#200 的 package/schema/fixture/validator 实现。

Lode 的边界仍沿用 ADR 0002、ADR 0004、ADR 0005：Lode 是站点知识、能力包、schema、normalizer、fixture 和 post-check 的事实源；Core 负责执行和结果事实；Harbor 负责 browser runtime、profile、session 和 evidence refs；App 负责 Library 展示、配置和人机入口。

## Decision

### 1. 首批真实任务范围

| 站点 | 首批 read capability | 首批输入边界 | 首批输出边界 | 明确不覆盖 |
| --- | --- | --- | --- | --- |
| 小红书 | 搜索笔记 | `keyword`，后续可扩展 sort/filter；必须记录登录、页面就绪、安全拦截和空结果失败类。 | 笔记行、标题、作者、互动数、`note_id`、`xsec_token` 或 signed note URL、follow-up ref。 | 评论、用户主页、feed、收藏、点赞、下载、关注、删除、发布。 |
| 小红书 | 笔记详情 | signed note URL，或 `note_id` + `xsec_token`，优先由搜索结果 follow-up ref 传入。 | 标题、正文、作者、互动数、标签、图片 refs、发布时间、IP 属地、source refs。 | 评论分页、用户主页、作者统计、创作者中心。 |
| BOSS 直聘 | 职位搜索 | `query`、城市、经验、学历、薪资、行业等小集合过滤；必须记录账号态、城市解析和分页风险。 | 职位行、薪资、公司、地点、经验、学历、技能、boss 元信息、`securityId`、`encryptJobId`、detail URL。 | 沟通、打招呼、投递、批量采集、候选人管理。 |
| BOSS 直聘 | 职位详情 | 来自搜索结果的 `securityId`；必要时保留 `encryptJobId` 和 source refs。 | 职位、公司、招聘者、福利、技能、地点、失败类。 | 聊天页、消息发送、简历投递、招聘侧写动作。 |

写前验证只作为未来候选能力：允许 `validate_only`、`draft`、`preview` 语义；禁止 upload、file picker、DataTransfer injection、submit、publish、send、greet、apply、follow、delete 等外部可见动作。首批 package 不实现写前验证，只在后续 #198/#199/#200 设计时消费本 ADR。

### 2. 站点知识层级

| 层级 | Lode 形态 | 内容 | 消费者 | 进入条件 |
| --- | --- | --- | --- | --- |
| 站点知识 | `domain-skill` 或站点知识文档 | 路由、登录态、页面就绪、token、过滤器、DOM/API caveat、失败提示、人工操作提示。 | App Library、能力作者、agent、CLI。 | 信息可复核，且不包含 session、cookie、raw evidence 或生产 payload。 |
| 只读能力 | `site-capability` | input/output/source schema、normalizer、fixture、resource requirements、post-check、failure mapping、follow-up refs。 | Core、App Library、agent/CLI。 | 有明确只读目标、首批 fixture 可脱敏、source 到 normalized result 可验证。 |
| 写前验证能力 | `site-capability`，operation mode 为 `validate_only`、`draft` 或 `preview` | 预检、草稿、预览、风险提示和 no-submit guard。 | Core admission、App 预览、agent/CLI。 | 明确 no-submit 边界，且不执行真实写、上传、发送或发布。 |
| 未来多步流程 | `workflow-package` | search-to-detail、详情后评论、创作者中心草稿、BOSS 沟通前检查等步骤编排。 | Core workflow、App 任务入口。 | 依赖的站点能力已经稳定，且失败/恢复点可表示。 |
| agent/CLI 技能 | `domain-skill` + capability refs | 人类可读流程、参数建议、失败解释和命令行复用形态。 | agent、CLI、App 辅助面板。 | 不能单独当作可执行合同；必须引用 capability package 才能进入稳定执行路径。 |

### 3. bb-sites 盘点与选择

| 来源 | 结论 | 理由 |
| --- | --- | --- |
| `bb-sites` 设计原则 | 吸收 | same-origin 浏览器身份、domain 作为执行边界、direct fetch / header eval / Pinia store 分层、结构化 `{error,hint,action}`、search-to-detail follow-up refs 都适合作为 Lode package 设计输入。 |
| `xiaohongshu/search.js` | 改造后吸收 | 使用页面路由、Pinia search store、fetch/XHR 拦截和 `xsec_token` 缓存，适合作为搜索 capability 的 source/ref 机制；需要重写为 schema、fixture、post-check 和 failure mapping。 |
| `xiaohongshu/note.js` | 改造后吸收 | 确认详情依赖 signed URL 或 `note_id + xsec_token`，字段形态可作为详情 normalized result seed；不能直接复制代码。 |
| `xiaohongshu/comments.js` | 参考 | 评论是后续 workflow/capability 候选，不在首批真实任务范围。 |
| `xiaohongshu/user_posts.js` | 参考 | 用户主页和 SSR `__INITIAL_STATE__` 解析可作为后续用户能力知识，不进入首批。 |
| `xiaohongshu/feed.js` | 参考 | feed store 可辅助发现 token 和首页笔记，但不是首批明确任务。 |
| `xiaohongshu/me.js` | 参考 | 登录态和用户 store 检测可沉淀为 site readiness 知识，不作为用户数据能力首批交付。 |
| `boss/search.js` | 改造后吸收 | `/wapi/zpgeek/search/joblist.json`、城市/经验/学历过滤、`securityId`、`encryptJobId` 和职位字段是 BOSS 搜索 capability seed。 |
| `boss/detail.js` | 改造后吸收 | `/wapi/zpgeek/job/detail.json?securityId=...` 和职位/公司/招聘者字段是详情 capability seed。 |

`sources/epiral/bb-sites` 未发现仓库级 LICENSE 文件。Lode 不直接复制 bb-sites adapter 源码；只吸收可复核机制、字段、失败类和设计结论，并在后续 package 中重写实现与 fixture。

### 4. OpenCLI、浏览器技能、旧 WebEnvoy 盘点与选择

| 来源 | 结论 | Lode 使用方式 |
| --- | --- | --- |
| OpenCLI 小红书 sitemap / pitfalls / workflows | 吸收 | 路由、登录探针、`xsec_token` 要求、creator host 区分、搜索 API 不稳定、DOM fallback、publish 风险说明进入站点知识。 |
| OpenCLI 小红书 `search` / `note` | 改造后吸收 | DOM 搜索、signed note URL、详情字段和安全/登录失败类可补充小红书 read capability；OpenCLI Apache-2.0，但后续仍应按 Lode schema 重写。 |
| OpenCLI 小红书 `drafts` / `draft-open` | 参考 | 可作为未来草稿/预览写前验证知识，不进入首批。 |
| OpenCLI 小红书 `publish` / `follow` / `delete` 类写动作 | 拒绝进入首批 | 涉及真实发布、关注或删除；只可作为未来强治理写侧研究材料。 |
| OpenCLI BOSS `search` / `detail` / `utils` | 改造后吸收 | BOSS city/filter map、typed auth errors、`bossFetch` XHR with credentials、分页/去重规则可补强 BOSS read capability。 |
| 浏览器技能小红书 scraping | 吸收 | 直接搜索 URL、筛选面板、重复 DOM 节点、state 中 `xsecToken`、不要剥离 tokenized URL，进入 domain-skill。 |
| 浏览器技能 BOSS navigation/job-search | 吸收 | SPA hydration、root redirect、job seeker/recruiter 身份、`/wapi` 需要浏览器 session、API 薪资比 DOM 更可信，进入 domain-skill。 |
| 浏览器技能 BOSS chat | 参考/拒绝首批 | 只保留“未经明确许可不发送消息”的风险边界；聊天、打招呼、发送消息不进入首批。 |
| 旧 WebEnvoy 小红书 read spike | 改造后吸收 | ability envelope、page target、gate/failure 分类和 detail/user_home 合同可帮助 Lode 输出 capability 合同；运行桥接属于 Core/Harbor。 |
| 旧 WebEnvoy 小红书 write / live write admission | 参考/拒绝首批 | fail-closed、identity binding、operator confirmation 和 no irreversible action 约束进入写前验证边界；真实写不进入首批。 |

### 5. 吸收 / 改造 / 参考 / 拒绝清单

| 类别 | 条目 |
| --- | --- |
| 吸收 | same-origin domain identity；结构化错误和 hint；小红书 `xsec_token` follow-up refs；BOSS `securityId` detail ref；BOSS city/filter/auth error map；浏览器技能中的页面就绪和 selector caveat；旧 WebEnvoy read gate/failure 分类。 |
| 改造 | bb-sites 和 OpenCLI concrete adapters 必须改造成 Lode schema、fixture、post-check、resource requirements、failure mapping；OpenCLI columns 不能直接当 output schema；bb-sites `readOnly` 不能替代 operation mode/risk taxonomy；旧 WebEnvoy FR 字段需要拆分为 Lode asset refs、Core runtime refs、Harbor evidence refs。 |
| 参考 | 小红书 comments、user_posts、feed、me；OpenCLI drafts/draft-open/publish workflow；MediaCrawler 字段命名和 normalization 经验；BOSS chat/read navigation；旧 WebEnvoy live write gates。 |
| 拒绝 | 无 license 的源码直拷；把 raw DOM/network/session/cookie 存入 Lode；generic browser loop 作为正式能力；批量 crawler queue；真实 publish/submit/upload/send/greet/apply/follow/delete；绕过登录、安全拦截或风控。 |

### 6. 首批 package 的后续实现提示

后续 #198/#199/#200 若创建 package，应把本 ADR 作为 scope carrier，并至少产出：

- 每个 read capability 的 input schema、source schema、normalized output schema、normalizer、redacted fixture、post-check 和 failure mapping。
- search-to-detail follow-up refs，尤其是小红书 signed note URL / `xsec_token` 和 BOSS `securityId`。
- resource requirements：目标 domain、是否需要已登录浏览器 session、页面就绪探针、账号态失败类、禁止动作。
- no-write guard：明确 read capability 不允许触发提交、发送、发布、上传、关注、删除、投递。

## Consequences

本 ADR 让 #197 的产品/资产边界可以被 #198/#199/#200 消费，但不会制造伪 package 或提前承诺 runtime 行为。

小红书首批能力被压缩到 search/detail，因为 tokenized follow-up ref 是核心不确定性。评论、用户主页和创作者中心延后，避免在首批混入多步流程和写侧风险。

BOSS 首批能力被压缩到 job search/detail，因为搜索到详情的 `securityId` 链路清晰。聊天、打招呼、投递和候选人管理是外部可见动作，必须等待单独的写前验证或强治理故事。

## Alternatives Considered

- 直接迁移 bb-sites adapter 代码。拒绝：bb-sites license 不明确，且 Lode 需要 schema、fixture、post-check、version 和 failure mapping，而不是浏览器脚本源码本体。
- 把 OpenCLI 命令列直接作为 Lode output schema。拒绝：columns 适合 CLI 展示，不等于稳定 normalized result contract。
- 首批同时包含评论、用户主页、feed、发布草稿和 BOSS 聊天。拒绝：范围扩大到多步流程和写侧交互，会遮蔽 #197 的核心目标。
- 用 generic browser agent skill 替代 capability package。拒绝：技能可以辅助人类和 agent，但没有稳定 schema/fixture/version/post-check，不能成为 Lode 执行事实源。

## Research Evidence

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

## Implementation-time Decisions

- #198/#199/#200 must decide exact package IDs, schema files, fixture format and post-checks.
- ADR 0002 pending decisions PD-0003、PD-0004、PD-0011 remain active for operation risk enum、search-to-detail references and domain-skill substructure.
- If later work wants to include BOSS communication, it must create a separate write-precheck story with explicit no-send guard before any runtime implementation.
