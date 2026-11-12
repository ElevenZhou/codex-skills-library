# 工程结构与代码模式（Godot 4.x, GDScript）

> 本文是实践建议，API 细节以所用 4.x 版本的官方文档为准。starter 在 `assets/godot-starter/`，**未经编辑器验证**（见 `validation-status.md`）。

## 目录

```
project.godot
autoload/      全局单例：events.gd(信号总线)、game_state.gd(状态+存档)、audio.gd、analytics.gd
scenes/        场景及其同名脚本（main.tscn/main.gd；ui/、gameplay/ 子目录）
core/          纯逻辑（无节点依赖，易测）：规则、生成器、数值计算
cfg/           JSON/Resource 配置（数值、关卡、文案）
assets_imported/  资源（回导资源见 rebuild-asset-recovery）
tests_dev/     headless 测试（test_*.gd）
docs/ 
```

命名：文件 `snake_case.gd`，类 `PascalCase`，常量 `UPPER_SNAKE`，信号过去式或事件式（`score_changed`），私有成员前缀 `_`。

## Autoload 与事件总线

- 只放真正全局的东西：状态、信号总线、音频、埋点。不要把一切塞进单例。
- `Events`：只声明信号，无状态无逻辑。发送方 `Events.score_changed.emit(v)`，监听方 `Events.score_changed.connect(_on_score_changed)`。双方互不引用，场景可单独运行。
- `GameState`：纯数据 + 规则 + 存档，不依赖场景树，所以能被 `extends SceneTree` 的测试直接驱动。
- 监听方在 `_ready()` 连接；被释放节点自动断开。对长生命周期单例连接短生命周期节点的 Callable 时，避免用匿名 lambda 捕获 `self` 而不断开。
- 信号连接失败只在日志里报 `nonexistent`，headless 不当错误处理，所以冒烟命令必须 grep `nonexistent`。

## 场景组合

- 组合优于继承：小场景（`Enemy.tscn`、`HealthBar.tscn`）+ 在父场景中实例化；行为通过子节点组件（`HitBox`、`Mover`）拼装。
- "call down, signal up"：父调用子的方法，子通过信号通知父。
- 节点引用用 `@onready var x: Label = $Path/To/Label`；路径多处用到时用 Unique Name（`%Name`）。
- 一个场景一个职责；UI 与玩法分离，UI 只通过 `Events` / `GameState` 读写。

## 类型化 GDScript（推荐）

```gdscript
var speed: float = 200.0
var items: Array[String] = []
func damage(amount: int) -> void: ...
```
- 好处：编辑器补全、解析期报错、略快。类型错误会在解析期暴露，配合冒烟命令及早发现。
- 用 `:=` 推断时右值必须能确定类型；从 `Variant`（如 `JSON.parse_string`、`Dictionary.get`）取值要显式写类型或转换（`int(...)`）。
- 引用 autoload 的全局名称在普通游戏脚本里没问题；在 `-s` 运行的 `SceneTree` 脚本里它们在脚本解析时尚未注册，需用 `root.get_node_or_null("GameState")`（starter 测试就这样写）。

## 对象池

适用：子弹、飘字、特效、消除块——每秒大量创建/销毁。

```gdscript
class_name Pool
extends Node

var _scene: PackedScene
var _free: Array[Node] = []

func setup(scene: PackedScene, prewarm: int = 16) -> void:
	_scene = scene
	for i in prewarm:
		var n := _scene.instantiate()
		_deactivate(n)
		_free.append(n)
		add_child(n)

func acquire() -> Node:
	var n: Node = _free.pop_back() if not _free.is_empty() else _scene.instantiate()
	if n.get_parent() == null:
		add_child(n)
	n.process_mode = Node.PROCESS_MODE_INHERIT
	if n is CanvasItem:
		n.visible = true
	return n

func release(n: Node) -> void:
	_deactivate(n)
	_free.append(n)

func _deactivate(n: Node) -> void:
	n.process_mode = Node.PROCESS_MODE_DISABLED
	if n is CanvasItem:
		n.visible = false
```
- 回收时重置状态（位置、血量、tween、计时器）；池元素不要在 `release` 后继续接收信号。
- 先测量再池化：对象数量不大时直接 `queue_free()` 更简单。

## 常见坑

| 坑 | 说明与做法 |
|---|---|
| Tween 泄漏/叠加 | 重复触发动画前 `kill()` 旧 tween（starter 的 `_pop()`）；节点被释放时 tween 随之失效，但存着的引用要用 `is_valid()` 判断 |
| `await` 之后节点已释放 | `await get_tree().create_timer(1.0).timeout` 之后检查 `is_inside_tree()` / `is_instance_valid(self)` |
| 信号重复连接 | `connect` 前 `is_connected` 判断，或在 `_ready` 只连一次 |
| `_process` 里分配 | 每帧 `Array`/`Dictionary`/字符串拼接产生垃圾，放进成员变量复用 |
| `queue_free` 与同帧访问 | 释放后同一帧仍可访问；用 `is_queued_for_deletion()` 判断 |
| 浮点比较 | 用 `is_equal_approx` |
| 整数除法 | `a / b` 两个 int 是整除并有警告；需要时 `floori(float(a)/b)` |
| 日期逻辑 | 用 ordinal/儒略日计算天数差，测试覆盖跨月、跨年（`rebuild-dev-milestones`） |
| 脚本批量替换 | 改完立刻跑冒烟，Python 替换容易把 `\n` 写坏 |
| Resource 共享 | 多个实例共享同一个 `Resource`；需要独立副本时 `duplicate()` |
| ETC2/ASTC | `[rendering] textures/vram_compression/import_etc2_astc=true`，否则 Android 导出失败且无报错 |
