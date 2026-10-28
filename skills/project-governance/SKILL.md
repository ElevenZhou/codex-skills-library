---
name: project-governance
description: Standardize new software projects, keep core docs current at milestones, and create traceable daily Git checkpoints.
---

# Project Governance

Use this skill when starting, auditing, or maintaining a software project where inconsistent folders, incomplete README files, stale milestone documentation, or irregular Git history create delivery risk.

This skill provides a project governance layer. Reuse `project-ops-standards` for detailed operations documentation instead of duplicating it.

## Operating contract

Every governed project has a short root `AGENTS.md`, a root `README.md`, predictable `docs/` project records, a machine-readable `project-governance.yml`, a `CHANGELOG.md`, an `AI_PROJECT_HANDOFF.md`, and at least one meaningful local Git checkpoint per working day. Do not invent facts; mark unknowns as `TBD` with a verification method. Separate local runtime secrets from tracked project configuration.

`AI_PROJECT_HANDOFF.md` is mandatory for AI-developed projects. Every AI session reads it before work and updates it after a meaningful change, milestone, context switch, or session end. It must state the current stage, verified progress, files changed, tests/evidence, open risks, blocked items, exact next action, and instructions for the next AI. Keep it concise and factual; it is a coordination record, not a transcript.

Every new project also starts with `docs/project/intake.md`. The intake has a small mandatory core and a recommended section. Do not block initialization because a recommended item is unknown; write `TBD` and add the source or decision needed to resolve it. Do block the first build milestone when a mandatory item is missing and no explicit assumption has been recorded.

Feishu or Lark webhook notifications are an optional project capability. If enabled in `project-governance.yml`, use the available `feishu-webhook-push` workflow for important results and conclusions only. A notification-only webhook may be written directly in the project configuration and committed to Git because it is intentionally a delivery endpoint. Other credentials may exist in local project runtime configuration when needed, but they must be excluded from Git and never enter a commit. Do not notify for every edit or unchanged status.

The baseline is intentionally extensible. A project AI may add project-specific fields, documents, checks, scripts, or milestone gates when real use shows they are needed. Keep the shared baseline intact, record the reason and scope in `docs/project/governance-overrides.md`, and make the change reversible. Do not silently delete a baseline requirement or change the shared skill from inside one project.

## Modes

### Initialize

Inspect the repository before editing. If the target is an empty directory and the operator provided no project information, stop before creating the skeleton and ask for the mandatory intake using [references/intake-prompt.md](references/intake-prompt.md). Do not invent the project name, code, goal, target user, scope, exclusions, acceptance criteria, stage, or reference objects. If some information was provided, ask only for missing mandatory fields. Create the project skeleton only after the mandatory intake is complete or the operator explicitly records an assumption for each missing field. Preserve existing conventions when they already cover the same information. Create only missing files and directories. Read [references/project-layout.md](references/project-layout.md) and use [references/templates.md](references/templates.md).

Collect or infer the mandatory intake: project name and code, one-sentence goal, target user or internal consumer, initial scope and exclusions, first acceptance criteria, current stage, and reference objects when references exist. Treat provided reference objects as authorized by default. Collect recommended material when available: repository setup mode (new or cloned), remote URL, deadline, target platforms, technical preferences, dependencies, design references, competitor/reference products, environment matrix, deployment target, test strategy, budget/cost limits, and known risks. Label assumptions.

### Milestone update

Run this after a major feature, architecture change, integration, release candidate, or other declared node completes. Update the smallest consistent set of README, overview, architecture, decisions, milestones, changelog, and `AI_PROJECT_HANDOFF.md`. A milestone is not complete until code, tests, docs, handoff, and status agree.

### AI handoff update

At session start, read `AI_PROJECT_HANDOFF.md` before exploring broadly. At session end, update it even when blocked. Use [references/ai-handoff-template.md](references/ai-handoff-template.md). Never claim completion without evidence; distinguish `completed`, `partial`, `blocked`, and `not verified`.

### Adjustment and feedback

When a project needs a different rule, classify the change:

- **Extension**: add a field, document, check, or workflow. The AI may apply it and record it.
- **Project exception**: temporarily relax or replace a rule for this repository. Record the old rule, new rule, reason, owner of the decision, effective date, and rollback condition in `docs/project/governance-overrides.md`.
- **Baseline proposal**: a change that should apply to future projects. Record the evidence and proposal in the shared skill backlog; do not silently rewrite the shared baseline during ordinary project work.

Prefer additive changes. After two or more projects independently need the same extension, consider promoting it to the shared baseline.

### Daily checkpoint

Inspect `git status`, branch, and latest checkpoint. If there are meaningful changes, create one focused local commit before the configured daily cutoff. Default cutoff is `00:00 America/Los_Angeles`; configure it in `project-governance.yml`. Do not include secrets, generated noise, or unrelated changes.

Pushing is separate from committing. Follow `push_policy`: `manual` (default), `on-success`, or `scheduled`. Never silently push to a protected or production branch. Preserve unrelated dirty work.

### Important-result notification

When project notifications are enabled, notify after a meaningful milestone, delivery, decision, blocker, or risk change. Include the project name/code, conclusion, evidence, impact, and next action. Report only notification success or a non-secret error. A successful webhook means the message was accepted, not that the underlying work was deployed or completed.

## Validation and output

Before storing local credentials, verify the destination is ignored and is not already tracked (`git check-ignore` and `git ls-files`). `.gitignore` does not protect files already tracked. Use a separate ignored file when needed, preserve existing local values, and inspect staged changes without printing credential values. Keep shared docs and handoffs limited to paths and variable names. This local-runtime exception takes precedence over broader no-secret-in-project wording in reused documentation guidance; it never permits committing business credentials.

After any mode, verify required files, internal links where practical, non-placeholder commands, and Git status. Use [references/checklist.md](references/checklist.md). For production or operational projects, also apply `project-ops-standards`.

Report mode, files created or updated, facts versus `TBD`, validation, Git checkpoint status, and any action requiring explicit authorization. A commit is not a deployment and a push is not proof that the application runs.
