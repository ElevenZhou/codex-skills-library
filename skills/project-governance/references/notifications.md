# Optional Feishu Notifications

Notifications are disabled by default and are opt-in per project.

```yaml
notifications:
  enabled: true
  provider: feishu-webhook
  webhook_url: https://open.feishu.cn/open-apis/bot/v2/hook/replace-with-project-notification-hook
  events:
    - milestone_completed
    - important_conclusion
    - blocker_or_risk_change
    - delivery_ready
  quiet_on_unchanged: true
```

The actual notification-only webhook URL may be committed to `project-governance.yml` or another project configuration file so every project AI can use the same group destination. This exception applies only to a delivery webhook intended for project notifications.

Business API keys, admin credentials, tokens, passwords, private keys, and cookies may be written to local runtime configuration when the project needs them, but that file must be ignored by Git and verified absent from the staged diff. The rule is “local project use is allowed; Git submission is forbidden.”

Send one concise card for a meaningful event. Include:

- project name or code;
- event and conclusion;
- evidence or verification state;
- user or delivery impact;
- next action or required decision.

Do not send routine file edits, every AI turn, unchanged health checks, raw logs, tokens, or full transcripts. If the webhook fails, keep the project work result separate from the notification result and record the failure in the handoff when it affects coordination.
