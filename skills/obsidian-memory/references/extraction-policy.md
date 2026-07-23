# Extraction Policy

Convert raw conversations into durable memory only when the information is likely to be useful later.

## Keep

- Stable user preferences, working style, goals, recurring constraints, and language preferences.
- Project facts: names, repositories, architecture choices, current status, blockers, important paths, deployment details, and business context.
- Decisions with rationale and consequences.
- Lessons learned from debugging, product work, customer work, writing, operations, or strategy.
- Reusable prompts, checklists, scripts, naming conventions, and workflows.
- Open loops that need future action.

## Usually Drop

- Tool chatter, temporary command outputs, failed attempts that do not teach a reusable lesson.
- Low-signal pleasantries and repeated restatements.
- Raw secrets, keys, tokens, passwords, private customer identifiers, or sensitive personal data.
- Facts with weak evidence unless marked as inferred or needs-confirmation.

## Confidence

- `confirmed`: Explicitly stated by the user or directly present in a source file.
- `inferred`: Reasonable conclusion from repeated behavior or indirect evidence.
- `needs-confirmation`: Useful but uncertain, contradictory, or incomplete.

## Compression Targets

- A long conversation should normally produce 3-12 durable bullets, not a transcript.
- A source digest can be longer, but project/profile notes should stay curated.
- Prefer adding one dated timeline bullet to a project note over rewriting the note.

## Safety

- If source material contains secrets, write `[redacted secret]` and describe only the existence or operational implication.
- For sensitive business data, store a summary and link to the source location instead of copying raw payloads.
