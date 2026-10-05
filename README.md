# Codex Skills Library

这个仓库用于集中管理、版本化和共享个人/团队 Codex skills。适合多设备同步，也适合同事之间复用成熟工作流。

仓库地址：

```text
https://github.com/ElevenZhou/codex-skills-library
```

## 适合怎么用

- **个人多设备同步**：一台机器沉淀技能，其他设备 clone 后一键安装。
- **团队共享能力**：把稳定的工作流、工具说明、QA 标准沉淀成 skill，同事按需安装。
- **版本管理**：每次升级技能都有 Git 记录，可以回退、对比、协作。
- **标准化交付**：让 PPT、调研、开发、自动化等重复工作有统一执行规范。

建议保持仓库为 **Private**，避免误传内部方法、客户资料或敏感提示词。

## 快速安装

克隆仓库：

```bash
git clone https://github.com/ElevenZhou/codex-skills-library.git
cd codex-skills-library
```

安装全部技能：

```bash
./scripts/install-skills.sh
```

只安装指定技能：

```bash
./scripts/install-skills.sh auto-loop deck-studio-loop
```

默认安装到：

```text
${CODEX_HOME:-$HOME/.codex}/skills
```

安装后重新打开 Codex / 新开线程，让技能列表刷新。

## 版本对齐

每个技能的 `SKILL.md` 标题下都有 `Skill version` 标记，README 的技能目录也同步记录同一版本号。不同设备安装或同步后，可以直接对比这两个位置确认技能版本是否一致。

当前技能库基线版本：`2026.10.05`

## 技能目录

共 39 个技能，按用途分 9 类。★ 表示该类首选；同类技能有重叠时，表下的「怎么选」说明分工。

### 1. 自动驾驶与项目管理

| 技能 | 版本 | 适合场景 | 推荐触发词 / 用法 |
| --- | --- | --- | --- |
| ★ `auto-loop`（老大） | `2026.10.05` | 自动驾驶舱 / 总调度，按内置技能表调用其他技能（见 `references/skill-registry.md`）。复杂目标的全自动规划、执行、验证、优化，覆盖 PPT、PDF/文档、调研、网站/App、代码工程、量化交易等。**全员推荐。** | `老大`、`大哥`、`Use $auto-loop 自动驾驶舱模式...`、`全自动`、`强制执行`、`循环优化` |
| `project-inception-analysis-cockpit`（小二） | `2026.10.05` | 立项分析驾驶舱：动态裁剪市场、竞品、开源、用户、技术、财务等研究模块，十角色评审加权评分，给出立项/有条件立项/先验证/暂缓/否决结论和四阶段推行计划。 | `小二`、`老二`、`二哥`、`Use $project-inception-analysis-cockpit 分析这个项目值不值得做...` |
| `project-employee-agents`（小三） | `2026.10.05` | 虚拟项目团队：自动调度 CEO、COO、产品、市场、设计、技术、测试、客户、投放、财务等 15 个岗位，按 12 个生命周期阶段产出可验收管理成果。 | `小三`、`老三`、`三哥`、`三神`、`启动项目员工团队...`、`项目员工开工...`、`继续推进项目...` |
| `project-ops-standards` | `2026.07.24` | 创建、审计或改进软件项目的项目管理与运营文档。 | `Use $project-ops-standards 检查项目文档...` |

怎么选：老大总调度；**该不该做**找老二（一次性立项报告）；**决定做了之后持续推进**找老三（立项前需要深度分析时，老三会转交老二）；只需要补齐项目文档用 `project-ops-standards`；不属于以上的复杂交付用 `auto-loop`。

### 2. Agent 与工具开发

| 技能 | 版本 | 适合场景 | 推荐触发词 / 用法 |
| --- | --- | --- | --- |
| `production-agent-architecture` | `2026.07.25` | 设计生产级 AI agent 架构，覆盖 loop、工具、上下文、记忆、权限、观测、评估和发布。 | `Use $production-agent-architecture 设计一个 agent...` |
| `agent-scaffolder` | `2026.07.25` | 从 Agent Build Spec 生成可运行 Python agent 项目，包含 controller loop、工具桩、状态、权限和观测。 | `Use $agent-scaffolder 基于这份 spec 生成 agent 项目...` |
| ★ `cli-creator` | `2026.07.25` | 从 API 文档、OpenAPI、curl、SDK、本地脚本创建可复用 CLI，并配套 skill。 | `Use $cli-creator 基于这个 API 创建 CLI...` |

怎么选：先用 `production-agent-architecture` 出设计，再用 `agent-scaffolder` 生成代码。

### 3. 前端设计与浏览器

