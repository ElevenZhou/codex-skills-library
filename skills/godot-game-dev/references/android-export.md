# Android 导出

完整流程、工具链准备、keystore、安装冒烟、交付清单和发布人工门禁（G-PUBLISH）全部在 **`rebuild-build-release`**，这里不复制。其中 Godot 4.x 的来源细节在 `rebuild-workflow/references/engines/godot.md`（项目 D，Godot 4.6.3 验证）。

导出五坑（一句话版）：

1. 导出模板目录名必须等于编辑器版本号（如 `export_templates/4.6.3.stable/`），tpz 解压出的 `templates/` 要改名。
2. build-tools 版本需 ≥ 模板 target SDK（Godot 4.6 → 35+）；新命名无次版本号（`build-tools_r36_...`），以 `repository2-3.xml` 为准。
3. SDK/JDK/Godot/keystore/输出路径全部用纯 ASCII 路径。
4. keystore 三元组（路径 + user + password）debug/release 各自要么全填要么全空，空字符串不等于没填。
5. `project.godot` 的 `[rendering]` 必须有 `textures/vram_compression/import_etc2_astc=true`，缺了导出失败且错误列表为空（starter 已带这一项）。

导出命令：
```bash
godot --headless --path . --export-release "Android" build/<app>.apk
```
导出后用 `game-playtest-qa/scripts/apk_budget_check.py` 查包体，用 `rebuild-device-evidence` 做真机安装冒烟。keystore 不入仓库，双人双地备份。
