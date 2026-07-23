---
name: image-gen
description: "Generate images from text prompts via the flaios image API using the user's own API key (grok-imagine-image, grok-imagine-image-quality, gpt-image-2 models). Use when the user asks to 作图 / 生成图片 / 画一张图 / 画图 / generate an image / draw / create a picture / AI painting, AND especially when they want the flaios/grok models or to use their own key instead of the built-in OpenAI image tool. Calls /v1/images/generations, decodes base64, detects real format from magic bytes, saves to ~/Pictures/opencode-gen. Distinct from the built-in 'imagegen' skill which uses OpenAI's native tool."
---

# Image Generation (作图)

Generate images from a text prompt using the flaios image API. Runs a single
`curl` call, decodes the returned base64 image, and writes it to disk.

**Relationship to the built-in `imagegen` skill:** The built-in skill uses
OpenAI's native `image_gen` tool / OpenAI API. This skill uses the **flaios
proxy + the user's own key**, which exposes `grok-imagine-image` and
`gpt-image-2`. Use THIS skill when the user wants those models, or wants to use
their own key. Use the built-in `imagegen` for ordinary OpenAI-tool generation.

## Endpoint & credentials

- **Endpoint**: `POST https://flaios.com/v1/images/generations`
- **Auth header**: `Authorization: Bearer <KEY>`
- **API key location**: `/Users/Johnny/Projects/本地管理/大模型apikey/自用大模型apikey.txt`
  - The key sits inside a JSON object on its line: `{"_type":"newapi_channel_conn","key":"sk-...","url":"..."}`

### Reading the key SAFELY (security rules)

- **NEVER print, echo, log, or paste the key** into chat output, a shown file, or a commit. Reference it only through a shell variable.
- Read it once into `$KEY` and reuse:

```bash
KEY=$(python3 -c 'import re;print(re.search(r"\"key\"\s*:\s*\"([^\"]+)\"",open("/Users/Johnny/Projects/本地管理/大模型apikey/自用大模型apikey.txt").read()).group(1))')
```

- If extraction fails (file moved / no match), stop and tell the user the key file could not be read. Do not guess a key.

## Models

| Model (full id) | Aliases users may say | Format | Speed | Notes |
|---|---|---|---|---|
| `grok-imagine-image` | grok / grok-imagine / 默认 | JPEG | fast (~30-60s) | **default recommendation** |
| `grok-imagine-image-quality` | grok-quality / 高质量 / 高画质 | JPEG | medium | best quality grok |
| `gpt-image-2` | gpt-image / gpt-image-2 / gpt | PNG | slow (~60-120s) | GPT-style; also supports `/v1/images/edits` |

**Model selection rule:** Ask the user which model to use each time, UNLESS they
already named one (full id or any alias above). If they give no preference and
you must pick, suggest `grok-imagine-image`. Warn that `gpt-image-2` is slower
(long timeout) before choosing it.

## Sizes

`size` is an **aspect-ratio hint** — the model picks the actual pixel count.

| `size` value | aspect |
|---|---|
| `1024x1024` | square (default) |
| `1024x1536` | portrait (tall) |
| `1536x1024` | landscape (wide) |

Default to `1024x1024` unless the user asks for tall/wide or names a use case
(phone wallpaper → portrait, banner → landscape).

## Prompt handling (smart completion)

- If the user's prompt is **clear and specific**, use it as-is.
- If it is **vague** (e.g. "画只猫"), enrich it yourself before generating:
  add style, composition, lighting, mood, detail level. Write the final prompt
  in English (models respond best to English). Briefly tell the user the
  enriched prompt you used.
- Do NOT ask for confirmation on every image — only enrich and proceed. Only
  ask back if the request is genuinely ambiguous or contradictory.

## Output location

- Fixed folder: `~/Pictures/opencode-gen/` (create with `mkdir -p` if missing). Shared with the opencode version of this skill so all AI images land together.
- Filename: `<slug>-<YYYYMMDD-HHMMSS>.<ext>`
  - `<slug>`: 3-6 ASCII words derived from the prompt, lowercase, hyphen-separated, max ~40 chars. Drop accents/non-ascii.
  - `<ext>`: from magic bytes (see decode step) — `jpg` or `png`.

## Full generation procedure

### 1. Prep

```bash
mkdir -p ~/Pictures/opencode-gen
KEY=$(python3 -c 'import re;print(re.search(r"\"key\"\s*:\s*\"([^\"]+)\"",open("/Users/Johnny/Projects/本地管理/大模型apikey/自用大模型apikey.txt").read()).group(1))')
TS=$(date +%Y%m%d-%H%M%S)
```

### 2. Call the API (timeout MUST be 600s — gpt-image-2 can take 2+ minutes)

```bash
curl -s --max-time 600 -w "\nHTTP_STATUS:%{http_code}\n" \
  -o /tmp/imagegen_resp.json \
  -H "Authorization: Bearer $KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "grok-imagine-image",
    "prompt": "<FINAL ENGLISH PROMPT HERE — escape double quotes>",
    "n": 1,
    "size": "1024x1024"
  }' \
  https://flaios.com/v1/images/generations
```

### 3. Check status, then decode + save with correct extension

```bash
python3 - <<'PY'
import json, base64, os, datetime
resp = json.load(open("/tmp/imagegen_resp.json"))
if "data" not in resp or not resp["data"]:
    raise SystemExit("API returned no image. Full response: " + json.dumps(resp, ensure_ascii=False)[:500])
img = base64.b64decode(resp["data"][0]["b64_json"])
ext = "png" if img[:8] == b"\x89PNG\r\n\x1a\n" else ("jpg" if img[:3] == b"\xff\xd8\xff" else "bin")
out = os.path.expanduser(f"~/Pictures/opencode-gen/<slug>-{datetime.datetime.now():%Y%m%d-%H%M%S}.{ext}")
open(out, "wb").write(img)
print("SAVED:" + out)
print("BYTES:" + str(len(img)))
print("EXT:" + ext)
PY
```

Replace `<slug>` with the real slug. The magic-byte check decides jpg vs png —
**do not trust the model name for the extension**.

### 4. Report to the user

- The saved file path (the `SAVED:` line).
- The final prompt you used (especially if you enriched it).
- The model and size.
- Then clean up: `rm -f /tmp/imagegen_resp.json`

### 5. On failure

- Non-200 HTTP or no `data` field: show the `message`/error from the response body, then retry once with the same params. If it still fails, report the error verbatim and stop.
- curl timeout (status `000`): tell the user the model was too slow / service unresponsive; offer to retry with `grok-imagine-image` (faster).

## Do NOT

- Do not call `/chat/completions` for these models — image models are rejected there with `model X is only supported on /v1/images/generations and /v1/images/edits`.
- Do not print the API key.
- Do not commit the key file or generated images unless the user asks.
- Do not invent models — only the three ids in the table above exist.
