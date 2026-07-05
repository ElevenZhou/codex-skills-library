#!/usr/bin/env python3
import argparse
import json
import os
import re
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional
from urllib import error, request


SEOUL_HOST = "150.109.233.152"
SSH_BIND_IP = "192.168.31.68"
SSH_KEY_PATH = r"C:\Users\AprilWu\.ssh\ShouerUbunutNewapi.pem"
SSH_USER = "ubuntu"
FEISHU_MEMORY_PATH = Path(r"C:\Users\AprilWu\memory\preferences\feishu-reminders.md")

HTTP_TARGETS = [
    {"name": "api.yumiai.art", "url": "https://api.yumiai.art", "ok_codes": {302}},
    {"name": "api1.yumiai.art", "url": "https://api1.yumiai.art", "ok_codes": {302}},
    {"name": "api100.yumiai.art", "url": "https://api100.yumiai.art", "ok_codes": {302}},
    {"name": "flaios.com", "url": "https://flaios.com", "ok_codes": {200}},
    {"name": "sub2api.flaios.com", "url": "https://sub2api.flaios.com", "ok_codes": {200}},
]

REQUIRED_CONTAINERS = {
    "new-api",
    "new-api-caddy",
    "new-api-mysql",
    "new-api-redis",
    "sub2api",
    "sub2api-redis",
    "sub2api-postgres",
    "flaios-jimmyai-adapter",
    "flaios-kmood-adapter",
    "flaios-tokensfactory-omni-adapter",
}

REMOTE_SCRIPT = r"""
set -u
echo '===UPTIME==='
uptime
echo '===FREE_M==='
free -m
echo '===DF_ROOT==='
df -P -h /
echo '===DOCKER_PS==='
if ! sudo -n docker ps -a --format '{{.Names}}|{{.Status}}|{{.Image}}' 2>&1; then
  true
fi
"""


class NoRedirect(request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


@dataclass
class HttpResult:
    name: str
    url: str
    ok: bool
    code: Optional[int]
    detail: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Check Seoul server HTTP endpoints and Docker containers, then optionally notify Feishu."
    )
    parser.add_argument("--notify", action="store_true", help="Send the report to the Feishu webhook.")
    parser.add_argument("--no-notify", action="store_true", help="Do not send the report to the Feishu webhook.")
    parser.add_argument("--webhook", help="Override the Feishu webhook URL.")
    parser.add_argument("--timeout", type=int, default=20, help="Timeout in seconds for HTTP and SSH checks.")
    parser.add_argument("--json", action="store_true", help="Print machine-readable JSON in addition to the text report.")
    return parser.parse_args()


def choose_notify(args: argparse.Namespace) -> bool:
    if args.no_notify:
        return False
    return args.notify


def resolve_webhook(explicit: Optional[str]) -> Optional[str]:
    if explicit:
        return explicit.strip()
    env_webhook = os.environ.get("FEISHU_COMPANY_IMPORTANT_WEBHOOK", "").strip()
    if env_webhook:
        return env_webhook
    if FEISHU_MEMORY_PATH.exists():
        text = FEISHU_MEMORY_PATH.read_text(encoding="utf-8")
        match = re.search(r"https://open\.feishu\.cn/open-apis/bot/v2/hook/[A-Za-z0-9-]+", text)
        if match:
            return match.group(0)
    return None


def check_http(url: str, ok_codes: set, timeout: int) -> HttpResult:
    opener = request.build_opener(NoRedirect)
    req = request.Request(url, headers={"User-Agent": "seoul-server-status-check/1.0"})
    try:
        with opener.open(req, timeout=timeout) as response:
            code = response.getcode()
            ok = code in ok_codes
            return HttpResult(url=url, name=url, ok=ok, code=code, detail=f"HTTP {code}")
    except error.HTTPError as exc:
        ok = exc.code in ok_codes
        location = exc.headers.get("Location")
        detail = f"HTTP {exc.code}"
        if location:
            detail += f" -> {location}"
        return HttpResult(url=url, name=url, ok=ok, code=exc.code, detail=detail)
    except Exception as exc:
        return HttpResult(url=url, name=url, ok=False, code=None, detail=f"ERROR: {exc}")


