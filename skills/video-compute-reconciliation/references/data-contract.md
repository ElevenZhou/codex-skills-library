# 数据契约

`scripts/reconcile.py` 支持 CSV、TSV、PSV，分隔符按首行自动判断。读取时会跳过 SSH 二维码横幅、psql 提示行，以及 `(N rows)` 这类列数不齐的行。所有金额都用 Decimal 计算，单位是元。

## 站内导出（`--old` / `--new`）

格式与 `references/queries/*_daily.sql` 或 `*_tasks.sql` 的输出一致。

| 字段 | 别名 | 说明 |
|---|---|---|
| bill_day | d、date、日期 | 北京时间完成日。没有这一列时用 completed_at 推算 |
| completed_at | finish_time | ISO 时间或 unix 秒；不带时区的按北京时间处理 |
| model | model_name | |
| status | | SUCCESS / succeeded → success，FAILURE / failed → failed |
| n | count | 聚合行的任务数，逐笔行默认为 1 |
| tokens | tok、total_tokens | |
| list_yuan | | **官方原价**（元），用来和账单比对。老站 = `final_quota/group_ratio/500000`，新站 = `official_amount/1e6` |
| cust_yuan | | 客户实扣（元），用来算毛利 |
| upstream_task_id | adapter_task_id | 逐笔匹配的主键（`cgt-…`） |
| our_task_id | public_task_id | |

## 渠道账单（`--vendor`）

- **日汇总**：`bill_day, amount`，可选 `opening, closing`。有期初和期末时，会检查余额是否连续。
- **逐笔**：`upstream_task_id, completed_at|bill_day, amount`。
- 别名：amount 可以写成 consumption、消耗额；opening 可以写成 期初；closing 可以写成 期末。
- 账单金额必须先换算成和 list_yuan 同一个口径（官方原价）。如果账单给的是折后价，先除以折扣，并在报告里注明。

## 判定

- `verdict = pass`：合计差异率的绝对值小于 `--threshold`（默认 0.01）。
- `needs_per_task`：合计差异率达到或超过阈值。
- `no_vendor`：没有提供账单。

## 差异类型（discrepancies.csv）

| type | 含义 |
|---|---|
| daily_diff_large | 单日差异率的绝对值 ≥ 5%，且差额绝对值 ≥ 100 元 |
| missing_vendor_day / missing_ours_day | 某一天只有一方有数 |
| balance_adjustment | 当日期初 ≠ 前一日期末（充值或重置） |
| failed_with_charge | 我方任务失败，但仍扣了客户的钱 |
| duplicate | 同一个上游 ID 在任一方出现多次（逐笔） |
| missing_vendor | 我方有原价，账单里没有（逐笔） |
| missing_ours | 账单有，我方没有：创建超时、孤儿任务（逐笔） |
| failed_but_vendor_charged | 我方失败，但上游扣了费（逐笔） |
| amount_diff | 同一个 ID 金额相差超过 0.01 元（逐笔） |
| time_boundary_diff | 同一个 ID 在双方落在不同日（逐笔） |

## 输出

- `summary.json`：窗口、判定、四组汇总、差异计数
- `daily.csv`、`by_model.csv`、`discrepancies.csv`
- `report.md`：可以直接作为汇总报告

推送飞书前，用 `by_model.csv` 和 `daily.csv` 复算报告里的数字。
