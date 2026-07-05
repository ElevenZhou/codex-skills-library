---
name: post-wechat-moments
description: Create ready-to-post WeChat Moments text-and-image posts. Use when the user asks to发朋友圈, 发图文朋友圈, 写朋友圈文案, 配朋友圈图, or promote an idea, product, resource, service, project, event, case, recruitment,合作邀约, or personal update on WeChat Moments, especially when images should be generated or selected.
---

# Post WeChat Moments

## Goal

Turn a rough intent into a natural WeChat Moments post with an image plan and publish-ready assets. Optimize for "像真人发的朋友圈": clear, warm, lightly persuasive, and not too much like an ad.

## Workflow

1. Identify the post purpose:
   - **邀约合作**: attract partners, projects, clients, or resources.
   - **展示能力**: signal expertise, resources, cases, or progress.
   - **轻转化**: invite DMs, consultation, trial, signup, or purchase.
   - **记录分享**: personal reflection, milestone, behind-the-scenes.
2. Infer the likely audience and relationship temperature:
   - **熟人圈**: more casual, direct, personal.
   - **行业圈**: more precise, credible, understated.
   - **潜在客户**: value-first, avoid pressure.
3. Draft copy in Chinese unless the user requests otherwise.
4. Decide image count:
   - **1 image** for a clean announcement, quote card, or strong hero visual.
   - **3 images** for a story arc: hook -> value/proof -> call to action. Default to 3 for business collaboration posts.
   - **6 or 9 images** only when there is real material: cases, screenshots, process, events, or product details.
5. Create or specify images:
   - If the user asks to generate images, use the available local image generation workflow/tooling when present.
   - Prefer square `1024x1024` or `1080x1080` for WeChat Moments.
   - For generated visuals, avoid random English text, fake logos, unreadable UI, and over-polished stock-photo vibes.
   - If adding text to cards, keep each image to one core line plus a short support line.
6. Return:
   - Final post copy.
   - Recommended image order.
   - Absolute paths to generated images, if any.
   - Optional shorter/stronger alternate caption when useful.

## Copy Style

Use short lines and natural pauses. Keep the first line strong enough to stop scrolling.

Prefer:

```text
我出算力，你做项目。

如果你有场景、有客户、有产品想法，
但卡在模型、推理成本、并发和资源上，
可以来聊聊。
```

Avoid:

```text
重磅推出！顶级算力赋能千行百业，助力企业智能化转型升级！
```

## Common Structures

### Cooperation Invitation

```text
<一句话抛出合作关系>

<说明你能提供什么>
<说明对方适合带什么来>

<降低门槛的行动邀请>
```

### Capability Signal

```text
<最近在做什么>

<资源/能力/优势，少量具体化>
<适合解决什么问题>

<欢迎交流>
```

### Soft Sales

```text
<一个痛点或场景>

<你的解决方式>
<适合的人群>

<私信/评论/来聊>
```

## Image Direction

For business/AI/compute posts, choose a high-end but human visual language:

- **算力/模型**: data center, GPU cloud, neural light streams, graphite/navy/silver palette.
- **项目共创**: runway, bridge, workshop table, blueprint, launch path, warm accent color.
- **资源整合**: connected nodes, modular blocks, layered infrastructure, calm enterprise feel.

Prompt rules for generated images:

- Include `no text, no logos, no UI labels` for pure visuals.
- Include "WeChat Moments square social media visual" and the desired mood.
- Generate a clean base visual first, then add Chinese copy with local graphics tools when text must be accurate.

## Quality Checklist

Before finalizing, check:

- The opening line is specific and not generic.
- The post sounds like a person, not a press release.
- The ask is clear but not pushy.
- Image count matches the content depth.
- Generated images have no unwanted text/logos.
- File paths are absolute when showing local images in Codex desktop.