def run_ssh(timeout: int) -> str:
    cmd = [
        "ssh",
        "-o",
        "BatchMode=yes",
        "-o",
        f"ConnectTimeout={timeout}",
        "-b",
        SSH_BIND_IP,
        "-i",
        SSH_KEY_PATH,
        f"{SSH_USER}@{SEOUL_HOST}",
        REMOTE_SCRIPT,
    ]
    completed = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=timeout + 10,
        check=False,
    )
    if completed.returncode != 0:
        stderr = completed.stderr.strip() or "unknown ssh error"
        raise RuntimeError(f"SSH check failed: {stderr}")
    return completed.stdout


def parse_sections(raw: str) -> Dict[str, str]:
    sections: Dict[str, List[str]] = {}
    current = None
    for line in raw.splitlines():
        if line.startswith("===") and line.endswith("==="):
            current = line.strip("=").strip()
            sections[current] = []
            continue
        if current:
            sections[current].append(line)
    return {key: "\n".join(value).strip() for key, value in sections.items()}


def parse_memory(free_text: str) -> Dict[str, Optional[float]]:
    for line in free_text.splitlines():
        if line.strip().startswith("Mem:"):
            parts = re.split(r"\s+", line.strip())
            if len(parts) >= 7:
                total = float(parts[1])
                available = float(parts[6])
                used_pct = round((total - available) / total * 100, 1) if total else None
                return {"total_mb": total, "available_mb": available, "used_pct": used_pct}
    return {"total_mb": None, "available_mb": None, "used_pct": None}


def parse_disk(df_text: str) -> Dict[str, Optional[str]]:
    lines = [line for line in df_text.splitlines() if line.strip()]
    if len(lines) >= 2:
        parts = re.split(r"\s+", lines[1].strip())
        if len(parts) >= 6:
            return {
                "filesystem": parts[0],
                "size": parts[1],
                "used": parts[2],
                "avail": parts[3],
                "used_pct": parts[4],
                "mount": parts[5],
            }
    return {"filesystem": None, "size": None, "used": None, "avail": None, "used_pct": None, "mount": None}


def parse_containers(docker_text: str) -> Dict[str, Dict[str, str]]:
    containers: Dict[str, Dict[str, str]] = {}
    for line in docker_text.splitlines():
        if not line.strip():
            continue
        parts = line.split("|", 2)
        if len(parts) != 3:
            continue
        name, status, image = parts
        containers[name] = {"status": status, "image": image}
    return containers


def parse_docker_error(docker_text: str) -> Optional[str]:
    lines = []
    for line in docker_text.splitlines():
        if "|" not in line and line.strip():
            lines.append(line.strip())
    if lines:
        return " ".join(lines)
    return None


def evaluate(http_results: List[HttpResult], containers: Dict[str, Dict[str, str]], memory: Dict[str, Optional[float]], disk: Dict[str, Optional[str]], ssh_error: Optional[str], docker_error: Optional[str]) -> Dict[str, object]:
    issues: List[str] = []
    for item in http_results:
        if not item.ok:
            issues.append(f"HTTP {item.url} {item.detail}")

    missing: List[str] = []
    stopped: List[str] = []
    if docker_error:
        issues.append(f"Docker inspection failed: {docker_error}")
    else:
        missing = sorted(name for name in REQUIRED_CONTAINERS if name not in containers)
        stopped = sorted(
            name for name, info in containers.items() if name in REQUIRED_CONTAINERS and "Up" not in info["status"]
        )
        for name in missing:
            issues.append(f"Missing container: {name}")
        for name in stopped:
            issues.append(f"Container not running: {name} ({containers[name]['status']})")

    mem_used = memory.get("used_pct")
    if isinstance(mem_used, float) and mem_used >= 92:
        issues.append(f"Memory pressure high: {mem_used}% used")

    disk_used = disk.get("used_pct")
    if isinstance(disk_used, str):
        try:
            disk_pct = int(disk_used.rstrip("%"))
            if disk_pct >= 90:
                issues.append(f"Disk usage high on /: {disk_used}")
        except ValueError:
            pass

    if ssh_error:
        issues.append(ssh_error)

    if ssh_error:
        overall = "down"
    elif issues:
        overall = "degraded"
    else:
        overall = "healthy"

    return {"overall": overall, "issues": issues, "missing": missing, "stopped": stopped}


