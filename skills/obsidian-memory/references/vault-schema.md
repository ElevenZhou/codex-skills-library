# Vault Schema

Use this default layout unless the user's vault already has a clear organization. Preserve existing conventions when present.

```text
00 Inbox/
  Memory Inbox.md
10 Memory/
  User Profile.md
  Preferences.md
  Working Style.md
20 Projects/
  <Project Name>.md
30 Decisions/
  YYYY-MM-DD - <Decision>.md
40 Knowledge/
  Patterns/
  Lessons/
50 Reviews/
  Weekly/
  Monthly/
90 Index/
  MOC - Memory.md
  MOC - Projects.md
  MOC - Decisions.md
99 System/
  Memory Runs.md
```

## Common Frontmatter

```yaml
---
title: Example Note
type: project | profile | preference | decision | lesson | pattern | open-loop | source-digest | moc
status: active | archived | confirmed | inferred | needs-confirmation
date: 2026-07-01
updated: 2026-07-01
sources:
  - Current Codex thread
confidence: confirmed | inferred | needs-confirmation
tags:
  - memory
---
```

## Note Templates

### Project Note

```markdown
---
title: Project Name
type: project
status: active
updated: YYYY-MM-DD
tags:
  - project
---

# Project Name

## Current State

## Business Context

## Architecture / System Notes

## Decisions

- [[YYYY-MM-DD - Decision Title]]

## Open Loops

- [ ] Follow-up item

## Timeline

- YYYY-MM-DD: Update with source.
```

### Decision Note

```markdown
---
title: Decision Title
type: decision
status: confirmed
date: YYYY-MM-DD
updated: YYYY-MM-DD
confidence: confirmed
sources:
  - Source label
---

# Decision Title

## Decision

## Context

## Options Considered

## Rationale

## Consequences

## Links
```

### Lesson or Pattern Note

```markdown
---
title: Lesson or Pattern
type: lesson
date: YYYY-MM-DD
updated: YYYY-MM-DD
confidence: confirmed
sources:
  - Source label
tags:
  - memory/lesson
---

# Lesson or Pattern

## Summary

## Trigger / Evidence

## Reusable Rule

## Example

## Related
```

## Index Notes

Keep indexes short and link-rich. Example:

```markdown
# MOC - Projects

## Active

- [[Project Name]] - one-line current state

## Paused / Archived
```
