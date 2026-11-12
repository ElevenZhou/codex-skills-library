# 引擎：Flutter / Dart（⚠️ 未验证：无真实案例）

## 识别特征（S1）
- `lib/<abi>/libflutter.so`（引擎）+ `lib/<abi>/libapp.so`（Dart AOT 快照，Release）；`assets/flutter_assets/`（`AssetManifest.json`、`FontManifest.json`、图片/字体/音频原样存放）。
- Debug 构建会有 `flutter_assets/kernel_blob.bin`（Dart kernel，可读性远高于 AOT），线上包基本不会有。

## 源码可恢复性（S1 出口必写）
- **资源：高**——`flutter_assets/` 里的图片、字体、音频、JSON 通常**不加密**，直接复制即可（仍走 `rebuild-asset-recovery` 的样品先行与报告流程）。
- **逻辑：低~中**——Release 的 `libapp.so` 是 AOT 快照，不是字节码。可借助 Flutter 逆向工具恢复类/函数符号与字符串，逻辑本身需重写。工具与版本强相关（Dart 版本由快照哈希决定）：
  - reFlutter（重打包并拦截流量，用于动态分析，仍须遵守安全红线：不绕过证书校验到第三方生产服务）
  - Blutter（对 arm64 AOT 快照生成符号/汇编注释，**对 Dart 版本有支持范围**）
  - 以上均 **未验证**，首次使用时在 M0 工具链表登记版本与结论。
- 网络层：Flutter 默认不走系统代理，静态分析优先；动态抓包需要 scope.md 中「联网与服务端」已勾选。

## 开发（S5）
- 选 Flutter 重写：复用 `flutter_assets` 命名与目录；选 Godot 重写：游戏类优先 Godot，工具类/表单类应用优先继续 Flutter。
- UI 布局信息可从截图 + `AssetManifest.json` 推断；`libapp.so` 里的字符串（页面名、接口路径）作为 `01-` 文档的旁证（证据等级按 `rebuild-recon` 的置信度标注）。

## 打包（S7）
- 常规 `flutter build apk --release --split-per-abi`；签名流程同 `rebuild-build-release`。**未验证**，首次实践后补坑。

## 案例
- （待补）
