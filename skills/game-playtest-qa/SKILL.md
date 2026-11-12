---
name: game-playtest-qa
description: 游戏试玩与质量：冒烟测试分级、各阶段/里程碑验收清单、设备矩阵与性能预算（帧率/内存/加载/包体）、崩溃与 ANR 分诊、埋点事件规范（核心漏斗、命名、属性）、5 人观察式试玩脚本、软启动指标阈值、回归清单；附 stdlib Python 工具 apk_budget_check.py（包体预算+最大文件）与 telemetry_lint.py（埋点规范校验）。Use when the user says 试玩, 玩测, 测试游戏, 冒烟测试, 验收, 真机测试, 兼容性, 设备矩阵, 性能预算, 掉帧, 卡顿, 包体, 崩溃, ANR, 埋点, 事件设计, 漏斗, 留存, D1, D7, 软启动, 回归测试, playtest, QA, smoke test, telemetry, crash, performance budget, soft launch metrics.
---

# 游戏试玩与质量（game-playtest-qa）

Skill version: `2026.11.12`

回答三件事：**能不能玩懂（试玩）、能不能稳定跑（真机/性能/崩溃）、数据能不能证明它在变好（埋点/软启动）**。沿用 `shared/huaqiang-method.md`：证据先于结论——"我觉得流畅"不算，要有设备型号、fps 曲线、日志、录屏；样本量不够就写"方向性"。

## 何时用 / 何时不用

**用**：任何阶段的验收（G2 试玩、G3 回归、G4 真机、G5 软启动判读）、设计埋点、查包体和性能、分诊崩溃/ANR。

**不用**
- 阶段划分与立项决策 → `game-dev-workflow`（本 skill 提供它引用的指标和工具）。
- 数值/经济平衡本身 → `game-design-economy`。
- Godot 代码结构与单测写法 → `godot-game-dev`（本 skill 定验收标准，那边写实现）。
- 非游戏的 Web 应用测试 → `playwright` / `product-tech-quality`。

## 工作流程

1. **定当前阶段与验收对象**（G2/G3/G4/G5），读上一份验收记录，避免重复测。
2. **选测试层级**（`references/smoke-and-acceptance.md`）：
   - S0 冒烟（每次提交，≤3 分钟）→ S1 功能回归（每个里程碑）→ S2 真机矩阵（G4）→ S3 浸泡/性能（发布前）。
3. **跑自动检查**
   - Godot 冒烟：`godot --headless --path . --quit-after 3 2>&1 | grep -E "SCRIPT ERROR|Parse Error|nonexistent"`（必须 grep `nonexistent`，见 `rebuild-dev-milestones`）。
   - 包体：`python3 scripts/apk_budget_check.py build/game.apk --budget-mb 80 --top 15`（0 通过，1 超预算，2 出错）。
   - 埋点：`python3 scripts/telemetry_lint.py telemetry/spec.json --strict`。
4. **真机取证**：用 `rebuild-device-evidence`（ADB 启动、截图、logcat、录屏）；H5 游戏用 `playwright`（截图、控制台错误、点击流程）。证据放 `evidence/playtest/<日期>-<设备>/`。
5. **观察式试玩**（G2 起）：按 `references/playtest-session-script.md` 做 5 人测试，记录而不引导。
6. **性能与崩溃**：按 `references/perf-budgets.md` 对预算，崩溃按其中的分诊表走。
7. **判定**：通过/有条件通过/不通过，格式见 `game-dev-workflow/references/stage-gates.md`；缺陷进待优化清单，P0/P1 未清零不放行。
8. **软启动判读**：`references/softlaunch-metrics.md`，先看样本量再看数字。

## 验收分级速查

| 级别 | 时机 | 内容 | 判定 |
|---|---|---|---|
| S0 冒烟 | 每次提交/构建 | 启动 → 主界面 → 进一局 → 结算 → 返回；无 SCRIPT ERROR | 全绿才继续 |
| S1 回归 | 每个里程碑 | 核心玩法、存档读写、商业化流程（可模拟）、埋点触发 | P0/P1 清零 |
| S2 真机矩阵 | G4 | 低/中/高端设备各 ≥1：安装、全流程、横竖屏/中断恢复 | 无崩溃，性能达标 |
| S3 浸泡 | 发布前 | 连续玩 30–60 分钟、后台切换、弱网、内存增长 | 无泄漏趋势，无 ANR |

## 缺陷分级

| 级别 | 定义 | 放行规则 |
|---|---|---|
| P0 | 崩溃、无法进入游戏、存档损坏、支付/奖励错发 | 不放行 |
| P1 | 核心流程阻断、严重卡顿、数值导致卡关 | 不放行（G5 前清零） |
| P2 | 非核心功能错误、明显视觉错位 | 记录，排期 |
| P3 | 打磨项 | 待优化清单 |

## 交付物

- 验收记录：版本/构建号、设备、命令、结果、证据路径、缺陷清单、判定。
- `telemetry/spec.json`（已通过 lint）。
- 性能与包体报告（含 `apk_budget_check.py` 输出）。
- 试玩记录表（每位玩家一行 + 汇总）。
- 软启动判读报告：样本量、指标 vs 门槛、结论、下一步。

## 不做的事

- 用开发机或模拟器的数据代替真机结论（模拟器只能辅助冒烟）。
- 在样本量很小时下统计结论（试玩 5 人只回答"能不能玩懂"）。
- 在试玩中提示/辅导玩家（会污染观察）。
- 采集个人身份信息；埋点不含手机号、邮箱、设备硬件标识明文（`telemetry_lint.py` 会拦截常见命名）。隐私合规见 `game-dev-workflow/references/monetization-compliance.md`（检查清单，非法律意见）。

## 参考资料

- `references/smoke-and-acceptance.md`：冒烟/里程碑验收/回归清单
- `references/perf-budgets.md`：设备矩阵、预算、崩溃/ANR 分诊
- `references/telemetry-spec.md`：埋点规范与核心漏斗
- `references/playtest-session-script.md`：观察式试玩脚本
- `references/softlaunch-metrics.md`：软启动指标与判读
- `assets/telemetry_example.json`：可通过 lint 的示例规范

## 相关 skill

`game-dev-workflow`、`game-design-economy`（用实测回填数值）、`godot-game-dev`、`rebuild-device-evidence`（ADB 截图/日志/录屏）、`playwright`（H5 游戏）、`rebuild-build-release`（签名包与安装冒烟）、`rebuild-dev-milestones`（M0–M5 出口标准）。

## 变更记录

- 2026.11.12：首版。`apk_budget_check.py` 与 `telemetry_lint.py` 已在 /tmp 构造的小 zip 与示例/坏规范上实际运行验证。
