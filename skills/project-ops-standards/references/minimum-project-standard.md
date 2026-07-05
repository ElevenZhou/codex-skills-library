# Minimum Project Standard

Use this standard when creating or auditing project management and operations documentation.

## Minimum Directory Set

At the repository root, maintain:

```text
AGENTS.md
docs/
  ops/
    server.md
    deploy.md
    troubleshooting.md
    runbook.md
  project/
    overview.md
    architecture.md
    decisions.md
.env.example
```

If the repo already has a clear docs structure, adapt names conservatively but preserve the same information coverage.

## AGENTS.md

Include:

- Project purpose and primary domain/service name.
- Tech stack, runtime versions, package manager, build/test commands.
- Local development startup and required env files.
- Repository map with the most important directories.
- Codex working rules for this project: inspect first, preserve secrets, avoid destructive production changes, verify after edits.
- Links to `docs/ops/*` and `docs/project/*`.
- Current known production environment and where authoritative server information lives.

Keep `AGENTS.md` short enough to be read at the start of every task. Move details into `docs/`.

## docs/project/overview.md

Include:

- What the product/service does.
- Users or clients of the service.
- Main public domains and APIs.
- Major dependencies and external services.
- Ownership/contact notes if known.
- Open questions and `TBD` facts.

## docs/project/architecture.md

Include:

- High-level request flow.
- Main modules and data stores.
- Background jobs, queues, cron tasks, workers, and third-party APIs.
- Runtime boundaries: local, staging, production.
- Ports and protocols.
- A simple Mermaid diagram when useful.

## docs/project/decisions.md

Use lightweight ADR-style entries:

```text
## YYYY-MM-DD - Decision title

Context:
Decision:
Consequences:
```

Record deployment model, runtime manager, database choices, auth model, and other decisions Codex should not rediscover.

## docs/ops/server.md

Include:

- Provider, region, OS, hostname/IP, domain names.
- SSH access method as a placeholder or secure reference, never raw passwords or private keys.
- Application path on server.
- Runtime/process manager: systemd, pm2, Docker, compose, supervisor, or other.
- Service names, ports, nginx/Caddy config paths, TLS/cert locations.
- Log locations for app, web server, process manager, and deployment logs.
- Data locations and backup notes.
- Environment file locations with variable names only.
- Common safe read-only inspection commands.
- Change rules: what requires approval, backup, or rollback prep.

## docs/ops/deploy.md

Include:

- Deployment prerequisites.
- Exact deploy path and branch/tag policy.
- Build/install commands.
- Migration commands if any.
- Restart/reload commands.
- Post-deploy health checks, including HTTP checks and log checks.
- Rollback procedure with commands or exact manual steps.
- Smoke-test checklist.

For live services, avoid deploy instructions that assume destructive cleanup or blind restarts.

## docs/ops/troubleshooting.md

Include playbooks for:

- 502/504 or upstream unavailable.
- Service not starting.
- High CPU/memory/disk.
- Failed deploy/build.
- Database/API dependency errors.
- TLS/domain/nginx issues.
- Missing env variables or secrets.

Each playbook should follow:

```text
Symptoms:
First checks:
Likely causes:
Safe fixes:
Escalation/rollback:
```

## docs/ops/runbook.md

Include routine operational tasks:

- Check service health.
- Tail logs.
- Restart service safely.
- Renew/reload TLS if applicable.
- Inspect disk usage.
- Backup/restore summary.
- Rotate or update environment variables.
- Add a new domain or route, if relevant.

## .env.example

Include variable names and short comments only:

```text
API_KEY=replace-me
DATABASE_URL=replace-me
```

Do not include real production values, tokens, passwords, cookies, or private keys.

## Audit Checklist

A project meets the standard when:

- `AGENTS.md` tells Codex how to work in the repo.
- All minimum docs exist or equivalent existing docs are linked.
- Production/server facts are documented without leaking secrets.
- Deploy and rollback steps are present.
- Troubleshooting has concrete first checks and safe fixes.
- `.env.example` lists required config without real secrets.
- Unknowns are marked as `TBD` with how to verify them.