| 技能 | 版本 | 适合场景 | 推荐触发词 / 用法 |
| --- | --- | --- | --- |
| ★ `advanced-frontend-design` | `2026.07.24` | 生产级前端设计与实现，落地高辨识度界面、复杂状态和浏览器验证。 | `Use $advanced-frontend-design 做一个前端页面...` |
| `frontend-design-lab` | `2026.07.24` | 多方案设计实验室：固定产品约束下产出并对比多个视觉方向，再选定精修。 | `Use $frontend-design-lab 做几个前端风格方案...` |
| `taste-skill` | `2026.07.25` | 面向 landing page、作品集和 redesign 的反模板化审美工作流，触发名为 `design-taste-frontend`。 | `Use $design-taste-frontend 重设计这个页面...` |
| ★ `playwright` | `2026.07.25` | 命令行驱动真实浏览器：网页操作、截图、表单、UI 流程验证。 | `Use $playwright 自动测试这个页面...` |
| `playwright-interactive` | `2026.07.25` | 持久浏览器/Electron 调试，适合连续 UI QA 和本地 Web/App 调试。 | `Use $playwright-interactive 调试这个本地应用...` |
| `screenshot` | `2026.07.25` | 桌面/系统截图，适合浏览器工具拿不到的窗口、全屏、区域截图。 | `Use $screenshot 截取这个窗口...` |

怎么选：方向已定直接做用 `advanced-frontend-design`；方向未定先比稿用 `frontend-design-lab`；落地页/作品集追求审美差异化用 `design-taste-frontend`。

### 4. 部署

| 技能 | 版本 | 适合场景 | 推荐触发词 / 用法 |
| --- | --- | --- | --- |
| `cloudflare-deploy` | `2026.07.24` | 部署应用和基础设施到 Cloudflare Workers、Pages 等平台。 | `Use $cloudflare-deploy 部署...` |
| `vercel-deploy` | `2026.07.24` | 部署应用和网站到 Vercel。 | `Use $vercel-deploy 部署...` |

### 5. 文档、材料与商务

| 技能 | 版本 | 适合场景 | 推荐触发词 / 用法 |
| --- | --- | --- | --- |
| ★ `deck-studio-loop` | `2026.07.25` | 高质量 PPT、商业计划书、公司/产品介绍、路演材料，强调叙事、视觉差异化、渲染 QA、多角色评审。 | `Use $deck-studio-loop 做一套产品介绍 PPT...` |
| `doc` | `2026.07.24` | 读取、创建、编辑 `.docx`，适合需要格式和版式控制的交付物。 | `Use $doc 编辑这个 Word...` |
| `pdf` | `2026.07.24` | 读取、创建、审阅 PDF，适合需要渲染和版式检查的任务。 | `Use $pdf 看这个 PDF...` |
| `rich-html-docs` | `2026.07.24` | 精美、可分享的单文件 HTML 文档，替代普通 Markdown 说明。 | `Use $rich-html-docs 做一份 HTML 文档...` |
| `xiaowu-contract-review`（小五） | `2026.09.29` | 合同审阅与修订（Agent 身份"小五"）：业务+法务双视角，七步流程（读审报批改查验），P0/P1/P2 问题对照表 + 对外话术，未经许可不改正文。 | `Use $xiaowu-contract-review 审查这份合同...`、`小五看合同` |
| `domain-brand-finder` | `2026.07.24` | 项目命名、品牌域名策略和域名可用性。 | `Use $domain-brand-finder 给项目起名...` |
| `post-wechat-moments` | `2026.07.24` | 可直接发布的微信朋友圈图文内容。 | `Use $post-wechat-moments 发朋友圈...` |

### 6. 广告投放

| 技能 | 版本 | 适合场景 | 推荐触发词 / 用法 |
| --- | --- | --- | --- |
| `overseas-ad-autopilot` | `2026.07.24` | 海外广告自动驾驶舱工作区：梳理投放目标、输入、角色分工、QA 和交付检查。 | `Use $overseas-ad-autopilot 规划海外广告自动化...` |
| ★ `meta-ads-analysis` | `2026.07.25` | **只读**分析 Meta/Facebook Ads 账户、campaign、ad set、ad、素材、Pixel 漏斗和异常。 | `Use $meta-ads-analysis 分析 Meta 广告表现...` |
| `meta-ads-control` | `2026.07.25` | 用 meta-ads CLI 检查、导出报表，并在明确授权下暂停或启用投放。 | `Use $meta-ads-control 检查 Meta 广告账户...` |
| `meta-ads-auto-publish` | `2026.07.25` | 通过已有 Chrome 会话发布准备好的 Meta Ads 草稿，并验证提交状态。 | `Use $meta-ads-auto-publish 发布这些广告草稿...` |

