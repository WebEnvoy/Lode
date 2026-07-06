# bb-sites 小红书与 BOSS 吸收冻结

状态：拟定，2026-07-06。

本合同覆盖 Lode #230/#231/#232/#233/#234，锚点工作项为 #231。它冻结从
`epiral/bb-sites` 吸收的小红书和 BOSS 站点知识、字段映射、许可证边界、首批能力范围和执行前用户确认事项。

## 证据来源

本次只读消化以下位置，不复制源码，不访问真实账号，不生成真实证据：

- `sources/epiral/bb-sites@f0cdfbf17e0f`: `SKILL.md`, `DESIGN.md`, `README.md`, `xiaohongshu/search.js`, `xiaohongshu/note.js`, `xiaohongshu/comments.js`, `xiaohongshu/feed.js`, `xiaohongshu/me.js`, `xiaohongshu/user_posts.js`, `boss/search.js`, `boss/detail.js`
- `research/subjects/epiral/bb-sites/wiki/versions/9aba7d0d/pages/4.1-xiaohongshu-suite.md`
- `research/subjects/epiral/bb-sites/wiki/versions/9aba7d0d/pages/5.2-boss-zhipin-adapters.md`
- `research/subjects/epiral/bb-sites/wiki/versions/9aba7d0d/pages/3.2-adapter-patterns-and-approaches.md`
- `research/subjects/epiral/bb-sites/wiki/versions/9aba7d0d/pages/3.3-authentication-and-browser-sessions.md`
- `research/absorability/themes/site-knowledge-and-capability-assets.md`
- Existing Lode carriers under `sites/xiaohongshu/**`, `sites/boss/**`, `docs/adr/0006-xhs-boss-site-knowledge-selection.md`, and `docs/contracts/*-capabilities.md`

## 吸收 / 参考 / 拒绝

| 类别 | 内容 | 进入 Lode 的方式 |
| --- | --- | --- |
| 吸收 | `domain` 作为同源身份边界、登录态复用、`credentials: include`、结构化 `{error,hint}`、搜索到详情的后续引用。 | 写入能力包资源要求、失败映射、后置检查和本合同。 |
| 吸收 | 小红书 Vue/Pinia hydration、search/note/user/feed store 就绪、`xsec_token` 或带签名 URL 作为详情引用。 | 已冻结到 `search-notes` 和 `read-note-detail` 的 input/output/resource/failure 合同。 |
| 吸收 | BOSS `/wapi/zpgeek/search/joblist.json` 和 `/wapi/zpgeek/job/detail.json?securityId=...` 的只读来源形态。 | 已冻结到 `job-search` 和 `read-job-detail` 的字段映射、fixture、post-check。 |
| 吸收 | bb-sites 的“搜索索引轻量、详情再展开”原则。 | 首批只读能力保持 search/detail 两段式，不把全文、评论或批量分页塞进搜索结果。 |
| 参考 | 小红书 comments、feed、me、user_posts。 | 只作为后续评论、feed、用户主页或登录探针知识；不进入首批真实能力。 |
| 参考 | BOSS 聊天、打招呼、发送、投递相关站点表面。 | 只作为写前验证风险词汇；不执行外部可见动作。 |
| 拒绝 | 直接复制 bb-sites adapter 源码、helper、XHR/fetch monkey-patch 代码、Pinia store 调用代码。 | bb-sites 根目录未发现 LICENSE；Lode 只重写为 schema/fixture/post-check/metadata。 |
| 拒绝 | Cookie、token、profile、runtime session、raw DOM、HAR、完整 screenshot body、生产 payload、用户业务明文。 | Lode 只保存 source/evidence refs 和脱敏 fixture。 |
| 拒绝 | 发布、上传、保存、发送、打招呼、投递、关注、删除、绕过验证码或风控。 | 当前包仅 `read` 或 `validate_only`；true write 继续 blocked/deferred。 |

## 小红书字段映射

