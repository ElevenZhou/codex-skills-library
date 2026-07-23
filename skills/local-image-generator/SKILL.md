---
name: local-image-generator
description: Legacy alias for the user's local still-image generator. Use for image generation only, with gpt-image-2, grok-imagine-image, or grok-imagine-image-quality. For Grok video generation, use local-grok-video-generator-2-0 instead.
---

# Local Image Generator

Skill version: `2026.07.24`

This is the legacy still-image entrypoint. For the versioned image workflow, prefer `local-image-generator-1-0`. For Grok video, use `local-grok-video-generator-2-0`.

## Tool Location

Use this local tool project:

```powershell
\\192.168.31.121\projects\服务器管理\腾讯云-首尔-Ubunut-150.109.233.152\dev\image-generator
```

Mapped drive path, when available:

```powershell
Y:\服务器管理\腾讯云-首尔-Ubunut-150.109.233.152\dev\image-generator
```

It reads `.env.local`, where the default image model should be `gpt-image-2`.

## Workflow

1. Treat the current shell working directory as the active project unless the user names another project path.
2. Choose an image model:
   - `gpt-image-2`: default stable high-quality image model.
   - `grok-imagine-image`: fast drafts.
   - `grok-imagine-image-quality`: Grok quality images.
3. Generate the image from the local tool directory. Prefer `node` on UNC paths:

```powershell
Set-Location '\\192.168.31.121\projects\服务器管理\腾讯云-首尔-Ubunut-150.109.233.152\dev\image-generator'
node scripts\generate-image.mjs --model gpt-image-2 --size 1536x1024 --output output\hero.png "prompt"
```

4. Preserve the tool's paired outputs:

```text
output/<name>.<format>
prompts/<name>.txt
```

5. If the user requested a project destination, create its parent directory and copy the generated image there:

```powershell
New-Item -ItemType Directory -Force -Path .\public\images | Out-Null
Copy-Item -Force -Path "\\192.168.31.121\projects\服务器管理\腾讯云-首尔-Ubunut-150.109.233.152\dev\image-generator\output\hero.png" -Destination .\public\images\hero.png
```

Adjust paths for the actual active project and requested destination.

6. Verify the generated image, saved prompt, and copied destination with `Get-Item` or equivalent.

## Prompting

Write production-ready image prompts for the user's actual use case. For website hero/background assets:

- Specify layout needs such as negative space for headline text.
- Include "no text, no logos, no UI labels" unless the user explicitly wants text inside the image.
- Choose dimensions appropriate for the destination. Default to `1536x1024` for hero images.
- Keep the user's core idea intact, then add style, lighting, composition, and usability constraints.

## Failure Handling

- If the user asks for video or `grok-imagine-video`, use `local-grok-video-generator-2-0`.
- If the API says the model is unavailable, check `.env.local` and prefer `gpt-image-2` before trying other models.
- If the request fails because `OPENAI_API_KEY` is empty, tell the user the key must be filled in `.env.local`.
- Do not print or reveal API keys.
- Do not run repeated real image generations just for testing because it can consume quota.
