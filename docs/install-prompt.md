# 本机 AI 技能安装提示词（Codex / WorkBuddy / Trae CN / OpenCode）

本机这几个 AI 都使用"每个技能一个目录 + `SKILL.md`"的格式，只是技能目录不同。把对应那段整段发给它即可。

| AI | 技能目录 |
| --- | --- |
| Codex | `E:\AI_Dev\Codex\home\skills`（即 `$CODEX_HOME\skills`） |
| WorkBuddy | `C:\Users\AprilWu\.workbuddy\skills` |
| Trae CN | `C:\Users\AprilWu\.trae-cn\skills` |
| Claude Code（已装好，供对照） | `C:\Users\AprilWu\.claude\skills` |
| OpenCode | 不单独安装，自动读取 `C:\Users\AprilWu\.claude\skills` |

技能源：`Y:\Skills\codex-skills-library\skills`（NAS 不可用时改用 `\\192.168.31.121\projects\Skills\codex-skills-library\skills`）。

---

## 通用提示词（把 <目标目录> 换成上表对应路径）

```text
请从我的技能库安装技能，按下面执行，做完再汇报，中途不要问我。

源目录：Y:\Skills\codex-skills-library\skills
目标目录：<目标目录>

1. 先在源仓库执行 git -C Y:\Skills\codex-skills-library pull，拿到最新版。
2. 安装这 5 个技能（整个目录复制，保持 SKILL.md、references\、scripts\、agents\ 结构不变）：
   - auto-loop（别名：老大、大哥、老大哥、大当家、头儿）
   - project-inception-analysis-cockpit（别名：小二、老二、二哥、二当家）
   - project-employee-agents（别名：小三、老三、三哥、三神、三当家）
   - xiaowu-contract-review（别名：小五）
   - local-image-generator（唯一出图技能）
3. 目标目录里已有同名技能时，先改名为 <技能名>-backup-20261005 备份，再复制新版本。
4. 目标目录里如果有 image-gen 或 local-image-generator-1-0，它们已被合并下线，同样改名备份，不要删除。
5. 不修改技能内容；不读取、不打印、不复制任何 API key 或 .env 文件。
6. 安装后验收并回报：
   a. 列出 5 个技能的安装路径和 SKILL.md 里的 Skill version，应为：auto-loop 2026.10.05、project-inception-analysis-cockpit 2026.10.05、project-employee-agents 2026.10.05、xiaowu-contract-review 2026.09.29、local-image-generator 2026.10.05。
   b. 别名路由自测（只回答会调用哪个技能，不要真正执行）：
      “老大，帮我做个产品介绍 PPT” / “小二，看看这个项目值不值得做” / “三哥，继续推进项目” / “小五看下这份合同” / “画一张网站首图”
   c. 如需重启或新开会话才能识别新技能，告诉我。
```

## 直接可发的三段

**Codex**

```text
请从我的技能库安装技能：源目录 Y:\Skills\codex-skills-library\skills，目标目录 E:\AI_Dev\Codex\home\skills。其余步骤按 Y:\Skills\codex-skills-library\docs\install-prompt.md 的「通用提示词」执行，做完按第 6 步汇报。
```

**WorkBuddy**

```text
请从我的技能库安装技能：源目录 Y:\Skills\codex-skills-library\skills，目标目录 C:\Users\AprilWu\.workbuddy\skills。注意你这里已有旧版 auto-loop，先备份再覆盖。其余步骤按 Y:\Skills\codex-skills-library\docs\install-prompt.md 的「通用提示词」执行，做完按第 6 步汇报。
```

**Trae CN**

```text
请从我的技能库安装技能：源目录 Y:\Skills\codex-skills-library\skills，目标目录 C:\Users\AprilWu\.trae-cn\skills。其余步骤按 Y:\Skills\codex-skills-library\docs\install-prompt.md 的「通用提示词」执行，做完按第 6 步汇报。
```

## OpenCode：不用安装，直接共用 Claude 的技能

OpenCode（本机 1.18.21）会自动加载 `~/.claude/skills` 和 `~/.agents/skills` 里的技能。2026-10-05 用 `opencode debug skill` 实测：5 个技能都已识别，路径都在 `C:\Users\AprilWu\.claude\skills`，版本与仓库一致，没有重复。

**不要**再往 `~/.config/opencode/skills` 复制一份，否则同名技能会重复。以后只需更新 `~/.claude/skills`，OpenCode 自动跟上。

发给 OpenCode 做验收：

```text
请验证你已加载我的技能库技能，不要安装或复制任何文件。
1. 运行 opencode debug skill，确认以下 5 个技能各出现一次，且来源是 C:\Users\AprilWu\.claude\skills：
   auto-loop、project-inception-analysis-cockpit、project-employee-agents、xiaowu-contract-review、local-image-generator
2. 回报每个技能 SKILL.md 里的 Skill version，应为：auto-loop 2026.10.05、project-inception-analysis-cockpit 2026.10.05、project-employee-agents 2026.10.05、xiaowu-contract-review 2026.09.29、local-image-generator 2026.10.05。
3. 别名路由自测（只回答会调用哪个技能，不要真正执行）：
   “老大，帮我做个产品介绍 PPT” / “小二，看看这个项目值不值得做” / “三哥，继续推进项目” / “小五看下这份合同” / “画一张网站首图”
4. 如果某个技能缺失，检查是否设置了环境变量 OPENCODE_DISABLE_CLAUDE_CODE、OPENCODE_DISABLE_CLAUDE_CODE_SKILLS 或 OPENCODE_DISABLE_EXTERNAL_SKILLS，告诉我结果，不要自行改配置。
```

## 以后同步

技能库更新后，对任一 AI 说：

```text
同步技能库：git -C Y:\Skills\codex-skills-library pull，然后按 docs\install-prompt.md 重新安装到你的技能目录，并回报版本号。
```
