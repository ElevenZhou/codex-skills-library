---
name: project-ops-standards
description: Create, audit, or improve the minimum project management and operations documentation for a software project. Use when the user asks to standardize a project directory, create AGENTS.md, establish Codex project management practices, document server/production operations, deployment steps, rollback, troubleshooting, environment variables, service ownership, or says future projects should follow a minimum docs standard.
---

# Project Ops Standards

Use this skill to make a repository manageable by Codex and humans across development, deployment, and production operations.

## Workflow

1. Inspect the repository root, existing docs, README files, package/runtime files, deployment configs, and service/process config before editing.
2. If an external server-info directory or file is mentioned, read it and extract only operational facts. Do not copy secrets into generated docs.
3. Create or update the minimum project documentation set described in `references/minimum-project-standard.md`.
4. Prefer improving existing files over creating duplicates. Preserve project-specific conventions and user-authored notes.
5. Mark unknown facts explicitly as `TBD` with the command or source needed to confirm them.
6. For production services, include health checks, log locations, deploy steps, rollback steps, and safe-change rules.
7. Never include real tokens, passwords, private keys, cookies, or full connection secrets. Use placeholders and point to the secure source location.
8. After edits, run a lightweight validation: list created/updated files, check links/paths where practical, and confirm the standard is complete or note gaps.

## Required Reference

Read `references/minimum-project-standard.md` before creating or auditing project docs.

## Output Style

When finished, report the docs created or updated, key facts captured, unresolved `TBD` items, and recommended next operational action.
