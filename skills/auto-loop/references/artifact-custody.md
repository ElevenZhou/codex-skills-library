# Artifact Custody And Reconciliation

Use this reference whenever the task produces files, generated media, screenshots, exports, or several linked documents.

## Durable Delivery Rule

A preview is not a deliverable. A tool response, chat attachment, temporary file, session payload, browser download, or tool-owned cache is not a final project asset until it is saved under a user-owned or project-owned path.

Do not report a path until it exists and the artifact opens, renders, or passes an appropriate file check.

## Artifact Manifest

For substantial work, keep a lightweight manifest under `artifacts/` or `qa/`:

```text
Artifact:
Purpose:
Final path:
Source/tool:
Prompt/specification:
Consumed by:
Validation:
Checksum/version (optional):
Status: final / superseded / reference-only
```

Record every requested final file. For generated images, include the final prompt or a stable prompt-document path. For screenshots, identify the route and viewport. Mark exploratory outputs as reference-only so they are not confused with runtime assets.

## Save And Validate

1. Save or copy the selected output into the project.
2. Use stable descriptive names and avoid silent overwrites unless replacement was requested.
3. Open, render, or inspect the saved artifact.
4. Confirm dimensions, content, format, and intended role.
5. Link it from the relevant document or runtime only after validation.
6. Remove or label stale references rather than leaving conflicting versions unexplained.

If the preferred tool does not expose a normal path, use a supported local export or recovery mechanism. If durable saving still fails, report the limitation honestly; do not claim the preview was saved.

## Final Reconciliation Gate

Before delivery, compare:

- requested deliverables
- artifact manifest
- files on disk
- README/design/product documentation
- QA ledger and acceptance checks
- code, HTML, Markdown, or configuration references
- final screenshots or rendered previews

Fix broken links, missing files, stale statements, outdated screenshots, mismatched filenames, and claims that no longer reflect the artifact. Re-run the smallest relevant validation after reconciliation.

## Absorb Reusable Learnings

When the user asks to absorb or improve the workflow:

1. Identify the observed failure or friction from evidence.
2. State the general rule that would prevent it in other projects.
3. Update the smallest relevant skill, reference, checklist, or deterministic script.
4. Validate syntax and run a representative check.
5. Record what changed and why.

Do not encode a single user's aesthetic preference as a universal rule. Absorb process reliability, decision criteria, and reusable domain knowledge.
