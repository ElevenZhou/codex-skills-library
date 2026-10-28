# -*- coding: utf-8 -*-
"""
大模型注册表助手：读 E:\\Dev-2\\本地大模型调用\\config\\providers.json，选端点、查模型、做零成本探测。

任何子命令都不打印完整 key。需要 key 的程序用 `run` 子命令注入环境变量。

用法：
  py -3 registry.py providers
  py -3 registry.py find seedance            # 在登记清单里搜模型
  py -3 registry.py find --category 视频
  py -3 registry.py live sg01 --grep grok    # 实时 /v1/models
  py -3 registry.py probe-video              # 主站视频模型零成本通道探测
  py -3 registry.py chat n12 gpt-6.1-sol "只回复 OK"
  py -3 registry.py run sg01 -- node my-script.mjs   # 注入 OPENAI_* / FLAIOS_* 后执行

<via> 选择端点：key 别名（K_ALL、K_NODE…）或 base_url 片段（sg01、n12、flaios.com…）。
注册表目录可用环境变量 LLM_REGISTRY_DIR 覆盖。
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

REGISTRY_DIR = Path(os.environ.get("LLM_REGISTRY_DIR", r"E:\Dev-2\本地大模型调用"))
PROVIDERS_JSON = REGISTRY_DIR / "config" / "providers.json"
VIDEO_HINTS = ("video", "veo", "sora", "seedance", "omini", "omni", "wonder", "happyhorse", "sd2_mx")

for stream in (sys.stdout, sys.stderr):
    if hasattr(stream, "reconfigure"):
        stream.reconfigure(encoding="utf-8")


def load():
    if not PROVIDERS_JSON.exists():
        sys.exit(f"找不到 {PROVIDERS_JSON}；先在注册表目录运行 py -3 scripts/build_summary.py")
    return json.loads(PROVIDERS_JSON.read_text(encoding="utf-8"))


def mask(key: str) -> str:
    return f"{key[:6]}…{key[-4:]}" if key and len(key) > 12 else "***"


def api_base(url: str) -> str:
    url = url.rstrip("/")
    if url.endswith("/chat/completions"):
        url = url[: -len("/chat/completions")]
    return url if url.endswith("/v1") else url + "/v1"


def resolve(cfg, via: str):
    """返回 (provider, base_url_with_v1, key)。别名精确匹配优先，其次 base_url 片段。"""
    providers = cfg["providers"]
    hits = [p for p in providers if p["key_alias"].lower() == via.lower()]
    if not hits:
        hits = [p for p in providers if via.lower() in p["base_url"].lower() or via in p["name"]]
    if not hits:
        sys.exit(f"没有匹配 {via!r} 的端点；先运行 providers 看看有哪些")
    p = hits[0]
    return p, api_base(p["base_url"]), p["key"]


def http(method, url, key, body=None, timeout=60):
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, method=method, headers={
        "Authorization": f"Bearer {key}", "Content-Type": "application/json", "User-Agent": "curl/8",
    })
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, r.read().decode(errors="replace")
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode(errors="replace")
    except Exception as e:  # 网络 / TLS
        return "ERR", str(e)


def cmd_providers(cfg, _args):
    for p in cfg["providers"]:
        print(f"{p['key_alias']:11s} {p['status']:6s} {p['base_url']:45s} {p['name']} | {p['usage']} | key {mask(p['key'])}")


def cmd_find(cfg, args):
    q = (args.keyword or "").lower()
    rows = [m for m in cfg["models"]
            if q in m["name"].lower() and (not args.category or args.category in m["category"])]
    for m in rows:
        note = f" | {m['note']}" if m["note"] else ""
        print(f"{m['name']:42s} {m['category']:8s} 端：{m['ends']:22s} 协议：{m['endpoint_types']}{note}")
    print(f"共 {len(rows)} 个（登记清单，更新于 {cfg.get('updated')}；是否真能调用要实测）")


def live_ids(base, key):
    status, body = http("GET", f"{base}/models", key, timeout=30)
    if status != 200:
        sys.exit(f"/models 失败：{status} {body[:200]}")
    return sorted(m["id"] for m in json.loads(body).get("data", []))


def cmd_live(cfg, args):
    p, base, key = resolve(cfg, args.via)
    ids = live_ids(base, key)
    shown = [i for i in ids if not args.grep or args.grep.lower() in i.lower()]
    print(f"{base}（{p['key_alias']}）实时 {len(ids)} 个模型，显示 {len(shown)} 个：")
    for i in shown:
        print(" ", i)
    if args.diff:
        listed = {m["name"] for m in cfg["models"]}
        new = [i for i in ids if i not in listed]
        print(f"\n实时有、登记清单没有：{len(new)} 个")
        for i in new:
            print(" +", i)


def cmd_probe_video(cfg, args):
    """不带 prompt 调 /v1/videos：有渠道 → 参数校验错；无渠道 → model_not_found。不出片、不扣费。"""
    p, base, key = resolve(cfg, args.via)
    models = args.models or [i for i in live_ids(base, key) if any(h in i.lower() for h in VIDEO_HINTS)]
    status, body = http("POST", f"{base}/videos", key, {"model": "nonexistent-probe-model-xyz"})
    print(f"对照（假模型）：{status} {body[:160]}")
    if "model_not_found" not in body and "No available channel" not in body:
        print("⚠️ 假模型没有返回 model_not_found，这个网关先做参数校验，下面的结果不能说明有渠道。")

    def probe(m):
        for attempt in range(3):
            s, b = http("POST", f"{base}/videos", key, {"model": m})
            if s != "ERR":
                break
            time.sleep(2)
        if "prompt" in b.lower() and s == 400:
            verdict = "有渠道"
        elif "model_not_found" in b or "No available channel" in b:
            verdict = "无渠道"
        else:
            verdict = "异常"
        return f"{verdict:4s} {m:40s} {s} {b[:140]}"

    with ThreadPoolExecutor(6) as ex:
        for line in ex.map(probe, models):
            print(line)
    print("\n「有渠道」只代表网关能分发到上游，不代表上游能出片；正式用前做一次低规格真实生成。")


def cmd_chat(cfg, args):
    p, base, key = resolve(cfg, args.via)
    t = time.time()
    status, body = http("POST", f"{base}/chat/completions", key, {
        "model": args.model, "messages": [{"role": "user", "content": args.prompt}], "max_tokens": args.max_tokens,
    }, timeout=180)
    took = time.time() - t
    if status == 200:
        d = json.loads(body)
        msg = d["choices"][0]["message"]
        print(f"OK {took:.1f}s model={d.get('model')} usage={d.get('usage')}")
        print(msg.get("content"))
    else:
        print(f"FAIL {status} {took:.1f}s {body[:400]}")
        sys.exit(1)


def cmd_run(cfg, args):
    p, base, key = resolve(cfg, args.via)
    if not args.command:
        sys.exit("用法：registry.py run <via> -- <command ...>")
    env = dict(os.environ, OPENAI_API_KEY=key, OPENAI_BASE_URL=base, FLAIOS_API_KEY=key, FLAIOS_BASE_URL=base)
    print(f"[registry] 注入 {p['key_alias']} @ {base}", file=sys.stderr)
    sys.exit(subprocess.call(args.command, env=env))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("providers")
    f = sub.add_parser("find"); f.add_argument("keyword", nargs="?"); f.add_argument("--category")
    l = sub.add_parser("live"); l.add_argument("via"); l.add_argument("--grep"); l.add_argument("--diff", action="store_true")
    v = sub.add_parser("probe-video"); v.add_argument("--via", default="K_ALL"); v.add_argument("models", nargs="*")
    c = sub.add_parser("chat"); c.add_argument("via"); c.add_argument("model"); c.add_argument("prompt")
    c.add_argument("--max-tokens", type=int, default=200)
    r = sub.add_parser("run"); r.add_argument("via"); r.add_argument("command", nargs=argparse.REMAINDER)
    args = ap.parse_args()
    if args.cmd == "run" and args.command[:1] == ["--"]:
        args.command = args.command[1:]
    cfg = load()
    {"providers": cmd_providers, "find": cmd_find, "live": cmd_live, "probe-video": cmd_probe_video,
     "chat": cmd_chat, "run": cmd_run}[args.cmd](cfg, args)


if __name__ == "__main__":
    main()
