---
name: local-image-generator
description: 唯一的静态图片生成技能。通过用户的本地图片生成工具（dev/image-generator）出图，模型和渠道由工具的 .env.local 统一配置。Use when the user asks to 作图 / 生成图片 / 画一张图 / 画图 / 出图 / generate an image / draw / create a picture, or needs website hero images, design assets, product visuals, social images, or other project assets. Still images only; for video use local-grok-video-generator-2-0.
---

# Local Image Generator

Skill version: `2026.10.23`

本技能是技能库里唯一的静态图片生成入口，已合并原 `local-image-generator-1-0` 和 `image-gen`。视频请用 `local-grok-video-generator-2-0`。

## 工具位置

```powershell
\\192.168.31.121\projects\服务器管理\腾讯云-首尔-Ubunut-150.109.233.152\dev\image-generator
```

映射盘可用时：

```powershell
Y:\服务器管理\腾讯云-首尔-Ubunut-150.109.233.152\dev\image-generator
```

自动化或沙箱 shell 中优先用 UNC 路径，映射盘可能不可用。

## 模型与渠道

- **默认模型由工具的 `.env.local` 决定**（`OPENAI_IMAGE_MODEL`），渠道由 `OPENAI_BASE_URL` 决定；主渠道失败（含 200 但没返回图片）时工具自动走 `OPENAI_FALLBACK_BASE_URL`。
- 当前配置（2026-10-23）：主渠道 `https://flaios.com/v1` + 全能 key `K_ALL`；备用渠道 `https://sg01-cli.api.flaios.com/v1` + 节点 key `K_NODE`（原备用 `n07.api.flaios.com` 已 TLS 握手失败，已替换）。
- Key 和端点的唯一来源：`E:\Dev-2\本地大模型调用\`（看 `README.md`；端点与 key 在 `docs/01-接入配置总表.md`，机器可读在 `config/providers.json`，按 `key_alias` 取）。原来的 `自用大模型apikey.txt` / `全能key使用说明.md` 已合并进该目录，不再存在。

### 可点名的模型（2026-10-23 实测均能出图）

| 模型 ID | 接口（工具自动选） | 定位 / 何时用 |
| --- | --- | --- |
| `gpt-image-2.5-flare` | images | **默认**。快速高质量：网页素材、配图、草稿、批量出图 |
| `gpt-image-2.5-sunburst` | images | 精细终稿、复杂构图、文字排版、局部编辑；更慢 |
| `gpt-image-2` | images | 上一代，2.5 不可用时后备 |
| `grok-imagine-image-2.0` | images | 用户点名 Grok 出图时用（另有 `grok-imagine-image`、`grok-imagine-image-quality`） |
| `nano-banana-2` | chat | 用户点名 nano banana / Gemini 风格时首选，主站可用 |
| `gemini-3.1-flash-image` | chat | 用户点名 Gemini 出图时用；**主站返回空，实际由 sg01 备用渠道出图** |

- **用户没有点名模型时，不传 `--model`**；要精细终稿传 `--model gpt-image-2.5-sunburst`；点名 Grok / Gemini / nano banana 时按上表传 `--model`。
- 接口选择：`--api auto`（默认）对 `gemini-*image`、`nano-banana*`、`banana*` 自动走 `/v1/chat/completions` 并从回复里取图，其余走 `/v1/images/generations`。网关明确拒绝在 images 接口调 Gemini 图片模型，不要强行 `--api images`。
- chat 接口的模型不支持 `--quality`、`--background`、精确 `--size`；尺寸只作为提示词提示，实际比例由模型决定，向用户说明。
- 官方**没有**裸的 `gpt-image-2.5`（网关列出了，但不要用），2.5 只用带 `-flare` / `-sunburst` 后缀的 ID。
- **GPT 画质一律用 `high`**（`.env.local` 默认）。不要降到 `low` / `medium`，sunburst 低画质会出明显马赛克。2.5 另支持 `xhigh`、`max`，仅在用户明确要求时使用；`--size` 支持推荐尺寸或自定义 `宽x高`（边长为 16 的倍数，比例 1:3 到 3:1，单边不超过 3840）。
- 不确定某个模型是否可用，先查渠道的 `GET /v1/models`，不要猜测或编造模型 ID。`/v1/models` 列出只代表登记了，不代表能出图。返回 `This token has no access to model ...` 表示当前 key 没开通该模型，不要自行降级后假装成功；如果换了模型出图，必须向用户写明。

## 工作流

1. 把当前 shell 工作目录当作目标项目，除非用户指定了其他项目路径。
2. 在工具目录用 `node` 运行（UNC 路径下 `npm` 会回落到 `C:\Windows`，只在本地盘路径下用 `npm run image -- ...`）：

```powershell
Set-Location '\\192.168.31.121\projects\服务器管理\腾讯云-首尔-Ubunut-150.109.233.152\dev\image-generator'
node scripts\generate-image.mjs --size 1536x1024 --quality high --output output\hero.png "prompt"
```

Git Bash（如 Claude Code on Windows）下：

```bash
cd "/y/服务器管理/腾讯云-首尔-Ubunut-150.109.233.152/dev/image-generator"
node scripts/generate-image.mjs --size 1536x1024 --quality high --output output/hero.png "prompt"
```

3. 工具会成对保存产物，保持这个结构：

```text
output/<name>.<format>
prompts/<name>.txt
```

4. 用户要求放到项目目录时，创建父目录并复制过去：

```powershell
New-Item -ItemType Directory -Force -Path .\public\images | Out-Null
Copy-Item -Force -Path "<工具目录>\output\hero.png" -Destination .\public\images\hero.png
```

5. 用 `Get-Item` 验证图片、提示词文件和复制目标都存在。
6. 向用户汇报：保存路径、最终提示词（尤其是补全过的）、模型（未传 `--model` 时写明"`.env.local` 默认模型"）、尺寸；输出里出现 `succeeded with fallback provider` 时写明走了备用渠道。

## 尺寸

`--size` 是比例提示，实际像素由模型决定。

| 用途 | `--size` |
| --- | --- |
| 网页 hero / 横幅 / 默认 | `1536x1024` |
| 方图 / 头像 / 社交配图 | `1024x1024` |
| 手机壁纸 / 竖版海报 | `1024x1536` |

其他参数：`--quality`（固定 `high`，见上文）、`--background`（auto / transparent / opaque）、`--format`（png / jpeg / webp）、`--api`（auto / images / chat）。

## 提示词

- 用户提示词清楚具体时，原样使用。
- 模糊时（如"画只猫"）自行补全风格、构图、光线、氛围、细节，用英文写最终提示词，并把补全后的提示词告诉用户。不必每张都确认，只有需求矛盾或确实含糊时才追问。
- 网页 hero / 背景素材：写明给标题留出的负空间；除非用户要求，加上 "no text, no logos, no UI labels"。
- 保留用户的核心想法，再补充风格、光线、构图和可用性约束。

## 失败处理

- 请求视频或 `grok-imagine-video`：改用 `local-grok-video-generator-2-0`。
- 模型不可用 / 不支持 `/v1/images/generations`：报告原始错误信息，检查 `.env.local` 的 `OPENAI_IMAGE_MODEL`，并用 `GET /v1/models` 确认渠道实际提供的模型；不要擅自换模型反复重试。
- `200 but no image`（chat 接口模型）：该渠道对此模型只回文字不出图；主备都这样时报告给用户，换 `nano-banana-2` 或 GPT 模型前先问。
- 提示模型价格未配置：告诉用户在后台配置模型价格或开启自用模式。
- `OPENAI_API_KEY` 为空：告诉用户在工具的 `.env.local` 里填写。
- 超时：告诉用户模型较慢或服务无响应，询问是否重试。

## 禁止

- 不打印、不回显、不提交任何 API key；不读出 `.env.local` 的 key 值。
- 不为测试反复真实出图，会消耗额度。
- 不提交生成的图片，除非用户要求。
