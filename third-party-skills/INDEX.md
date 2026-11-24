# 第三方技能镜像（本机已安装）

来源：`~/.agents/skills`（Claude Code / Codex 的技能目录多为它的软链接或拷贝），2026-11-24 快照；目录名已去掉版本号后缀，文件内容未改。

> **未随包带 LICENSE，授权依据不明；仅作本机备份与同步。** 公开分发前必须逐个确认授权。这些技能**不受** `scripts/lint-skills.py` 约束，也不在 `scripts/install-skills.sh` 的默认安装范围。
> 未收录：`autoglm-browser-agent`（约 160MB，含依赖与构建产物）。

## 飞书 / Lark

| 技能 | 说明 |
| --- | --- |
| `feishu-chat-history` | Fetch and summarize Feishu group chat history. Use when the user asks to read, review, or summarize messages f |
| `feishu-cron-reminder` | Create cron jobs that reliably deliver reminders to Feishu (飞书) chats. Use when the user asks to set up schedu |
| `feishu-doc` | Fetch content from Feishu (Lark) Wiki, Docs, Sheets, and Bitable. Automatically resolves Wiki URLs to real ent |
| `feishu-drive` | 飞书云空间文件管理 Skill。上传/下载/移动/搜索文件、创建文件夹、获取元数据等。当需要管理飞书云空间中的文件和文件夹时使用此 Skill。 |
| `feishu-perm` | Feishu permission management for documents and files. Activate when user mentions sharing, permissions, collab |
| `feishu-screenshot` | Capture macOS screenshots and send to Feishu. Use when the user asks to take a screenshot and share it via Fei |
| `feishu-send-file` | Send files to a Feishu group or user via REST API. Use when the user explicitly asks to send a file, attachmen |
| `lark-approval` | 飞书审批 API：审批实例、审批任务管理。 |
| `lark-attendance` | 飞书考勤打卡：查询自己的考勤打卡记录 |
| `lark-base` | 当需要用 lark-cli 操作飞书多维表格（Base）时调用：搜索 Base、建表、字段管理、记录读写、记录分享链接、视图配置、历史查询，以及角色/表单/仪表盘管理/工作流；也适用于把旧的 +table / +fiel |
| `lark-calendar` | 飞书日历（calendar）：提供日历与日程（会议）的全面管理能力。核心场景包括：查看/搜索日程、创建/更新日程、管理参会人、查询忙闲状态及推荐空闲时段、查询/搜索与预定会议室。注意：涉及【预约日程/会议】或【查询/预定 |
| `lark-contact` | 飞书 / Lark 通讯录,用于按姓名 / 邮箱把员工解析成 open_id,以及按 open_id 反查员工的姓名 / 部门 / 邮箱 / 联系方式。当用户说出某人姓名而下一步需要发消息 / 加群 / 排日程时,先用本 |
| `lark-doc` | 飞书云文档（v2）：创建和编辑飞书文档。使用本 skill 时，docs +create、docs +fetch、docs +update 必须携带 --api-version v2；默认使用 DocxXML 格式（也支 |
| `lark-drive` | 飞书云空间：管理云空间中的文件和文件夹。上传和下载文件、创建文件夹、复制/移动/删除文件、查看文件元数据、管理文档评论、管理文档权限、订阅用户评论变更事件、修改文件标题（docx、sheet、bitable、file、f |
| `lark-event` | Lark/Feishu real-time event listening / subscribing / consuming: stream events as NDJSON via `lark-cli event c |
| `lark-im` | 飞书即时通讯：收发消息和管理群聊。发送和回复消息、搜索聊天记录、管理群聊成员、上传下载图片和文件（支持大文件分片下载）、管理表情回复。当用户需要发消息、查看或搜索聊天记录、下载聊天中的文件、查看群成员时使用。 |
| `lark-mail` | 飞书邮箱 — draft, compose, send, reply, forward, read, and search emails; manage drafts, folders, labels, contacts |
| `lark-markdown` | 飞书 Markdown：查看、创建、上传和编辑 Markdown 文件。当用户需要创建或编辑 Markdown 文件、读取或修改时使用。 |
| `lark-minutes` | 飞书妙记：妙记相关基本功能。1.查询妙记列表（按关键词/所有者/参与者/时间范围）；2.获取妙记基础信息（标题、封面、时长 等）；3.下载妙记音视频文件；4.获取妙记相关 AI 产物（总结、待办、章节）；5.上传音视频生 |
| `lark-okr` | 飞书 OKR：管理目标与关键结果。查看和编辑 OKR 周期、目标（Objective）、关键结果（Key Result）、对齐关系、量化指标和进展记录。当用户需要查看或创建 OKR、管理目标和关键结果、查看对齐关系时使用 |
| `lark-openapi-explorer` | 飞书/Lark 原生 OpenAPI 探索：从官方文档库中挖掘未经 CLI 封装的原生 OpenAPI 接口。当用户的需求无法被现有 lark-* skill 或 lark-cli 已注册命令满足，需要查找并调用原生飞书 |
| `lark-shared` | 飞书/Lark CLI 共享基础：应用配置初始化、认证登录（auth login）、身份切换（--as user/bot）、权限与 scope 管理、Permission denied 错误处理、安全规则。当用户需要第一 |
| `lark-sheets` | 飞书电子表格：创建和操作电子表格。支持创建表格、创建/复制/删除/更新工作表、读写单元格、追加行数据、查找内容、导出文件。当用户需要创建电子表格、管理工作表、批量读写数据、在已知表格中查找内容、导出或下载表格时使用。若用 |
| `lark-skill-maker` | 创建 lark-cli 的自定义 Skill。当用户需要把飞书 API 操作封装成可复用的 Skill（包装原子 API 或编排多步流程）时使用。 |
| `lark-slides` | 飞书幻灯片：创建和编辑幻灯片，接口通过 XML 协议通信。创建演示文稿、读取幻灯片内容、管理幻灯片页面（创建、删除、读取、局部替换）。当用户需要创建或编辑幻灯片、读取或修改单个页面时使用。 |
| `lark-task` | 飞书任务：管理任务、清单和任务智能体。创建待办任务、查看和更新任务状态、拆分子任务、组织任务清单、分配协作成员、上传任务附件、注册或注销任务智能体、更新任务智能体的主页数据、写入智能体任务记录。当用户需要创建待办事项、查 |
| `lark-vc` | 飞书视频会议：查询会议记录、获取会议纪要产物（总结、待办、章节、逐字稿）。1. 查询已经结束的会议数量或详情时使用本技能(如历史日期｜ 昨天 \| 上周 \| 今天已经开过的会议等场景)，查询未开始的会议日程使用 lar |
| `lark-whiteboard` | 飞书画板：查询和编辑飞书云文档中的画板。支持导出画板为预览图片、导出原始节点结构、使用 DSL（转成 OpenAPI 格式）、PlantUML/Mermaid 格式更新画板内容。 当用户需要查看画板内容、导出画板图片、编 |
| `lark-wiki` | 飞书知识库：管理知识空间、空间成员和文档节点。创建和查询知识空间、查看和管理空间成员、管理节点层级结构、在知识库中组织文档和快捷方式。当用户需要在知识库中查找或创建文档、浏览知识空间结构、查看或管理空间成员、移动或复制节 |
| `lark-workflow-meeting-summary` | 会议纪要整理工作流：汇总指定时间范围内的会议纪要并生成结构化报告。当用户需要整理会议纪要、生成会议周报、回顾一段时间内的会议内容时使用。 |
| `lark-workflow-standup-report` | 日程待办摘要：编排 calendar +agenda 和 task +get-my-tasks，生成指定日期的日程与未完成任务摘要。适用于了解今天/明天/本周的安排。 |

## 视频 / Remotion / Hyperframes

| 技能 | 说明 |
| --- | --- |
| `ffmpeg-video-editor` | Generate FFmpeg commands from natural language video editing requests - cut, trim, convert, compress, change a |
| `hyperframes` | Read first to make, edit, animate or render any video with HyperFrames (HTML rendered to video), including lau |
| `hyperframes-cli` | The HyperFrames CLI by job - scaffold, check, look at frames, edit the timeline, preview, render locally or in |
| `remotion-best-practices` | Router for all Remotion skills |
| `remotion-captions` | Transcribing, displaying and animating captions |
| `remotion-create` | Create a new Remotion video |
| `remotion-interactivity` | Structure Remotion markup for interactivity |
| `remotion-markup` | Content, animation and effects best practices |
| `remotion-multimedia` | Interacting with Mediabunny |
| `remotion-render` | Export a Remotion video |
| `remotion-studio` | Preview a Remotion video |
| `remotion-to-hyperframes` | Bring existing video code or footage into HyperFrames and verify it frame by frame against the original - Remo |
| `video-frames` | Extract frames or short clips from videos using ffmpeg. |

## 其他

| 技能 | 说明 |
| --- | --- |
| `1password` | Set up and use 1Password CLI (op). Use when installing the CLI, enabling desktop app integration, signing in ( |
| `a-stock-analysis` | A股实时行情与分时量能分析。获取沪深股票实时价格、涨跌、成交量，分析分时量能分布（早盘/尾盘放量）、主力动向（抢筹/出货信号）、涨停封单。支持持仓管理和盈亏分析。Use when: (1) 查询A股实时行情, (2) 分 |
| `agent-self-reflection` | Periodic self-reflection on recent sessions. Analyzes what went well, what went wrong, and writes concise, act |
| `aminer-open-academic` | 使用 AMiner 开放平台 API 进行学术数据查询与分析。当用户需要查询学者信息、论文详情、机构数据、期刊内容或专利信息时使用此 skill。 触发场景：提到 AMiner、学术数据查询、查论文/学者/机构/期刊/专 |
| `architecture-designer` | Use when designing new system architecture, reviewing existing designs, or making architectural decisions. Inv |
| `autoglm-deepresearch` | 对用户提出的课题进行深度研究和调研，输出结构化的深度报告。当用户需要深入了解某个话题、做行业调研、专题研究、竞品分析等场景时使用此 skill。 与普通搜索不同，deepresearch 会先做少量定向搜索，再对少量关键 |
| `autoglm-generate-image` | 使用 AutoGLM 文生图接口，根据用户输入的文字描述生成图片。当用户需要生成图片、文字转图片、AI绘图等场景时使用此 skill。 Token 通过本地服务 http://127.0.0.1:53699/get_to |
| `autoglm-open-link` | 使用 AutoGLM Open Link 接口打开指定网页并提取页面正文内容。当用户需要读取某个网页详情、提取文章全文、抓取页面正文做摘要或分析时使用此 skill。 Token 通过本地服务 http://127.0. |
| `autoglm-search-image` | 使用 AutoGLM 搜图接口，根据用户输入的关键词搜索相关图片。当用户需要搜索图片、查找图片素材等场景时使用此 skill。 Token 通过本地服务 http://127.0.0.1:53699/get_token  |
| `automation-workflows` | Design and implement automation workflows to save time and scale operations as a solopreneur. Use when identif |
| `backtest-expert` | Expert guidance for systematic backtesting of trading strategies. Use when developing, testing, stress-testing |
| `blog-writer` | This skill should be used when writing blog posts, articles, or long-form content in the writer's distinctive  |
| `brainstorming` | You MUST use this before any creative work - creating features, building components, adding functionality, or  |
| `clawdefender` | Security scanner and input sanitizer for AI agents. Detects prompt injection, command injection, SSRF, credent |
| `code` | Coding workflow with planning, implementation, verification, and testing for clean software development. |
| `content-strategy` | Build and execute a content marketing strategy for a solopreneur business. Use when planning what content to c |
| `copywriting` | Write persuasive copy for landing pages, emails, ads, sales pages, and marketing materials. Use when you need  |
| `debug-pro` |  |
| `dingtalk-message` | 钉钉消息发送。当用户提到"钉钉消息"、"发消息"、"发通知"、"群通知"、"群消息"、"Webhook"、"机器人消息"、"机器人发消息"、"工作通知"、"单聊消息"、"群聊消息"、"撤回消息"、"消息已读"、"发送Ma |
| `executing-plans` | Use when you have a written implementation plan to execute in a separate session with review checkpoints |
| `facebook-ads` | Facebook Ads integration. Manage Campaigns, Audiences, Pixels. Use when the user wants to interact with Facebo |
| `find-skills` | Helps users discover and install agent skills when they ask questions like "how do I do X", "find a skill for  |
| `frontend-design` | Create distinctive, production-grade frontend interfaces with high design quality. Use this skill when buildin |
| `git-essentials` | Essential Git commands and workflows for version control, branching, and collaboration. |
| `interview-designer` | Analyze resumes and design interview strategies using evidence-based methodology. Transforms interview prep fr |
| `market-research` | Size markets, analyze competitors, and validate opportunities with practical frameworks and free data sources. |
| `memory` | Infinite organized memory that complements your agent's built-in memory with unlimited categorized storage. |
| `obsidian-ontology-sync` | Bidirectional sync between Obsidian PKM (human-friendly notes) and structured ontology (machine-queryable grap |
| `opencode-controller` | Control and operate Opencode via slash commands. Use this skill to manage sessions, select models, switch agen |
| `research-paper-writer` | Creates formal academic research papers following IEEE/ACM formatting standards with proper structure, citatio |
| `security-auditor` | Use when reviewing code for security vulnerabilities, implementing authentication flows, auditing OWASP Top 10 |
| `self-improving` | Self-reflection + Self-criticism + learning from corrections. Agent evaluates its own work, catches mistakes,  |
| `seo` | SEO specialist agent with site audits, content writing, keyword research, technical fixes, link building, and  |
| `seo-content-writer` | Use when the user asks to "write SEO content", "create a blog post", "write an article", "content writing", "d |
| `session-logs` | Search and analyze your own session logs (older/parent conversations) using jq. |
| `skill-creator` | Guide for creating effective skills. This skill should be used when users want to create a new skill (or updat |
| `skill-vetter` | Security-first skill vetting for AI agents. Use before installing any skill from ClawdHub, GitHub, or other so |
| `social-content-generator` | When the user wants help creating, scheduling, or optimizing social media content for LinkedIn, Twitter/X, Ins |
| `social-media-scheduler` | Plan, draft, and organize social media content across platforms. Create content calendars, write platform-opti |
| `supabase-postgres-best-practices` | Postgres performance optimization and best practices from Supabase. Use this skill when writing, reviewing, or |
| `test-runner` |  |
| `tmux` | Remote-control tmux sessions for interactive CLIs by sending keystrokes and scraping pane output. |
| `ui-ux-pro-max` | UI/UX design intelligence and implementation guidance for building polished interfaces. Use when the user asks |
| `writing-plans` | Use when you have a spec or requirements for a multi-step task, before touching code |