| 能力 | bb-sites 来源 | Lode 输入 | Lode 输出字段 | follow-up / 失败边界 |
| --- | --- | --- | --- | --- |
| `xiaohongshu/search-notes` | `xiaohongshu/search.js`, wiki 4.1 | `url`, `keyword`, `sort`, `limit` | `keyword`, `sort`, `result_count`, `notes[].title`, `notes[].author`, `notes[].interaction_metrics`, `notes[].note_id`, `notes[].xsec_token`, `notes[].url`, `follow_up_ref` | 详情必须消费搜索产生的带签名 URL 或 `note_id + xsec_token`；失败类包括未登录、页面未就绪、安全拦截、字段缺失。 |
| `xiaohongshu/read-note-detail` | `xiaohongshu/note.js`, wiki 4.1 | 带签名笔记 `url`；可选 `note_id`、`xsec_token` | `title`, `body_summary`, `author`, `interaction_metrics`, `tags`, `image_refs`, `published_at_hint`, `ip_location_hint`, `source_citation` | 缺少 `xsec_token` 不自动探索或绕过；要求用户/Core 提供搜索结果后续引用。 |

小红书评论、feed、当前用户和用户主页只保留为后续候选。它们不能扩展本批搜索/详情能力的完成口径。

## BOSS 字段映射

| 能力 | bb-sites 来源 | Lode 输入 | Lode 输出字段 | follow-up / 失败边界 |
| --- | --- | --- | --- | --- |
| `boss/job-search` | `boss/search.js`, wiki 5.2 | `url`, `query`, `city`, `experience`, `degree`, `salary`, `industry`, `page` | `query`, `city`, `filters`, `result_count`, `jobs[].name`, `jobs[].salary`, `jobs[].company`, `jobs[].location`, `jobs[].experience`, `jobs[].degree`, `jobs[].skills`, `jobs[].welfare`, `jobs[].recruiter`, `jobs[].securityId`, `jobs[].encryptJobId`, `detail_ref` | 第一页只读搜索；分页和批量采集不进入首批。 |
| `boss/read-job-detail` | `boss/detail.js`, wiki 5.2 | 详情 `url`、必需 `securityId`、可选 `encryptJobId` | `job.description`, `job.salary`, `job.experience`, `job.degree`, `job.location`, `job.address`, `job.skills`, `job.status`, `company.name`, `company.stage`, `company.scale`, `company.industry`, `company.intro`, `recruiter.name`, `recruiter.title` | `securityId` 必须来自搜索后续引用；失败类包括身份不足、需要验证码、职位过期、权限不足。 |

## 首批能力冻结

| 站点 | 只读能力 | 写前验证能力 | 当前状态 |
| --- | --- | --- | --- |
| 小红书 | `search-notes`, `read-note-detail` | `publish-note-precheck` | 拟定；静态合同、脱敏样本、后置检查和本地登记表已可校验；真实页面验证等待人工登录浏览器。 |
| BOSS | `job-search`, `read-job-detail` | `greet-precheck` | 拟定；静态合同、脱敏样本、后置检查和本地登记表已可校验；真实页面验证等待人工登录浏览器。 |

写前验证只允许输出预期变化、风险提示、目标/来源/证据引用和禁止提交保护。它不代表可发布、可发送、可投递或可保存。

## 执行前用户确认

任何 Core/Harbor/App 后续真实运行前，必须先由用户明确确认：

- 使用哪个用户控制的浏览器 profile 和目标 tab。
- 允许的站点、页面和动作边界：只读 search/detail 或 validate-only precheck。
- 禁止动作仍然生效：不发布、不上传、不保存、不发送、不打招呼、不投递、不关注、不绕过验证码或风控。
- 证据只保存 refs 和脱敏摘要；不保存 cookie/token/profile/raw DOM/HAR/screenshot body/生产 payload。
- 若出现登录墙、验证码、安全拦截、权限不足、职位下架或签名引用缺失，流程停止并请求人工处理。

## 覆盖与非目标

覆盖：#231 素材盘点、#232 入口/页面/字段来源映射、#233 license 与不可吸收边界、#234 首批能力边界和执行前确认。

非目标：不新增运行时代码，不修改 Harbor/Core/App，不创建真实站点执行，不关闭 issue，不 merge PR，不把 bb-sites 源码迁入 Lode。
