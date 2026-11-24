# 子代理构建简报模板

每个方向一个子代理，三个同时启动（一条消息里三个 Agent 调用，`subagent_type: general-purpose`）。把【】换成本次内容。简报要自包含——子代理看不到对话。

---

You are building ONE design direction for a controlled frontend design comparison ("比稿"). Work only inside `【工作目录】/【x-name】/` (create `index.html`, `styles.css`, `app.js`, optional `bg.js`). Do not modify anything else, especially not `../shared/`.

## Read first (required)
1. `【工作目录】/CONTRACT.md` — shared product contract: required content blocks, required states, technical constraints, viewports, direction matrix. Everything there is mandatory.
2. `【工作目录】/shared/core.js` — the behaviour API. All data/behaviour comes from it; you only render.
3. Data shape: `head -c 3000 【工作目录】/shared/data.js` 【列出关键字段】.
4. `~/.claude/skills/advanced-frontend-design/SKILL.md` — follow its anti-template and quality rules, EXCEPT where the user's explicit brief overrides: 【例如：the user explicitly wants many saturated colours, a dreamy feel and motion】. Still: no generic glass-card grids, no default fonts, real states.

## Your direction: 【方向名】
- **Visual thesis**: 【一句话】
- **Silhouette**: 【页面骨架，含桌面与手机如何重新编排、详情以什么形式出现】
- **Type voice**: 【展示字 + 中文字体 + 等宽字，个性放在哪里】
- **Colour**: 【底色温度、身份色映射、文字对比度要求】
- **Material**: 【材质语言，明确禁止什么】
- **Motion grammar**: 【动效语法；尊重 reduced；document.hidden 时暂停】
- **Signature moment**: 【和产品相关的标志时刻】
- **Main risk to manage**: 【这个方向最可能伤害可用性的地方，以及要怎么守住】

## Engineering rules
- Load order: `../shared/data.js` → `../shared/core.js` → your scripts. Subscribe via the core's `on()`; list its change reasons 【init, tick, clock, select, filter, conn, finish, toast】.
- Escape all user text before inserting HTML. Keyed updates for live elements every tick; rebuild lists only on init/filter/finish; never steal focus from inputs.
- Must render every block and state in CONTRACT.md (`?state=…`, `?motion=reduced`, filter-empty with clear button, toast with aria-live, focus-visible, Esc closes detail, `/` focuses search, disabled actions where not applicable, honest labels for replayed/sample data).
- UI copy in 【中文】.
- **Output-size limit**: each response is capped at ~6000 tokens. Write files in pieces — first ≤200 lines, then append chunks (`cat >> file <<'EOF'`) — never a whole large file in one call.
- Syntax-check JS: `/System/Library/Frameworks/JavaScriptCore.framework/Versions/Current/Helpers/jsc file.js` (runtime DOM errors are expected there). The orchestrator verifies in a real browser at 1440×900 and 390×844 and will send fixes.

## Report back (≤200 words)
Files written, how each contract block/state is implemented, the signature moment, anything not done, known risks.

---

## 修改轮简报（SendMessage 给同一个子代理）

```
Refinement pass for direction 【X】, from real-browser checks (Chrome, 1440×900 and 390×844). 【已通过的项一句话】. Fix these, nothing else:
1. 【现象 + 位置 + 期望】
2. …
Keep files in 【x-name】 only, write in small chunks, jsc-check, then report in ≤80 words what changed.
```

经验：问题要写**看到的现象和位置**（"节拍是纯白块且压在动作文字下"），不要写成泛泛的"再优化一下"。
