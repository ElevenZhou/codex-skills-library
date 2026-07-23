---
name: seoul-server-status-check
description: Read-only Seoul server health inspection and Feishu notification workflow. Use when the user asks to check 首尔服务器, `api.yumiai.art`, `api1.yumiai.art`, `api100.yumiai.art`, `flaios.com`, `sub2api.flaios.com`, Docker container status on the Seoul host, or to push a server status summary into the company important-reminder Feishu webhook.
---

# Seoul Server Status Check

Skill version: `2026.07.24`

Use this skill to perform a read-only health check of the Seoul server and optionally send the result to the company Feishu reminder webhook. This skill must not restart services, rebuild Docker images, or modify production code.

## Workflow

1. Keep the scope read-only.
   - Use HTTP probes plus SSH inspection only.
   - Do not run `docker build`, `docker compose up --build`, `systemctl restart`, `git pull`, or any write action on the server.
2. Run the bundled checker script:

```powershell
python C:\Users\AprilWu\.codex\skills\seoul-server-status-check\scripts\check_seoul_server.py --notify
```

3. If you only need a local verification first, run:

```powershell
python C:\Users\AprilWu\.codex\skills\seoul-server-status-check\scripts\check_seoul_server.py --no-notify --json
```

4. Review the report:
   - `healthy`: all HTTP endpoints passed, all required containers are running, and no major memory or disk pressure was detected.
   - `degraded`: at least one endpoint failed, a required container is missing or stopped, or the host shows pressure signals.
   - `down`: the SSH inspection failed, so container and host status could not be confirmed.
5. If the user asks to adjust the check list, read `references/targets.md` and update the constants in `scripts/check_seoul_server.py`.

## What the script checks

- HTTP status of:
  - `https://api.yumiai.art`
  - `https://api1.yumiai.art`
  - `https://api100.yumiai.art`
  - `https://flaios.com`
  - `https://sub2api.flaios.com`
- SSH reachability to the Seoul host
- Host uptime, memory, and root disk usage
- Docker status for the required containers, including:
  - `new-api`
  - `new-api-caddy`
  - `new-api-mysql`
  - `new-api-redis`
  - `sub2api`
  - `sub2api-redis`
  - `sub2api-postgres`
  - `flaios-jimmyai-adapter`
  - `flaios-kmood-adapter`
  - `flaios-tokensfactory-omni-adapter`

## Notification rules

- Prefer `FEISHU_COMPANY_IMPORTANT_WEBHOOK` if it is set.
- Otherwise resolve the webhook from `C:\Users\AprilWu\memory\preferences\feishu-reminders.md`.
- Keep the webhook out of normal chat replies unless the user explicitly asks for it.

## Expected output

- Print a concise text report for the operator.
- When `--notify` is used, push the same report to the Feishu company important-reminder group.
- Preserve failure reasons in the report so the user can see why the status is degraded or down.