def make_report(
    checked_at: str,
    http_results: List[HttpResult],
    sections: Dict[str, str],
    containers: Dict[str, Dict[str, str]],
    memory: Dict[str, Optional[float]],
    disk: Dict[str, Optional[str]],
    summary: Dict[str, object],
    ssh_error: Optional[str],
    docker_error: Optional[str],
) -> str:
    icons = {"healthy": "OK", "degraded": "WARN", "down": "DOWN"}
    lines = [f"[{icons[summary['overall']]}] Seoul server status @ {checked_at}"]
    uptime = sections.get("UPTIME") or "unavailable"
    lines.append(f"Host: {SEOUL_HOST}")
    lines.append(f"Uptime: {uptime}")

    mem_text = "unknown"
    if memory.get("total_mb") and memory.get("available_mb") is not None:
        mem_text = f"{memory['used_pct']}% used, {int(memory['available_mb'])}MB available"
    lines.append(f"Memory: {mem_text}")

    disk_text = "unknown"
    if disk.get("size"):
        disk_text = f"{disk['used_pct']} used ({disk['used']}/{disk['size']})"
    lines.append(f"Disk /: {disk_text}")

    lines.append("HTTP:")
    for target, result in zip(HTTP_TARGETS, http_results):
        marker = "OK" if result.ok else "BAD"
        lines.append(f"- {marker} {target['name']}: {result.detail}")

    lines.append("Containers:")
    if docker_error:
        lines.append(f"- BAD docker inspection: {docker_error}")
    else:
        for name in sorted(REQUIRED_CONTAINERS):
            info = containers.get(name)
            if not info:
                lines.append(f"- BAD {name}: missing")
                continue
            marker = "OK" if "Up" in info["status"] else "BAD"
            lines.append(f"- {marker} {name}: {info['status']}")

    if ssh_error:
        lines.append(f"SSH: {ssh_error}")

    issues = summary.get("issues", [])
    if issues:
        lines.append("Issues:")
        for issue in issues:
            lines.append(f"- {issue}")
    else:
        lines.append("Issues: none")

    return "\n".join(lines)


def post_to_feishu(webhook: str, text: str, timeout: int) -> None:
    payload = json.dumps({"msg_type": "text", "content": {"text": text}}, ensure_ascii=False).encode("utf-8")
    req = request.Request(
        webhook,
        data=payload,
        headers={"Content-Type": "application/json; charset=utf-8"},
        method="POST",
    )
    with request.urlopen(req, timeout=timeout) as response:
        body = response.read().decode("utf-8", errors="replace")
        data = json.loads(body)
        if data.get("code") != 0:
            raise RuntimeError(f"Feishu webhook rejected the message: {body}")


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    args = parse_args()
    notify = choose_notify(args)
    webhook = resolve_webhook(args.webhook) if notify else None
    checked_at = datetime.now(timezone.utc).astimezone().strftime("%Y-%m-%d %H:%M:%S %z")

    http_results: List[HttpResult] = []
    for target in HTTP_TARGETS:
        result = check_http(target["url"], target["ok_codes"], args.timeout)
        result.name = target["name"]
        http_results.append(result)

    sections: Dict[str, str] = {}
    containers: Dict[str, Dict[str, str]] = {}
    memory = {"total_mb": None, "available_mb": None, "used_pct": None}
    disk = {"filesystem": None, "size": None, "used": None, "avail": None, "used_pct": None, "mount": None}
    ssh_error = None
    docker_error = None
    try:
        sections = parse_sections(run_ssh(args.timeout))
        memory = parse_memory(sections.get("FREE_M", ""))
        disk = parse_disk(sections.get("DF_ROOT", ""))
        docker_text = sections.get("DOCKER_PS", "")
        containers = parse_containers(docker_text)
        docker_error = parse_docker_error(docker_text)
    except Exception as exc:
        ssh_error = str(exc)

    summary = evaluate(http_results, containers, memory, disk, ssh_error, docker_error)
    report = make_report(checked_at, http_results, sections, containers, memory, disk, summary, ssh_error, docker_error)

    print(report)
    if args.json:
        payload = {
            "checked_at": checked_at,
            "overall": summary["overall"],
            "issues": summary["issues"],
            "http": [result.__dict__ for result in http_results],
            "containers": containers,
            "memory": memory,
            "disk": disk,
            "ssh_error": ssh_error,
            "docker_error": docker_error,
        }
        print(json.dumps(payload, ensure_ascii=False, indent=2))

    if notify:
        if not webhook:
            print("Feishu webhook not found; skipping notification.", file=sys.stderr)
            return 2
        post_to_feishu(webhook, report, args.timeout)
        print("Feishu notification sent.")

    return 0 if summary["overall"] == "healthy" else 1


if __name__ == "__main__":
    sys.exit(main())
