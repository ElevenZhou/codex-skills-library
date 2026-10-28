# Templates

## project-governance.yml

```yaml
version: 1
project: TBD
stage: discovery
timezone: America/Los_Angeles
daily_checkpoint:
  enabled: true
  cutoff: "00:00"
  minimum: one-meaningful-local-commit
push_policy: manual
required_docs:
  - AGENTS.md
  - README.md
  - docs/project/overview.md
  - docs/project/architecture.md
  - docs/project/decisions.md
  - docs/project/milestones.md
  - docs/project/intake.md
  - CHANGELOG.md
  - AI_PROJECT_HANDOFF.md
milestone_update_required: true
ai_handoff_required: true
production_change_requires_confirmation: true
notifications:
  enabled: false
  provider: feishu-webhook
  webhook_url: https://open.feishu.cn/open-apis/bot/v2/hook/replace-with-project-notification-hook
  events:
    - milestone_completed
    - important_conclusion
    - blocker_or_risk_change
    - delivery_ready
  quiet_on_unchanged: true
```

## Intake document

```markdown
# Project Intake

## Mandatory to start

- Project name: `...`
- Project code: `...`
- Goal in one sentence: `...`
- Target user or internal consumer: `...`
- Initial scope: `...`
- Explicit exclusions: `...`
- First acceptance criteria: `...`
- Current stage: `discovery | build | integration | validation | release | maintenance`
- Reference objects: `none` or `...`

## Recommended

- Repository setup mode: `new | cloned-existing`
- Remote URL: `...` or `TBD`
- Deadline or review date: `...`
- Target platforms and runtime versions: `...`
- Technical preferences and constraints: `...`
- Dependencies and external services: `...`
- Design or competitor references: `...`
- Environment matrix: `local | staging | production`
- Deployment target and rollback expectation: `...`
- Test strategy: `...`
- Budget/cost limit: `...`
- Known risks and open questions: `...`

Unknowns must be marked `TBD` with the person, source, or decision needed to resolve them. Local runtime secrets belong in an ignored file such as `.env.local`, not in tracked configuration.
```

## governance-overrides.md

Create this file only when the project extends or overrides the baseline.

```markdown
# Governance Overrides

## YYYY-MM-DD — Short title

Type: extension | project-exception | baseline-proposal
Baseline rule: `...`
Change: `...`
Reason/evidence: `...`
Scope: `this project | future projects`
Decision owner: `...` or `TBD`
Effective date: `YYYY-MM-DD`
Rollback condition: `...`
Status: active | retired | proposed
```

## Milestone entry

```markdown
## YYYY-MM-DD — Milestone title

Status: completed | partial | blocked
Evidence: tests, screenshots, build ID, review link, or command output
Docs updated: list files changed
Known risks: none or concrete risks
Next node: the next observable deliverable
```
