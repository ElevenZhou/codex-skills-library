#!/usr/bin/env python3
"""verify_frontend.py - frontend QA for advanced-frontend-design / frontend-design-review.

Two modes, chosen automatically:
  browser : python `playwright` + Chromium installed -> screenshots, console errors,
            horizontal overflow, missing alt, unnamed buttons/links (real rendering).
  static  : stdlib only (html.parser) -> structural audit of the HTML source.
            Does NOT prove layout, overflow, contrast or console health.

Usage:
  verify_frontend.py PATH_OR_URL [--viewports 1440x900,390x844] [--out DIR]
                     [--format md|json] [--static] [--strict]
Exit codes: 0 ok, 1 findings at error level with --strict, 2 bad input.
"""
import argparse
import json
import os
import re
import sys
import urllib.request
from html.parser import HTMLParser
from pathlib import Path

VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link",
        "meta", "param", "source", "track", "wbr"}
CDN_HINT = re.compile(r"https?://[^\s\"')>]+", re.I)
FONT_HOSTS = ("fonts.googleapis.com", "fonts.gstatic.com", "use.typekit.net",
              "cdn.jsdelivr.net", "unpkg.com", "cdnjs.cloudflare.com",
              "cdn.tailwindcss.com", "ajax.googleapis.com", "code.jquery.com")


class Audit(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.lang = None
        self.title = None
        self.viewport = False
        self.imgs = []          # (src, has_alt_attr, alt)
        self.headings = []      # int levels
        self.controls = []      # dicts for a/button
        self.stack = []
        self.style_text = []
        self.inline_style_attrs = []
        self.urls = []
        self.in_title = False
        self.in_style = False
        self.in_script = False
        self.line_of = {}
        self.stray_tabindex = 0

    def handle_starttag(self, tag, attrs):
        a = {k: (v if v is not None else "") for k, v in attrs}
        line = self.getpos()[0]
        if tag == "html":
            self.lang = a.get("lang")
        elif tag == "title":
            self.in_title = True
            self.title = ""
        elif tag == "style":
            self.in_style = True
        elif tag == "script":
            self.in_script = True
        elif tag == "meta" and a.get("name", "").lower() == "viewport":
            self.viewport = True
        elif tag == "img":
            self.imgs.append({"src": a.get("src", "")[:80], "has_alt": "alt" in a,
                              "alt": a.get("alt", ""), "line": line})
            if self.stack and a.get("alt", "").strip():
                self.stack[-1]["named"] = True
        elif re.fullmatch(r"h[1-6]", tag):
            self.headings.append((int(tag[1]), line))
        if tag in ("a", "button") or a.get("role") in ("button", "link"):
            if tag == "a" and "href" not in a and a.get("role") not in ("button", "link"):
                pass
            else:
                c = {"tag": tag, "line": line, "text": "", "named": bool(
                    a.get("aria-label", "").strip() or a.get("aria-labelledby", "").strip()
                    or a.get("title", "").strip()), "id": a.get("id", ""),
                    "cls": a.get("class", "")}
                if tag == "input":
                    c["named"] = True
                self.controls.append(c)
                if tag not in VOID:
                    self.stack.append(c)
        if tag in ("svg",) and self.stack and (a.get("aria-label") or a.get("title")):
            self.stack[-1]["named"] = True
        if tag == "input" and a.get("type", "").lower() in ("button", "submit") \
                and not a.get("value", "").strip() and not a.get("aria-label", "").strip():
            self.controls.append({"tag": "input", "line": line, "text": "", "named": False,
                                  "id": a.get("id", ""), "cls": a.get("class", "")})
        if "style" in a:
            self.inline_style_attrs.append(a["style"])
        for k in ("src", "href", "poster", "data-src"):
            v = a.get(k, "")
            if v.startswith(("http://", "https://", "//")):
                self.urls.append((tag, v, line))

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)

    def handle_endtag(self, tag):
        if tag == "title":
            self.in_title = False
        elif tag == "style":
            self.in_style = False
        elif tag == "script":
            self.in_script = False
        elif tag in ("a", "button", "div", "span", "li", "p"):
            # role=button on a div/span is pushed too; pop only a matching control
            if self.stack and self.stack[-1]["tag"] == tag:
                self.stack.pop()

    def handle_data(self, data):
        if self.in_title and self.title is not None:
            self.title += data
        elif self.in_style:
            self.style_text.append(data)
        elif self.in_script:
            return
        elif self.stack:
            self.stack[-1]["text"] += data
            if data.strip():
                self.stack[-1]["named"] = True


