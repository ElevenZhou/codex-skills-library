-- 新站逐笔导出（仅在需要逐笔匹配时用）。
SET TIME ZONE 'Asia/Shanghai';
\pset format unaligned
\pset fieldsep '\t'
SELECT t.public_task_id AS our_task_id, t.adapter_task_id AS upstream_task_id, t.channel_id, t.user_id, t.model,
       t.status, (t.usage->>'total_tokens')::bigint AS tokens,
       t.submitted_at AS submit_at, t.completed_at,
       t.pricing_snapshot->'hold'->>'resolution' AS resolution,
       round(t.official_amount/1e6,6) AS list_yuan,
       round(coalesce(-l.net,0)/1e6,6) AS cust_yuan,
       t.account_reroute_count AS reroutes,
       (t.abandoned_at IS NOT NULL) AS abandoned
FROM video_tasks t
LEFT JOIN (SELECT task_id, sum(amount) AS net FROM billing_ledger GROUP BY task_id) l ON l.task_id = t.id
WHERE t.channel_id IN ({CHANNEL_IDS})
  AND t.completed_at >= '{START}' AND t.completed_at < '{END}'
ORDER BY t.completed_at;