怎么选：规划用 `overseas-ad-autopilot`；看数据用 `meta-ads-analysis`（只读，最安全）；要启停投放才用 `meta-ads-control`；发布新广告用 `meta-ads-auto-publish`。

### 7. 图片与视频生成

| 技能 | 版本 | 适合场景 | 推荐触发词 / 用法 |
| --- | --- | --- | --- |
| ★ `local-image-generator` | `2026.10.05` | 唯一的静态出图技能（已合并原 `image-gen` 和 `local-image-generator-1-0`）：调用本地图片工具，模型和渠道由工具 `.env.local` 统一配置，主力为 GPT Image 2.5（`gpt-image-2.5-flare` 日常 / `gpt-image-2.5-sunburst` 精细）。适合网页素材、插画、产品图、社交配图。 | `Use $local-image-generator 生成一张图...`、`作图`、`画图` |
| `local-grok-video-generator-2-0` | `2026.07.24` | 通过本地 FlaioS Grok video API 生成 Grok Imagine 视频。 | `Use $local-grok-video-generator-2-0 生成视频...` |
| `video-channel-onboarding` | `2026.07.25` | 新视频生成渠道接入：资料归档、适配、部署、冒烟测试、文档和交接。 | `Use $video-channel-onboarding 接入这个视频渠道...` |

### 8. 个人工作台、知识与邮件

| 技能 | 版本 | 适合场景 | 推荐触发词 / 用法 |
| --- | --- | --- | --- |
| `personal-workbench` | `2026.07.24` | 更新、审查、总结或补充个人 workbench 状态。 | `Use $personal-workbench 更新工作台...` |
| `submit-results-to-workbench` | `2026.07.24` | 将已完成项目成果提交到个人 workbench / FlaiOS 枢纽仓库。 | `Use $submit-results-to-workbench 提交成果...` |
| `flaios-content-submit` | `2026.07.24` | 将网站、工具、项目、Agent、Skill、workflow 或个人记忆提交到 FlaiOS。 | `Use $flaios-content-submit 提交...` |
| `obsidian-memory` | `2026.07.25` | 从对话、日志、项目笔记中提取并维护 Obsidian 长期记忆、项目知识和决策记录。 | `Use $obsidian-memory 整理这段对话到 Obsidian...` |
| `gmail-mail` | `2026.07.24` | 通过 Gmail API 搜索、阅读、草稿、发送、回复、转发邮件。 | `Use $gmail-mail 查一下邮件...` |
| `claude-daily-training` | `2026.07.24` | 通过 Codex 和 Chrome 执行 Claude.ai 每日创作训练。 | `Use $claude-daily-training...`、`Claude 每日训练` |

### 9. 服务器与配置运维

| 技能 | 版本 | 适合场景 | 推荐触发词 / 用法 |
| --- | --- | --- | --- |
| `seoul-node-onboarding` | `2026.07.24` | 配置新上线的 FRP sub2api 国家节点到 Seoul 服务器。 | `Use $seoul-node-onboarding 配置节点...` |
| `seoul-server-status-check` | `2026.07.24` | 只读检查 Seoul 服务器健康状态并发送飞书通知。 | `Use $seoul-server-status-check 检查首尔服务器...` |
| `ccswitch-config-transfer` | `2026.07.25` | 备份并迁移 CCSwitch / CC-Switch 用户配置，尤其适合同步到 Salt 管理的 CRS 节点。 | `Use $ccswitch-config-transfer 同步 ccswitch 配置到 TS08...` |
| `t0-work-session` | `2026.07.24` | T0-SemiAuto 工作会话交接和 Git 同步。 | `Use $t0-work-session 结束工作...` |

## 别名与总调度

常用技能可以直接用中文别名点名，说别名和说技能名效果一样：

| 别名 | 技能 | 角色 |
| --- | --- | --- |
| 老大、大哥、老大哥、大当家、头儿 | `auto-loop` | 总调度：拆目标、按技能表调用其他技能、QA、交付 |
| 小二、老二、二哥、二当家 | `project-inception-analysis-cockpit` | 立项调研：回答"这个项目该不该做" |
| 小三、老三、三哥、三神、三当家 | `project-employee-agents` | 项目团队：立项后的计划、执行、上线、运营 |
| 小五 | `xiaowu-contract-review` | 合同审阅与修订 |

老大调度时会查 `skills/auto-loop/references/skill-registry.md`（技能表）：里面列出了它能调用的技能、别名、调用方式和常见组合。被调用技能自己的门禁（例如小五"未经许可不改合同"、广告技能"启停投放需授权"）优先于老大的"免打扰"原则。