def add(findings, sev, code, msg, count=None, examples=None):
    f = {"severity": sev, "code": code, "message": msg}
    if count is not None:
        f["count"] = count
    if examples:
        f["examples"] = examples[:5]
    findings.append(f)


def static_audit(html):
    p = Audit()
    p.feed(html)
    p.close()
    css = "\n".join(p.style_text)
    findings = []
    if not (p.title or "").strip():
        add(findings, "error", "title", "Missing or empty <title>")
    if not p.lang:
        add(findings, "warn", "lang", "<html> has no lang attribute (screen readers and CJK font selection depend on it)")
    if not p.viewport:
        add(findings, "error", "viewport", "Missing <meta name=viewport>; mobile layout will not work")
    no_alt = [f"line {i['line']} {i['src']}" for i in p.imgs if not i["has_alt"]]
    if no_alt:
        add(findings, "error", "img-alt", "<img> without alt attribute (use alt=\"\" for decorative)", len(no_alt), no_alt)
    bad = [f"line {c['line']} <{c['tag']}> id={c['id'] or '-'} class={c['cls'][:30] or '-'}"
           for c in p.controls if not c["named"]]
    if bad:
        add(findings, "error", "unnamed-control", "Links/buttons with no accessible name", len(bad), bad)
    lv = [h[0] for h in p.headings]
    if not lv:
        add(findings, "warn", "headings", "No headings found")
    else:
        if lv.count(1) == 0:
            add(findings, "warn", "h1", "No <h1>")
        elif lv.count(1) > 1:
            add(findings, "warn", "h1", f"{lv.count(1)} <h1> elements; expected one per page")
        jumps = [f"line {p.headings[i][1]}: h{lv[i-1]} -> h{lv[i]}" for i in range(1, len(lv)) if lv[i] > lv[i-1] + 1]
        if jumps:
            add(findings, "warn", "heading-order", "Heading levels skip", len(jumps), jumps)
    imp_css = len(re.findall(r"!important", css))
    imp_inline = sum(s.count("!important") for s in p.inline_style_attrs)
    if imp_css + imp_inline:
        add(findings, "info", "important", f"!important: {imp_css} in <style>, {imp_inline} in style=\"\" attributes", imp_css + imp_inline)
    ext = []
    for tag, url, line in p.urls:
        if tag in ("a",):
            continue
        ext.append(f"line {line} <{tag}> {url[:90]}")
    for m in CDN_HINT.finditer(css):
        ext.append("css " + m.group(0)[:90])
    if ext:
        add(findings, "warn", "external-resources",
            "External resources (free-first rule: prefer local/self-hosted fonts and assets; remote hosts break offline and add privacy/CN-network risk)",
            len(ext), ext)
    has_anim = bool(re.search(r"@keyframes|transition\s*:|animation\s*:", css + " ".join(p.inline_style_attrs)))
    has_rm = "prefers-reduced-motion" in css
    if has_anim and not has_rm:
        add(findings, "warn", "reduced-motion", "Animations/transitions present but no prefers-reduced-motion rule")
    elif not has_anim and not has_rm:
        add(findings, "info", "reduced-motion", "No motion detected; prefers-reduced-motion not needed in <style> (external CSS/JS not scanned)")
    if not re.search(r":focus-visible|:focus\b", css):
        add(findings, "warn", "focus-style", "No :focus-visible / :focus rule found in <style> (external CSS not scanned)")
    return findings, {"images": len(p.imgs), "controls": len(p.controls), "headings": len(lv),
                      "style_bytes": len(css)}


