---
name: video-compute-reconciliation
description: 对视频生成双站（老站 Flaios-Video / 新站 VideoAi-New）或多渠道做只读算力、任务、账务和渠道账单对账。Use when reconciling Flaios-Video and VideoAi-New against a vendor bill (智算谷/zsg/zhisuangu and future channels), matching vendor Excel/CSV/API/screenshot bills, checking daily 00:00 Asia/Shanghai consumption, computing cost/margin under a vendor discount, or onboarding a new video channel into reconciliation.
---

# 视频算力对账

把老站、新站和渠道账单统一到同一套口径，输出四组数据：老站、新站、合计、渠道账单。全程只读：不写生产、不重跑任务、不补账、不改账、不改价。

## 工作流

1. **锁定范围。** 先列出站点、生产主机、数据库、渠道名、站内渠道 ID、适配器和真实上游，再用账单反推范围：哪几个渠道加起来能对上账单，范围就是哪几个。渠道 ID 只在所属站点内有效。上游相同但经第三方结算的渠道不在同一张账单里（见 `references/site-profiles.md` 的 ch94）。
2. **读资料。** 读两个项目的 README、运维手册、历史对账脚本、表结构和渠道配置，先确认实际字段再写 SQL。
3. **只读核实生产。** 只执行 `SELECT`、`SHOW`、`\d`、容器状态和时区检查。老站 SQL 包在 `START TRANSACTION READ ONLY` 里；新站 psql 设置 `PGOPTIONS=-c default_transaction_read_only=on`。凭据从本机安全文件读取，不要打印连接串或环境变量全集（`printenv` 必须带 grep，并且排除 `DATABASE_URL`）。
4. **确定口径（最容易错）：**
   - **金额口径**：先判断账单的"消耗额"是官方原价还是折后价。做法是拿两站的官方原价逐日对比账单，有几天能对到分，就说明账单是原价。是原价时，实际成本 = 消耗额 × 折扣（如 0.77）；**不要**用 ÷0.77 反算。只有逐日对比证明账单是折后价时才反算。
   - **折扣窗口**：官方对特定模型、时段的折扣（如 fast/mini 在 10-09 之前的折扣）一般已经算进站内原价单价，不要再额外套一次。合同折扣（0.77）只在最后算成本时乘一次。
   - **日切**：按任务完成时间切北京自然日 `[00:00, 24:00)`。账单截止时刻不到 24:00 的那天标为 `partial_day`，只要与截止时刻存疑，就整天排除，不参与结论。
5. **导出。** 用 `references/queries/` 里的模板，先导出日 × 模型 × 状态的聚合。渠道提供逐笔账单时，再导出逐笔任务，以上游任务 ID 为主键。
6. **跑脚本。** 运行 `scripts/reconcile.py`，得到四组汇总、逐日对照、分模型数据、毛利、差异清单和报告。
7. **分级处理：**
   - 合计差异率 < `--threshold`（默认 1%）：判定通过，不做逐笔核对，只列出异常日。
   - ≥ 阈值，或单日 |差异率| ≥ 5% 且金额 ≥ 100 元：要求渠道提供逐笔账单，或经用户同意只读调用上游任务列表接口，按上游任务 ID 逐笔匹配。
8. **检查项。** 缺单（我方有上游无 / 上游有我方无）、重复、金额差异、失败但上游计费、退款、悬空 hold、重试或改派（reroute）、跨日、余额跳增（账单期初 ≠ 前一日期末）、模型或折扣不一致。
9. **交付。** 输出放在项目的 `outputs/reconciliation/<渠道>-<起>-<止>/` 目录。重要结论推送飞书：首行写结论，附数字和后续动作；中文正文先写进 JSON 文件，再用 `--data-binary @file` 发送。推送前从明细 CSV 复算报告里的每个数字。

## 站点与渠道

渠道资料、表字段、金额公式和环境坑都记录在 [references/site-profiles.md](references/site-profiles.md)。新增渠道时按其中的「新渠道接入清单」补一节，不要复制旧渠道的 ID 或折扣。

## 脚本

```powershell
py -3 scripts/reconcile.py --old old_daily.tsv --new new_daily.tsv --vendor vendor_daily.csv `
  --start 2026-09-29 --end 2026-10-10 --discount 0.77 --threshold 0.01 --output out
```

输入格式和差异标记的含义见 [references/data-contract.md](references/data-contract.md)。回归样例在 `tests/fixtures/zsg-20260929-20261009/`；脚本改动后运行 `py -3 scripts/reconcile.py --selftest`。

## 安全边界

生产变更、数据库写入、任务提交、补账、改价、余额调整、删除和重跑，都需要当次明确授权。截图只能用于日汇总和余额滚动校验，不能当作逐笔账单。原始请求体、密钥、Bearer、客户内容和完整上游响应不得写入技能仓库或交付报告。老站 `tasks.private_data` 里存着上游密钥，只能用 `JSON_EXTRACT` 取叶子字段。
