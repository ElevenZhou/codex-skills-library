# Staged Development Protocol

Use this reference for projects divided into Spike, Prototype/Demo, MVP, Pilot/Beta, Production, migration waves, rollout phases, or other gated stages.

## Core rule

Treat each stage as a separate Auto Loop contract with explicit inherited evidence. A later stage may reuse earlier artifacts, but it must not assume an earlier stage passed unless the required evidence exists and is readable.

## Stage input package

Before starting a stage, identify:

- **Stage name and responsibility:** what new risk this stage is allowed to take.
- **Objective:** the observable outcome for this stage only.
- **Entry gate:** evidence required from previous stages.
- **Inherited artifacts:** exact files, schemas, APIs, fixtures, decisions, and known defects.
- **User-only prerequisites:** credentials, accounts, approvals, paid services, legal choices, or production access that the agent cannot synthesize.
- **Discoverable prerequisites:** repository state, tools, dependencies, local files, and documentation the agent should inspect itself.
- **Assumptions:** defaults that may be filled without changing business intent.
- **Authorized side effects:** local writes, test-account writes, production writes, deployments, messages, purchases, and deletions.
- **Deliverables:** exact paths, commands, services, migrations, reports, and evidence.
- **Non-goals:** capabilities explicitly deferred.
- **Acceptance checks:** tests and observable outcomes required to exit the stage.
- **Failure/rollback boundary:** what to stop, revert, disable, or preserve when verification fails.
- **Exit evidence:** logs, screenshots, IDs, test output, reports, and sign-offs.
- **Handoff package:** what the next stage receives and unresolved risks it must inherit.

## Entry-gate decision

Classify stage readiness before implementation:

- `READY`: all blocking inputs and prior evidence exist.
- `READY_WITH_ASSUMPTIONS`: only non-critical preferences are missing; record defaults and proceed.
- `BLOCKED_USER_INPUT`: credential, account, approval, purchase, or irreversible authority is missing.
- `BLOCKED_PREVIOUS_STAGE`: required earlier-stage evidence is absent or failed.
- `RESEARCH_ONLY`: implementation is blocked, but useful local research, mocks, schemas, or test harnesses can still be produced.

Never report a blocked external integration as implemented. Produce mockable work separately and label it.

## Stage semantics

### Spike

Reduce uncertainty. Prefer disposable experiments and primary evidence. Do not generalize a successful request into production readiness.

Required exit evidence usually includes real capability results, permissions, error behavior, IDs, timings, limitations, and a Go/No-Go decision.

### Demo / prototype

Prove an end-to-end user or technical flow. Allow shortcuts only when they are explicit and cannot be mistaken for production controls.

Required exit evidence includes a repeatable demo command or flow, known limitations, and proof that inputs map to outputs correctly.

### MVP

Deliver the smallest version safe enough for intended real users. Prioritize state, validation, authorization, idempotency, recovery, logs, and understandable errors over broad UI or feature count.

### Pilot / beta

Run the MVP under restricted real conditions. Fix scope, volume, users, duration, metrics, incident handling, and human verification before starting.

### Production

Require durable credentials, deployment, monitoring, backup, recovery, runbooks, security checks, operational ownership, and proven rollback/kill controls. Production means supportable operation, not only deployed code.

## Side-effect matrix

Record authorization separately for:

| Side effect | Examples |
|---|---|
| Local | code, tests, schemas, fixtures, databases |
| Test external | sandbox API writes, test account content, staging deploys |
| Production external | public publishing, real account changes, customer data writes |
| Destructive | delete, revoke, overwrite, rollback data |
| Financial/legal | purchases, paid infrastructure, contracts, regulated actions |

Authorization for one category does not imply another. A request to build a publisher does not automatically authorize a live production publish during development.

## Stage execution loop

1. Read the master roadmap and current stage input package.
2. Validate the entry gate and inherited artifacts.
3. Separate user-only blockers from discoverable work.
4. Freeze the stage scope and acceptance checklist.
5. Implement the smallest critical path first.
6. Test normal, failure, restart, and unauthorized paths.
7. Collect exit evidence.
8. Run role review and improvement.
9. Mark the stage `PASSED`, `FAILED`, or `PARTIAL`; never infer passage from elapsed effort.
10. Produce the next-stage handoff with changed assumptions and unresolved risks.

## Handoff format

```text
Stage:
Result: PASSED | FAILED | PARTIAL
Delivered artifacts:
Commands/tests run:
External evidence:
Decisions locked:
Known defects:
Deferred work:
Security/operational risks:
Next-stage entry evidence satisfied:
User-only inputs still required:
Recommended next action:
```

## Continuation safety

- Re-read actual artifacts when a later Auto Loop run starts; do not rely only on conversation summaries.
- Preserve failed experiments and remote IDs needed for reconciliation, while keeping secrets out of artifacts.
- Do not advance a stage merely because code exists; require the stage-specific evidence.
- If a user orders forced execution, auto-fill preferences but still stop at missing credentials, production authorization, destructive actions, purchases, or material legal/security boundaries.
