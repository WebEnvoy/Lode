# 真实页面写前验证能力

本合同原覆盖 GitHub #200/#213/#214/#215/#216。LODE-236 在 milestone #14 下
刷新小红书部分以覆盖 FR #235/#238/#239。Lode 提供能力包、结构定义、脱敏固定样本、
后置检查、失败分类和本地登记表发现能力；Core/App/Harbor 后续可消费这些事实生成写前预览。
本合同不授权真实发布、投递、打招呼、发送消息、上传或保存到外部站点。

## 能力包

| 站点 | package ref | 路径 | 目标 |
| --- | --- | --- | --- |
| 小红书 | `lode://site-capability/xiaohongshu/publish-note-precheck@0.1.0` | `sites/xiaohongshu/publish-note-precheck` | 创作中心发布页、标题/正文编辑目标和不发布边界 |
| BOSS 直聘 | `lode://site-capability/boss/greet-precheck@0.1.0` | `sites/boss/greet-precheck` | 职位/招聘者沟通目标、招呼语预览和不发送边界 |

两个包的 `operation_mode` 都是 `validate_only`。登记表和固定样本均声明
`no_submit_guard: active` 与 `true_write_execution: blocked`，只允许产生预期变更、
风险提示、写前检查结果和未提交状态。

## 统一输出

两个包共享以下输出语义：

- `expected_change`：说明准备影响哪个页面目标、哪些字段会被预览、是否存在外部提交。
- `risk_hints`：说明用户必须复核、目标可能变化、证据可能失效和 no-submit guard 必须生效。
- `no_submit_guard_status`：固定为 `active`。
- `source_refs` / `evidence_refs`：只保存占位引用，不保存完整页面、网络响应、截图正文或生产材料。
- `failure_mapping`：区分页变化、登录不足、权限不足、目标不可写、站点安全拦截、用户取消和资源不可用。

## 参考材料吸收

小红书吸收：

- `docs/contracts/bb-sites-xhs-boss-absorption-freeze.md`
- `docs/adr/0006-xhs-boss-site-knowledge-selection.md`
- `research/subjects/epiral/bb-sites/wiki/versions/9aba7d0d/index.md`
- `research/subjects/epiral/bb-sites/wiki/versions/9aba7d0d/pages/4.1-xiaohongshu-suite.md`
- `research/subjects/epiral/bb-sites/wiki/versions/9aba7d0d/pages/3.2-adapter-patterns-and-approaches.md`
- `research/subjects/epiral/bb-sites/wiki/versions/9aba7d0d/pages/3.3-authentication-and-browser-sessions.md`
- `research/subjects/jackwener/OpenCLI/wiki/versions/09a0af7a/pages/5.6-site-sitemaps.md`
- `research/subjects/rmourey26/WebEnvoy/wiki/versions/HEAD/pages/21-xiao-hong-shu-ming-ling-mian-sou-suo-xiang-qing-yong-hu-zhu-ye-yu-bian-ji-qi-shu-ru.md`
- `research/subjects/rmourey26/WebEnvoy/wiki/versions/HEAD/pages/22-shou-kong-shi-shi-xie-ru-fa-bu-zhun-ru-yu-shang-chuan-zheng-ju-bu-huo.md`
- `research/subjects/rmourey26/WebEnvoy/wiki/versions/HEAD/pages/23-feng-xian-men-jin-zhang-hao-an-quan-yu-xie-ru-mo-ren-suo.md`
- `sources/epiral/bb-sites/xiaohongshu/search.js`
- `sources/epiral/bb-sites/xiaohongshu/note.js`
- `sources/epiral/bb-sites/xiaohongshu/comments.js`
- `sources/epiral/bb-sites/xiaohongshu/user_posts.js`
- `sources/epiral/bb-sites/xiaohongshu/feed.js`
- `sources/epiral/bb-sites/xiaohongshu/me.js`

吸收内容：创作中心独立来源、发布页 URL、内容编辑入口、编辑器输入验证、页面就绪、
登录/风控/签名链接/来源引用的失败分类，以及 bb-sites 的同源会话、结构化失败和
搜索到详情引用机制。未吸收：源码复制、图片上传、文件选择、草稿保存、发布按钮、
定时发布和真实写入路径。

LODE-236 小红书写前验证补充：

- `publish-note-precheck` 只声明 `validate_only`，`no_submit_guard: active`，
  `true_write_execution: blocked`。
- 输出必须包含 `expected_change`、`risk_hints`、`no_submit_guard_status`、
  `source_refs` 和 `evidence_refs`。
- 后置检查计划只验证目标仍可定位、预期变更仍是 preview、外部提交仍为 false、
  source/evidence 仍为 refs-only。

BOSS 吸收：

- `docs/adr/0006-xhs-boss-site-knowledge-selection.md`
- `sources/epiral/bb-sites/boss/search.js`
- `sources/epiral/bb-sites/boss/detail.js`
- `research/subjects/jackwener/OpenCLI/wiki/versions/raw/pages/3.1-built-in-commands-reference.md`
- `research/subjects/Panniantong/Agent-Reach/wiki/versions/raw/pages/3.9-instagram-linkedin-and-boss-channels.md`

吸收内容：职位搜索/详情中的 `securityId`、`encryptJobId`、职位、公司和招聘者摘要作为
沟通目标引用；greet/send/batchgreet 等写侧命令只作为必须阻断真实动作的站点表面；
登录、职位下架、目标不可写、页面变化和沟通入口缺失作为失败分类。未吸收：源码复制、
打招呼、批量打招呼、发送消息、投递简历和聊天动作。

## 非目标

- 不新增 Core、Harbor 或 App 代码。
- 不访问真实账号或站点页面，不产生 live evidence。
- 不保存账号、运行现场、完整页面、网络响应、生产载荷或用户业务明文。
- 不修改 GitHub 依赖图，不关闭 issue，不合并 PR。
