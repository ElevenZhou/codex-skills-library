---
name: local-image-generator
description: 唯一的静态图片生成技能。通过用户的本地图片生成工具（dev/image-generator）出图，模型和渠道由工具的 .env.local 统一配置。Use when the user asks to 作图 / 生成图片 / 画一张图 / 画图 / 出图 / generate an image / draw / create a picture, or needs website hero images, design assets, product visuals, social images, or other project assets. Still images only; for video use local-grok-video-generator-2-0.
---

# Local Image Generator

Skill version: `2026.10.05`

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

- **默认模型由工具的 `.env.local` 决定**（`OPENAI_IMAGE_MODEL`），渠道由 `OPENAI_BASE_URL` 决定；主渠道失败时工具会自动走 `OPENAI_FALLBACK_BASE_URL`。
- 主力模型是 GPT Image 2.5。官方**没有**裸的 `gpt-image-2.5`，只有两个带后缀的模型，ID 必须完全一致：

| 模型 ID | 定位 | 何时用 |
| --- | --- | --- |
| `gpt-image-2.5-flare` | 快速、高质量日常出图（约快 50%） | 默认：网页素材、配图、草稿、批量出图 |
| `gpt-image-2.5-sunburst` | 精细创作与编辑精度，生成更慢 | 用户要求精细/高质量终稿、复杂构图、文字排版、局部编辑 |
| `gpt-image-2` | 上一代 | 2.5 渠道不可用时的后备 |

- `.env.local` 的 `OPENAI_IMAGE_MODEL` 应设为 `gpt-image-2.5-flare`。**用户没有点名模型时，不传 `--model`**；用户要精细/高质量终稿时传 `--model gpt-image-2.5-sunburst`。
- 2.5 的 `--quality` 额外支持 `xhigh`、`max`（旧模型最高 `high`）；`--size` 支持推荐尺寸或自定义 `宽x高`（边长为 16 的倍数，比例 1:3 到 3:1，单边不超过 3840）。
- 不确定某个模型是否可用，先查渠道的 `GET /v1/models`，不要猜测或编造模型 ID。返回 `This token has no access to model ...` 表示当前 key 没开通该模型，需要用户提供有权限的 key / 渠道，不要自行降级后假装成功；如果改用 `gpt-image-2` 出图，必须向用户写明。
- 不要用 `/chat/completions` 调图片模型；工具走的是 `/v1/images/generations`。

## 工作流

1. 把当前 shell 工作目录当作目标项目，除非用户指定了其他项目路径。
2. 在工具目录用 `node` 运行（UNC 路径下 `npm` 会回落到 `C:\Windows`，只在本地盘路径下用 `npm run image -- ...`）：

```powershell
Set-Location '\\192.168.31.121\projects\服务器管理\腾讯云-首尔-Ubunut-150.109.233.152\dev\image-generator'
node scripts\generate-image.mjs --size 1536x1024 --quality high --output output\hero.png "prompt"
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
6. 向用户汇报：保存路径、最终提示词（尤其是补全过的）、模型（未传 `--model` 时写明"`.env.local` 默认模型"）和尺寸。

## 尺寸

`--size` 是比例提示，实际像素由模型决定。

| 用途 | `--size` |
| --- | --- |
| 网页 hero / 横幅 / 默认 | `1536x1024` |
| 方图 / 头像 / 社交配图 | `1024x1024` |
| 手机壁纸 / 竖版海报 | `1024x1536` |

其他参数：`--quality`（auto / medium / high）、`--background`（auto / transparent / opaque）、`--format`（png / jpeg / webp）。

## 提示词

- 用户提示词清楚具体时，原样使用。
- 模糊时（如"画只猫"）自行补全风格、构图、光线、氛围、细节，用英文写最终提示词，并把补全后的提示词告诉用户。不必每张都确认，只有需求矛盾或确实含糊时才追问。
- 网页 hero / 背景素材：写明给标题留出的负空间；除非用户要求，加上 "no text, no logos, no UI labels"。
- 保留用户的核心想法，再补充风格、光线、构图和可用性约束。

## 失败处理

- 请求视频或 `grok-imagine-video`：改用 `local-grok-video-generator-2-0`。
- 模型不可用 / 不支持 `/v1/images/generations`：报告原始错误信息，检查 `.env.local` 的 `OPENAI_IMAGE_MODEL`，并用 `GET /v1/models` 确认渠道实际提供的模型；不要擅自换模型反复重试。
- 提示模型价格未配置：告诉用户在后台配置模型价格或开启自用模式。
- `OPENAI_API_KEY` 为空：告诉用户在工具的 `.env.local` 里填写。
- 超时：告诉用户模型较慢或服务无响应，询问是否重试。

## 禁止

- 不打印、不回显、不提交任何 API key；不读出 `.env.local` 的 key 值。
- 不为测试反复真实出图，会消耗额度。
- 不提交生成的图片，除非用户要求。
