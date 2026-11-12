# 引擎选型

结论先行：**没有最好的引擎，只有对团队、品类和分发渠道最合适的。** 选型一次，写进定位卡，之后不要因为"看到别人用 X"中途换。换引擎的成本通常 ≥ 一个完整里程碑。

## 矩阵（参考值，按团队和品类校准）

| 维度 | Godot 4 | Unity | Cocos Creator | Phaser / Laya (H5) |
|---|---|---|---|---|
| 语言 | GDScript / C# | C# | TypeScript | JS/TS（Laya 也支持 AS/TS） |
| 许可 | MIT，无分成 | 商业条款与收入档位有变，上线前核对当前条款 | 引擎开源/免费，部分商业服务收费 | Phaser MIT；Laya 免费，核对条款 |
| 2D 手游 | 强，GL Compatibility 兼容性好 | 强，生态最全 | 强，国内小游戏生态好 | 中，取决于浏览器 |
| 3D | 够用，上限低于 Unity | 强 | 中 | 弱（Laya 有 3D） |
| Android 空包体积 | 约 20–30 MB 级（模板，视配置） | 约 20–40 MB 级（IL2CPP 视配置） | 小（原生）/ 极小（小游戏） | 浏览器内，首包 1–5 MB 级 |
| 迭代速度 | 快（轻量编辑器，headless 测试方便） | 中（编译/域重载） | 快 | 最快（刷新即看） |
| 广告/支付 SDK | 需插件（社区 Android 插件，需自己维护） | 最成熟（官方/聚合 SDK 齐全） | 国内 SDK 成熟 | 平台提供（微信/抖音）或 JS SDK |
| 热更新 | 可 PCK 替换，需自建 | Addressables 等成熟 | 内建热更新方案 | 天然 |
| AI/脚本自动化 | 文本场景/脚本，易于 Agent 读写和 diff | 序列化 YAML，较重 | 文本较友好 | 纯文本最佳 |
| 团队招聘 | 少 | 多 | 国内多 | 前端多 |

## 何时选哪个

**Godot 4**：单人或 ≤3 人、2D 休闲/超休闲/轻中度、预算紧、想完全掌控且希望对 AI 辅助开发友好（文本场景 `.tscn`、GDScript）。限制：商业 SDK（广告聚合、MMP）需要插件；主机/3D 重度项目不合适。本仓库有 `godot-game-dev` 和 `rebuild-build-release` 的完整 Android 路径。

**Unity**：要接大量商业 SDK（Max/AdMob 中介、Adjust/AppsFlyer、IAP）、3D、或预期有中度以上长线与大团队、已有 Unity 资产/人员。代价：版本与授权需跟进、体积和编译较重。

**Cocos Creator**：目标是微信/抖音小游戏或国内安卓渠道、轻度 2D、团队熟 TypeScript。小游戏包体限制严（主包限制以平台当前规定为准，核对后再定资源策略）。

**Phaser / Laya (H5)**：纯网页分发、广告联盟 H5 游戏、最快验证玩法（G2 原型阶段可用 H5 先验证再迁移）。测试可直接用 `playwright`。限制：性能和原生能力、变现 SDK 受平台约束。

## 决策表（品类 × 目标）

| 品类 / 目标 | 首选 | 备选 | 理由 |
|---|---|---|---|
| 超休闲（单指、IAA） | Unity 或 Godot | Phaser（先测） | 买量验证为主，SDK 成熟度 vs 轻量 |
| 休闲 / 益智 / 合成 / 消除 | Godot | Unity | 2D UI 为主，Godot 迭代快 |
| 放置 / 挂机 | Godot | Cocos | UI 与数值密集，数据驱动 |
| 微信/抖音小游戏 | Cocos Creator | Laya | 平台生态与体积限制 |
| 国内安卓中度 | Unity | Cocos | SDK 与渠道接入 |
| 海外中度 / 3D | Unity | — | 生态和人才 |
| 玩法验证原型（1 周） | Phaser / Godot | — | 最快出可玩版本 |
| 逆向分析后重写 | 与原引擎无关，优先 Godot | Unity | 避免携带原包代码；资源回导见 `rebuild-asset-recovery` |

## 评估清单（定引擎前过一遍）

1. 是否有人已经能用它交付过东西？没有则预留 2 周学习成本。
2. 目标变现 SDK 在该引擎有可用、仍在维护的集成吗？（查最近一年有更新）
3. 目标平台导出流程你跑通过吗？先做"空项目 → 签名 APK → 真机启动"的 1 天验证（`rebuild-build-release`）。
4. 包体空载多大？用 `game-playtest-qa/scripts/apk_budget_check.py` 测空项目导出包。
5. 许可条款和费用是否在上线日仍成立？记录核对日期。

## 迁移原则

原型阶段可用最快的引擎（H5/Godot），只要把**数值与配置放在引擎无关的 JSON**（见 `game-design-economy`），换引擎时损失的只是表现层。
