# Multi-Agent Orchestration

Use this when a task is broad enough to benefit from parallel or independent review.

## Rule

Use actual subagents only when the current tool policy allows it and the user's request authorizes autonomous or multi-agent work. Otherwise run the same roles internally.

## Agent Roles

- **Planner:** creates goal contract, task graph, acceptance checks, risk register.
- **Researcher:** gathers local context, web sources, examples, and constraints.
- **Architect:** designs system, narrative, data model, workflow, or visual system.
- **Builder:** implements files, deck, document, code, data pipeline, or prototype.
- **Verifier:** runs tests, renders, screenshots, backtests, validations, source checks.
- **Critic:** evaluates from audience, customer, investor, domain, security, financial, or visual perspective.
- **Integrator:** merges results, resolves contradictions, applies fixes, and prepares final handoff.

## Parallelization Patterns

Use parallel lanes only when outputs are independent:

- Researcher investigates market/current facts while Builder sets up workspace.
- Designer proposes visual direction while Writer builds narrative.
- Frontend and backend workers edit disjoint modules.
- Quant researcher validates data assumptions while Builder implements backtest harness.
- Verifier reviews rendered outputs while Builder works on next revision.

Avoid parallel lanes when:

- The task is small.
- Workers would edit the same files.
- The result depends on a single design decision.
- External state or credentials are missing.

## Subagent Prompt Pattern

Use concise prompts:

```text
Use $auto-loop at /Users/shenji/.codex/skills/auto-loop to perform <role> for this task.
Goal: <objective>
Inputs: <paths/URLs>
Scope: <what to inspect or edit>
Deliverable: <specific output>
Constraints: do not modify files outside <scope>; do not revert others' work.
```

## Review Roles By Artifact

- **PPT:** product manager, sales/customer, investor/executive, domain expert, visual director, copy editor.
- **PDF/doc:** subject expert, editor, citation checker, layout reviewer.
- **Research:** source auditor, skeptic, strategy synthesizer.
- **Website/app:** UX reviewer, frontend QA, backend/API reviewer, security reviewer.
- **Quant:** data auditor, strategy skeptic, risk reviewer, implementation verifier.

## Integration Checklist

- Resolve contradictions between agents.
- Prefer source-backed evidence over stylistic preference.
- Re-run QA after integrating fixes.
- Close or ignore stale agent outputs that no longer match the current artifact.
