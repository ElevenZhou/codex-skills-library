# 只读查询模板

先把 `{CHANNEL_IDS}`、`{START}`、`{END}` 替换成实际值（时间为北京时间半开区间），SQL 从本地通过 stdin 传给服务器，服务器上不落文件。

老站（东京）：

```bash
sed -e 's/{CHANNEL_IDS}/93/' -e 's/{START}/2026-09-29/' -e 's/{END}/2026-10-10/' old_daily.sql \
 | ssh -i <tokyo.pem> ubuntu@43.130.235.209 'P=$(sudo docker exec new-api-mysql printenv MYSQL_ROOT_PASSWORD); sudo docker exec -i -e MYSQL_PWD="$P" new-api-mysql mysql -uroot --default-character-set=utf8mb4 newapi' > old_daily.tsv
```

新站（上海）：

```bash
sed -e 's/{CHANNEL_IDS}/6/' -e 's/{START}/2026-09-29/' -e 's/{END}/2026-10-10/' new_daily.sql \
 | ssh -i <zhou2026.pem> ubuntu@111.229.213.213 'U=$(sudo docker exec deploy-postgres-1 printenv POSTGRES_USER); D=$(sudo docker exec deploy-postgres-1 printenv POSTGRES_DB); sudo docker exec -i -e PGOPTIONS="-c default_transaction_read_only=on" deploy-postgres-1 psql -X -U "$U" -d "$D" -v ON_ERROR_STOP=1 -P pager=off' > new_daily.tsv
```

新站输出里混有二维码横幅和 psql 提示行，`reconcile.py` 读取时会自动跳过，不用手工清理。

Windows 上 pem 文件要先复制到 `/tmp` 并 `chmod 600`，用完删掉。
