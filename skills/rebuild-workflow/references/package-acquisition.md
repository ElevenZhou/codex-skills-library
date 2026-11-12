# APK 原包获取规则

当负责人只提供应用名称，或只提供 Google Play 链接而没有本地 APK/XAPK/APKS 时，可先补齐原包输入，再进入 S0/S1。

## 来源优先级

1. 负责人提供的自有归档、构建产物或官方 Google Play 下载结果。
2. 由 Google Play 链接解析出的包名，再到 APKPure 等可信第三方商店查找对应版本。
3. 只有应用名称时，先核对开发者、包名、图标、版本和地区，再定位 APKPure 页面；不能只凭名称直接下载。

APKPure 仅作为原包获取来源，不等同于官方来源。报告中必须同时记录：来源 URL、访问日期、应用名称、开发者、包名、版本号、ABI/分包情况、文件名和 SHA-256。若签名证书可取得，记录证书摘要并与已知官方包或同版本证据比对。

## 下载门禁

- 下载前确认目标属于负责人声明的自有产品或明确授权范围；下载本身不等于获得逆向、动态、联网或重建授权。
- Google Play 链接优先用于确认包名和开发者；只有名称时必须做开发者、图标、包名和版本交叉核对。
- 页面无法确认包名/版本、出现多个同名应用、签名不一致、来源跳转异常或文件哈希不稳定时，停止并标记 `blocked`，不要猜测。
- 不绕过登录、付费墙、验证码、风控或地区限制；不下载来路不明的修改版、破解包、注入包或带额外权限的重打包文件。
- APKPure 下载的包先保存为原始证据，计算 SHA-256，再复制到项目输入目录；不要直接覆盖已有原包。
- 若只有 APK 而官方页面显示 XAPK/APKS 或多 ABI 分包，记录 `PARTIAL`，并在 `scope.md` 登记缺失分包对资源和运行时结论的影响。

## 记录模板

```text
package_source:
  input: app-name | google-play-url
  source_url: <Google Play or APKPure URL>
  source_kind: official | third-party
  accessed_at: YYYY-MM-DD
  app_name: <verified display name>
  developer: <verified developer>
  package_name: <applicationId>
  version: <version name/code>
  artifact: <APK/XAPK/APKS filename>
  sha256: <full hash>
  signature_digest: <if available>
  completeness: full | partial
  notes: <mismatch, missing split, or verification limits>
```
