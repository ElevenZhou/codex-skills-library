#!/usr/bin/env python3
"""识别 APK/XAPK/AAB 的引擎与加固特征。

用法: python detect_engine.py <package.apk|xapk|aab>
输出: JSON（引擎候选、证据文件、加固候选、内嵌 APK 列表）
"""
import json
import struct
import sys
import zipfile

HERMES_MAGIC = bytes.fromhex("c61fbc03c103191f")

ENGINE_MARKERS = {
    "godot": ["libgodot_android.so", ".pck", ".godot/imported/"],
    "unity-il2cpp": ["libil2cpp.so", "global-metadata.dat"],
    "unity-mono": ["libmono.so", "libmonobdwgc-2.0.so", "Assembly-CSharp.dll"],
    "cocos": ["libcocos2djs.so", "libcocos.so", "libcocos2dcpp.so", ".jsc", "jsb-adapter", "cocos-js/"],
    "unreal": ["libUE4.so", "libUnreal.so"],
    "flutter": ["libflutter.so", "libapp.so", "flutter_assets/"],
    "react-native": ["libreactnativejni.so", "index.android.bundle"],
    # 以下为 v1.5 新增，特征为经验值，首次命中请人工复核（engines/*.md 标 未验证）
    "xamarin-maui": ["libmonodroid.so", "Mono.Android.dll", "libxamarin-app.so"],
    "cordova-capacitor": ["assets/www/cordova.js", "assets/public/cordova.js", "capacitor.config.json"],
    "h5-engine": ["egret.min.js", "laya.core.js", "phaser.min.js", "pixi.min.js"],
    "gamemaker": ["libyoyo.so"],
}

# 初步判断提示，仅供 S1 起步；正式的「源码可恢复性结论」必须以解包实测为准
RECOVERABILITY_HINT = {
    "godot": "资源：高；脚本：.gd 明文可读，.gdc/.gde 加密则按纯重做",
    "unity-il2cpp": "资源：高（AssetRipper/UnityPy）；逻辑：仅签名与字符串（Il2CppDumper），需重写",
    "unity-mono": "资源：高；逻辑：高（Assembly-CSharp.dll 可用 ILSpy 近乎还原，除非被混淆）",
    "cocos": "资源：高；逻辑：JS 明文高，.jsc 需 xxtea 密钥（常在 libcocos2djs.so）",
    "unreal": "资源：中（.pak 可能加密）；逻辑：Blueprint/C++ 低，通常只能行为级重做",
    "flutter": "资源：高（flutter_assets 明文）；逻辑：Dart AOT 仅能恢复符号，需重写",
    "react-native": "Hermes 字节码需反汇编，明文 JS bundle 则高；见 engines/react-native-hermes.md",
    "xamarin-maui": "逻辑：高（.NET 程序集可反编译，可能被 XALZ 压缩包装需先解压）",
    "cordova-capacitor": "逻辑与资源：高（assets/www 或 assets/public 即网页源码，可能被压缩/混淆）",
    "h5-engine": "逻辑与资源：高（JS 可读，注意混淆与资源 json 清单）",
    "gamemaker": "资源：中；逻辑：低（YYC 为原生编译，VM 模式有 data.win 可解）",
}
PACKER_MARKERS = {
    "360jiagu": ["libjiagu"],
    "bangcle": ["libsecexe.so", "libDexHelper"],
    "tencent-legu": ["libshell", "libtup.so"],
    "ijiami": ["libexec.so", "libexecmain.so"],
}


def scan_names(names):
    engines, packers = {}, {}
    for n in names:
        for eng, marks in ENGINE_MARKERS.items():
            if any(m in n for m in marks):
                engines.setdefault(eng, []).append(n)
        for p, marks in PACKER_MARKERS.items():
            if any(m in n for m in marks):
                packers.setdefault(p, []).append(n)
    return engines, packers


def rn_details(zf):
    """RN 包：判断 bundle 是 Hermes 字节码（含版本号）还是明文 JS；识别 Expo。"""
    info = {}
    names = zf.namelist()
    if "assets/index.android.bundle" in names:
        with zf.open("assets/index.android.bundle") as f:
            head = f.read(12)
        if head[:8] == HERMES_MAGIC:
            info["js_bundle"] = f"hermes:v{struct.unpack('<I', head[8:12])[0]}"
        else:
            info["js_bundle"] = "plain-js"
    if "assets/app.config" in names:
        try:
            cfg = json.loads(zf.read("assets/app.config"))
            info["expo"] = {k: cfg.get(k) for k in ("sdkVersion", "owner", "slug") if cfg.get(k)}
        except Exception:
            info["expo"] = "app.config 存在但无法解析"
    return info


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    path = sys.argv[1]
    result = {"file": path, "inner_apks": [], "engines": {}, "packers": {}, "dex_count": 0}
    with zipfile.ZipFile(path) as z:
        names = z.namelist()
        inner = [n for n in names if n.endswith(".apk")]
        result["inner_apks"] = inner
        all_names = list(names)
        rn = rn_details(z)
        for n in inner:  # XAPK：扫描内嵌 APK
            with z.open(n) as f, zipfile.ZipFile(f) as iz:
                all_names += [f"{n}!{x}" for x in iz.namelist()]
                rn.update(rn_details(iz))
        if inner:
            result["split_apks"] = [n for n in inner if n.split("/")[-1].startswith("config.")]
    result["dex_count"] = sum(1 for n in all_names if n.endswith(".dex"))
    engines, packers = scan_names(all_names)
    result["engines"] = {k: v[:5] for k, v in engines.items()}
    result["packers"] = {k: v[:5] for k, v in packers.items()}
    if rn:
        result["react_native"] = rn  # 例：{"js_bundle": "hermes:v96", "expo": {...}}
    if engines:
        result["recoverability_hint"] = {k: RECOVERABILITY_HINT[k] for k in engines if k in RECOVERABILITY_HINT}
        if "unity-il2cpp" in engines and "unity-mono" in engines:
            result["warning"] = "同时命中 il2cpp 与 mono 标记：多为 Unity 的 libmono 误报或混合构建，以 global-metadata.dat 是否存在为准"
    if not engines:
        result["note"] = "未命中引擎特征：可能是原生 Android（走 engines/native-android.md），或需要人工检查 lib/ 与 assets/"
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
