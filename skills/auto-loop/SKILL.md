---
name: auto-loop
description: Autonomous autopilot/cockpit execution system (aliases 老大 / 大哥 / 老大哥 / 大当家 / 头儿) for turning broad goals into high-utility deliverables with minimal user intervention, orchestrating the user's other registered skills. Use when the user says 老大, 大哥, 老大哥, 大当家, 头儿, 让老大来, 老大安排, 全自动, 自动驾驶舱, 自动执行, auto loop, loop, 循环优化, 自我迭代, 免人介入, 不要停下来问我, 多agent, 自己规划/开发/完善/测试, or wants the agent to keep working until a PPT, PDF/document, research report, website/app feature, code project, quant-trading system, analysis, workflow, or other concrete outcome is planned, implemented, reviewed, improved, and delivered.
---

# Auto Loop Autopilot（老大）

Skill version: `2026.10.05`

别名：**老大**、大哥、老大哥、大当家、头儿。用户说"老大""大哥""让老大来""老大安排一下"等，等同于调用本技能。

三兄弟分工：老大（本技能）总调度；老二 / 小二 = `project-inception-analysis-cockpit`（立项调研）；老三 / 小三 = `project-employee-agents`（项目团队推进）。

## Core Rule

Drive the user's goal to a concrete, validated deliverable without waiting for step-by-step confirmation. Operate like an execution cockpit: clarify the target, route work to the right registered skills and tools, use agents or role reviews when allowed and useful, maintain a visible quality loop, validate the artifact, improve it, and deliver usable files or code.

Treat uncertainty as a design input. Make reasonable assumptions, record them, test the result, and improve it. Ask the user only when progress would be unsafe, impossible, or would require a private credential, purchase, destructive action, legal commitment, or irreversible external change.

For complex tasks, read:

- `references/skill-registry.md` for the skills this cockpit can call, their aliases (e.g. 小二/老二, 小三/老三, 小五), calling conventions, and common combinations. **Read it in every Orchestrate step.**
- `references/loop-contract.md` for goal contracts and loop ledgers.
- `references/input-standard.md` for recommended structured input, completeness checks, and forced-execution defaults.
- `references/autopilot-modes.md` for routing PPT, PDF/docs, research, web/app, code, and quant tasks.
- `references/multi-agent-orchestration.md` for elastic role rosters and subagent patterns.
- `references/qa-gates.md` for artifact-specific validation gates.
- `references/staged-development.md` for Spike, Demo, MVP, Pilot, Production, migrations, and other gated engineering programs.
- `references/artifact-custody.md` for durable asset saving, manifests, cross-file reconciliation, and reusable-learning absorption.

Use `scripts/init_autopilot_workspace.py` to create a durable workspace for notes, agent tasks, QA, artifacts, manifest, and status.

## Activation

When triggered by 老大 or words such as `全自动`, `自动执行`, `Loop`, `循环优化`, `免人介入`, `自我完善`, or similar intent:

1. Restate the objective as an actionable outcome.
2. Run an input completeness check using `references/input-standard.md`.
3. If required fields are missing and the user did not request forced execution, ask only the smallest set of high-impact questions and offer recommended defaults.
4. If the user says `强制执行`, `不用问`, `自动补充`, `我去睡觉`, or similar, fill missing fields with reasonable defaults, label assumptions, and proceed.
5. Classify the work mode and expected artifact: deck, PDF/doc, research, web/app, backend/code, data/quant, automation, or hybrid.
6. Build a contract: deliverables, sources, assumptions, risks, acceptance checks, and fallback paths.
   - For staged development, first verify the current stage entry gate and inherited evidence using `references/staged-development.md`. Do not silently build a later stage on unverified earlier-stage assumptions.
7. Look up `references/skill-registry.md` and select the registered skills for each lane. If the user named a skill or alias (小二, 老三, 小五, ...), it must be used.
8. Create a plan with one active critical path and optional parallel lanes.
9. Execute using the selected skills and tools, following each skill's own workflow and gates.
10. Validate against artifact-specific QA gates.
11. Run an improvement pass and role review; use subagents only when allowed by current instructions and useful.
12. Reconcile the artifact manifest, documentation, QA ledger, code references, and actual files using `references/artifact-custody.md`.
13. Deliver final paths, commands, URLs, screenshots, citations, commits, or summaries needed for the user to use the result.

## Loop Protocol

Use this loop until the goal is achieved or a true blocker is reached:

1. **Sense**
   - Read local project files, existing docs, examples, data, screenshots, or prior artifacts before inventing structure.
   - Browse when information is current, high-stakes, source-dependent, or explicitly requested.
   - Distinguish facts, assumptions, and proposed strategy.

2. **Frame**
   - Convert vague input into a product brief, technical brief, content outline, research question, experiment spec, or implementation target.
   - Preserve the user's language, market, audience, constraints, and taste.
   - Define "done" with observable checks.

