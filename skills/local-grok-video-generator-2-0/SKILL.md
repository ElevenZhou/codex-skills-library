---
name: local-grok-video-generator-2-0
description: Generate Grok Imagine videos through the user's FlaioS Grok video API. Use when the user asks to make, test, poll, download, or save videos with grok-imagine-video. This skill is for video only; use local-image-generator for still images.
---

# Local Grok Video Generator 2.0

Skill version: `2026.07.24`

## Scope

This skill handles Grok video only.

Supported model:

- `grok-imagine-video`

Do not send `grok-imagine-video` to `/v1/images/generations` or `/v1/images/edits`; those are image endpoints.

## API Shape

Known working base URL:

```text
https://sg01-cli.api.flaios.com/
```

Required endpoint:

```text
POST /v1/videos
GET /v1/videos/{id}
```

The completed video URL is returned by `GET /v1/videos/{id}` at:

```text
video.url
```

Do not rely on these endpoints for this provider:

```text
GET /v1/videos/{id}/content
GET /v1/videos/{id}/result
```

They returned `404` in testing.

## Parameters

Use only these durations:

- `6`
- `10`

Use `seconds` as a string, for example `"6"`.

The API currently accepts these `size` values:

- `720x1280`: 720p vertical, maps to 9:16.
- `1280x720`: 720p widescreen, maps to 16:9.
- `1024x1792`: higher-quality vertical.
- `1792x1024`: higher-quality widescreen.

The provider did not honor `ratio`, `aspect_ratio`, or `aspectRatio` in testing; pass the final `size` explicitly.

The UI may show 2:3, 3:2, and 1:1 options, but this `/v1/videos` API did not accept square or 2:3/3:2 sizes during testing.

## Workflow

1. Ask for missing creative intent only if the prompt is too vague to produce a useful video.
2. Choose duration and size:
   - Default duration: `6`.
   - Default size: `1280x720` unless the user asks for vertical/social video.
   - Vertical social video: `720x1280`.
3. Use the bundled helper script from this skill:

```powershell
node C:\Users\AprilWu\.codex\skills\local-grok-video-generator-2-0\scripts\generate-grok-video.mjs --base-url https://sg01-cli.api.flaios.com/ --api-key $env:GROK_VIDEO_API_KEY --seconds 6 --size 1280x720 --output output\grok-video.mp4 "prompt"
```

Prefer environment variables for secrets:

```powershell
$env:GROK_VIDEO_BASE_URL='https://sg01-cli.api.flaios.com/'
$env:GROK_VIDEO_API_KEY='...'
node C:\Users\AprilWu\.codex\skills\local-grok-video-generator-2-0\scripts\generate-grok-video.mjs --seconds 6 --size 1280x720 --output output\grok-video.mp4 "prompt"
```

4. Save the resulting `.mp4`, a paired prompt `.txt`, and a metadata `.json`.
5. If the user requested a project destination, copy the generated `.mp4` into that project.

## Output Files

For `--output output\demo.mp4`, the helper saves:

```text
output/demo.mp4
output/demo.txt
output/demo.json
```

The JSON contains task id, model, status, progress, size, duration, source video URL, and timestamps.

## Failure Handling

- `401 Invalid API key`: the key is missing, inactive, or not valid for the selected base URL.
- `400 unsupported model on /v1/images/...`: the video model was sent to an image endpoint; use `/v1/videos`.
- `size must be one of ...`: map the user's requested ratio/resolution to one of the accepted `size` values.
- `status=failed` or `FAILURE`: report the provider response and do not claim a video was generated.
- Never print or reveal API keys.
- Avoid repeated generation tests because each request can consume quota.
