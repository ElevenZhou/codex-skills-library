---
name: ccswitch-config-transfer
description: Back up and copy CCSwitch / CC-Switch user configuration from the current workstation to another machine, especially Salt-managed CRS nodes. Use when the user asks to migrate, restore, clone, deploy, back up, or sync ccswitch/cc-switch config, `~/.cc-switch`, `cc-switch.db`, CCSwitch desktop state, or CCSwitch settings to a node such as TS08.
---

# CCSwitch Config Transfer

Use this skill to clone CCSwitch configuration while preserving rollback backups and avoiding WebView/cache noise.

## What To Copy

Prefer the cross-platform user config directory:

- Windows source: `%USERPROFILE%\.cc-switch`
- macOS target/source: `~/.cc-switch`
- Core files: `cc-switch.db`, `settings.json`, optional `copilot_auth.json`, optional `skills/`

Do not copy browser/WebView caches by default:

- Windows: `%LOCALAPPDATA%\com.ccswitch.desktop\EBWebView`
- macOS: `~/Library/Caches/com.ccswitch.desktop`, `~/Library/WebKit/com.ccswitch.desktop`

These contain platform-specific runtime data and can be large. Only inspect or migrate them when the user explicitly asks for full desktop state/login state and accepts the risk.

## Salt Node Workflow

For CRS Salt-managed macOS nodes, use `scripts/Copy-CCSwitchConfigToSaltNode.ps1` from a Windows workstation that can SSH to the Salt master.

Example:

```powershell
& "$HOME\.codex\skills\ccswitch-config-transfer\scripts\Copy-CCSwitchConfigToSaltNode.ps1" `
  -TargetNodeId TS08 `
  -TargetUser april `
  -MasterHost <salt-master-host> `
  -MasterKey <path-to-ssh-key> `
  -BindAddress <salt-fileserver-bind-address>
```

The script:

1. Builds a local zip under `backups/ccswitch-<timestamp>.zip`.
2. Uploads the archive to the Salt master.
3. Publishes it through the Salt fileserver.
4. Pulls it to the target node with `cp.get_file`.
5. Verifies SHA256.
6. Stops CCSwitch processes on the target.
7. Backs up the target `~/.cc-switch` to `~/.cc-switch.restore-backups/<timestamp>/`.
8. Restores the source config and runs SQLite integrity check when `sqlite3` exists.

## Manual Workflow

When not using the script:

1. Package only the source `.cc-switch` core files.
2. Transfer the archive with a binary-safe path. Avoid old `salt-cp` behavior that reads zip files as UTF-8; prefer `cp.get_file` via fileserver.
3. On the target, stop CCSwitch before replacing config.
4. Back up the target config before overwriting.
5. Restore ownership to the target user.
6. Verify `cc-switch.db` with `sqlite3 ~/.cc-switch/cc-switch.db "PRAGMA integrity_check;"`.

## Safety

Treat CCSwitch config as sensitive. It may contain account/session/provider data. Do not paste file contents into chat, docs, git, or issue trackers. Record only paths, timestamps, checksums, and high-level outcomes.

Before recursive deletion or replacement, verify the final target is exactly the intended `.cc-switch` directory under the target user's home.
