# 移动端性能、触屏输入与竖屏 UI

预算数字见 `game-playtest-qa/references/perf-budgets.md`（参考值，按品类校准），这里只写 Godot 侧的做法。

## 渲染器

- 移动休闲 2D：**GL Compatibility**（`rendering_method="gl_compatibility"`），兼容性最好、包体和发热更友好；需要高级 3D/光照再考虑 Mobile 渲染器并实测低端机。
- 纹理压缩：`textures/vram_compression/import_etc2_astc=true`，Android 导出必需。
- 大图集合并、避免大面积半透明叠加、避免每帧改变着色器参数。

## 性能清单

| 项 | 做法 |
|---|---|
| 帧率 | 目标 60；静态界面可 `Engine.max_fps = 30` 省电；暂停时停止 `_process` |
| 节点数 | 大量同类对象用对象池或 `MultiMeshInstance2D`；避免深层树每帧遍历 |
| 物理 | 休闲游戏能不用物理就不用；碰撞层/掩码精简；`physics_ticks_per_second` 按需降低 |
| GC/分配 | `_process` 内不新建数组/字典/字符串；复用 |
| 加载 | 用 `ResourceLoader.load_threaded_request` 异步加载大场景；SDK 初始化放首帧之后 |
| 音频 | 长音乐 OGG 流式，短音效 WAV/OGG；限制同时播放数 |
| 监控 | `Performance.get_monitor(Performance.TIME_FPS)`、`OBJECT_COUNT`、`MEMORY_STATIC`；调试面板显示；真机用 `adb shell dumpsys gfxinfo` |
| 发热 | 30 分钟浸泡测试；后台暂停渲染 |

## 触屏输入

- 开发期 `input_devices/pointing/emulate_touch_from_mouse=true`（starter 已开），桌面也能点。
- 优先用 `Button.pressed` / `TouchScreenButton`；自定义手势用 `_input(event)` 处理 `InputEventScreenTouch` / `InputEventScreenDrag`，用 `event.index` 区分多指。
- 点击目标最小约 48dp（720 宽设计稿下约 90–110 px），间距足够，避免误触。
- 不要依赖 hover；不要把关键操作放在屏幕边缘手势区（系统返回手势）。
- 返回键：Android 返回走 `NOTIFICATION_WM_GO_BACK_REQUEST`；需要自己处理时在项目设置中关闭默认退出（`application/config/auto_accept_quit` 与 `set_auto_accept_quit(false)`）。
- 震动：`Input.vibrate_handheld(ms)`，给用户关闭开关。

## 竖屏 UI 缩放

starter 设置：设计分辨率 720×1280，`stretch/mode="canvas_items"`，`stretch/aspect="expand"`。

| 设置 | 效果 |
|---|---|
| `canvas_items` + `expand` | 保持清晰（按设备分辨率渲染 UI），长屏/宽屏会多出空间；UI 用锚点贴边、居中，背景要铺满 |
| `canvas_items` + `keep` | 留黑边，布局最可控；适合不想适配异形比例的小项目 |
| `viewport` | 像素风游戏，整体放大，清晰度取决于设计分辨率 |

做法：
1. 根节点 `Control` 设为全屏锚点；用 `VBoxContainer/MarginContainer/AspectRatioContainer` 而非手写坐标。
2. 背景用 `TextureRect` 全屏拉伸或 `ColorRect`，让超长屏不露底。
3. 刘海/手势条：用 `DisplayServer.get_display_safe_area()` 获取安全区，顶栏下移（需在真机验证，坐标是物理像素，要按窗口缩放换算）。
4. 屏幕方向：`display/window/handheld/orientation`（竖屏锁定），确认导出预设与之一致。
5. 在编辑器里用多个窗口尺寸测试：360×640、360×780（长屏）、412×915、768×1024（平板）；`window/size/window_width_override` 控制桌面预览窗口大小。
6. 字号以设计稿为准，别在代码里按分辨率乘系数；多语言留余量。

## 测试与冒烟（Godot 部分）

```bash
godot --headless --path . --quit-after 3 2>&1 | grep -E "SCRIPT ERROR|Parse Error|nonexistent"
godot --headless -s tests_dev/test_xxx.gd      # extends SceneTree，exit code 判定
```
测试写法：`extends SceneTree`，在 `_initialize()` 里跑断言，最后 `quit(0|1)`；每个用例先重置单例/存档，避免跨用例污染；日期、随机用固定种子/注入。starter 的 `tests_dev/test_gamestate.gd` 是模板（未经运行验证）。
