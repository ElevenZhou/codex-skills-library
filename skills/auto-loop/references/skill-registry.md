# Skill Registry（可被 auto-loop 调度的技能）

auto-loop（别名：老大、小一、大哥、老大哥、大当家、头儿）是总调度。下表声明它可以组织和调用的技能。在 Orchestrate 阶段按任务类型查表，选出要用的技能，并把选择写进 loop ledger。

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
| 项目文档规范 | `project-ops-standards` | | 补齐或审计项目管理与运维文档 |
| 复刻微创新 / 产品技术质量 | `product-tech-quality` | 老四、小四、四哥、四当家 | 拆解对标产品做复刻微创新；产品技术方案评审；质量门禁和发布门禁 |
| 合同审阅 | `xiaowu-contract-review` | 老五、小五、五哥、五当家 | 采购、SaaS、服务、合作类合同的审查与修订 |
| 公司管理 | `company-management` | 老六、小六、六哥、六当家 | 证照、合同台账、签章、资产、权限、到期提醒和归档（不审条款） |
| 市场商务 | `market-business` | 老七、小七、七哥、七当家 | 渠道、客户、合作、投放统筹；先算单位经济和止损线，再小预算验证 |
| 金融增值 | `capital-growth` | 老八、小八、八哥、八当家 | 自有资金投资判断、仓位、止盈止损、复盘（不代下单、不记账） |
| 财务管理 | `finance-management` | 老九、小九、九哥、九当家 | 记账、逐笔对账、现金流、经营报表；视频双站对账转 `video-compute-reconciliation` |
| 运维管理 | `ops-management` | 老十、小十、十哥、十当家 | 只读巡检、故障分层定位、生产变更（盘点→备份→canary→验证→放量），写操作需授权 |
| PPT / 路演材料 | `deck-studio-loop` | | 商业计划书、公司或产品介绍、路演 |
| Word 文档 | `doc` | | `.docx` 读写与排版 |
| PDF | `pdf` | | PDF 读取、生成、审阅 |
| HTML 文档 | `rich-html-docs` | | 可分享的单文件 HTML 文档 |
| 命名 / 域名 | `domain-brand-finder` | | 项目命名、品牌域名 |
| 朋友圈 | `post-wechat-moments` | | 朋友圈图文 |
| 静态图片 | `local-image-generator` | | 一切出图需求；默认 gpt-image-2.5-flare，high 画质 |
| 视频生成 | `local-grok-video-generator-2-0` | | Grok 视频 |
| 视频渠道接入 | `video-channel-onboarding` | | 新视频生成渠道的接入 |
| 视频算力对账 | `video-compute-reconciliation` | | 视频双站与渠道账单的只读对账（智算谷等）；先读其 site-profiles 锁定渠道和金额口径；可接 `video-channel-onboarding` 的新渠道 |
| 前端实现 | `advanced-frontend-design` | | 设计方向已定，做生产级界面 |
| 前端比稿 | `frontend-design-lab` | | 设计方向未定，先出多个方案对比 |
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
| 服务器运维 | `seoul-node-onboarding`、`seoul-server-status-check`、`ccswitch-config-transfer`、`t0-work-session` | | 对应服务器和会话的专项流程 |

## 常见组合

- **复刻一个产品：** 老二（值不值得做）→ 老四（拆对标、复刻微创新、技术方案）→ 老三（推进）→ 老四（发布门禁）→ 老十（上线运维）。
- **线上出故障：** 老十（取证、分层定位、最小处置）→ 老九（受影响请求逐笔核对扣费）→ 老四（预防性质量门禁）。
- **月度经营复盘：** 老九（对账、现金流、经营报表）→ 老七（渠道单位经济）→ 老八（闲置资金配置）→ 老大汇总给本人。
- **合同全流程：** 老五（审条款）→ 本人批准 → 老六（签章、归档、到期提醒）→ 老九（付款 / 回款节点）。
- **新项目从零到可执行：** 老二（立项）→ 老三（推进）→ `deck-studio-loop`（汇报材料）。
- **做网站：** `frontend-design-lab` 或 `advanced-frontend-design` → `local-image-generator`（素材）→ `playwright`（验收）→ 部署技能。
- **合同进来：** 小五审查；涉及项目取舍时，把结论交给老三（`project-employee-agents`）的风险台账。
- **广告：** `overseas-ad-autopilot`（规划）→ `local-image-generator`（素材）→ `meta-ads-auto-publish`（发布）→ `meta-ads-analysis`（复盘）。

## 维护

新增或下线技能时，同步更新本表和技能库 README。别名必须同时写进对应技能的 `description`，否则在 auto-loop 之外说别名不会触发。
