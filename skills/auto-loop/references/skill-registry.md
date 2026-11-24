# Skill Registry（可被 auto-loop 调度的技能）

auto-loop（别名：老大、大哥、老大哥、大当家、头儿）是总调度。下表声明它可以组织和调用的技能。在 Orchestrate 阶段按任务类型查表，选出要用的技能，并把选择写进 loop ledger。

## 调用约定

1. **先查表，再动手。** 表里有对口技能时，必须先加载该技能的 `SKILL.md` 并按它的流程执行，不要自己重写一套。
2. **加载方式：**
   - Claude Code：用 Skill 工具按技能名调用（例如 `local-image-generator`）。
   - Codex：按 `$<skill-name>` 引用，或读取 `$CODEX_HOME/skills/<skill-name>/SKILL.md`。
   - 本机没装这个技能时，到技能库仓库 `skills/<skill-name>/SKILL.md` 里读，并在交付中注明"技能未安装"。
3. **别名：** 用户说出别名等于点名该技能。
4. **主从关系：** auto-loop 只负责目标契约、调度、QA 和交付。被调技能内部的门禁（例如小五的"未经许可不改合同"、广告技能的"启停投放需授权"）**优先于** auto-loop 的"免打扰"原则，不得绕过。
5. **分工：** 并行使用多个技能时，每个技能对应 ledger 里的一条 lane，各自写入不重叠的文件。
6. **记录：** 在 ledger 里记下用了哪些技能、为什么用、产出在哪里。表里没有对口技能时，写明"无对口技能，内部完成"。

## 技能表

