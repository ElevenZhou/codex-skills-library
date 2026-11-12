# 引擎：Unity Mono（⚠️ 未验证：无独立案例；资源侧可复用 unity-il2cpp.md 的经验）

> 与 IL2CPP 的区别只在**逻辑层**：Mono 包里的托管程序集可直接反编译。资源（Texture2D / AudioClip / Addressables / CCD）的做法与 `unity-il2cpp.md` 一致，不重复。

## 识别特征（S1）
- `assets/bin/Data/Managed/Assembly-CSharp.dll`（及 `Assembly-CSharp-firstpass.dll`、`UnityEngine*.dll`）；`lib/*/libmono.so` 或 `libmonobdwgc-2.0.so`。
- **没有** `libil2cpp.so` 与 `global-metadata.dat`。两者都出现时，以 metadata 是否存在为准（detect_engine 会给 warning）。
- `assets/bin/Data/ScriptingAssemblies.json` 给出完整程序集清单。

## 源码可恢复性（S1 出口必写）
- **逻辑：高。** ILSpy / dnSpyEx 可近乎还原 C#（含类名、方法名、字段名）。
- 例外：被混淆（符号名乱码、控制流平坦化）或程序集被加壳/加密（DLL 头不是 `MZ`）。此时降为中，并在 `01-` 文档记录证据。
- 仍然遵守「Agent 不发布反编译产物」铁律：反编译源码只做理解与重写依据，不进入交付工程。

## 工具
| 目的 | 工具 | 验证状态 |
|---|---|---|
| 反编译 C# | ILSpy（CLI: `ilspycmd`）、dnSpyEx | 未验证 |
| 资源回导 | AssetRipper / AssetStudio / UnityPy（见 unity-il2cpp.md） | 沿用 il2cpp 条目 |
| 程序集加壳判断 | 文件头 `4D 5A`；`ScriptingAssemblies.json` 与实际 DLL 比对 | 未验证 |

## 开发（S5）
- 因为逻辑可读，S5 可选「行为等价重写」或「按反编译结果逐类重写」；仍建议走 `rebuild-dev-milestones` 的 M0–M5，**不要整包搬运**。
- 其余开发/打包约定同 `unity-il2cpp.md`（Unity 编辑器与 Android 模块为硬依赖，纯 ASCII 路径）。

## 案例
- （待补）