**新增或下线技能时**，要同步更新技能表和本 README；别名必须同时写进该技能 `SKILL.md` 的 `description`，否则在老大之外说别名不会触发。

## 在 Claude Code 中安装

Claude Code 从 `~/.claude/skills/<技能名>/` 读取技能，不需要 `agents/openai.yaml`（Codex 专用）：

```bash
for s in auto-loop project-inception-analysis-cockpit project-employee-agents; do
  rm -rf ~/.claude/skills/$s && mkdir -p ~/.claude/skills/$s
  cp -r skills/$s/* ~/.claude/skills/$s/ && rm -rf ~/.claude/skills/$s/agents
done
```

安装后新开会话，技能列表会刷新。

给本机 Codex、WorkBuddy、Trae CN、OpenCode 统一安装（含各自技能目录；OpenCode 直接共用 `~/.claude/skills`）：把 [`docs/install-prompt.md`](docs/install-prompt.md) 里的提示词整段发给对方即可。

## 推荐组合

### 自动驾驶舱基础组合

适合所有人：

```bash
./scripts/install-skills.sh auto-loop
```

### 项目立项与推进组合

适合新项目评估、立项后持续推进和合同审阅：

```bash
./scripts/install-skills.sh auto-loop project-inception-analysis-cockpit project-employee-agents project-ops-standards xiaowu-contract-review
```

### 商业材料 / PPT 组合

适合做公司介绍、BP、路演、汇报材料：

```bash
./scripts/install-skills.sh auto-loop deck-studio-loop screenshot
```

### 文档 / 内容组合

适合 Word、PDF、HTML 文档、朋友圈内容、项目资料沉淀：

```bash
./scripts/install-skills.sh auto-loop doc pdf rich-html-docs post-wechat-moments project-ops-standards
```

### Web / App 开发组合

适合网页、管理后台、产品 Demo、UI QA：

```bash
./scripts/install-skills.sh auto-loop playwright playwright-interactive screenshot
```

### 工具与自动化组合

适合把内部 API、脚本、后台能力封装成 CLI：

```bash
./scripts/install-skills.sh auto-loop cli-creator playwright
```

### 部署组合

适合 Cloudflare / Vercel 发布和上线检查：

```bash
./scripts/install-skills.sh auto-loop cloudflare-deploy vercel-deploy playwright screenshot
```

### 本地生成 / FlaiOS 组合

适合本地图像、视频生成，以及结果提交到个人工作台：

```bash
./scripts/install-skills.sh auto-loop local-image-generator local-grok-video-generator-2-0 flaios-content-submit submit-results-to-workbench personal-workbench
```

### Seoul / T0 运维组合

适合 Seoul 节点、服务器状态检查和 T0 工作会话交接：

```bash
./scripts/install-skills.sh auto-loop seoul-node-onboarding seoul-server-status-check t0-work-session
```

## 查看可用技能

```bash
./scripts/list-skills.sh
```

## 本机技能回写到仓库

当你在本机新增或修改 `$CODEX_HOME/skills`（默认 `~/.codex/skills`）后：

```bash
cd codex-skills-library
./scripts/pull-from-local-codex.sh              # 回写仓库里已有的技能
./scripts/pull-from-local-codex.sh new-skill    # 新技能需要显式点名
./scripts/check-no-secrets.sh
git status
```

两个同步脚本都按单个技能同步：安装不会删除本机独有的技能，回写不会删除仓库独有的技能，也不会把未点名的本地私有技能带进仓库。

```bash
git add .
git commit -m "Update Codex skills"
git push
```

## 更新其他设备

```bash
cd codex-skills-library
git pull
./scripts/install-skills.sh
```

## 新增技能规范

一个可共享 skill 建议至少包含：

```text
skill-name/
├── SKILL.md
├── agents/openai.yaml
├── references/       # 复杂流程、标准、检查清单
└── scripts/          # 可复用脚本，可选
```

要求：

- `SKILL.md` 必须有清晰的 `name` 和 `description`。
- `description` 要写明什么时候触发，不要只写功能名。
- 复杂技能不要只写单文件，尽量拆出 `references/` 和必要脚本。
- 涉及交付质量的技能要有 QA / loop / 自审机制。
- 不要提交 API key、客户资料、`.env`、本地运行日志、缓存目录。

## 安全检查

提交前运行：

```bash
./scripts/check-no-secrets.sh
```

这个脚本只能做明显密钥扫描，不能替代人工检查。提交前仍建议看一遍：

```bash
git diff --cached
```

## 仓库不包含什么

- 不包含 `~/.codex/skills/.system` 系统技能。
- 不包含插件缓存、运行时缓存、API key、客户资料。
- 不包含每台机器自己的 Codex 配置文件。
