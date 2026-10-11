-- 新站（VideoAi-New / Postgres）日 × 模型 × 状态聚合。以 PGOPTIONS 只读方式运行。
SET TIME ZONE 'Asia/Shanghai';
\pset format unaligned
\pset fieldsep '\t'
SELECT date(t.completed_at) AS bill_day, t.model, t.status, count(*) AS n,
       coalesce(sum((t.usage->>'total_tokens')::bigint),0) AS tokens,
       round(sum(t.official_amount)/1e6,4) AS list_yuan,
       round(coalesce(sum(-l.net),0)/1e6,4) AS cust_yuan
FROM video_tasks t
LEFT JOIN (SELECT task_id, sum(amount) AS net FROM billing_ledger GROUP BY task_id) l ON l.task_id = t.id
WHERE t.channel_id IN ({CHANNEL_IDS})
  AND t.completed_at >= '{START}' AND t.completed_at < '{END}'
  AND t.status IN ('succeeded','failed')
GROUP BY 1,2,3 ORDER BY 1,2,3;
