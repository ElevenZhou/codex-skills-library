---
name: game-design-economy
description: 玩法、数值与经济设计：核心循环画布、成长曲线、难度曲线、资源产出与消耗（source/sink）、抽卡掉率与保底、激励广告经济（IAA）与内购价格阶梯（IAP）、留存钩子（每日/连续/元成长），并提供可运行的 Python 工具（经济模拟器、掉率计算器、难度曲线生成器）把数值表当代码来测。Use when the user says 数值, 数值策划, 经济系统, 玩法设计, 核心循环, 成长曲线, 难度曲线, 关卡难度, 掉率, 抽卡, 保底, 概率, 资源产出, 金币, 体力, 内购定价, 价格档位, 激励视频, 广告收益, 留存钩子, 签到, 平衡性, economy sim, drop rate, gacha, pity, progression curve, difficulty curve, game balance.
---

# 玩法 / 数值 / 经济设计（game-design-economy）

Skill version: `2026.11.12`

数值不是拍脑袋填表：把它当代码——写成配置、跑模拟、看分布、再改。工作方式沿用 `shared/huaqiang-method.md`：证据先于结论（模拟和真机数据，不是感觉）、最小可逆（一次只改一个参数并记录）。

## 何时用 / 何时不用

**用**
- 设计或调整核心循环、成长、难度、资源经济、抽卡、广告奖励、内购价格、留存钩子。
- 需要回答"玩家几天能到第 N 关/第 N 级""有多少人会卡住""抽卡期望多少抽/保底会不会太狠"。
- G1/G2 出数值骨架，G3 做平衡，G5 之后用真实数据回填校准。

**不用**
- 阶段管理、引擎选型、合规 → `game-dev-workflow`。
- 数值已定，要写 Godot 的配置加载代码 → `godot-game-dev`。
- 埋点设计与 A/B 指标阈值 → `game-playtest-qa`。
- 逆向得到的数值要核对原包 → 先用 `rebuild-device-evidence` 采证，再回来建模。

## 工作流程

1. **画核心循环**：填 `references/core-loop-canvas.md`。30 秒 / 5 分钟 / 每日三层循环，每层写清"玩家做什么 → 得到什么 → 为什么再来"。
2. **列资源表**：每种货币一行：来源（source）、去向（sink）、上限/过期、是否可购买。规则：**每个 source 必须有对应 sink，否则通胀**；每个 sink 必须有 source，否则卡关。
3. **定曲线骨架**：成长（成本曲线 `base * growth^level`，常见 growth 1.10–1.35，按品类校准）、难度（`difficulty_curve.py` 生成目标胜率与尝试次数）。详见 `references/progression-curves.md`。
4. **写配置**：数值一律放 JSON（`design/economy.json`），不写进代码；格式参照 `assets/economy_example.json`，Godot 侧加载见 `godot-game-dev`。
5. **跑模拟**：`economy_sim.py` 看货币曲线、里程碑到达天数、卡住比例；`drop_rate_calc.py` 看抽卡期望与尾部；每次改参数记录前后对比。
6. **定变现数值**：激励视频奖励占比、IAP 价格阶梯、首充；见 `references/monetization-economy.md`。
7. **定留存钩子**：每日、连续、元成长；见 `references/retention-hooks.md`。
8. **交接验证**：把"要用真人/埋点验证的假设"列清单交给 `game-playtest-qa`；上线后用实测回填模拟参数。

## 工具（`scripts/`，Python 3.9 兼容，仅标准库）

| 脚本 | 回答的问题 |
|---|---|
| `economy_sim.py --config assets/economy_example.json` | N 个玩家 D 天后货币曲线怎样？到各里程碑要几天？多少人卡住？ |
| `drop_rate_calc.py expected\|prob\|fifty\|copies\|simulate` | 期望几抽？N 抽内拿到的概率？50/50 加保底的尾部多长？ |
| `difficulty_curve.py --shape sawtooth --period 5` | 每关目标胜率、期望尝试次数、衍生参数表 |

全部有 `--help`、`--seed`。真实输出样例与读法见 `references/tool-usage.md`。

## 核心原则（带条件，非教条）

- **先保证"前 3 分钟 + 前 3 天"**：新手期产出慷慨、消耗温和、反馈密集。绝大多数流失发生在这里。
- **难度用锯齿，不用一条斜线**：每 4–6 关一个小峰，峰后给缓冲关；Boss/卡点前留出资源缓冲。
- **随机要有下限**：连续倒霉的保护（保底、软保底、递增概率）。实测 P99 尾部比平均值更能预测投诉。
- **货币分层**：软币（高产出、高消耗）、硬币（稀缺、可付费）、体力/时间门（节奏控制）。不要让同一个资源既当奖励又当付费点而没有汇率。
- **广告经济**：激励视频让玩家"主动换价值"，奖励价值应对应玩家 1–3 分钟的游玩产出，翻倍类奖励不要超过 2x，避免掏空自然产出的意义。
- **价格阶梯**：低档位用于试水（常见 $0.99 首充 / 6 元），中档位给性价比锚点，高档位给少数重度玩家；每档的"价值系数"应单调递增但递增幅度递减。
- **可调性**：所有数值可远程覆盖（或至少改配置文件重打包），把调整成本降到一次配置变更。
- 本 skill 中所有阈值与区间是**参考值，按品类校准**。

## 交付物

- `design/core-loop.md`（画布）、`design/economy.json`（可被模拟器直接读取）、`design/difficulty.csv`（关卡表）。
- 模拟报告：命令 + 种子 + 关键输出 + 结论（追加 `docs/metrics-log.md`）。
- 假设清单：哪些数值待真人/真机验证，对应的埋点与门槛。

## 门禁（进入 G3 前）

- 经济模拟 D1/D7/D30：主线里程碑中位到达日符合设计目标（偏差 ±30%）。
- `stalled%`：D7 ≤ 15%，D30 ≤ 25%（参考值，按品类校准）；超出则调整阶梯或产出。
- 抽卡（如有）：硬保底后最坏支出已被计算并写入文案/公示。
- 广告：每 DAU 预期广告展示数在设计目标内，且不触发"广告过多"差评（以软启动数据确认）。

## 相关 skill

`game-dev-workflow`（阶段与门禁）、`godot-game-dev`（配置加载与存档）、`game-playtest-qa`（埋点与实测回填）、`rebuild-dev-milestones`（M2 商业化、M3 留存的参数外置纪律）、`rebuild-device-evidence`（原包数值采证）。

## 变更记录

- 2026.11.12：首版。三个 stdlib 工具（economy_sim / drop_rate_calc / difficulty_curve），已实际运行验证。
