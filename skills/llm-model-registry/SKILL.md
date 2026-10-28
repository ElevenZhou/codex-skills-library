---
name: llm-model-registry
description: 大模型选型与注册表维护。用户自有的全部大模型端点、key、模型清单都在 E:\Dev-2\本地大模型调用，本技能负责从中挑选合适的模型和渠道来调用，并维护这个目录（新增 key/节点、复测可用性、更新清单）。Use when a task needs a model other than the current assistant (GPT / Gemini / Grok / Claude / DeepSeek / Kimi / GLM / Qwen / seedance / veo / sora 等), when the user asks 用哪个模型 / 选模型 / 调用某个模型 / 换个模型 / 模型能不能用 / 测一下模型 / 加一个 key / 新节点 / 更新模型清单 / 大模型 API 汇总, or when any script needs an API key or base URL for flaios or its nodes. 出图走 local-image-generator，Grok 视频走 local-grok-video-generator-2-0，本技能负责其余所有模型以及注册表本身。
---

# 大模型选型与注册表维护

Skill version: `2026.10.23`

## 注册表在哪

```text
E:\Dev-2\本地大模型调用\
├─ README.md                    入口索引
├─ config/providers.json        机器可读：providers（端点 + key_alias + key）、models（169 个）
├─ docs/01-接入配置总表.md       端点 / key 一览（手写）
├─ docs/02-模型清单总表.md       模型 × 端可用矩阵（脚本生成）
├─ docs/03-全能key使用说明.md    主站全能 key 实测与示例
├─ docs/04-Gemini原生接口文档.md generateContent 协议（域名未填）
├─ scripts/build_summary.py     数据源：PROVIDERS / FLAIOS_ALL / SG01 / N04 / ISSUES / FILES_INDEX
├─ scripts/smoke_test.py        文本连通性自检
└─ 大模型API汇总.xlsx            给人看的汇总表（脚本生成）
```

**唯一数据源是 `scripts/build_summary.py` 顶部的数据区**；`providers.json`、`docs/02`、xlsx 都由它生成。`docs/01` 是手写的，改端点时要同步。

## 助手脚本

本技能自带 `scripts/registry.py`。所有子命令都不打印完整 key。`<via>` 是 key 别名（`K_ALL`、`K_NODE`…），或者 base_url 片段（`sg01`、`n12`、`flaios.com`…）。

```bash
R=~/.claude/skills/llm-model-registry/scripts/registry.py   # Codex 下是 ~/.codex/skills/...
py -3 $R providers                        # 端点一览（key 打码）
py -3 $R find seedance                    # 在登记清单里搜模型
py -3 $R find --category 视频
py -3 $R live sg01 --grep grok            # 实时 /v1/models
py -3 $R live K_ALL --diff                # 实时有、清单没有的模型
py -3 $R chat n12 gpt-6.1-sol "只回复 OK"   # 发一条文本，费用极低
py -3 $R probe-video                      # 主站视频模型零成本通道探测
py -3 $R run sg01 -- node my-script.mjs   # 注入 OPENAI_API_KEY/OPENAI_BASE_URL/FLAIOS_* 后执行
```

别的程序需要 key 时，优先用 `run` 注入；在代码里读的话，按 `key_alias` 从 `providers.json` 取。**不要把 key 写进命令行、日志、提交或回复。**

## 选型（2026-10-23 状态）

先按任务类型找到对应的行，再看「验证」列。「已验证」是指这一天实测打通过；「有渠道」只代表网关能分发到上游，没有真实产出过结果。

| 需求 | 首选：端点 + 模型 | 备选 | 验证 |
| --- | --- | --- | --- |
| 通用文本 / 便宜快速 | `K_ALL` 主站 `gpt-5.4-mini`、`deepseek-chat` | `claude-haiku-4-5` | 2026-08-20 已验证 |
| 最新 GPT（GPT-6 系列） | `n12` `gpt-6.1-sol` | 主站 | 已验证，4.4s |
| 强 Claude | `n09` `claude-opus-4-6-thinking` | 主站 `claude-opus-*` | 已验证，4.4s |
| Gemini 文本 | `n10` `gemini-3-flash` | sg01 | 已验证，1.9s（主站 OpenAI chat 格式会报 `contents is not specified`） |
| Grok 文本 | `sg01` `grok-4.x` | — | 只确认列出，没测 |
| 推理 / 代码 | 主站 `deepseek-reasoner` | `gpt-5.4-mini` | 短 prompt 可能返回空，要用业务 prompt 测 |
| **静态图片** | 交给 `local-image-generator` 技能 | | 已验证（flare / sunburst / grok-image-2.0 / nano-banana-2 / gemini-3.1-flash-image） |
| **Grok 视频** | 交给 `local-grok-video-generator-2-0` 技能（sg01） | | 已验证：`grok-imagine-video` 6s ≈ $0.30，`-1.5` 6s ≈ $0.48 |
| 其他视频（seedance / veo / sora2 / gemini-omini / sd2_mx / happyhorse / Wonder-Pro） | `K_ALL` 主站 `POST /v1/videos` | — | 49 个都**有渠道**，但都没有真实出过片 |
| 视频超分 | 主站 `ali-video-super-resolution-*` | — | 有渠道，没出过片 |

