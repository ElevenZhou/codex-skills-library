# 设备矩阵、性能预算与崩溃分诊

所有阈值：**参考值，按品类校准**。预算在 G2 前写下，G3 起每次发版对比。

## 设备矩阵（至少覆盖 3 档）

| 档位 | 代表规格（示例，按目标市场更新） | 作用 |
|---|---|---|
| 低端 | Android 8–10、2–3 GB RAM、入门 SoC、720p | 暴露内存/加载/发热问题，决定最低支持线 |
| 中端 | Android 11–13、4–6 GB RAM、1080p | 主流体验基线，性能预算的主测机 |
| 高端 | 当年旗舰、高刷屏（90/120Hz） | 检查高刷/异形屏/大屏适配 |
| 补充 | 平板、折叠屏、Android 最新版本、低版本边界 | 布局与权限行为差异 |

选择方法：用目标市场的设备份额数据（商店后台或第三方统计）挑 Top 机型覆盖；记录"没测到的风险"。每台设备记录：型号、Android 版本、RAM、屏幕、构建号。

## 性能预算

| 指标 | 超休闲 | 休闲 | 中度 | 测法 |
|---|---|---|---|---|
| 目标帧率 | 60 | 60（静态界面可 30） | 30–60 | Godot 的 Monitors/`Performance.get_monitor`，或 `adb shell dumpsys gfxinfo <pkg> framestats` |
| 卡顿帧占比（>2× 帧预算） | < 2% | < 3% | < 5% | gfxinfo 的 janky frames |
| 冷启动到可玩 | < 3 s | < 5 s | < 8 s | `adb shell am start -W -n <pkg>/<activity>` 的 TotalTime；中端机 |
| 关卡加载 | < 1 s | < 2 s | < 5 s | 打点 `load_ms` |
| 内存（PSS，稳态） | < 250 MB | < 400 MB | < 700 MB | `adb shell dumpsys meminfo <pkg>` |
| 内存增长（30 分钟浸泡） | < 10% | < 10% | < 15% | 同上，每 5 分钟采样 |
| 包体（APK/AAB） | < 30 MB | < 80 MB | < 200 MB | `scripts/apk_budget_check.py` |
| 安装后占用 | 包体的 2–3 倍以内 | 同 | 同 | `dumpsys package` / 设置页 |
| 电量/发热 | 30 分钟升温 < 8°C 且无降频卡顿 | 同 | 同 | `dumpsys battery`、手感 |
| 耗流量（首次） | < 5 MB | < 20 MB | 视热更而定 | 抓包/统计 |

Google Play 对基础包体和 AAB 大小有上限且会调整，上线前以官方当前文档为准。

### 采样命令

```bash
adb shell dumpsys meminfo <package> | sed -n '1,30p'
adb shell dumpsys gfxinfo <package> reset      # 复位计数后操作 60 秒
adb shell dumpsys gfxinfo <package> | grep -E "Total frames|Janky frames|90th|95th|99th"
adb shell am start -W -n <package>/<activity> | grep -E "TotalTime|WaitTime"
adb logcat -d -b crash,main | tail -200
```
截图/日志统一用 `rebuild-device-evidence` 的规范存放。

### 常见优化抓手

| 症状 | 先查 | 手段 |
|---|---|---|
| 掉帧 | 每帧分配、`_process` 里的重计算、大量节点 | 对象池、降低更新频率、合批、减少透明叠加 |
| 内存高 | 纹理尺寸、未释放场景、音频流 | 压缩纹理（ETC2/ASTC）、图集、按需加载、`queue_free` |
| 加载慢 | 启动时同步加载大资源、SDK 初始化 | 异步加载、首帧后再初始化 SDK |
| 包体大 | `apk_budget_check.py` 的 Top-N | 压缩音频、裁剪导出模板/ABI、删未用资源 |
| 发热 | 一直满帧、后台仍在渲染 | 静态界面降帧、暂停时停止更新 |

## 崩溃 / ANR 分诊

目标（参考）：会话崩溃率 < 1%（内测）/ < 0.5%（上线）；ANR < 0.3%。

```text
收到崩溃报告
 ├─ 能复现？
 │   ├─ 是 → 记录步骤、设备、构建号 → 修 → 加回归用例
 │   └─ 否 → 看 logcat/tombstone/Play Console 堆栈
 ├─ 堆栈归属？
 │   ├─ 引擎/native (libgodot / libc / SIGSEGV) → 查驱动/设备特异、纹理格式、导出模板版本；用最小场景复现
 │   ├─ 游戏脚本 (SCRIPT ERROR / null instance) → 修空引用、信号重复连接、已释放节点访问
 │   ├─ 第三方 SDK (广告/统计) → 隔离：禁用该 SDK 复测；升级版本；初始化放后台
 │   └─ OOM (OutOfMemoryError / lowmemorykiller) → 查内存峰值，见预算表
 ├─ 影响面？(版本/设备/系统/占比)
 └─ 决策：热修 / 下版修 / 远程关闭相关功能
```

ANR 常见原因：主线程阻塞（同步 IO、SDK 初始化、同步网络）、死锁、广告回调内做重活。处理：看 `adb pull /data/anr/` 或 Play Console 的 ANR 堆栈，找主线程停在哪。

每个 P0 崩溃修复必须附回归用例（测试脚本或手动步骤写入 `smoke-and-acceptance.md` 的项目副本）。
