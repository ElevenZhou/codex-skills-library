# 站点与渠道档案

最近核实：2026-10-10（只读）。数据可能变化，用之前先实查一遍。

## 老站 Flaios-Video（NewAPI）

- 项目：`E:\Dev-2\Flaios-Video`
- 生产：**东京 43.130.235.209**，ssh 别名 `flaios-tokyo-video`，目录 `/opt/new-api`，容器 `new-api-mysql`（MySQL 8.4），库 `newapi`
- 不是首尔 150.109.233.152。首尔那台是 NewAPI 文本 / Claude 入口，它的 ch90 是 Claude 渠道。
- 会话时区 `+08:00`，所以 `FROM_UNIXTIME()` 直接得到北京时间。
- 连库：root 密码用 `docker exec new-api-mysql printenv MYSQL_ROOT_PASSWORD` 读出，通过 `MYSQL_PWD` 环境变量传入，不要打印。
- 事实表：
  - `tasks`：`task_id`、`upstream_task_id`（`cgt-…`）、`channel_id`、`user_id`、`status`（SUCCESS / FAILURE / IN_PROGRESS / NOT_START）、`quota`、`pre_consumed_quota`、`final_quota`、`billing_status`、`total_tokens`、`submit_time`、`finish_time`（unix 秒）、`properties.origin_model_name`、`private_data.billing_context.{group_ratio,model_ratio,video_resolution,other_ratios}`
  - `logs`：type 2 消费、type 6 退款；`other.task_id` 关联到任务
- 金额：**500000 quota = 1 元**
  - 客户实扣 = `final_quota / 500000`
  - **官方原价 = `final_quota / group_ratio / 500000`**
  - 失败任务会全额退款，`final_quota` 为 0
- 分组倍率会变。例如用户 26 在 10-08 从 0.85 改为 0.83，所以必须逐行取 `billing_context.group_ratio`，不能用常数。

## 新站 VideoAi-New

- 项目：`E:\Dev-2\VideoAi-New`
- 生产：**111.229.213.213**，用户 `ubuntu`，目录 `~/videoai`，容器 `deploy-postgres-1`（Postgres 16）
- 连接时 SSH 会先输出一大段微信扫码二维码横幅，输出要过滤掉 `██`、`请使用`、`Please use`、`up.yd` 这几类行。
- 存储为 UTC，查询前先执行 `SET TIME ZONE 'Asia/Shanghai'`，之后不要再写 `AT TIME ZONE`。
- 事实表：
  - `video_tasks`：`public_task_id`、`adapter_task_id`（上游 `cgt-…`）、`channel_id`、`model`、`status`（succeeded / failed / running / pending）、`usage.total_tokens`、`official_amount`、`pricing_snapshot`、`completed_at`、`account_reroute_count`、`abandoned_at`
  - `billing_ledger`：type 有 hold / settle / adjust / refund，按 `task_id` 汇总净额，客户实扣 = −净额
  - `request_logs`：按月分区，用于查创建超时、孤儿任务等
  - `channels`、`channel_models`、`models`（存放价格矩阵）、`price_discounts`
- 金额：**官方原价 = `official_amount / 1e6` 元**。目前客户倍率为 1，客户实扣等于原价。

## 智算谷（zsg / zhisuangu），上游项目 zsg15_1

| 站 | 渠道 | 是否在 zsg15_1 账单内 |
|---|---|---|
| 新站 | ch6 `zhisuangu`（adapter `volcengine_ark`） | ✅ |
| 老站 | ch93 `视频-Volcengine-Seedance-智算谷-官方`（type 61，直连 Ark） | ✅ |
| 老站 | ch94 `K通道二号`（kmoodzsg adapter，上游是 zsg，经 kmood 结算） | ❌ |
| 老站 | ch90 `筷子丽帧` | ❌ 与智算谷无关 |
| 新站 | ch7 / ch8 jieyue（kmood adapter） | ❌ |

- 账单"消耗额" = **官方原价**。实际成本 = 消耗额 × **0.77**。
- 账单期初有时不等于前一日期末（09-30、10-09、10-10），这是充值造成的，标记为 `balance_adjustment`，不算差异。
- 上游项目由多个用户共享。逐笔匹配只能按我方的 `cgt-` ID 过滤；官方任务列表接口只能查最近 7 天。
- 基线（2026-09-29～10-09）：账单 194,205.21，新站 133,614.00，老站 60,532.94，差额 +58.27（+0.03%），判定通过。10-10 截止时刻存疑，已排除。

## 新渠道接入清单

为新渠道补一节，至少写清以下内容：

1. 两站各自的渠道 ID、名称、adapter、真实上游，以及谁负责结算。
2. 账单形态：截图、日汇总 CSV、逐笔 CSV 还是 API；有哪些字段；金额单位；是否含税。
3. 账单金额是原价还是折后价，用逐日对比来验证。
4. 合同折扣，以及官方限时折扣的生效时间窗。
5. 上游任务 ID 的格式，以及它在两站分别存在哪个字段。
6. 一段已对平的基线区间和数字，作为回归样例。