不要用的：
- `n04` 的 GPT **文本**：2026-10-23 稳定性测试成功率只有 22.7%（上游过载加熔断），见 `n04-gpt稳定性测试报告.md`；n04 出图正常。
- 主站的 Grok 视频：返回 `invalid api platform: 48`；Grok 视频只走 sg01。
- `video.flaios.cn` 视频站：`K_VIDEO` 鉴权返回 401 Invalid token，生成接口没有文档，需要用户找提供方确认。
- `K_DEF`、`K_TEST`、`K_AISC`：用途不明或信息不全，用户没点名就不用。

### 选型规则

1. 用户点名了模型，就用 `find` 找出哪些端有它，再按上表挑端点；表里没有的端点，先跑 `live <via> --grep <模型>` 确认实时列表里有。
2. `/v1/models` 列出来不等于能用。正式用之前，文本模型发一条 `chat`；视频模型先 `probe-video` 看有没有渠道，再**征得用户同意**跑一次最低规格的真实生成（会花钱）。
3. 返回的模型名和请求的不一样，说明网关做了别名或路由，要如实告诉用户。
4. 失败了，先换同模型的另一个端点（主站 ↔ 节点），再考虑换模型；换了模型必须告诉用户，不能假装成功。
5. 错误码速查：`model_not_found` / `No available channel` 是当前分组没有渠道；`auth_unavailable` 是上游鉴权或熔断，等 1–2 分钟或换节点；`server_is_overloaded` 是上游过载。

## 维护注册表

用户给了新 key、新节点、新模型清单，或者目录里出现了新的 txt / md / xlsx 时：

1. **备份**：`cp -r "E:/Dev-2/本地大模型调用" "C:/tmp/本地大模型调用.bak-<日期>"`。
2. **改数据区**（`scripts/build_summary.py`）：
   - 新端点 / key → `PROVIDERS` 加一条 `dict(name, usage, base_url, key_alias, key, status, note, source)`；同一把 key 沿用已有的 `key_alias`。
   - 新模型清单 → `FLAIOS_ALL` / `SG01` / `N04` / `SELF_HOSTED`；新节点要加新的清单列表，得同时改 `build_union()` 和输出列。
   - 测试结论、冲突、待办 → `ISSUES`；新文件的去向 → `FILES_INDEX`。
   - 更新 `UPDATED` 日期。
3. **重新生成**：`cd "E:/Dev-2/本地大模型调用" && py -3 scripts/build_summary.py`，然后确认 `providers.json` 里的条目数对得上。
4. **同步手写文档**：`docs/01` 的一览表和节点章节；`README.md` 的「已知问题」和「变更记录」各加一行。
5. **复测**：新端点跑 `live`、`chat`；涉及视频就跑 `probe-video`。结论写回 `ISSUES`，再重跑第 3 步。
6. **定期体检**（用户要求或距上次超过一个月）：对 K_ALL 跑 `live --diff`（模型增减），对 n09 / n10 / n12 / sg01 各跑一条 `chat`，再跑 `probe-video`；只把**状态变化**写回注册表，并按全局约定推送飞书（失败、推翻旧结论的优先发）。

原始 key 文件合并进注册表以后，留不留原件由用户决定，不要擅自删除。

## 安全

- 这个目录全是明文 key（`README.md` 首页也写了两把）。不要整目录外发、截图，也不要 `git push` 到公开仓库。
- 回复、日志、飞书里只写 key 别名或打码（`registry.py` 的 `mask` 格式），不写完整 key。
- 视频站的 AK/SK 属于凭证，也不要外发。
