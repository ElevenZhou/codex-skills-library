# Codex Skills Library

这个仓库用于集中管理和共享个人/团队 Codex skills。

## 目录结构

```text
skills/      # 可同步到 ~/.codex/skills 的技能目录
scripts/     # 安装、同步、检查脚本
```

## 当前技能

- `auto-loop`：自动驾驶舱，全自动规划、执行、验证、优化。
- `deck-studio-loop`：高质量 PPT/商业材料工作室式制作循环。
- `cli-creator`：CLI 创建技能。
- `playwright`：浏览器自动化技能。
- `playwright-interactive`：交互式浏览器调试技能。
- `screenshot`：桌面截图技能。

## 安装到当前设备

```bash
./scripts/install-skills.sh
```

默认同步到：

```text
${CODEX_HOME:-$HOME/.codex}/skills
```

## 从本机 Codex skills 回写到仓库

当你在本机修改或新增 skill 后：

```bash
./scripts/pull-from-local-codex.sh
```

然后提交：

```bash
git status
git add .
git commit -m "Update Codex skills"
git push
```

## 团队协作建议

- 建议 GitHub 仓库先设为 **Private**。
- 不要提交 API key、客户数据、`.env`、运行日志、缓存目录。
- 新增 skill 前先确认 `SKILL.md` 有清晰的 `name` 和 `description`。
- 重要技能建议包含 `references/` 和 `scripts/`，不要只写一个单文件说明。
- 修改后用 Codex 的 skill validator 检查，再提交。

