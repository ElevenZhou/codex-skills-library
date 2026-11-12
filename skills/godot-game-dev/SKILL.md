---
name: godot-game-dev
description: Godot 4.x（GDScript）游戏开发实践：工程结构、Autoload 与事件总线、场景组合、数据驱动配置（JSON/Resource）、带版本的存档、对象池、移动端性能预算、触屏输入、竖屏 UI 缩放（stretch）、本地化、headless 测试与冒烟命令、常见坑（类型化 GDScript、信号、await、Tween 泄漏、ETC2/ASTC 导入标志），并附一个最小 starter 工程（未经编辑器验证，需按文档命令验证）。Use when the user says Godot, GDScript, godot 4, 做 Godot 游戏, 场景, 节点, 信号, 自动加载, autoload, 存档, 对象池, 竖屏适配, 触屏, headless 测试, 冒烟, 导出安卓, tscn, project.godot, extends SceneTree.
---

# Godot 4.x 游戏开发（godot-game-dev）

Skill version: `2026.11.12`

用 GDScript 做 2D 移动/休闲游戏的工程实践。沿用 `shared/huaqiang-method.md`：证据先于结论（跑过的命令才算验证）、最小可逆（小步改、每步冒烟）。

## 何时用 / 何时不用

**用**：新建或维护 Godot 4.x 项目；写 GDScript；设计单例/信号/存档/配置；排查性能、竖屏适配、headless 测试、导出相关问题。

**不用**
- 引擎选型、阶段门禁 → `game-dev-workflow`。
- 数值与经济本身 → `game-design-economy`（本 skill 只管加载与使用）。
- 验收清单、埋点规范、性能预算数值 → `game-playtest-qa`。
- Android 签名包 → `rebuild-build-release`（`references/android-export.md` 只给链接与五坑一句话版）。
- 按里程碑重写已有游戏的流程 → `rebuild-dev-milestones`（本 skill 提供其 M0 骨架的写法参考）。
- Unity / Cocos / H5 项目。

## 重要的诚实声明

`assets/godot-starter/` 在**没有 Godot 二进制**的机器上写成，**从未在编辑器或 headless 里运行**。使用前必须先跑 `references/validation-status.md` 里的三条命令；跑完把结果回写那份文档。已验证的只有来自项目 D（Godot 4.6.3）的冒烟命令、`extends SceneTree` 测试方式和导出五坑（见 `rebuild-workflow/references/engines/godot.md`）。

## 工作流程

1. **确认版本与目标**：`godot --version`（没有就先装与导出模板一致的版本）；目标平台、方向（竖屏 720×1280）、渲染器（GL Compatibility）。
2. **起工程**：复制 `assets/godot-starter/` 为新项目，改 `config/name`；先跑 starter 的三条命令（import、冒烟、单测），确认基线可用。
3. **搭骨架（M0）**：目录、`Events` 总线、`GameState`、空的主场景；冒烟 0 错误。详见 `references/structure-and-patterns.md`。
4. **数据驱动**：数值进 `cfg/*.json`，加载器带兜底与校验；见 `references/data-driven-config.md`。
5. **做核心玩法**：纯逻辑放 `core/`（可 headless 测），场景只做表现和输入；每个功能配一个 `tests_dev/test_*.gd`。
6. **存档**：带 `version` + `migrate()`；读取失败降级；暂停时存档。
7. **移动端适配与性能**：stretch、安全区、触摸目标、帧率与内存；见 `references/mobile-performance-ui.md`。
8. **每次改动后**跑冒烟：
   ```bash
   godot --headless --path . --quit-after 3 2>&1 | grep -E "SCRIPT ERROR|Parse Error|nonexistent"
   for t in tests_dev/test_*.gd; do godot --headless -s "$t" || echo "FAILED $t"; done
   ```
   一定 grep `nonexistent`：信号连接失败只报这个。
9. **导出与真机**：`references/android-export.md` → `rebuild-build-release` → `rebuild-device-evidence`；包体用 `game-playtest-qa/scripts/apk_budget_check.py` 检查。

## 关键约定

- 类型化 GDScript；文件 `snake_case.gd`；单例只放全局状态/信号/音频/埋点。
- 信号向上、调用向下；监听方在 `_ready()` 连一次。
- `project.godot` 必有 `textures/vram_compression/import_etc2_astc=true`。
- 参数外置，代码里的兜底值加注释指向 cfg 键。
- 不用脚本批量改代码，除非改完立刻冒烟。
- keystore、API Key 不进仓库（starter 的 `.gitignore` 已排除常见项）。
- 日期逻辑用 ordinal/儒略日；测试 setup 彻底重置单例与存档。

## 常见坑速查

| 现象 | 常见原因 |
|---|---|
| 信号不触发，日志只有 `nonexistent` | 信号名/方法名拼写错；连接目标已释放 |
| Android 导出失败但无错误文案 | 缺 ETC2/ASTC 导入标志；见 `rebuild-build-release` 五坑 |
| 动画越点越卡/叠加 | 旧 Tween 没 `kill()` |
| `await` 后报 "previously freed" | 等待期间节点被释放，恢复后先判有效性 |
| 测试里取不到 autoload | `-s` 脚本中用 `root.get_node_or_null("Name")` |
| 数值一改全崩 | 配置没校验、没兜底 |
| 竖屏长屏露底/错位 | stretch 选择与锚点；背景没铺满 |
| JSON 数字当下标报错 | JSON 数字是 float，需 `int()` |

## 交付物

- 可运行工程（冒烟 0 错误，测试全绿），`tests_dev/`、`cfg/`、`docs/`。
- 验证记录：命令、Godot 版本、输出、日期（回写 `references/validation-status.md` 或项目文档）。
- 导出的签名包与交付清单交给 `rebuild-build-release`。

## 参考资料

- `references/structure-and-patterns.md`：目录、Autoload/总线、场景组合、对象池、类型化、坑
- `references/data-driven-config.md`：JSON/Resource、版本化存档、本地化
- `references/mobile-performance-ui.md`：渲染器、性能、触屏、竖屏 UI、headless 测试
- `references/android-export.md`：导出链接与五坑
- `references/validation-status.md`：starter 的验证状态与待跑命令
- `assets/godot-starter/`：最小起步工程（未验证）

## 相关 skill

`game-dev-workflow`、`game-design-economy`、`game-playtest-qa`、`rebuild-dev-milestones`、`rebuild-build-release`、`rebuild-asset-recovery`（回导资源接入）、`rebuild-device-evidence`、`local-image-generator`（出图）。

## 变更记录

- 2026.11.12：首版。starter 工程与文档在无 Godot 二进制的环境中编写，**未运行验证**，状态见 `references/validation-status.md`。
