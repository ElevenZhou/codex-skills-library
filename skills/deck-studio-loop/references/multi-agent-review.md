# Multi-Agent Review

Use role review even if actual subagent tools are unavailable. If subagents are available and the task is important, run independent reviews with minimal context.

## Internal Roles

### Product Manager

Checks whether the product, workflow, user value, and roadmap are clear.

Questions:

- Can a non-technical buyer understand what the product does?
- Are use cases concrete?
- Does the deck avoid overpromising?

### Sales / Customer

Checks whether a prospect would care.

Questions:

- Is the pain obvious?
- Does each feature connect to a business result?
- Is the call to action clear?

### Investor / Executive

Checks strategic logic.

Questions:

- Is the category shift credible?
- Are business model and defensibility understandable?
- Is the deck concise enough for a senior audience?

### Domain Expert

Checks professional credibility.

Questions:

- Are claims consistent with industry practice?
- Are technical and compliance boundaries stated correctly?
- Are risky claims softened or sourced?

### Visual Director

Checks design.

Questions:

- Does the deck have a distinctive system?
- Are there too many similar cards?
- Is hierarchy strong at thumbnail size?
- Do images and diagrams carry meaning?

### Copy Editor

Checks language.

Questions:

- Are titles natural and specific?
- Is there repeated slogan-like structure?
- Is copy short enough?
- Are old brand names and placeholders removed?

## Optional Subagent Prompts

Use prompts like these when subagents are available:

```text
Use $deck-studio-loop at <skill path> to review this rendered deck preview and PPTX for product clarity, narrative, visual quality, and QA risks. Return only findings and concrete fixes.
PPTX: <path>
Preview/contact sheet: <path>
Audience: <audience>
```

```text
Use $deck-studio-loop at <skill path> to critique this deck as a skeptical customer or investor. Identify unclear claims, missing proof, and slides that feel generic.
PPTX: <path>
Preview/contact sheet: <path>
```

Do not leak intended answers to subagents. Pass artifacts and the evaluation job, not the diagnosis.

## Review Ledger

Track:

- Finding
- Role
- Severity: blocker / important / polish
- Slide
- Fix made or reason not changed
