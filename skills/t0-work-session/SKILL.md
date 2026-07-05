---
name: t0-work-session
description: T0-SemiAuto work-session handoff and Git synchronization workflow. Use when the user says Chinese end-of-work phrases such as "下班了", "完成了", "好了休息了", "睡觉了", "收工", "结束任务" to update handoff docs, verify, commit, and push when possible; or start-of-work phrases such as "开工", "开始任务", "继续任务" to fetch/pull Git and load project state before new work.
---

# T0 Work Session

Use this skill to keep `T0-SemiAuto` recoverable across computers, Codex threads, and other AI assistants.

## Start-Of-Work Workflow

Trigger examples: `开工`, `开始任务`, `继续任务`, `接着做`, `开始研究`.

1. Locate the repository root and run:
   ```powershell
   git status -sb
   git remote -v
   ```
2. If an upstream remote exists, fetch first:
   ```powershell
   git fetch --all --prune
   git status -sb
   ```
3. Pull only when the worktree is clean or when all local changes are clearly unrelated and safe.
   Prefer:
   ```powershell
   git pull --ff-only
   ```
   Do not auto-stash, merge, rebase, reset, or discard local work.
4. Read the handoff documents before editing:
   - `README.md`
   - `RULES.md`
   - `AI_HANDOFF.md`
   - `正式版/正式版V4/README.md` when the task is about current 300617 research.
5. Summarize what changed since the last local commit, current branch/upstream status, and the next safe action.

## End-Of-Work Workflow

Trigger examples: `下班了`, `完成了`, `好了休息了`, `睡觉了`, `收工`, `结束任务`.

1. Inspect the worktree:
   ```powershell
   git status --short
   git diff --stat
   ```
2. Update handoff docs when anything material changed:
   - `AI_HANDOFF.md`: current state, key files, current conclusions, next steps.
   - `README.md`: user-facing recent changes, important paths, cross-computer instructions.
   - `RULES.md`: durable collaboration rules only; do not use it as a daily log.
   - Version or folder README files, such as `正式版/正式版V4/README.md`, when that area changed.
3. Run the lightest meaningful verification for touched code. Examples:
   ```powershell
   python -m py_compile <changed-python-files>
   ```
   Use focused backtests or report-generation scripts only when needed and practical.
4. Inspect staged content before committing:
   ```powershell
   git status --short
   git diff --cached --stat
   ```
   Do not commit `.venv/`, cache folders, secrets, tokens, local broker config, or unrelated private files.
5. Commit when there are changes:
   ```powershell
   git add -A
   git commit -m "<concise handoff message>"
   ```
   If there are no changes, report that no commit is needed.
6. If a remote is configured, push so another computer can pull the work:
   ```powershell
   git push
   ```
   If network or approval blocks the push, leave the local commit in place and report the exact push command.
7. Final response must include the commit hash, whether push succeeded, and the handoff files that were updated.

## Safety Rules

- Never use `git reset --hard`, `git checkout --`, destructive deletes, or forced pushes unless the user explicitly requests and approves them.
- If local changes appear that you did not create, stop and ask how to proceed unless they are clearly expected from the user's prior action.
- Do not restore user-deleted Trae artifacts unless the user explicitly asks.
- Keep the single-order target amount at `50000` CNY unless the user explicitly changes it.
- Treat `legacy_full_day` as attribution/reference only; do not present it as live-safe strategy logic.

## Project-Specific Handoff Checklist

For the current `T0-SemiAuto` project, a good end-of-work handoff usually records:

- Current 300617 research target and candidate strategy names.
- Data freshness, especially the latest timestamp in 5-minute data.
- Key generated reports or recap HTML paths needed for review.
- Known failure environments, such as 2026-04 trend-following losses.
- The next research step, preferably one concrete experiment rather than a broad search.
