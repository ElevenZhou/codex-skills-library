# 数据驱动配置与存档

## 为什么

数值、关卡、文案放进数据文件，代码只负责解释。收益：改数不改代码、`game-design-economy` 的模拟器可以读同一份 JSON、AB 开关好做。契约（埋点名、AB 键名）原样继承，见 `rebuild-dev-milestones`。

## JSON 配置

`cfg/economy.json`（与 `game-design-economy/assets/economy_example.json` 同构的部分可共用）：

```json
{ "version": 1, "ladder": {"base_cost": 150, "growth": 1.22}, "taps_per_level": 10 }
```

加载器（放 `core/config.gd`，纯逻辑可测）：

```gdscript
class_name Config
extends RefCounted

static func load_json(path: String) -> Dictionary:
	if not FileAccess.file_exists(path):
		push_error("Config: missing %s" % path)
		return {}
	var f := FileAccess.open(path, FileAccess.READ)
	var parsed: Variant = JSON.parse_string(f.get_as_text())
	if typeof(parsed) != TYPE_DICTIONARY:
		push_error("Config: %s is not a JSON object" % path)
		return {}
	return parsed

static func get_num(d: Dictionary, key: String, fallback: float) -> float:
	return float(d.get(key, fallback))   # fallback 只作兜底，并注释对应 cfg 键
```

要点：
- JSON 中的数字解析后是 `float`，用于下标/计数要 `int()`。
- 打包后 `res://` 只读；用户可写数据放 `user://`。
- 配置加载失败要降级（用兜底值 + 日志），不要崩溃。
- 启动时做一次配置校验（必填键、范围）并打印，放进冒烟。

## Resource（`.tres`）何时用

- 需要编辑器里可视化编辑、引用场景/贴图（如道具定义带图标）时用自定义 `Resource` + `@export`。
- 纯数值表、需要被外部工具（Python 模拟器、表格）读写时用 JSON。
- 两者可结合：JSON 表给数值，Resource 做表现层引用。

## 存档（版本化）

starter 的 `GameState` 已实现：`to_dict()` / `from_dict()` / `migrate()` / `save_game()` / `load_game()`。规则：

1. 存档里必须有 `version`；每次改结构 +1，并在 `migrate()` 里写旧版本升级，保留旧版本样例用于测试（`tests_dev/test_gamestate.gd` 的 v1 迁移用例）。
2. 读取失败（缺文件、JSON 损坏、字段缺失）一律降级为默认值，不崩溃。
3. 写入用"先写临时文件再重命名"防止中途被杀导致半个文件（高价值存档建议）：
   ```gdscript
   var tmp := path + ".tmp"
   # 写入 tmp ... 成功后：
   DirAccess.rename_absolute(ProjectSettings.globalize_path(tmp), ProjectSettings.globalize_path(path))
   ```
4. 在 `NOTIFICATION_APPLICATION_PAUSED` 和关键节点（结算、购买后）存档；不要每帧存。
5. 涉及付费/排行榜的数据不要只信本地存档，服务端校验。
6. 测试：往返（保存→重置→加载→相等）、旧版迁移、损坏文件。
7. 加密/防篡改按需，不要把"存档加密"当成反作弊。

## 本地化

- 用 Godot 的翻译：CSV（`key,en,zh_CN`）导入为 `.translation`，代码里 `tr("KEY")`，Label 的 text 填 key 即可自动翻译。
- 切换语言：`TranslationServer.set_locale("zh_CN")`，并持久化选择。
- 字体：中日韩需要含对应字形的字体；把字体作为 fallback 配置，注意包体增加；字体许可证要核对（`rebuild-asset-recovery` 的版权审查）。
- 文案长度：德语/俄语常比英文长 30–50%，UI 用容器自适应，测试最长语言。
- 数字、日期、复数用格式化函数，不要拼接字符串。
