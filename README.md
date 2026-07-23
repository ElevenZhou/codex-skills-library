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

当前技能库基线版本：`2026.07.24`

## 技能目录

| 技能 | 版本 | 适合场景 | 推荐触发词 / 用法 | 建议 |
| --- | --- | --- | --- | --- |
| `advanced-frontend-design` | `2026.07.24` | 生产级前端设计与实现工作流，适合落地高辨识度界面、复杂状态和浏览器验证。 | `Use $advanced-frontend-design 做一个前端页面...` | 前端/设计推荐 |
| `agent-scaffolder` | `2026.07.24` | 从 Agent Build Spec 生成可运行 Python agent 项目，包含 controller loop、工具桩、状态、权限和观测。 | `Use $agent-scaffolder 基于这份 spec 生成 agent 项目...` | Agent 开发 |
| `auto-loop` | `2026.07.24` | 自动驾驶舱。适合复杂目标的全自动规划、执行、验证、优化。覆盖 PPT、PDF/文档、调研、网站/App、代码工程、量化交易等。 | `Use $auto-loop 自动驾驶舱模式...`、`全自动`、`强制执行`、`循环优化` | **全员推荐** |
| `ccswitch-config-transfer` | `2026.07.24` | 备份并迁移 CCSwitch / CC-Switch 用户配置，尤其适合同步到 Salt 管理的 CRS 节点。 | `Use $ccswitch-config-transfer 同步 ccswitch 配置到 TS08...` | 配置迁移 |
| `claude-daily-training` | `2026.07.24` | 通过 Codex 和 Chrome 执行 Claude.ai 每日创作训练。 | `Use $claude-daily-training...`、`Claude 每日训练` | 创作训练 |
| `cli-creator` | `2026.07.24` | 从 API 文档、OpenAPI、curl、SDK、本地脚本创建可复用 CLI，并配套 skill。 | `Use $cli-creator 基于这个 API 创建 CLI...` | 开发/自动化推荐 |
| `cloudflare-deploy` | `2026.07.24` | 部署应用和基础设施到 Cloudflare Workers、Pages 等平台。 | `Use $cloudflare-deploy 部署...` | 部署推荐 |
| `deck-studio-loop` | `2026.07.24` | 高质量 PPT、商业计划书、公司介绍、产品介绍、路演材料。强调叙事、视觉差异化、渲染 QA、多角色评审。 | `Use $deck-studio-loop 做一套产品介绍 PPT...` | 做材料的人推荐 |
| `doc` | `2026.07.24` | 读取、创建、编辑 `.docx` 文档，尤其适合需要格式和版式控制的交付物。 | `Use $doc 编辑这个 Word...` | 文档推荐 |
| `domain-brand-finder` | `2026.07.24` | 项目命名、品牌域名策略和域名可用性工作流。 | `Use $domain-brand-finder 给项目起名...` | 品牌/命名 |
| `flaios-content-submit` | `2026.07.24` | 将网站、工具、项目、Agent、Skill、workflow 或个人记忆提交到 FlaiOS。 | `Use $flaios-content-submit 提交...` | FlaiOS 内容入库 |
| `frontend-design-lab` | `2026.07.24` | 多方案前端设计实验室，在固定产品约束下产出并对比不同视觉方向，再选定方向继续精修。 | `Use $frontend-design-lab 做几个前端风格方案...` | 前端/设计实验 |
| `gmail-mail` | `2026.07.24` | 通过 Gmail API 管理邮件：搜索、阅读、草稿、发送、回复、转发。 | `Use $gmail-mail 查一下邮件...` | 邮件工作流 |
| `image-gen` | `2026.07.24` | 通过 FlaioS 图片 API 和用户自己的 key 生成静态图片，支持 Grok Imagine 和 gpt-image-2。 | `Use $image-gen 生成一张图...`、`作图`、`画图` | 图片生成 |
| `local-grok-video-generator-2-0` | `2026.07.24` | 通过本地 FlaioS Grok video API 生成 Grok Imagine 视频。 | `Use $local-grok-video-generator-2-0 生成视频...` | 视频生成 |
| `local-image-generator` | `2026.07.24` | 本地静态图像生成器的旧别名。 | `Use $local-image-generator 生成图片...` | 兼容旧流程 |
| `local-image-generator-1-0` | `2026.07.24` | 使用本地图片生成工具创建静态图片，支持网页素材、插画等。 | `Use $local-image-generator-1-0 生成图片...` | 图片生成 |
| `meta-ads-analysis` | `2026.07.24` | 只读分析 Meta/Facebook Ads 账户、campaign、ad set、ad、素材、Pixel 漏斗和异常。 | `Use $meta-ads-analysis 分析 Meta 广告表现...` | 广告分析 |
| `meta-ads-auto-publish` | `2026.07.24` | 通过用户已有 Chrome 会话发布已经准备好的 Meta/Facebook Ads 草稿，并验证提交状态。 | `Use $meta-ads-auto-publish 发布这些广告草稿...` | 广告发布 |
| `meta-ads-control` | `2026.07.24` | 使用 meta-ads CLI 检查、分析、导出报表，并在明确授权下安全暂停或启用投放。 | `Use $meta-ads-control 检查 Meta 广告账户...` | 广告控制 |
| `obsidian-memory` | `2026.07.24` | 从对话、日志、项目笔记中提取并维护 Obsidian 长期记忆、项目知识和决策记录。 | `Use $obsidian-memory 整理这段对话到 Obsidian...` | 知识沉淀 |
| `overseas-ad-autopilot` | `2026.07.24` | 海外广告自动驾驶舱工作区，用于梳理投放目标、输入、角色分工、QA 和交付检查。 | `Use $overseas-ad-autopilot 规划海外广告自动化...` | 广告/增长 |
| `pdf` | `2026.07.24` | 读取、创建、审阅 PDF，尤其适合需要渲染和版式检查的任务。 | `Use $pdf 看这个 PDF...` | PDF 推荐 |
| `personal-workbench` | `2026.07.24` | 更新、审查、总结或补充个人 workbench 状态。 | `Use $personal-workbench 更新工作台...` | 个人资产管理 |
| `playwright` | `2026.07.24` | 用命令行驱动真实浏览器，做网页操作、截图、表单、UI 流程验证。 | `Use $playwright 自动测试这个页面...` | 前端/网页任务推荐 |
| `playwright-interactive` | `2026.07.24` | 持久浏览器/Electron 调试，适合连续 UI QA 和本地 Web/App 调试。 | `Use $playwright-interactive 调试这个本地应用...` | 前端高级用户 |
| `post-wechat-moments` | `2026.07.24` | 创建可直接发布的微信朋友圈图文内容。 | `Use $post-wechat-moments 发朋友圈...` | 社交内容 |
| `production-agent-architecture` | `2026.07.24` | 设计生产级 AI agent 架构，覆盖 loop、工具、上下文、记忆、权限、观测、评估和发布。 | `Use $production-agent-architecture 设计一个 agent...` | Agent 架构 |
| `project-ops-standards` | `2026.07.24` | 创建、审计或改进软件项目的项目管理与运营文档。 | `Use $project-ops-standards 检查项目文档...` | 项目运营 |
| `rich-html-docs` | `2026.07.24` | 创建精美、可分享的单文件 HTML 文档，替代普通 Markdown 说明。 | `Use $rich-html-docs 做一份 HTML 文档...` | 高级文档 |
| `screenshot` | `2026.07.24` | 桌面/系统截图，适合浏览器工具拿不到的窗口、全屏、区域截图。 | `Use $screenshot 截取这个窗口...` | 按需安装 |
| `seoul-node-onboarding` | `2026.07.24` | 配置新上线的 FRP sub2api 国家节点到 Seoul 服务器。 | `Use $seoul-node-onboarding 配置节点...` | Seoul 节点运维 |
| `seoul-server-status-check` | `2026.07.24` | 只读检查 Seoul 服务器健康状态并发送飞书通知。 | `Use $seoul-server-status-check 检查首尔服务器...` | Seoul 运维 |
| `submit-results-to-workbench` | `2026.07.24` | 将已完成项目成果提交到个人 workbench / FlaiOS 枢纽仓库。 | `Use $submit-results-to-workbench 提交成果...` | 成果归档 |
| `t0-work-session` | `2026.07.24` | T0-SemiAuto 工作会话交接和 Git 同步工作流。 | `Use $t0-work-session 结束工作...` | T0 项目 |
| `taste-skill` | `2026.07.24` | 面向 landing page、作品集和 redesign 的反模板化前端审美工作流，触发名为 `design-taste-frontend`。 | `Use $design-taste-frontend 重设计这个页面...` | 前端/设计推荐 |
| `vercel-deploy` | `2026.07.24` | 部署应用和网站到 Vercel。 | `Use $vercel-deploy 部署...` | 部署推荐 |
| `video-channel-onboarding` | `2026.07.24` | 新视频生成渠道接入工作流，覆盖资料归档、适配、部署、冒烟测试、文档和交接。 | `Use $video-channel-onboarding 接入这个视频渠道...` | 视频平台接入 |

## 推荐组合

### 自动驾驶舱基础组合

适合所有人：

```bash
./scripts/install-skills.sh auto-loop
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
./scripts/install-skills.sh auto-loop local-image-generator-1-0 local-grok-video-generator-2-0 flaios-content-submit submit-results-to-workbench personal-workbench
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

当你在本机新增或修改 `~/.codex/skills` 后：

```bash
cd codex-skills-library
./scripts/pull-from-local-codex.sh
./scripts/check-no-secrets.sh
git status
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
