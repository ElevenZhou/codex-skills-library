# Project Layout

Use this as the default and adapt existing repositories conservatively.

```text
AGENTS.md
README.md
CHANGELOG.md
AI_PROJECT_HANDOFF.md
project-governance.yml
.env.example
docs/
  project/{overview.md,architecture.md,decisions.md,milestones.md}
  project/intake.md
  project/governance-overrides.md  # only when project-specific adjustments exist
  ops/{runbook.md,deploy.md,troubleshooting.md,server.md}
src/ or app/ or package-specific code/
tests/ or package-specific tests/
scripts/
```

`docs/ops/*` may be omitted for a library or offline tool, but the README must link to replacement notes or say `Not applicable`.

`AGENTS.md` is the start-of-task contract. `README.md` is for users and contributors. `docs/project/*` records durable truth. `docs/ops/*` records runtime operation. `CHANGELOG.md` records externally meaningful change. `project-governance.yml` is policy, not a progress log.

Optional project notifications may store their notification-only webhook address in `project-governance.yml` and commit it. Local runtime secrets may live in an ignored file such as `.env.local`; they must not be staged or committed.
