# Governance Checklist

## Initialize

- [ ] Repository, branch, and dirty files inspected
- [ ] If the directory was empty and intake was absent, the operator was prompted before files were created
- [ ] Root `AGENTS.md` and `README.md` exist and link to docs
- [ ] `AI_PROJECT_HANDOFF.md` exists and names the current stage, evidence, risks, and next action
- [ ] `project-governance.yml` has explicit timezone and push policy
- [ ] `docs/project/intake.md` contains all mandatory fields; unknowns are explicit assumptions or `TBD`
- [ ] Overview, architecture, decisions, and milestones exist or are marked not applicable
- [ ] Runtime and test commands are verified or marked `TBD`
- [ ] Local runtime secrets, if required, are stored in an ignored file and absent from the staged diff
- [ ] `.env.example` contains names or placeholders only
- [ ] If notifications are enabled, the tracked endpoint is notification-only; non-notification credentials are not staged

## Milestone

- [ ] Feature behavior and acceptance evidence recorded
- [ ] Relevant docs and changelog reconciled
- [ ] Tests/build/smoke checks recorded
- [ ] Risks and next node are explicit
- [ ] `AI_PROJECT_HANDOFF.md` agrees with code, tests, and milestone status

## Daily checkpoint

- [ ] `git status --short --branch` inspected
- [ ] Unrelated or sensitive files excluded
- [ ] Meaningful local checkpoint created before cutoff, or reason recorded
- [ ] Push status reported separately from commit status
- [ ] Handoff record updated before ending the session
- [ ] Important-result notification sent when configured, or explicitly marked not applicable
