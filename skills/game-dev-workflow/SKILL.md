---
name: game-dev-workflow
description: 游戏开发总控：从立项到上线的阶段流程（G0 立项 → G1 一页纸 → G2 垂直切片 → G3 生产 → G4 内测真机 → G5 软启动验证 → G6 上线运营），每个阶段有明确的通过/不通过指标门禁，并给出引擎选型矩阵（Godot 4 / Unity / Cocos Creator / Phaser·Laya）、工程目录和到兄弟 skill 的交接点。适用于原创游戏、按 GDD 开发、或逆向分析之后的重写阶段。Use when the user says 游戏开发, 做游戏, 做个小游戏, 休闲游戏, 超休闲, 立项, 策划案, GDD, 一页纸, 核心循环, 垂直切片, 原型, 选引擎, 软启动, 买量测试, CPI, D1, D7, 留存, 变现, 上线, game dev, game design document, prototype, vertical slice, soft launch, engine choice, or asks "这个游戏该怎么做 / 做到哪一步能上线".
---

# 游戏开发总控（game-dev-workflow）

Skill version: `2026.11.12`

把"做一款游戏"拆成 7 个带门禁的阶段，每一步回答三个问题：**现在在哪一段、下一道门的通过指标是什么、没过怎么办**。
工作方式沿用 `shared/huaqiang-method.md`：CEO 视角（值不值继续投入、总账、止损线）+ 专家视角（玩法/技术/数据哪一层有问题）、证据先于结论、最小可逆。

## 何时用 / 何时不用

**用**
- 从零做一款原创休闲/超休闲/中度手游或 H5 游戏，需要排阶段、定门禁、选引擎。
- 已有 GDD 或点子，要判断"现在该做什么、什么时候可以停"。
- 逆向分析（`rebuild-recon` / `rebuild-product-design`）之后，进入重写阶段前需要确认引擎和整体阶段。

**不用**
- 只问某个数值/掉率/经济问题 → `game-design-economy`。
- 只问 Godot 代码/项目结构/GDScript 问题 → `godot-game-dev`。
- 只问测试、埋点、性能预算 → `game-playtest-qa`。
- 已明确走"按里程碑重写已有游戏"的路径 → 直接用 `rebuild-dev-milestones`（M0–M5），本 skill 只在它之前（选引擎）和之后（G4 以后的软启动/上线）介入。
- 网页/管理后台类前端 → `advanced-frontend-design`。

## 阶段总览

| 阶段 | 目标 | 典型周期* | 核心产物 | 门禁（通过标准见 `references/stage-gates.md`） |
|---|---|---|---|---|
| G0 立项/定位 | 想清楚做给谁、凭什么 | 1–3 天 | 定位卡（品类、目标用户、对标、预算、止损线） | 有 1–3 个有市场证据的对标；总预算与止损线写明 |
| G1 一页纸+核心循环 | 一页纸能讲清楚怎么玩 | 2–5 天 | `gdd-one-pager.md`、核心循环图 | 30 秒内能向陌生人讲清；循环里有明确的"再来一局"理由 |
| G2 垂直切片 | 先能玩，再好看 | 1–3 周 | 可玩原型（灰盒）+ 一段完整循环 | 5 个陌生人试玩，≥3 人无提示完成首局并自愿再玩一局 |
| G3 生产 | 做出全部内容与系统 | 4–12 周 | 内容完整的 Alpha | 内容/系统清单 100%；冒烟与回归全绿；性能预算达标 |
| G4 内测/真机 | 在真设备上稳定可玩 | 1–2 周 | 内测包 + 真机报告 | 设备矩阵通过；崩溃率/ANR 达标；埋点完整 |
| G5 软启动/买量验证 | 用真实数据验证商业模型 | 2–4 周 | 软启动数据报告 | CPI/D1/D7/ARPDAU 过门槛（品类参考值） |
| G6 上线与运营 | 正式发布并持续运营 | 持续 | 上线清单、运营日历、复盘 | 合规清单全绿；回滚/热修方案就绪 |

\* 周期是单人到 3 人小团队的参考值，按实际校准。

## 工作流程

1. **定位阶段**：先问用户现在处于 G0–G6 哪一段，没有就按 G0 开始。读已有 GDD/工程/数据，别重复提问能从仓库读出来的东西。
2. **复述问题（3–5 行）**：目标、已有证据、边界（预算/人力/平台/地区）、未知。
3. **选引擎**（G0/G1 之间，只做一次）：按 `references/engine-choice.md` 的矩阵选，写进定位卡并说明为什么不选另外几个。默认建议：
   - 单人/小团队、2D、手游为主、想要开源且 APK 小 → Godot 4（GL Compatibility）。
   - 要接大量商业 SDK、3D 或要中度以上长线 → Unity。
   - 主战场是微信/抖音小游戏或国内 H5 → Cocos Creator / Laya。
   - 纯网页分发、最快迭代 → Phaser。
