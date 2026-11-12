# 埋点规范（telemetry spec）

规范存为 JSON（示例 `assets/telemetry_example.json`），用 `scripts/telemetry_lint.py` 校验；代码里的事件名、属性名必须与规范一致（契约原样继承，见 `rebuild-dev-milestones` 的纪律 4）。

```bash
python3 scripts/telemetry_lint.py telemetry/spec.json --strict
```

## 命名规则

- 事件名、属性名：`snake_case`，小写字母开头，≤40 字符，动宾或名词_动词：`level_start`、`ad_impression`。
- 事件名一经上线不改名；需要改语义就新增事件并保留旧事件一个版本。
- 枚举值同样 snake_case；枚举必须声明 `values`。
- 类型限于：`string`、`int`、`float`、`bool`、`enum`、`timestamp`。时间长用毫秒（`_ms` 后缀），金额用 `_usd` 等带币种后缀。
- 不要把变化的值放进事件名（错：`level_5_start`；对：`level_start` + `level_id`）。

## 公共属性（每个事件自动带）

| 属性 | 类型 | 说明 |
|---|---|---|
| `session_id` | string | 随机生成的会话 ID，非设备标识 |
| `app_version` | string | 构建版本 |
| `platform` | enum | android / ios / web |
| `install_day` | int | 距安装第几天（客户端计算，D0 = 0） |
| `client_ts` | timestamp | 客户端时间，服务端另记接收时间 |

用户标识用**匿名随机 ID**（首启生成并本地保存），不使用手机号、邮箱、IMEI、Android ID、IDFA 明文。广告 ID 的使用需遵守各平台政策与用户授权（`game-dev-workflow/references/monetization-compliance.md`）。

## 核心漏斗事件（最小集）

| 阶段 | 事件 | 关键属性 | 用途 |
|---|---|---|---|
| 启动 | `app_open` | `is_cold_start`、`load_ms` | 启动成功率、加载时长 |
| 新手 | `tutorial_start` / `tutorial_step` / `tutorial_complete` | `step_id`、`duration_ms` | 新手流失点 |
| 核心 | `level_start` / `level_complete` / `level_fail` | `level_id`、`attempt`、`duration_ms`、`reason` | 难度曲线、卡关点 |
| 经济 | `currency_change` | `currency`、`amount`、`balance_after`、`source` | 回填 `economy_sim.py` 的产出/消耗 |
| 广告 | `ad_request` / `ad_impression` / `ad_reward_granted` | `placement`、`ad_type`、`revenue_usd` | 填充率、展示数、ARPDAU |
| 付费 | `purchase_complete`（可加 `purchase_start`） | `product_id`、`price_usd`、`is_first_purchase` | 转化、ARPPU |
| 留存钩子 | `daily_reward_claim` | `streak_day` | 钩子有效性 |
| 异常 | `error_report`（可选） | `code`、`where` | 辅助崩溃平台 |

## 指标如何由事件得到

| 指标 | 计算 |
|---|---|
| D1/D7/D30 留存 | 安装日 + n 天有 `app_open` 的用户 / 安装用户 |
| 新手完成率 | `tutorial_complete` 用户 / `tutorial_start` 用户 |
| 关卡胜率 | `level_complete` / (`level_complete` + `level_fail`)，按 `level_id` |
| 平均尝试次数 | 每关 `attempt` 均值/分位 |
| 每 DAU 广告展示 | 当日 `ad_impression` / 当日活跃用户 |
| ARPDAU | (广告收入 + 内购收入) / DAU |
| 付费转化 | 累计付费用户 / 累计活跃用户 |

## 实施要点

1. 事件在代码中通过单一入口发送（Godot 见 `godot-game-dev` 的 `Events`/Analytics 封装），不要到处直接调 SDK。
2. 离线缓存与批量上报；上报失败不阻塞游戏。
3. 先在真机上用调试面板/日志核对事件序列，再接后台。
4. 采样与成本：高频事件（每帧、每次点击）不上报，必要时聚合为汇总事件。
5. 版本管理：规范文件带 `version`，变更写入变更记录；删除字段需保留兼容期。
6. 隐私：属性名命中 PII 关键词（email、phone、imei、idfa、ip_address 等）会被 lint 拦截；确需使用的，应先脱敏/分桶并改名，且更新隐私政策。
7. 本规范的阈值与指标是参考，具体门槛见 `softlaunch-metrics.md`。
