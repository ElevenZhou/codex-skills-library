---
name: submit-results-to-workbench
description: Submit finished work from any project into the user's personal workbench in the FlaiOS / 飞流AI枢纽 repository. Use when the user says 提交成果到工作台, 把成果登记到工作台, 记录项目成果, update my workbench, log this project's progress, or wants an agent in another project to write project status, progress, next actions, risks, assets, and optionally public FlaiOS catalog entries back to I:\Dev\通用性agent开发.
---

# 提交成果到工作台

Skill version: `2026.07.24`

把任意项目里的阶段性成果沉淀回飞流AI枢纽的个人工作台。默认只更新工作台状态文件；如果成果适合展示或复用，再可选提交到飞流AI枢纽内容库。

## Default Target

- Workbench repository: `I:\Dev\通用性agent开发`
- Workbench files: `workbench/*.yaml`
- Public catalog files: `content/*.yaml`, `agents/**`, `packages/codex-skills/**` only when explicitly useful

If the user gives another workbench path, use that path instead. If running outside the workbench repo, still edit the target repo directly and do not modify the current project unless the user explicitly asks.

## Decision

1. If the user only asks to submit or record progress, update the personal workbench only.
2. If the user asks to publish, share, submit to FlaiOS, add to catalog, or the result is clearly reusable as a website/tool/project/Agent/Skill/workflow/memory/guide, also prepare a draft public catalog entry.
3. If the request involves finance, legal, health, credentials, private relationships, tokens, accounts, or other sensitive facts, ask before writing those facts.

## Workbench Workflow

1. Locate the target repo, defaulting to `I:\Dev\通用性agent开发`.
2. Read `workbench/workbench.yaml` first.
3. Read only the needed module files:
   - `workbench/projects.yaml` for project status, stage, summary, next action.
   - `workbench/progress.yaml` for completed work or milestones.
   - `workbench/risks.yaml` for blockers, risks, limitations, privacy concerns.
   - `workbench/assets.yaml` for repos, domains, files, kits, datasets, or deliverables.
   - `workbench/plans.yaml` for follow-up plans.
   - `workbench/relations.yaml` only for people/groups/agent relationships.
4. Preserve existing IDs and fields. Use stable kebab-case IDs for new records.
5. Append new progress entries instead of overwriting history.
6. Update project `stage`, `status`, `summary`, `next_action`, links, and related assets when useful.
7. Run `npm run hub:catalog` from the workbench repo when available.
8. Final response must list changed files, new or updated IDs, validation result, and assumptions.

## Optional Public Catalog Workflow

Use this only when the user asks for public submission or the result should become a reusable FlaiOS item.

1. Read `docs/navigation-taxonomy.md` and `docs/submissions.md` in the target repo.
2. Classify the result as one of: `ai_website`, `tool`, `agent`, `skill`, `workflow`, `project`, `memory`, or `guide`.
3. Add or update the matching content location:
   - AI websites: `content/ai-websites.yaml`
   - Tools: `content/tools.yaml`
   - Projects: `content/projects.yaml`
   - Workflows: `content/workflows.yaml`
   - Memories: `content/memories.yaml`
   - Skills: `content/skills.yaml` or `packages/codex-skills/<skill-id>/SKILL.md`
   - Agents: existing `agents/<category>/<agent-id>/` convention
4. Default new public entries to `status: draft` unless the user asks to publish.
5. Fill conservative facts only: name, category, tags, one-liner, best_for, not_good_for, rating, owner_note, links, and limitations.
6. Run useful validation when available: `npm run catalog`, `npm run lint:agents`, `npm run website:build`.

## Minimum User Input To Infer

If details are missing, infer from the current repository and recent changes when safe:

- Project name from folder name, package name, README, or git remote.
- Completion summary from git diff, recent files, tests, or the user's message.
- Stage/status from evidence: building for active implementation, testing after validation, launched only with explicit deployment evidence, done only when the user says complete.
- Next action from failing checks, TODOs, or obvious follow-up.

Ask only if the target project cannot be identified or writing the inferred fact would be risky.

## Reusable Prompt

When another agent needs an exact instruction, use:

```text
使用 submit-results-to-workbench：把当前项目这次成果提交到我的工作台。

工作台仓库路径：I:\Dev\通用性agent开发

请只在工作台仓库中更新必要文件，默认只改 workbench/*.yaml，不要改当前项目源码。记录：项目名称、阶段、状态、本次完成进展、下一步、风险/注意事项、相关链接或资产。如果成果适合公开复用，再以 draft 状态提交到飞流AI枢纽内容库。完成后运行 npm run hub:catalog，并说明改了哪些文件和 ID。
```
