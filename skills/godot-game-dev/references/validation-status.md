# 验证状态（validation-status）

最后更新：2026.11.12

## 结论

`assets/godot-starter/` **没有在 Godot 编辑器或 headless 中运行过**。写作环境没有 Godot 二进制（`which godot` 为空）。所做的只有：对照 Godot 4.x GDScript 语法和 API 逐行人工复读、核对计数（13 个检查项）、核对 `project.godot` 与文件路径一致。

## 未验证的内容（运行时才能确认）

| 项 | 风险 |
|---|---|
| `project.godot` 能被引擎解析 | `config/features` 写的是 `"4.3"`，实际版本不同可能触发"用较新版本打开"提示；`window/handheld/orientation=1`（竖屏）的枚举值需在编辑器里确认 |
| `main.tscn` 手写，未经编辑器保存 | 首次打开可能提示重新保存/补 uid；布局数值（offset、字号）未目视检查 |
| 自动加载在 `-s` 脚本里的可用时机 | 测试用 `root.get_node_or_null("GameState")` 取得；若 autoload 在你的版本里于 `_initialize()` 之后才加入，测试会输出 `GameState autoload not found` 并退出 1 |
| GDScript 严格类型警告 | 可能有 `UNTYPED_DECLARATION` / `INFERENCE_ON_VARIANT` 之类警告；不应有 Parse Error |
| `NOTIFICATION_APPLICATION_PAUSED` 在你的 4.x 版本可用 | 4.0+ 的 Node 上存在，真机上才能确认暂停时会存档 |
| 导出 | 完全未试；按 `android-export.md` 的流程另行验证 |

## 你需要运行的命令（在 `assets/godot-starter/` 目录）

```bash
godot --headless --path . --import
godot --headless --path . --quit-after 3 2>&1 | grep -E "SCRIPT ERROR|Parse Error|nonexistent"
godot --headless -s tests_dev/test_gamestate.gd; echo "exit=$?"
```

通过标准：第 2 条无输出；第 3 条打印 `13 checks, 0 failures` 且 `exit=0`。

编辑器内：`godot --path . -e` 打开，F5 运行，点击 TAP 按钮：分数增加，每 10 次点击升一级，Reset 归零；关闭再打开，进度恢复。

## 运行后请回写

跑完后把结果追加到这里（版本号、日期、命令输出、修复了什么），并把状态改为"已在 Godot x.y.z 验证"。在此之前，任何依赖 starter 的项目都应当把它视为"待验证草稿"，不要把它当成已验证的 M0 骨架。

## 参考来源

`rebuild-workflow/references/engines/godot.md`（项目 D，Godot 4.6.3）中已验证的是：冒烟命令、`extends SceneTree` 测试运行方式、导出五坑。本 starter 的代码本身不在那份验证范围内。
