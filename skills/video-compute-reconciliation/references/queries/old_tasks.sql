-- 老站逐笔导出（仅在需要逐笔匹配时用）。private_data 只取叶子字段，不要整列导出（里面有上游密钥）。
START TRANSACTION READ ONLY;
SELECT task_id AS our_task_id, upstream_task_id, channel_id, user_id,
       JSON_UNQUOTE(JSON_EXTRACT(properties,'$.origin_model_name')) AS model,
       status, billing_status, total_tokens AS tokens,
       FROM_UNIXTIME(submit_time) AS submit_at, FROM_UNIXTIME(finish_time) AS completed_at,
       JSON_UNQUOTE(JSON_EXTRACT(private_data,'$.billing_context.group_ratio')) AS group_ratio,
       JSON_UNQUOTE(JSON_EXTRACT(private_data,'$.billing_context.video_resolution')) AS resolution,
       ROUND(final_quota / CAST(JSON_UNQUOTE(JSON_EXTRACT(private_data,'$.billing_context.group_ratio')) AS DECIMAL(10,4)) / 500000, 6) AS list_yuan,
       ROUND(final_quota/500000, 6) AS cust_yuan,
       LEFT(REPLACE(REPLACE(IFNULL(fail_reason,''),'\t',' '),'\n',' '),200) AS fail_reason
FROM tasks
WHERE channel_id IN ({CHANNEL_IDS})
  AND finish_time >= UNIX_TIMESTAMP('{START}') AND finish_time < UNIX_TIMESTAMP('{END}')
ORDER BY finish_time;
COMMIT;
