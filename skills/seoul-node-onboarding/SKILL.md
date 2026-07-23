---
name: seoul-node-onboarding
description: Configure newly online FRP sub2api nodes on the Seoul server. Use when the user says a node/country machine is online, asks to add a node such as n08/tw01/sg02/my03/jp04/kr05/ts01/uk01, or wants Seoul Caddy/NewAPI-facing routing prepared for an FRP node. The skill updates Seoul server Caddy mappings, validates/reloads Caddy, checks frps listening ports, and reports the NewAPI internal Base URL.
---

# Seoul Node Onboarding

Skill version: `2026.07.24`

## Scope

Use this skill only for the Seoul server `150.109.233.152`.

It may:

- Compute node `remotePort` from the node name.
- SSH to Seoul with `~/.ssh/ShouerUbunutNewapi.pem`.
- Backup and update `/opt/new-api/Caddyfile`.
- Run `caddy validate` and `caddy reload` inside `new-api-caddy`.
- Check `frps` listening ports.
- Report the NewAPI internal URL `http://172.17.0.1:<remotePort>`.

It must not:

- SSH into the node machine unless the user explicitly provides node credentials and asks for that.
- Change node `frpc.toml`.
- Print FRP token, API keys, or NewAPI keys.
- Add broad wildcard `*.api.flaios.com` Caddy blocks unless DNS-01 support is confirmed.

## Node Rules

All official node ports stay in `16xxx`:

| Region | Names | Ports |
| --- | --- | --- |
| Vietnam | `n01-n99` | `16001-16099` |
| Taiwan | `tw01-tw99` | `16101-16199` |
| Singapore | `sg01-sg99` | `16201-16299` |
| Malaysia | `my01-my99` | `16301-16399` |
| Japan | `jp01-jp99` | `16401-16499` |
| Korea | `kr01-kr99` | `16501-16599` |
| Test | `ts01-ts99` | `16601-16699` |
| United Kingdom | `uk01-uk99` | `16701-16799` |

Compatibility aliases:

```text
n6 = n06 = 16006
n7 = n07 = 16007
```

Legacy ports, do not reuse:

```text
18080 = cliproxyapi_8317
18081 = cliproxyapi_win_8317
```

## Workflow

1. Parse the node name from the user. Normalize aliases:
   - `n6` -> `n06`
   - `n7` -> `n07`
   - preserve `tw01`, `sg02`, `my03`, `jp04`, `kr05`, `ts01`, `uk01`.
2. Compute `remotePort`.
3. SSH to Seoul and check:

```powershell
ssh -b 192.168.31.68 -i "$env:USERPROFILE\.ssh\ShouerUbunutNewapi.pem" ubuntu@150.109.233.152 "sudo ss -ltnp | grep frps || true"
```

4. If the expected `remotePort` is not listening, say the FRP client is not connected yet. Do not add Caddy unless the user explicitly wants preconfiguration.
5. If the port is listening, backup `/opt/new-api/Caddyfile`.
6. Add the node host to the existing node Caddy block:

```text
<node>.api.flaios.com -> <remotePort>
```

Also add compatibility alias when applicable:

```text
n6.api.flaios.com and n06.api.flaios.com -> 16006
n7.api.flaios.com and n07.api.flaios.com -> 16007
```

7. Validate and reload:

```bash
cd /opt/new-api
sudo docker exec new-api-caddy caddy validate --config /etc/caddy/Caddyfile
sudo docker exec new-api-caddy caddy reload --config /etc/caddy/Caddyfile
```

8. Verify:

```bash
curl -I --max-time 10 https://<node>.api.flaios.com/
curl -I --max-time 10 http://172.17.0.1:<remotePort>/
```

For HTTPS, a `502` can still mean Caddy is correctly routing but upstream node service is not responding. Distinguish Caddy/TLS failure from upstream failure.

9. Final response must include:

- Node name and aliases.
- Public URL.
- FRP remotePort.
- NewAPI internal Base URL.
- Whether `frps` is listening.
- Caddy validate/reload result.
- Any remaining action for the node owner.

## Implementation Notes

Current Caddy does not have DNS-01 support for true `*.api.flaios.com` wildcard certificate automation. Keep using explicit hostnames in Caddy unless DNS-01 is added.

If adding many nodes, still add explicit hosts only for online or soon-online nodes.
