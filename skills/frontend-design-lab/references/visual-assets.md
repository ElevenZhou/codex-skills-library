# Visual Asset Strategy

Use assets to reveal the product, place, object, data, or material. Do not use them as atmosphere-only decoration.

## Routing

Prefer, in order:

1. existing project assets and real product media
2. code-native CSS, canvas, or framework visuals for deterministic diagrams and simple maps
3. freely licensed source assets with verified terms
4. generated bitmaps when a direction materially needs unique cartography, texture, photography, or illustration

Use `imagegen` for built-in generation or `local-image-generator-1-0` when the user has requested the local project-bound workflow. Ask before using an API that may consume quota when generation was not explicitly requested.

## Generated Asset Contract

Keep all functional interface elements out of the image:

- no UI labels
- no buttons or fake panels
- no state text
- no data values
- no logos unless the user explicitly requests brand art

Implement text, controls, and state in HTML or native components.

## Prompt Shape

```text
Use case: stylized-concept or another accurate taxonomy
Asset type: exact role in the interface
Primary request: subject or material the interface needs
Scene/backdrop: relevant environment
Style/medium: visual treatment tied to the selected direction
Composition/framing: crop behavior and quiet overlay zones
Color palette: compatible with interface tokens
Constraints: no text, labels, fake UI, logos, or watermark
Avoid: unrelated aesthetic defaults and unusable contrast
```

## Project Delivery

For every project-bound generated asset:

1. Save the selected original in the project.
2. Save the exact final prompt beside it.
3. Inspect the bitmap before use.
4. Create an optimized WebP or AVIF when browser support and quality are appropriate.
5. Keep stable dimensions to prevent layout shift.
6. Verify the optimized request returns successfully in the browser.
7. Record source and optimized file sizes.

Do not leave a referenced image only in a tool cache or temporary directory.

## Comparison Fairness

If only one direction uses a generated asset, explain why that asset is intrinsic to its design thesis. Do not give one variant expensive subject matter while forcing another to use a placeholder.

When imagery is not central, use the same real asset across variants and vary crop, hierarchy, and integration rather than subject quality.