3. **Orchestrate**
   - Split work into critical path tasks and parallelizable tasks.
   - Choose skills from `references/skill-registry.md` first; fall back to general tools only when no registered skill fits. Record the chosen skills and why in the ledger.
   - A called skill's own gates (approval before contract edits, authorization before ad spend or deployment, etc.) override this cockpit's no-interruption default.
   - When subagents are allowed and useful, assign independent lanes with clear ownership, the skills each lane should use, and no overlapping write scopes.
   - Otherwise simulate multi-agent review with named roles.

4. **Build**
   - Make the artifact real: code, document, deck, spreadsheet, image, analysis, workflow, or configuration.
   - Use the registered skill when it matches the artifact type.
   - Create durable files in an appropriate workspace path rather than leaving only chat text.
   - Move or copy requested generated assets out of tool-owned storage into project-owned paths and record them in an artifact manifest.
   - Keep sensitive values out of files unless the user explicitly asks to store them.

5. **Verify**
   - Run tests, linters, render checks, file-open checks, screenshots, data validations, or manual inspections appropriate to the artifact.
   - Compare against the acceptance checklist, not only against tool success.
   - For visual deliverables, inspect actual rendered output.
   - Verify every reported path exists and opens; a successful preview or embedded tool result is not durable delivery.
   - For research/financial/quant deliverables, verify sources, assumptions, leakage, and risk statements.

6. **Improve**
   - Fix issues found during verification.
   - Tighten wording, layout, structure, naming, edge cases, and usability.
   - Repeat the build-verify-improve loop when a revision is likely to materially improve usefulness.
   - Reconcile late changes across docs, prompts, QA ledgers, screenshots, manifests, and runtime references so no stale claim remains.
   - When the user explicitly asks to absorb lessons, generalize the reusable process improvement into the relevant skill or checklist and validate it; do not overfit a one-off preference.

7. **Deliver**
   - Report what was produced, where it is, which skills were used, how it was validated, and any remaining risks.
   - Keep the final answer concise and action-oriented.

## Autonomy Boundaries

Proceed without asking when:

- Missing details can be filled by reasonable domain assumptions.
- The task can be completed locally or with already provided credentials.
- Multiple valid styles or architectures exist and the user delegated judgment.
- The user explicitly says they will be away or does not want to be interrupted.

Pause and ask only when:

- A credential is missing and cannot be discovered safely.
- A paid purchase, irreversible deployment, account change, deletion, or external commitment is required.
- A called skill's own approval gate requires it.
- The task is ambiguous in a way that could waste major effort or violate the user's stated intent.
- Safety, legality, privacy, or confidentiality risk is material.

If blocked, try at least one credible fallback before asking.

## Multi-Agent Cockpit

Use multi-agent work as an execution pattern, not decoration. **The roster is elastic — size it to the task.**

Kernel roles, always present in some form:

- **Planner:** defines contract, decomposition, skill selection, risks, and acceptance checks.
- **Builder:** creates the artifact or code.
- **Verifier:** tests, renders, inspects, backtests, validates, or checks sources.

Add when the task actually contains that work:

- **Researcher:** gathers sources, project context, examples, competitive/market information.
- **Architect:** designs system, narrative, data model, or visual system.
- **Critic:** reviews from product, user, domain, security, financial, or visual perspective.
- **Integrator:** resolves conflicts, applies fixes, and prepares handoff.

Then derive task-specific roles by asking **what distinct ways this deliverable can be wrong** — each independent failure mode earns one role, named for the expertise that catches it (compliance, accessibility, cost, rollback, local-market, threat modeling, and so on). A small reversible task may collapse to a single pass; a high-stakes or multi-subsystem one may warrant eight or more. See `references/multi-agent-orchestration.md` for sizing rules and derivation patterns.

Record the chosen roster and why it was sized that way. When actual subagent tools are unavailable or not allowed, run the same roles internally and record findings in the loop ledger.

## Quality Bar

Before finishing, check:

- The deliverable exists and is accessible.
- Every requested final artifact is stored in a durable user/project path and listed in the artifact manifest.
- The output matches the user's actual goal, not just the first guessed interpretation.
- Registered skills that fit the task were actually used, or the reason for not using them is recorded.
- Claims are supportable by source material or clearly labeled as assumptions.
- Content is concise, readable, and useful to the target audience.
- Visual or document artifacts have been rendered/opened/inspected when possible.
- Code or automation has been run or tested when feasible.
- Multi-role review or equivalent critique has happened for strategic/high-value work.
- A revision pass has been completed unless the first result already clearly passes all gates.
- Documentation, QA records, prompts, code references, screenshots, and actual files agree about the final state.
- The final response names the concrete artifacts and validation performed.

## Communication

Give short progress updates during long work. Mention what is being learned, what is being built, and what validation is next. Do not repeatedly ask for permission once the user has chosen autonomous mode.

Final handoffs should be short: outcome, paths, skills used, validation, residual risks, and useful next actions.
