# Production Loop

## Tool Routing

- For PPTX: use the `Presentations` skill and `@oai/artifact-tool`.
- For raster visuals: use `imagegen`; if the user provides an OpenAI-compatible image API path, follow that skill's CLI fallback rules.
- For exact text-heavy graphics: create HTML/SVG and render with Playwright or a browser screenshot path.
- For spreadsheets/data charts: use native PPT charts or spreadsheet-derived charts when data is precise.

## Workspace Layout

Use a stable deck workspace:

```text
<workspace>/
├── tmp/
│   ├── assets/
│   ├── qa/
│   ├── notes/
│   └── build/
└── outputs/
```

`scripts/init_deck_workspace.py` creates this layout and a QA ledger.

## Build Loop

1. Draft contract and slide plan.
2. Generate or collect visual assets.
3. Build PPTX with editable text, shapes, tables, charts and embedded images.
4. Export slide PNGs and a contact sheet.
5. Run overflow/layout checks.
6. Inspect the contact sheet visually.
7. Revise the deck source.
8. Re-export and re-check.

## QA Checks

- Slide count and required sections match the task.
- No overflow or clipping warnings remain.
- Cover and section dividers are readable.
- Text fits and does not wrap awkwardly in buttons, labels, or diagrams.
- Tables have legible headers and not too many columns.
- Charts have a clear claim, not just data.
- Image assets are relevant, not generic filler.
- Brand names and product names are consistent.
- No old placeholders, TODOs, internal notes, or prompt text.
- Final files are saved in the project or requested output path.

## Revision Heuristic

Always revise when:

- The first deck reads like an outline instead of a presentation.
- Slides are visually repetitive.
- A diagram is hard to understand in 5 seconds.
- The audience cannot tell what action to take.
- A generated image looks attractive but does not explain the product or idea.

Stop when acceptance checks pass and further edits are mainly preference choices.
