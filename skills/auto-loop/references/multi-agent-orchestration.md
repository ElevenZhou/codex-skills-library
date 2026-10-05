# Multi-Agent Orchestration

Use this when a task is broad enough to benefit from parallel or independent review.

## Rule

Use actual subagents only when the current tool policy allows it and the user's request authorizes autonomous or multi-agent work. Otherwise run the same roles internally.

## Agent Roles

The roster is elastic. Start from the kernel, then scale the count and derive domain roles from the task. Do not run all seven kernel roles on a task that needs three, and do not stop at seven when the artifact has more independent failure modes than that.

### Kernel roles

Always present in some form, even if one agent (or you) wears several hats:

- **Planner:** creates goal contract, task graph, acceptance checks, risk register.
- **Builder:** implements files, deck, document, code, data pipeline, or prototype.
- **Verifier:** runs tests, renders, screenshots, backtests, validations, source checks.

### Elastic roles

Add only when the task actually contains that work:

- **Researcher:** gathers local context, web sources, examples, and constraints. Add when facts are current, contested, or external.
- **Architect:** designs system, narrative, data model, workflow, or visual system. Add when a structural decision precedes implementation.
- **Critic:** evaluates from audience, customer, investor, domain, security, financial, or visual perspective. Add when the work is strategic, high-stakes, or taste-dependent.
- **Integrator:** merges results, resolves contradictions, applies fixes, prepares handoff. Add whenever three or more lanes run in parallel.

### Sizing the roster

Scale by stakes and failure-mode count, not by task size alone:

| Situation | Roster |
| --- | --- |
| Small, single-file, reversible | Kernel collapsed into one pass; no separate agents. |
| Normal feature, doc, or analysis | 3–5 roles: kernel + Researcher or Critic. |
| High-stakes, external-facing, or irreversible | 6–8 roles: full kernel + elastic + 2–3 derived domain roles. |
| Broad audit, migration, or multi-subsystem sweep | Scale Verifier/Critic horizontally — one per subsystem or dimension, plus an Integrator. |

### Deriving domain roles

For each task, ask: **what distinct ways can this deliverable be wrong?** Each independent failure mode earns a role, named for the expertise that catches it. A role that would duplicate another's findings is not worth spawning.

- Regulated or legal content → compliance reviewer, claims/citation checker.
- Money, pricing, or unit economics → financial reviewer, assumption auditor.
- Anything user-facing → accessibility reviewer, i18n/localization reviewer.
- Anything handling credentials, PII, or untrusted input → security reviewer, threat modeler.
- Performance-sensitive systems → load/latency reviewer, cost reviewer.
- Multi-market or cross-cultural output → local-market reviewer per market.
- Operational changes → rollback reviewer, on-call/runbook reviewer.

Prefer **perspective diversity over redundancy**: three reviewers with distinct lenses beat three reviewers asking the same question. When verifying a single contested claim, redundancy is correct — spawn independent skeptics and go with the majority.

### Rules

- Name every role for the failure mode it owns, not for a generic title.
- Every spawned role must have a distinct deliverable and a non-overlapping write scope.
- Drop a role rather than let it produce a rubber-stamp review.
- Record the chosen roster and the reason in the loop ledger, so the next iteration can adjust it.

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

Use the platform's subagent mechanism and send independent lanes together so they run concurrently.

- **Claude Code:** the Agent tool. Pick the type by role: `Explore` for Researcher lanes, `Plan` for Architect lanes, `general-purpose` for Builder/Verifier/Critic lanes. Use `isolation: "worktree"` only when parallel Builders would otherwise edit the same files.
- **Codex:** spawn subagents when the current policy allows; otherwise run the roles internally.

```text
Perform <role> for this task.
Goal: <objective>
Inputs: <paths/URLs>
Scope: <what to inspect or edit>
Skills to use: <registered skills from references/skill-registry.md, if any>
Deliverable: <specific output>
Constraints: do not modify files outside <scope>; do not revert others' work.
```

## Review Roles By Artifact

Starting points, not closed lists. Extend each with roles derived from the task's own failure modes:

- **PPT:** product manager, sales/customer, investor/executive, domain expert, visual director, copy editor.
- **PDF/doc:** subject expert, editor, citation checker, layout reviewer.
- **Research:** source auditor, skeptic, strategy synthesizer.
- **Website/app:** UX reviewer, frontend QA, backend/API reviewer, security reviewer.
- **Quant:** data auditor, strategy skeptic, risk reviewer, implementation verifier.
- **Ads/growth:** creative reviewer, targeting/audience auditor, spend & pacing reviewer, policy/compliance reviewer, landing-page conversion reviewer.
- **Migration/refactor:** call-site sweeper, behavior-parity verifier, rollback reviewer.
- **Agent/automation:** tool-contract reviewer, permission/blast-radius reviewer, failure-path verifier.

If the artifact is not listed, build the roster from the derivation questions above rather than forcing it into the nearest row.

## Integration Checklist

- Resolve contradictions between agents.
- Prefer source-backed evidence over stylistic preference.
- Re-run QA after integrating fixes.
- Close or ignore stale agent outputs that no longer match the current artifact.
