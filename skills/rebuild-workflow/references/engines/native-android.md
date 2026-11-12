# 引擎：原生 Android（Java/Kotlin）+ 混合壳（Cordova / Capacitor / H5 引擎）（⚠️ 未验证：通用起步清单）

> `detect_engine.py` 未命中任何引擎时先看这里：多半是原生 App，或网页壳。工具类/小游戏里的 H5 包也在此处。

## 原生（Java/Kotlin）
### 识别
- 只有 `classes*.dex`、`res/`、`AndroidManifest.xml`，`lib/` 里只有第三方 SDK 的 so（广告、统计、地图）。
- Jetpack Compose 的界面在 res 里没有 layout XML，需看 dex。

### 源码可恢复性
- **逻辑：高**——jadx 可还原到接近源码；R8/ProGuard 混淆后类名为 a/b/c，但流程可读。若有 `mapping.txt`（极少随包发布）可反混淆。
- 加固（360 / 梆梆 / 腾讯乐固 / 爱加密等）命中时先判断「脱壳」是否在 scope.md 勾选；**未勾选 = 不做**，转行为级重做。`detect_engine.py` 的 packers 字段给初判。

### 工具
| 目的 | 工具 | 验证状态 |
|---|---|---|
| manifest / 资源 / smali | apktool（Windows 注意显式指向 JDK，见 unity-il2cpp.md 同款坑） | ✅ 项目 F 使用过 apktool 取 manifest |
| 反编译 Java/Kotlin | jadx / jadx-gui | ✅ 项目 F 工具就位 |
| SDK 与权限盘点 | manifest + `rebuild-recon` 的 asset_manifest.py | ✅ |
| 动态证据（截图/日志/UI 树） | `rebuild-device-evidence` | ✅ |

## 混合壳（Cordova / Capacitor）
- 特征：`assets/www/`（Cordova）或 `assets/public/`（Capacitor）、`cordova.js`、`capacitor.config.json`。**网页文件就是源码**，只需美化、Source Map 还原。
- 注意 `config.xml` / `capacitor.config.json` 中的远程 URL（live reload / server.url）：若线上包加载远端页面，则「游戏本体在服务端」，本地包不含全部逻辑，需按 `rea-integration.md` 的联网与服务端门禁处理。

## H5 游戏引擎（Laya / Egret / Phaser / Pixi / Cocos H5）
- 特征：`egret.min.js`、`laya.core.js`、`phaser.min.js`、`pixi.min.js`，以及 `resource/default.res.json`（Egret）、`.atlas`+`.json` 图集。
- 资源与逻辑几乎都是明文；混淆过的 JS 用 AST 美化 + 重命名辅助阅读（工具未验证）。
- 重写选型：H5 玩法体量小，通常「继续 H5（Phaser/Pixi）」或「迁移 Godot Web/Android」二选一，在 D 系列决策门里写明理由。

## 开发 / 打包
- 原生：按产品形态选 Kotlin/Compose；游戏类用 Godot/Unity 重做更省。
- 签名与交付统一走 `rebuild-build-release`。

## 案例
- （待补）
