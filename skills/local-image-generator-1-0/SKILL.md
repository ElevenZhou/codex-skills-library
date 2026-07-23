---
name: local-image-generator-1-0
description: Use the user's local image-generation tool to create still images only. Use for local image generation, website hero images, design assets, product visuals, social images, and project assets using gpt-image-2, grok-imagine-image, or grok-imagine-image-quality. Do not use for video.
---

# Local Image Generator 1.0

Skill version: `2026.07.24`

## Scope

This skill generates still images only. For Grok video, use `local-grok-video-generator-2-0`.

Supported image models:

- `gpt-image-2`: default, stable high-quality general image generation.
- `grok-imagine-image`: fast draft and exploration.
- `grok-imagine-image-quality`: Grok high-quality final image generation.

## Tool Location

Primary local tool path:

```powershell
\\192.168.31.121\projects\服务器管理\腾讯云-首尔-Ubunut-150.109.233.152\dev\image-generator
```

Mapped drive path, when available:

```powershell
Y:\服务器管理\腾讯云-首尔-Ubunut-150.109.233.152\dev\image-generator
```

Prefer the UNC path when running from automation or sandboxed shells because mapped drives can be unavailable.

## Workflow

1. Treat the current shell working directory as the active project unless the user names another project path.
2. Choose a model:
   - Default: `gpt-image-2`.
   - Fast draft: `grok-imagine-image`.
   - Grok quality: `grok-imagine-image-quality`.
3. Generate from the local tool directory with `node` rather than `npm` when using the UNC path:

```powershell
Set-Location '\\192.168.31.121\projects\服务器管理\腾讯云-首尔-Ubunut-150.109.233.152\dev\image-generator'
node scripts\generate-image.mjs --model gpt-image-2 --size 1536x1024 --quality high --output output\hero.png "prompt"
```

Use `npm run image -- ...` only when the current directory is a local drive path; `npm` can fall back to `C:\Windows` on UNC paths.

4. Preserve paired outputs:

```text
output/<name>.<format>
prompts/<name>.txt
```

5. If the user requested a project destination, create the parent directory and copy the generated image there.
6. Verify the generated image, saved prompt, and copied destination with `Get-Item`.

## Prompting

Write production-ready prompts for the user's actual use case.

For website hero/background assets:

- Specify composition and negative space for headline text.
- Include "no text, no logos, no UI labels" unless the user explicitly wants text in the image.
- Choose dimensions appropriate for the destination. Default to `1536x1024` for hero images.
- Keep the user's core idea intact, then add style, lighting, composition, and usability constraints.

## Failure Handling

- If `grok-imagine-video` is requested with this skill, stop and use `local-grok-video-generator-2-0`.
- If the API says the model is unavailable or not supported on `/v1/images/generations`, choose one of the supported image models.
- If the API says a model price is not configured, tell the user to configure the model price or enable self-use mode in the backend.
- If `OPENAI_API_KEY` is empty, tell the user the key must be filled in the tool's `.env.local`.
- Never print or reveal API keys.
- Do not run repeated real generations just for testing because it can consume quota.
