# Standard Input And Completeness Check

Use this before starting an Auto Loop task. The user does not need to provide every field, but the agent must check what is missing and decide whether to ask, recommend defaults, or auto-fill.

## Recommended Standard Input

Users can paste this structure:

```text
Use $auto-loop 自动驾驶舱模式

目标：
- 我要完成什么：
- 为什么要做：

产物：
- 类型：PPT / PDF文档 / 调研报告 / 网站 / App功能 / 代码工程 / 量化交易 / 数据分析 / 其他
- 最终格式：pptx / pdf / docx / md / html / app / code / notebook / zip
- 保存位置：

背景资料：
- 项目目录或文件：
- 参考链接：
- 已有素材/品牌/模板：
- 必须使用的信息：

受众与使用场景：
- 谁会看/用：
- 用于内部汇报 / 客户演示 / 投资人 / 生产系统 / 个人研究 / 交易研究：

要求：
- 必须包含：
- 不要包含：
- 风格/语气/技术栈：
- 语言：
- 时间或预算限制：

自动化级别：
- 先检查输入并问我补充 / 缺什么你建议 / 强制执行自动补充
- 是否允许多agent：
- 是否允许联网搜索：
- 是否允许写入/改动文件：

质量标准：
- 怎么算完成：
- 需要哪些测试/渲染/截图/引用/回测：

风险边界：
- 敏感信息：
- 不能做的操作：
- 需要人工确认的点：
```

## Minimal Input

If the user provides only one sentence, extract at least:

- **Goal:** desired outcome.
- **Artifact type:** infer if not stated.
- **Autonomy level:** infer from words such as 全自动, 强制执行, 不用问.
- **Likely source location:** current workspace by default.
- **Quality bar:** infer from intended use.

## Completeness Levels

### Complete Enough

Proceed immediately when these are clear:

- Goal
- Artifact type
- Inputs/source location or permission to infer
- Output expectation
- Autonomy level
- No obvious safety/security blocker

### Needs Recommendation

If useful details are missing but not blocking, provide a short "recommended defaults" block and proceed if user asked for autonomy.

Example:

```text
我会按这些默认值执行：
- 受众：非技术业务负责人
- 输出：PPTX + 预览图
- 风格：专业、清晰、非模板化
- 资料来源：当前项目目录 + 必要时联网
```

### Needs User Answer

Ask only when missing information can materially change the outcome or risk:

- Which account/API/credential to use.
- Whether to spend money, deploy externally, delete/overwrite, trade, or publish.
- Which of multiple conflicting business goals is primary.
- Legal/financial/medical/security boundary is unclear.
- Required input files are absent and cannot be inferred.

Ask at most 3 concise questions.

## Forced Execution Defaults

When user says `强制执行`, `不用问`, `自动补充`, `你自己判断`, `我去睡觉`, or equivalent:

- Do not stop for preferences.
- Fill missing non-critical details with domain defaults.
- Record assumptions in the contract/ledger.
- Use the current workspace as source if no source is specified.
- Save outputs under a clear `outputs/` or task-specific directory if no path is specified.
- Use specialist skills automatically.
- Run QA gates and at least one improvement pass.
- Only stop for credentials, destructive actions, irreversible external changes, or material safety/legal/financial risk.

## Default Assumptions By Artifact

### PPT / Deck

- Audience: business decision-makers unless stated.
- Output: `.pptx` plus contact sheet/preview.
- Style: professional, distinctive, non-template.
- Include chapter rhythm for decks over 12 slides.
- QA: render slides, inspect contact sheet, overflow check.

### PDF / Document

- Audience: formal reader or decision-maker.
- Output: `.docx` or `.pdf` based on request; default to editable source plus final PDF if possible.
- QA: render pages, inspect layout, check headings/tables/citations.

### Research / Strategy

- Output: structured report with citations.
- Sources: browse current/primary sources when needed.
- QA: source recency, contradictions, assumptions separated from facts.

### Website / App / Code

- Source: current repo.
- Output: working code changes and validation summary.
- QA: install/build/test/lint/typecheck/smoke/browser screenshot where applicable.
- Do not overwrite unrelated user changes.

### Quant Trading

- Output: research/backtest artifact, not investment advice.
- QA: data provenance, no look-ahead bias, transaction costs/slippage, benchmark, drawdown, reproducibility.
- Do not place real trades unless explicitly instructed and separately confirmed.

## Input Check Response Format

When not forced, respond like:

```text
我可以开始。输入完整度：中/高。

已明确：
- ...

建议补充：
- ...

如果你说“强制执行”，我会按以下默认值补齐：
- ...
```

When forced, respond briefly and continue:

```text
已进入强制执行模式。我会自动补齐缺失项，并把假设写入任务台账。当前默认值：...
```
