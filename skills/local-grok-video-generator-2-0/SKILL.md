---
name: local-grok-video-generator-2-0
description: Generate Grok Imagine videos through the user's FlaioS Grok video API. Use when the user asks to make, test, poll, download, or save videos with grok-imagine-video or grok-imagine-video-1.5 (Grok 视频 / 生成视频). This skill is for video only; use local-image-generator for still images.
---

# Local Grok Video Generator 2.0

Skill version: `2026.10.23`

## Scope

This skill handles Grok video only.

Supported models (both verified 2026-10-23 on sg01, 6s 1280x720):

| Model | Cost (6s) | When |
| --- | --- | --- |
| `grok-imagine-video` | ~$0.30 | Default |
| `grok-imagine-video-1.5` | ~$0.48 | User asks for Grok video 1.5 / newer / higher quality |

sg01 also lists `grok-imagine-video-1.5-lite` and `-1.5-preview`; they are untested, so check with the user before relying on them. Pass the model with `--model` or `GROK_VIDEO_MODEL`.

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

As of 2026-10-23, `POST /v1/videos` answers in xAI-native shape: only `{ "request_id": "..." }`. The helper accepts `request_id`, `id`, or `task_id`. Poll with `GET /v1/videos/{request_id}`; status ends as `done`.

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

The video URL is on `vidgen.x.ai`, which is not reachable without the system proxy. Node `fetch` ignores `HTTPS_PROXY`, so the helper falls back to `curl` for the download; this is expected, not an error.

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
3. Use the bundled helper script from this skill (the same script ships in `~/.claude/skills/` and `~/.codex/skills/`):

```bash
node ~/.claude/skills/local-grok-video-generator-2-0/scripts/generate-grok-video.mjs --seconds 6 --size 1280x720 --output output/grok-video.mp4 "prompt"
node ~/.claude/skills/local-grok-video-generator-2-0/scripts/generate-grok-video.mjs --model grok-imagine-video-1.5 --seconds 6 --size 1280x720 --output output/grok-video.mp4 "prompt"
```

Key resolution, in order: `--api-key`, `GROK_VIDEO_API_KEY`, then `K_NODE` from `E:/Dev-2/本地大模型调用/config/providers.json` (override the path with `GROK_VIDEO_PROVIDERS_JSON`). Normally nothing needs to be set. If `K_NODE` fails with 401, the registry also has `K_SG01_ALT` for sg01; pass it via `GROK_VIDEO_API_KEY` without printing it.

If a run is interrupted after the task was created (download failed, poll timed out), resume it instead of paying for a new video:

```bash
node .../generate-grok-video.mjs --model <same model> --task <request_id> --output output/grok-video.mp4 "same prompt"
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

- `401 Invalid API key`: the key is missing, inactive, or not valid for the selected base URL; try `K_SG01_ALT`.
- `Video API returned no task id`: the response shape changed again; read the printed JSON and update the helper rather than resubmitting.
- Download `fetch failed` followed by a curl error: the proxy is down; resume later with `--task`.
- `400 unsupported model on /v1/images/...`: the video model was sent to an image endpoint; use `/v1/videos`.
- `size must be one of ...`: map the user's requested ratio/resolution to one of the accepted `size` values.
- `status=failed` or `FAILURE`: report the provider response and do not claim a video was generated.
- Never print or reveal API keys.
- Avoid repeated generation tests because each request can consume quota.
