# Seoul Server Targets

Use this reference only when the user wants to update the target list or confirm why a check is considered healthy.

## SSH

- Host: `150.109.233.152`
- User: `ubuntu`
- Bind IP: `192.168.31.68`
- Key: `C:\Users\AprilWu\.ssh\ShouerUbunutNewapi.pem`

## HTTP endpoints

- `https://api.yumiai.art` -> healthy when it returns `302`
- `https://api1.yumiai.art` -> healthy when it returns `302`
- `https://api100.yumiai.art` -> healthy when it returns `302`
- `https://flaios.com` -> healthy when it returns `200`
- `https://sub2api.flaios.com` -> healthy when it returns `200`

## Required Docker containers

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

## Feishu notification target

- Company important reminder bot
- Resolve the webhook from `FEISHU_COMPANY_IMPORTANT_WEBHOOK`
- Fall back to `C:\Users\AprilWu\memory\preferences\feishu-reminders.md`