| 任务类型 | 技能 | 别名 | 何时调用 |
| --- | --- | --- | --- |
| 项目立项 / 可行性 | `project-inception-analysis-cockpit` | 小二、老二、二哥、二当家 | 判断项目该不该做：市场、竞品、开源选型、十角色评审、立项结论 |
| 项目持续推进 | `project-employee-agents` | 小三、老三、三哥、三神、三当家 | 立项后的计划、执行、上线、运营；按岗位和阶段交付管理成果 |
| APK/游戏逆向重建 | `rebuild-workflow`（总控）+ `rebuild-recon` + `rebuild-asset-recovery` + `rebuild-device-evidence` + `rebuild-product-design` + `rebuild-dev-milestones` + `rebuild-build-release` | 老大统筹；老三项目执行；技术经理/产品经理/设计经理/测试经理按阶段参与 | 允许所有作品进入分析，正式发布必须人工确认所有权（G-PUBLISH）；REA 负责静态/ADB Evidence，rebuild 技能负责 A0、S0-S7、R1/R2/R3、D1-D9、重写和交付；独立发布仓库 github.com/ElevenZhou/apk-rebuild-skills |
| 游戏开发（原创 / 按 GDD） | `game-dev-workflow`（总控）+ `game-design-economy` + `godot-game-dev` + `game-playtest-qa` | | 从立项到上线的 G0–G6 门禁、玩法数值、Godot 工程、试玩与埋点；逆向后的重做另叠加 rebuild-* |
| 项目治理 / 新项目规范 | `project-governance` | | 统一项目骨架、文档节点更新、日终 Git checkpoint；底层运维文档仍由 `project-ops-standards` 承担 |
| 项目文档规范 | `project-ops-standards` | | 补齐或审计项目管理与运维文档 |
| 复刻微创新综合工作组 | `product-tech-quality` | 老四、小四、四哥、四当家 | 对标拆解、微创新、技术方案、质量门禁和发布门禁 |
| 合同审阅 | `xiaowu-contract-review` | 小五 | 采购、SaaS、服务、合作类合同的审查与修订 |
| 公司管理 / 证照 / 合同归档 | `company-management` | 老六、小六、六哥、六当家 | 公司底账、证照、合同台账、签章、资产和到期跟踪；不代签、不盖章 |
| 市场商务 / 增长 | `market-business` | 老七、小七、七哥、七当家 | 客户、渠道、合作、报价和投放方案；不擅自发消息、签约或花预算 |
| 投资判断 / 资产配置 | `capital-growth` | 老八、小八、八哥、八当家 | 自有资金的研究、仓位、止盈止损与复盘；不代下单、不记账 |
| 财务 / 对账 / 回款 | `finance-management` | 老九、小九、九哥、九当家 | 记账、对账、成本、毛利、回款和经营报表；逐笔核对 |
| 服务器运维 / 生产变更 | `ops-management` | 老十、小十、十哥、十当家 | 服务器、网关、节点、监控、安全、故障和生产变更；先只读，变更需授权 |
| PPT / 路演材料 | `deck-studio-loop` | | 商业计划书、公司或产品介绍、路演 |
| Word 文档 | `doc` | | `.docx` 读写与排版 |
| PDF | `pdf` | | PDF 读取、生成、审阅 |
| HTML 文档 | `rich-html-docs` | | 可分享的单文件 HTML 文档 |
| 命名 / 域名 | `domain-brand-finder` | | 项目命名、品牌域名 |
| 朋友圈 | `post-wechat-moments` | | 朋友圈图文 |
| 静态图片 | `local-image-generator` | | 一切出图需求；默认 gpt-image-2.5-flare，high 画质 |
| 模型选型 / 注册表 | `llm-model-registry` | | 从本地模型注册表选择渠道、查询模型和执行调用前检查 |
| 视频生成 | `local-grok-video-generator-2-0` | | Grok 视频 |
| 视频渠道接入 | `video-channel-onboarding` | | 新视频生成渠道的接入 |
| 视频算力对账 | `video-compute-reconciliation` | | 视频双站与渠道账单的只读对账（智算谷等）；先读其 site-profiles 锁定渠道和金额口径；可接 `video-channel-onboarding` 的新渠道 |
| 前端实现 | `advanced-frontend-design` | | 设计方向已定，做生产级界面 |
| 前端比稿 | `frontend-design-lab` | | 设计方向未定，先出多个方案对比 |
| 设计比稿（高水准多方向） | `design-pitch` | 比稿、设计比稿、出三版 | 用真实数据并行做 3 个互斥视觉方向，浏览器验收 + 改一轮 + 对照台 + 按场景推荐；默认审美多色彩高饱和梦幻科技动感 |
| 前端二审 | `frontend-design-review` | | 现成页面/截图/代码的分级评审，默认不改代码 |
| 落地页审美 | `taste-skill`（触发名 `design-taste-frontend`） | | 落地页、作品集、改版 |
| 浏览器自动化 | `playwright` | | 网页操作、截图、UI 流程验证 |
| 持续调试 | `playwright-interactive` | | 持久浏览器 / Electron 调试 |
| 系统截图 | `screenshot` | | 浏览器工具拿不到的窗口截图 |
| 部署 | `cloudflare-deploy`、`vercel-deploy` | | 上线发布（属于外部变更，按授权边界执行） |
| Agent 架构 | `production-agent-architecture` | | 设计生产级 agent |
| Agent 代码 | `agent-scaffolder` | | 根据 spec 生成可运行的 agent 项目 |
| CLI 封装 | `cli-creator` | | 把 API 或脚本封装成 CLI |
| 广告规划 | `overseas-ad-autopilot` | | 海外投放规划 |
| 广告分析 | `meta-ads-analysis` | | Meta 广告只读分析 |
| 广告控制 | `meta-ads-control` | | 启停投放（需授权） |
| 广告发布 | `meta-ads-auto-publish` | | 发布已备好的广告草稿（需授权） |
| 知识沉淀 | `obsidian-memory` | | 把结论、决策写入 Obsidian |
| 成果归档 | `submit-results-to-workbench`、`flaios-content-submit`、`personal-workbench` | | 交付后归档到工作台或 FlaiOS |
| 邮件 | `gmail-mail` | | Gmail 收发 |
| 飞书 | `lark-*` 系列 | | 飞书文档、表格、消息、日历、任务等（以本机已安装的为准） |
| 服务器运维专项 | `seoul-node-onboarding`、`seoul-server-status-check`、`ccswitch-config-transfer`、`t0-work-session` | | 对应服务器和会话的专项流程；由老十统筹 |
| 重要结论通知 / 成果回写 | `feishu-webhook-push`、`submit-results-to-workbench`、`personal-workbench` | | 重要信息和关键结论按项目指向推送飞书；完成后回写工作台 |

## 常见组合

- **新项目从零到可执行：** 老二（立项）→ 老三（推进）→ `deck-studio-loop`（汇报材料）。
- **APK/游戏重建：** 老大（总调度）→ `rebuild-workflow` S0 → `rebuild-recon` + REA（S1/S2）→ 老三/项目经理推进 `rebuild-product-design`、`rebuild-dev-milestones` → `rebuild-device-evidence` 真机验收 → `rebuild-build-release` 交付。
- **做网站：** `frontend-design-lab` 或 `advanced-frontend-design` → `local-image-generator`（素材）→ `playwright`（验收）→ 部署技能。
- **合同进来：** 小五审查；涉及项目取舍时，把结论交给老三（`project-employee-agents`）的风险台账。
- **广告：** `overseas-ad-autopilot`（规划）→ `local-image-generator`（素材）→ `meta-ads-auto-publish`（发布）→ `meta-ads-analysis`（复盘）。

## 维护

新增或下线技能时，同步更新本表和技能库 README。别名必须同时写进对应技能的 `description`，否则在 auto-loop 之外说别名不会触发。
