---
name: obsidian-memory
description: Extract, organize, and maintain durable personal memory, project knowledge, decisions, lessons, and reusable patterns in an Obsidian vault from Codex/ChatGPT conversations, exported chat logs, project notes, meeting notes, daily logs, or automation runs. Use when the user asks to turn conversations into Obsidian notes, maintain long-term memory, summarize business/work history, create a knowledge base, update a vault, run a memory review, or design scheduled/automatic memory workflows.
---

# Obsidian Memory

Create and maintain an Obsidian-based memory system from work conversations and raw notes. Treat the vault as durable external memory: concise, linked, source-aware, and safe to update repeatedly.

## Core Workflow

1. **Locate sources**: Use material provided in the current prompt first. If the user names files, folders, exports, or Codex threads, read those sources. Do not claim access to all historical conversations unless they are present in context or available through tools/files.
2. **Locate the vault**: Use the user-provided vault path. If absent, look for `OBSIDIAN_VAULT`, `.obsidian-memory/config.json`, or obvious local vault folders. If still unknown, ask for the path before writing; otherwise produce a dry-run memory packet.
3. **Extract memory candidates**: Separate durable facts, preferences, projects, decisions, lessons, open loops, and reusable patterns. Ignore chit-chat and transient execution details unless they explain a decision.
4. **Classify confidence**: Mark items as `confirmed`, `inferred`, or `needs-confirmation`. Never upgrade inferred claims to confirmed without source evidence.
5. **Write Obsidian notes**: Use the vault schema in `references/vault-schema.md`. Prefer small topical notes with wikilinks over one giant dump. Use frontmatter properties consistently.
6. **Update indexes**: Maintain MOC/index notes and project notes so the new memory is discoverable.
7. **Report changes**: List files created/updated, the most important new memories, and unresolved questions. For automation runs, keep reports short and action-oriented.

## Memory Types

- **Profile**: Stable facts about the user, working style, preferences, constraints, and recurring goals.
- **Project**: Current state, architecture, business context, active threads, risks, and next steps for a project.
- **Decision**: A dated choice with context, options considered, rationale, consequences, and links.
- **Lesson**: A reusable insight from a failure, success, debugging session, customer conversation, or workflow improvement.
- **Pattern**: A repeatable method, prompt, checklist, script, design pattern, or operating habit.
- **Open loop**: A follow-up, unresolved question, missing credential, blocked dependency, or future check.
- **Source digest**: A compact summary of a conversation/export used as evidence.

## Update Rules

- Prefer updating existing notes when the topic already exists; create new notes only for distinct projects, decisions, lessons, or patterns.
- Preserve user-written prose. Add sections such as `## Latest update`, `## Timeline`, `## Decisions`, or `## Open loops` instead of overwriting whole notes.
- Include source links or source labels when available: thread id, file path, date, project name, or export filename.
- Use ISO dates (`YYYY-MM-DD`) and timezone-aware timestamps when available.
- Use Obsidian wikilinks for internal links (`[[Project Name]]`) and Markdown links for external URLs.
- Avoid sensitive data leakage: summarize secrets, credentials, personal identifiers, and private customer data rather than copying raw values.
- Mark uncertainty explicitly with `status: needs-confirmation` or inline language such as `Inferred:`.

## Automation Runs

For scheduled memory jobs, use the workflow in `references/automation.md`. A good automation prompt should specify:

- Vault path
- Source folders/files to scan
- Time window to process
- Whether to write changes or produce a dry run
- Where to place run logs

If an automation has no new source material, update only the run log and do not churn vault notes.

## Helper Script

Use `scripts/obsidian_memory.py` for deterministic vault setup and JSON-driven note writes.

```bash
python3 scripts/obsidian_memory.py init --vault /path/to/vault
python3 scripts/obsidian_memory.py write-json --vault /path/to/vault --input memory-packet.json
```

Read `references/vault-schema.md` before designing note paths or properties. Read `references/extraction-policy.md` when deciding what should become durable memory. Read `references/automation.md` when creating or updating scheduled jobs.
