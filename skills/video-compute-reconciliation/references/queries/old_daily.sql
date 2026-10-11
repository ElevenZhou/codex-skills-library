-- 老站（NewAPI / MySQL）日 × 模型 × 状态聚合。会话时区 +08:00。
-- 替换 {CHANNEL_IDS}、{START}、{END}（半开区间，北京时间 'YYYY-MM-DD'）。
START TRANSACTION READ ONLY;
SELECT DATE(FROM_UNIXTIME(finish_time)) AS bill_day,
       JSON_UNQUOTE(JSON_EXTRACT(properties,'$.origin_model_name')) AS model,
       status,
       COUNT(*) AS n,
       IFNULL(SUM(total_tokens),0) AS tokens,
       ROUND(IFNULL(SUM(final_quota / CAST(JSON_UNQUOTE(JSON_EXTRACT(private_data,'$.billing_context.group_ratio')) AS DECIMAL(10,4))),0)/500000,4) AS list_yuan,
       ROUND(IFNULL(SUM(final_quota),0)/500000,4) AS cust_yuan
FROM tasks
WHERE channel_id IN ({CHANNEL_IDS})
  AND finish_time >= UNIX_TIMESTAMP('{START}') AND finish_time < UNIX_TIMESTAMP('{END}')
  AND status IN ('SUCCESS','FAILURE')
GROUP BY 1,2,3 ORDER BY 1,2,3;
COMMIT;
