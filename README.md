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

## 技能目录

| 技能 | 适合场景 | 推荐触发词 / 用法 | 建议 |
| --- | --- | --- | --- |
| `auto-loop` | 自动驾驶舱。适合复杂目标的全自动规划、执行、验证、优化。覆盖 PPT、PDF/文档、调研、网站/App、代码工程、量化交易等。 | `Use $auto-loop 自动驾驶舱模式...`、`全自动`、`强制执行`、`循环优化` | **全员推荐** |
| `deck-studio-loop` | 高质量 PPT、商业计划书、公司介绍、产品介绍、路演材料。强调叙事、视觉差异化、渲染 QA、多角色评审。 | `Use $deck-studio-loop 做一套产品介绍 PPT...` | 做材料的人推荐 |
| `cli-creator` | 从 API 文档、OpenAPI、curl、SDK、本地脚本创建可复用 CLI，并配套 skill。 | `Use $cli-creator 基于这个 API 创建 CLI...` | 开发/自动化推荐 |
| `playwright` | 用命令行驱动真实浏览器，做网页操作、截图、表单、UI 流程验证。 | `Use $playwright 自动测试这个页面...` | 前端/网页任务推荐 |
| `playwright-interactive` | 持久浏览器/Electron 调试，适合连续 UI QA 和本地 Web/App 调试。 | `Use $playwright-interactive 调试这个本地应用...` | 前端高级用户 |
| `screenshot` | 桌面/系统截图，适合浏览器工具拿不到的窗口、全屏、区域截图。 | `Use $screenshot 截取这个窗口...` | 按需安装 |

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

## 查看可用技能

```bash
./scripts/list-skills.sh
```

## 本机技能回写到仓库

当你在本机新增或修改 `~/.codex/skills` 后：

```bash
cd /Users/shenji/Projects/codex-skills-library
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