4. **按阶段推进**：每个阶段先写"本阶段出口指标"，做完再对表；对不上不"差不多"，要么补做要么走决策（见下）。
5. **每道门做判定**：通过 / 有条件通过 / 不通过，格式：结论 + 指标实测值 vs 门槛 + 证据来源 + 遗留风险 + 下一步。
6. **回写**：阶段文档落到 `docs/`，指标落到 `docs/metrics-log.md`，待办落待优化清单（沿用 `rebuild-dev-milestones` 的"待优化清单是唯一登记处"纪律）。

### 决策规则（门没过时）

- **G2 没过**：玩法问题，不是美术问题。最多再迭代 2 轮核心循环；仍不过则换玩法或砍项目。**不要带着没过的切片进 G3**。
- **G5 CPI 过高但留存好**：先改素材/定位/商店页，再谈放弃；留存差则回 G2/G3 改循环，买量救不了。
- **任何阶段超预算 50%**：触发止损评审，CEO 视角重新算总账。

## 工程目录（引擎无关）

```
<game>/
  docs/              定位卡、gdd-one-pager.md、stage-gates 判定记录、metrics-log.md
  design/            数值表、配置草稿（见 game-design-economy）
  src|project/       引擎工程（Godot 见 godot-game-dev 的 starter）
  assets_src/        可编辑源美术/音频（版本管理）
  assets_imported/   引擎导入后的资源
  tests/ | tests_dev/ 自动化测试
  telemetry/         埋点规范 JSON（见 game-playtest-qa）
  release/           签名包与交付清单（keystore 不入仓库）
```

## 交接点

| 时机 | 交给 | 说明 |
|---|---|---|
| G1/G2 数值、掉率、经济、难度曲线 | `game-design-economy` | 用 `scripts/` 里的模拟器先算后做 |
| G2 起用 Godot 写代码 | `godot-game-dev` | 起步工程在 `assets/godot-starter/` |
| 每个阶段验收、G4 真机、G5 指标阈值、埋点 | `game-playtest-qa` | 含 `apk_budget_check.py`、`telemetry_lint.py` |
| 美术/图标/商店截图出图 | `local-image-generator` | 静态图；视频用 `local-grok-video-generator-2-0` |
| Android 签名包、导出 | `rebuild-build-release` | 含 Godot 4.x 导出五坑与发布人工门禁 G-PUBLISH |
| 按里程碑重写已有游戏 | `rebuild-dev-milestones` | M0–M5；本 skill 的 G3 可直接套用它的开发纪律 |
| 需要复用解包得到的素材 | `rebuild-asset-recovery` | 仅限自有或已授权来源 |
| H5 游戏的浏览器自动化测试 | `playwright` | 截图、点击流程、控制台错误 |
| 真机截图/日志/录屏 | `rebuild-device-evidence` | ADB 证据采集 |
| 全程无人值守推进 | `auto-loop` | 把本 skill 的门禁当循环退出条件 |
| 复刻对标做微创新 | `product-tech-quality` | 对标拆解与发布门禁 |

## 变现与合规

G3 之前必须确定变现模式（IAA/IAP/混合/买断）；G5 之前必须过合规清单。清单见 `references/monetization-compliance.md`。**那是检查清单，不是法律意见**，涉及版号、主体资质、未成年人、隐私时需律师或平台确认。

## 交付物

- `docs/定位卡.md`（G0）、`docs/gdd-one-pager.md`（G1，模板 `references/gdd-one-pager.md`）
- 每道门的判定记录（追加到 `docs/stage-gates-log.md`）
- 引擎选型结论与依据
- 当前阶段的"本阶段出口指标"和实测值对照表

## 不做的事

- 用"画面好看"代替"好玩"：G2 之前不投入正式美术。
- 用平均值掩盖分布：留存、时长都要看分位和分群，不只看均值。
- 用 5 个人的试玩下统计结论：G2 的试玩只回答"能不能玩懂"，不回答"能不能赚钱"。
- 未经人工确认自动对外发布（见 `rebuild-build-release` 的 G-PUBLISH）。
- 把行业参考值当硬标准：所有阈值是"参考值，按品类校准"。

## 相关 skill

`game-design-economy`、`godot-game-dev`、`game-playtest-qa`、`rebuild-dev-milestones`、`rebuild-build-release`、`rebuild-asset-recovery`、`rebuild-device-evidence`、`local-image-generator`、`playwright`、`auto-loop`、`product-tech-quality`。

## 变更记录

- 2026.11.12：首版。阶段 G0–G6、门禁、引擎选型、变现合规清单。
