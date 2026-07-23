---
name: deck-studio-loop
description: Premium autonomous presentation creation for business introductions, product decks, pitch decks, strategy decks, sales decks, board decks, roadshows, and richly designed PowerPoint/slide deliverables. Use when the user asks to make or improve PPT/PPTX/slides/decks/BP/商业计划书/公司介绍/产品介绍/路演材料, especially with requests for 图文并茂, 高级感, 不千篇一律, 多套方案, 自动循环优化, 自审, 多角色评审, or minimal user intervention.
---

# Deck Studio Loop

Skill version: `2026.07.24`

## Purpose

Create high-quality, non-generic decks through a studio workflow: clarify the communication job, build a narrative, design distinctive visual systems, produce real editable slides, render and inspect them, run role-based critique, revise, and deliver usable files.

Use the built-in `Presentations` skill for PPTX production and QA. Use `imagegen` for raster hero images, scene visuals, product mockups, or premium illustration assets. Use browser/HTML rendering for exact Chinese information graphics when text accuracy matters.

## Operating Mode

Default to autonomous execution when the user delegates judgment or asks for loop/全自动. Do not stop at outlines. Produce real deck files unless the user explicitly asks only for planning.

Pause only for missing private credentials, destructive actions, purchases, legal commitments, or a choice that would materially change the business intent. Otherwise make reasonable assumptions and record them in the working notes.

For broad or high-stakes decks, read these references:

- `references/deck-contract.md` for the goal contract and acceptance criteria.
- `references/narrative.md` for story architecture and slide planning.
- `references/visual-systems.md` for distinctive design systems and anti-template rules.
- `references/production-loop.md` for build, render, QA, and iteration.
- `references/multi-agent-review.md` for internal role review and optional subagent prompts.
- `references/slide-patterns.md` for reusable slide types.

Use `scripts/init_deck_workspace.py` to create a standard workspace for scratch files, assets, QA previews, and final outputs.

## Workflow

1. **Gather**
   - Read project docs, source files, prior decks, brand notes, images, data, and examples.
   - If external facts affect claims, browse and cite credible sources.
   - Separate source-backed facts, strategic assumptions, and copywriting choices.

2. **Contract**
   - Define audience, communication job, deliverables, constraints, visual directions, and acceptance checks.
   - Decide whether to create one polished deck, multiple visual alternatives, or a main deck plus reusable graphics.

3. **Narrative**
   - Build a cumulative storyline, not an agenda dump.
   - Give each slide one job and one audience-facing takeaway.
   - Add section rhythm with large-number chapter dividers for long decks.

4. **Visual System**
   - Choose a visual direction that fits the domain and audience.
   - Avoid generic blue-purple gradients, template-card sameness, and decorative filler.
   - Create reusable rules for palette, typography, chart style, page rhythm, image treatment, and section breaks.

5. **Production**
   - Build a real `.pptx` using the `Presentations` skill and `@oai/artifact-tool`.
   - Keep text, tables, charts, and diagrams editable whenever practical.
   - Use generated or searched raster visuals only where they materially improve comprehension or polish.
   - Use HTML/SVG rendered to PNG for exact Chinese infographics when image generation may corrupt text.

6. **QA**
   - Render slides to images, inspect a contact sheet, run overflow checks, and fix issues.
   - Check text density, hierarchy, alignment, contrast, chart meaning, image relevance, and brand consistency.
   - Verify old brand names, placeholders, internal notes, and unsupported claims are removed.

7. **Review Loop**
   - Run role-based self-review: product manager, customer/sales, investor/decision-maker, domain expert, visual director, and copy editor.
   - Revise at least once when the deck is client-facing or strategic.
   - Use subagents for independent review when available and worth the time; pass only the deck path/previews and the evaluation prompt.

8. **Deliver**
   - Provide final `.pptx` path, optional zipped assets, preview/contact sheet path, and a concise note about validation performed.
   - Recommend the strongest version when multiple versions exist.

## Quality Bar

Before final handoff, ensure:

- The deck opens as a PPTX and has the requested number/type of deliverables.
- Slides are rendered and visually inspected.
- No detected overflow remains.
- The story is clear to a non-expert but credible to a domain expert.
- The deck has visual variety and a coherent system, not random decoration.
- Every major claim is sourced, derived from provided materials, or clearly positioned as a proposal.
- The final answer is brief and names the artifacts.
