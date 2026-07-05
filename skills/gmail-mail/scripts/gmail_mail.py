#!/usr/bin/env python
"""Small Gmail API CLI for Codex mail workflows."""

from __future__ import annotations

import argparse
import base64
import json
import mimetypes
import os
import pathlib
import sys
from email.message import EmailMessage
from typing import Any


DEFAULT_SCOPE = "https://www.googleapis.com/auth/gmail.modify"
DEFAULT_BASE = pathlib.Path.home() / ".codex" / "gmail"


def _missing_dependency(name: str) -> None:
    print(
        json.dumps(
            {
                "ok": False,
                "error": "missing_dependency",
                "message": f"Python package is missing: {name}",
                "install": "python -m pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib",
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    raise SystemExit(2)


try:
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError
except ModuleNotFoundError as exc:
    _missing_dependency(exc.name or "google-api-python-client")


def out(data: Any) -> None:
    print(json.dumps(data, ensure_ascii=False, indent=2))


def account_paths(args: argparse.Namespace) -> tuple[pathlib.Path, pathlib.Path]:
    if args.account:
        base = DEFAULT_BASE / args.account
        credentials = pathlib.Path(args.credentials) if args.credentials else base / "credentials.json"
        token = pathlib.Path(args.token) if args.token else base / "token.json"
    else:
        credentials = pathlib.Path(args.credentials) if args.credentials else DEFAULT_BASE / "credentials.json"
        token = pathlib.Path(args.token) if args.token else DEFAULT_BASE / "token.json"
    return credentials.expanduser(), token.expanduser()


def scopes(args: argparse.Namespace) -> list[str]:
    if args.scopes:
        return [s.strip() for s in args.scopes.split(",") if s.strip()]
    return [DEFAULT_SCOPE]


def creds(args: argparse.Namespace) -> Credentials:
    credentials_path, token_path = account_paths(args)
    selected_scopes = scopes(args)
    credentials_path.parent.mkdir(parents=True, exist_ok=True)
    token_path.parent.mkdir(parents=True, exist_ok=True)

    current = None
    if token_path.exists():
        current = Credentials.from_authorized_user_file(str(token_path), selected_scopes)
    if current and current.valid:
        return current
    if current and current.expired and current.refresh_token:
        current.refresh(Request())
        token_path.write_text(current.to_json(), encoding="utf-8")
        return current
    if not credentials_path.exists():
        out(
            {
                "ok": False,
                "error": "credentials_file_not_found",
                "credentials": str(credentials_path),
                "next_step": "Create a Google OAuth Desktop Client JSON and save it at this path, or pass --credentials.",
            }
        )
        raise SystemExit(2)

    flow = InstalledAppFlow.from_client_secrets_file(str(credentials_path), selected_scopes)
    current = flow.run_local_server(port=0)
    token_path.write_text(current.to_json(), encoding="utf-8")
    return current


def service(args: argparse.Namespace):
    return build("gmail", "v1", credentials=creds(args))


def raw_message(message: EmailMessage) -> str:
    return base64.urlsafe_b64encode(message.as_bytes()).decode("ascii")


def make_message(args: argparse.Namespace) -> EmailMessage:
    msg = EmailMessage()
    msg["To"] = args.to
    if args.cc:
        msg["Cc"] = args.cc
    if args.bcc:
        msg["Bcc"] = args.bcc
    msg["Subject"] = args.subject
    if args.from_addr:
        msg["From"] = args.from_addr
    subtype = "html" if args.html else "plain"
    msg.set_content(args.body or "", subtype=subtype)
    for attach in args.attach or []:
        path = pathlib.Path(attach).expanduser()
        data = path.read_bytes()
        ctype, _ = mimetypes.guess_type(path.name)
        maintype, subtype2 = (ctype or "application/octet-stream").split("/", 1)
        msg.add_attachment(data, maintype=maintype, subtype=subtype2, filename=path.name)
    return msg


def headers(payload: dict[str, Any]) -> dict[str, str]:
    return {h["name"].lower(): h["value"] for h in payload.get("headers", [])}


def decode_body(data: str | None) -> str:
    if not data:
        return ""
    padding = "=" * (-len(data) % 4)
    return base64.urlsafe_b64decode((data + padding).encode("ascii")).decode("utf-8", errors="replace")


def collect_parts(part: dict[str, Any], acc: dict[str, list[str]]) -> None:
    mime = part.get("mimeType", "")
    body = part.get("body", {})
    if mime == "text/plain":
        acc["plain"].append(decode_body(body.get("data")))
    elif mime == "text/html":
        acc["html"].append(decode_body(body.get("data")))
    for child in part.get("parts", []) or []:
        collect_parts(child, acc)


def summarize_message(item: dict[str, Any]) -> dict[str, Any]:
    payload = item.get("payload", {})
    h = headers(payload)
    return {
        "id": item.get("id"),
        "threadId": item.get("threadId"),
        "labelIds": item.get("labelIds", []),
        "snippet": item.get("snippet", ""),
        "from": h.get("from", ""),
        "to": h.get("to", ""),
        "subject": h.get("subject", ""),
        "date": h.get("date", ""),
    }


def cmd_auth(args: argparse.Namespace) -> None:
    credentials_path, token_path = account_paths(args)
    c = creds(args)
    out(
        {
            "ok": True,
            "credentials": str(credentials_path),
            "token": str(token_path),
            "scopes": sorted(c.scopes or scopes(args)),
        }
    )


def cmd_profile(args: argparse.Namespace) -> None:
    svc = service(args)
    profile = svc.users().getProfile(userId="me").execute()
    out({"ok": True, "profile": profile})


def cmd_search(args: argparse.Namespace) -> None:
    svc = service(args)
    resp = svc.users().messages().list(userId="me", q=args.query, maxResults=args.limit).execute()
    ids = resp.get("messages", [])
    messages = []
    for item in ids:
        msg = svc.users().messages().get(userId="me", id=item["id"], format="metadata").execute()
        messages.append(summarize_message(msg))
    out({"ok": True, "messages": messages, "resultSizeEstimate": resp.get("resultSizeEstimate", 0)})


def cmd_read(args: argparse.Namespace) -> None:
    svc = service(args)
    msg = svc.users().messages().get(userId="me", id=args.id, format="full").execute()
    parts = {"plain": [], "html": []}
    collect_parts(msg.get("payload", {}), parts)
    result = summarize_message(msg)
    result["plain"] = "\n".join([p for p in parts["plain"] if p])
    result["html"] = "\n".join([p for p in parts["html"] if p])
    out({"ok": True, "message": result})


def cmd_draft(args: argparse.Namespace) -> None:
    svc = service(args)
    body = {"message": {"raw": raw_message(make_message(args))}}
    draft = svc.users().drafts().create(userId="me", body=body).execute()
    out({"ok": True, "draft": draft})


def cmd_send_draft(args: argparse.Namespace) -> None:
    svc = service(args)
    sent = svc.users().drafts().send(userId="me", body={"id": args.draft_id}).execute()
    out({"ok": True, "sent": sent})


def cmd_send(args: argparse.Namespace) -> None:
    svc = service(args)
    body = {"raw": raw_message(make_message(args))}
    sent = svc.users().messages().send(userId="me", body=body).execute()
    out({"ok": True, "sent": sent})


def cmd_labels(args: argparse.Namespace) -> None:
    svc = service(args)
    labels = svc.users().labels().list(userId="me").execute().get("labels", [])
    out({"ok": True, "labels": labels})


def cmd_modify(args: argparse.Namespace) -> None:
    svc = service(args)
    add = args.add_label or []
    remove = args.remove_label or []
    if args.archive:
        remove.append("INBOX")
    body = {"addLabelIds": add, "removeLabelIds": remove}
    msg = svc.users().messages().modify(userId="me", id=args.id, body=body).execute()
    out({"ok": True, "message": msg})


def add_common(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--account")
    parser.add_argument("--credentials")
    parser.add_argument("--token")
    parser.add_argument("--scopes", help="Comma-separated OAuth scopes")


def add_compose(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--to", required=True)
    parser.add_argument("--cc")
    parser.add_argument("--bcc")
    parser.add_argument("--from", dest="from_addr")
    parser.add_argument("--subject", required=True)
    parser.add_argument("--body", required=True)
    parser.add_argument("--html", action="store_true")
    parser.add_argument("--attach", action="append")


def main() -> int:
    parser = argparse.ArgumentParser(description="Gmail API CLI for Codex")
    add_common(parser)
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("auth")
    p.set_defaults(func=cmd_auth)
    p = sub.add_parser("profile")
    p.set_defaults(func=cmd_profile)
    p = sub.add_parser("search")
    p.add_argument("--query", default="")
    p.add_argument("--limit", type=int, default=10)
    p.set_defaults(func=cmd_search)
    p = sub.add_parser("read")
    p.add_argument("--id", required=True)
    p.set_defaults(func=cmd_read)
    p = sub.add_parser("draft")
    add_compose(p)
    p.set_defaults(func=cmd_draft)
    p = sub.add_parser("send-draft")
    p.add_argument("--draft-id", required=True)
    p.set_defaults(func=cmd_send_draft)
    p = sub.add_parser("send")
    add_compose(p)
    p.set_defaults(func=cmd_send)
    p = sub.add_parser("labels")
    p.set_defaults(func=cmd_labels)
    p = sub.add_parser("modify")
    p.add_argument("--id", required=True)
    p.add_argument("--add-label", action="append")
    p.add_argument("--remove-label", action="append")
    p.add_argument("--archive", action="store_true")
    p.set_defaults(func=cmd_modify)

    args = parser.parse_args()
    try:
        args.func(args)
        return 0
    except HttpError as exc:
        out({"ok": False, "error": "google_http_error", "message": str(exc)})
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