def load_source(target):
    if re.match(r"^https?://", target, re.I):
        req = urllib.request.Request(target, headers={"User-Agent": "verify_frontend/1.0"})
        with urllib.request.urlopen(req, timeout=20) as r:
            return r.read().decode(r.headers.get_content_charset() or "utf-8", "replace")
    return Path(target).read_text(encoding="utf-8", errors="replace")


BROWSER_JS = """() => {
  const vw = document.documentElement.clientWidth;
  const sw = document.documentElement.scrollWidth;
  const wide = [];
  document.querySelectorAll('body *').forEach(el => {
    const r = el.getBoundingClientRect();
    if (r.width > 0 && (r.right > vw + 1 || r.left < -1)) {
      let p = el.parentElement, clipped = false;
      while (p && p !== document.body) {
        const o = getComputedStyle(p).overflowX;
        if (o !== 'visible') { clipped = true; break; }
        p = p.parentElement;
      }
      if (!clipped && wide.length < 8)
        wide.push(el.tagName.toLowerCase() + (el.id ? '#' + el.id : '') +
                  (el.className && typeof el.className === 'string' ? '.' + el.className.trim().split(/\\s+/)[0] : ''));
    }
  });
  const name = el => (el.getAttribute('aria-label') || el.getAttribute('title') ||
    (el.getAttribute('aria-labelledby') ? 'ref' : '') || (el.innerText || '').trim() ||
    (el.querySelector('img[alt]:not([alt=""])') ? 'img' : '') || el.value || '');
  const unnamed = [...document.querySelectorAll('a[href],button,[role=button]')]
    .filter(el => !name(el)).slice(0, 8)
    .map(el => el.tagName.toLowerCase() + (el.id ? '#' + el.id : '') + (el.className && typeof el.className === 'string' ? '.' + el.className.trim().split(/\\s+/)[0] : ''));
  const noAlt = [...document.querySelectorAll('img:not([alt])')].slice(0, 8).map(i => i.getAttribute('src'));
  const small = [...document.querySelectorAll('a[href],button,input,select,[role=button]')]
    .filter(el => { const r = el.getBoundingClientRect(); return r.width > 0 && (r.width < 24 || r.height < 24); }).length;
  return {viewportWidth: vw, scrollWidth: sw, overflowX: sw > vw + 1, wideElements: wide,
          unnamedControls: unnamed, imgsWithoutAlt: noAlt, controlsUnder24px: small};
}"""


def browser_audit(target, viewports, outdir):
    from playwright.sync_api import sync_playwright  # may raise ImportError
    url = target if re.match(r"^https?://", target, re.I) else Path(target).resolve().as_uri()
    outdir.mkdir(parents=True, exist_ok=True)
    results = []
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        for w, h in viewports:
            page = browser.new_page(viewport={"width": w, "height": h})
            errors, failed = [], []
            page.on("console", lambda m, e=errors: e.append(m.text[:200]) if m.type in ("error", "warning") else None)
            page.on("pageerror", lambda x, e=errors: e.append("pageerror: " + str(x)[:200]))
            page.on("requestfailed", lambda r, f=failed: f.append(r.url[:120]))
            page.goto(url, wait_until="load", timeout=30000)
            try:
                page.wait_for_load_state("networkidle", timeout=5000)
            except Exception:
                pass
            shot = outdir / f"screenshot-{w}x{h}.png"
            page.screenshot(path=str(shot), full_page=True)
            data = page.evaluate(BROWSER_JS)
            data.update({"viewport": f"{w}x{h}", "screenshot": str(shot),
                         "consoleErrors": errors[:10], "failedRequests": failed[:10]})
            results.append(data)
            page.close()
        browser.close()
    return results


