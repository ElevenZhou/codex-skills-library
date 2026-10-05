# 使用调用案例

直接对 AI 说中文别名或任务描述就能调用技能，不需要记技能名。下面的案例在 Claude Code、Codex、WorkBuddy、Trae CN、OpenCode 中都适用。

## 一句话调用

| 你说 | 调用的技能 | 会做什么 |
| --- | --- | --- |
| 老大，帮我做个产品介绍 PPT | `auto-loop` → `deck-studio-loop` | 老大接单，拆目标后交给 PPT 技能制作，渲染检查后交付 |
| 小二，看看这个项目值不值得做 | `project-inception-analysis-cockpit` | 市场、竞品、开源、用户、财务调研，十角色评审，给出立项结论 |
| 三哥，继续推进项目 | `project-employee-agents` | 读取项目文件，判断阶段和阻塞点，安排岗位并产出管理成果 |
| 小五看下这份合同 | `xiaowu-contract-review` | 出问题对照表（P0/P1/P2），**等你同意后**才改合同 |
| 画一张网站首图 | `local-image-generator` | 用 gpt-image-2.5-flare 高画质出图，并保存图片和提示词 |

## 带上下文的写法（效果更好）

```text
小二，评估一下"面向小微企业的 AI 客服 SaaS"值不值得做。
目标市场：国内；预算：50 万以内；6 个月内要看到付费客户。
```

```text
三哥，项目目录在 E:\Projects\ai-cs，读取 project-brief.md，
告诉我现在卡在哪、本周该做什么、哪些事需要我拍板。
```

```text
小五看下这份合同：D:\合同\某某SaaS采购协议.docx。
我方是采购方，重点关注预付款能不能退、账号会不会被随意封。
```

```text
画一张网站首图：深色科技风，左侧留出标题位置，不要文字，
放到当前项目的 public/images/hero.png。
```

## 组合调用（让老大串起来）

```text
老大，全自动：
1. 让小二评估"跨境电商选品助手"值不值得做；
2. 结论是可以做的话，交给三哥出第一阶段计划；
3. 再做一份 10 页的立项汇报 PPT，配图用出图技能。
我去开会，做完给我结果。
```

老大会按 `skills/auto-loop/references/skill-registry.md` 依次调用：小二 → 三哥 → `deck-studio-loop` → `local-image-generator`，每一步验收后再交付。

```text
老大，帮我做个产品落地页：先出 3 个风格方案对比，
选定后实现，首图用 gpt-image-2.5-sunburst，最后用浏览器截图验收。
```

对应调用：`frontend-design-lab` → `advanced-frontend-design` → `local-image-generator` → `playwright`。

## 会停下来问你的情况

全自动模式也会在这些节点停下来，等你确认：

- 小五改合同正文之前。
- 启停广告投放、发布广告、部署上线之前。
- 需要花钱、删除数据、对外发送或做出承诺之前。
- 缺少只有你能提供的 key 或账号时。

## 预留别名

| 别名 | 规划用途 | 状态 |
| --- | --- | --- |
| 老四 | 复刻微创新综合工作组（skill 组合） | 预留，技能未建，暂不可调用 |