def browser_findings(results):
    out = []
    for r in results:
        vp = r["viewport"]
        if r["overflowX"]:
            add(out, "error", "overflow-x", f"[{vp}] horizontal overflow: scrollWidth {r['scrollWidth']} > {r['viewportWidth']}", None, r["wideElements"])
        if r["consoleErrors"]:
            add(out, "error", "console", f"[{vp}] console errors/warnings", len(r["consoleErrors"]), r["consoleErrors"])
        if r["failedRequests"]:
            add(out, "error", "failed-requests", f"[{vp}] failed requests", len(r["failedRequests"]), r["failedRequests"])
        if r["unnamedControls"]:
            add(out, "error", "unnamed-control", f"[{vp}] controls without accessible name", len(r["unnamedControls"]), r["unnamedControls"])
        if r["imgsWithoutAlt"]:
            add(out, "error", "img-alt", f"[{vp}] images without alt", len(r["imgsWithoutAlt"]), r["imgsWithoutAlt"])
        if r["controlsUnder24px"]:
            add(out, "warn", "target-size", f"[{vp}] {r['controlsUnder24px']} interactive elements smaller than 24x24 CSS px (WCAG 2.2 AA minimum; aim for 44 on touch)")
    return out


def render_md(rep):
    L = [f"# verify_frontend report", "", f"- target: `{rep['target']}`", f"- mode: **{rep['mode']}**"]
    for n in rep["notes"]:
        L.append(f"- note: {n}")
    L.append(f"- stats: {json.dumps(rep['stats'], ensure_ascii=False)}")
    L += ["", "## Findings", ""]
    if not rep["findings"]:
        L.append("No findings.")
    for f in rep["findings"]:
        c = f" (x{f['count']})" if "count" in f else ""
        L.append(f"- **{f['severity'].upper()}** `{f['code']}`: {f['message']}{c}")
        for e in f.get("examples", []):
            L.append(f"  - {e}")
    for r in rep.get("browser", []):
        L.append(f"\nScreenshot {r['viewport']}: `{r['screenshot']}`")
    return "\n".join(L)


def parse_viewports(s):
    out = []
    for part in s.split(","):
        m = re.fullmatch(r"\s*(\d{2,5})x(\d{2,5})\s*", part)
        if not m:
            raise ValueError(f"bad viewport '{part}', expected WIDTHxHEIGHT")
        out.append((int(m.group(1)), int(m.group(2))))
    return out


def main(argv=None):
    ap = argparse.ArgumentParser(description="Frontend QA: browser audit via playwright if available, else static HTML audit.")
    ap.add_argument("target", help="HTML file path or http(s) URL")
    ap.add_argument("--viewports", default="1440x900,390x844", help="comma list, default 1440x900,390x844")
    ap.add_argument("--out", default="verify-output", help="screenshot directory (browser mode)")
    ap.add_argument("--format", choices=("md", "json"), default="md")
    ap.add_argument("--static", action="store_true", help="force the static audit even if playwright exists")
    ap.add_argument("--strict", action="store_true", help="exit 1 if any error-level finding")
    a = ap.parse_args(argv)
    try:
        vps = parse_viewports(a.viewports)
        html = load_source(a.target)
    except Exception as e:
        print(f"error: {e}", file=sys.stderr)
        return 2
    findings, stats = static_audit(html)
    rep = {"target": a.target, "mode": "static", "notes": [], "stats": stats}
    if not a.static:
        try:
            import playwright  # noqa: F401
            res = browser_audit(a.target, vps, Path(a.out))
            rep["mode"] = "browser+static"
            rep["browser"] = res
            findings = [f for f in findings if f["code"] not in ("img-alt", "unnamed-control")] \
                + browser_findings(res)
        except ImportError:
            rep["notes"].append("python playwright not installed: static audit only. No screenshots, overflow, console or contrast checks were run. Install with `pip install playwright && playwright install chromium`, or use the playwright skill.")
        except Exception as e:  # browsers missing, navigation failure
            rep["notes"].append(f"browser path failed ({type(e).__name__}: {str(e)[:120]}); fell back to static audit only.")
    else:
        rep["notes"].append("--static forced: no rendering checks were run.")
    rep["findings"] = findings
    print(json.dumps(rep, ensure_ascii=False, indent=2) if a.format == "json" else render_md(rep))
    if a.strict and any(f["severity"] == "error" for f in findings):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
