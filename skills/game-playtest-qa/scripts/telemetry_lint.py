#!/usr/bin/env python3
"""telemetry_lint.py - validate a game telemetry spec (JSON).

Stdlib only, Python 3.9 compatible.

Checks (errors fail the run; warnings fail only with --strict):
  * event and property names are snake_case ([a-z][a-z0-9_]*, <= 40 chars)
  * property types are one of: string int float bool enum timestamp
  * enum properties declare a non-empty "values" list of snake_case strings
  * every event has a description; no duplicate event names
  * "required" lists only reference declared event/common properties
  * no PII-looking property names (email, phone, imei, idfa, ip_address, ...)
  * "funnel" lists only declared events; core funnel events recommended
  * event count and per-event property count within sane limits (warnings)

Spec format:
{
  "version": 1,
  "common_properties": {"session_id": "string", "app_version": "string"},
  "events": [
    {"name": "level_start", "description": "...",
     "properties": {"level_id": "int", "mode": {"type": "enum", "values": ["normal", "hard"]}},
     "required": ["level_id"]}
  ],
  "funnel": ["app_open", "level_start", "level_complete"]
}

Exit codes: 0 clean (or warnings only), 1 errors (or warnings with --strict), 2 usage/IO.

Example:
    python3 telemetry_lint.py assets/telemetry_example.json
    python3 telemetry_lint.py spec.json --strict --json
"""
import argparse
import json
import re
import sys

NAME_RE = re.compile(r"^[a-z][a-z0-9_]{0,39}$")
TYPES = {"string", "int", "float", "bool", "enum", "timestamp"}
PII_TOKENS = {"email", "phone", "mobile", "imei", "idfa", "gaid", "ssn", "password", "passwd",
              "passport", "birthday", "latitude", "longitude", "ip"}
PII_PHRASES = ["android_id", "device_id", "ip_address", "real_name", "user_name", "id_card",
               "mac_address", "phone_number", "access_token", "auth_token", "full_name",
               "home_address", "credit_card", "card_number"]
CORE_FUNNEL = ["app_open", "tutorial_start", "tutorial_complete", "level_start",
               "level_complete", "level_fail", "ad_impression", "purchase_complete"]
MAX_EVENTS = 80
MAX_PROPS = 15


def pii_hit(name):
    toks = name.split("_")
    for t in toks:
        if t in PII_TOKENS:
            return t
    for ph in PII_PHRASES:
        if ph in name:
            return ph
    return None


def norm_prop(v):
    """-> (type, values or None, err or None)"""
    if isinstance(v, str):
        return v, None, None
    if isinstance(v, dict):
        return v.get("type"), v.get("values"), None
    return None, None, "property definition must be a type string or an object"


def lint(spec):
    errors, warnings = [], []

    def err(m):
        errors.append(m)

    def warn(m):
        warnings.append(m)

    if not isinstance(spec, dict):
        err("top level must be a JSON object")
        return errors, warnings
    if "version" not in spec:
        warn("missing 'version'")
    common = spec.get("common_properties", {})
    if not isinstance(common, dict):
        err("common_properties must be an object")
        common = {}
    events = spec.get("events")
    if not isinstance(events, list) or not events:
        err("'events' must be a non-empty list")
        return errors, warnings

    def check_props(owner, props):
        for pname, pdef in props.items():
            if not NAME_RE.match(pname):
                err("%s: property '%s' is not snake_case (<=40 chars)" % (owner, pname))
            hit = pii_hit(pname)
            if hit:
                err("%s: property '%s' looks like PII (matched '%s'); do not collect, or hash/bucket it first and rename" % (
                    owner, pname, hit))
            t, values, perr = norm_prop(pdef)
            if perr:
                err("%s: property '%s': %s" % (owner, pname, perr))
                continue
            if t not in TYPES:
                err("%s: property '%s' has unknown type %r (allowed: %s)" % (
                    owner, pname, t, ", ".join(sorted(TYPES))))
            if t == "enum":
                if not isinstance(values, list) or not values:
                    err("%s: enum property '%s' needs a non-empty 'values' list" % (owner, pname))
                else:
                    for val in values:
                        if not isinstance(val, str) or not NAME_RE.match(val):
                            err("%s: enum '%s' value %r is not snake_case" % (owner, pname, val))

    check_props("common_properties", common)

    seen = set()
    for idx, ev in enumerate(events):
        if not isinstance(ev, dict):
            err("events[%d] must be an object" % idx)
            continue
        name = ev.get("name")
        owner = "event '%s'" % name
        if not isinstance(name, str) or not NAME_RE.match(name):
            err("events[%d]: name %r is not snake_case (<=40 chars)" % (idx, name))
            continue
        if name in seen:
            err("%s: duplicate event name" % owner)
        seen.add(name)
        if not ev.get("description"):
            err("%s: missing description" % owner)
        props = ev.get("properties", {})
        if not isinstance(props, dict):
            err("%s: properties must be an object" % owner)
            props = {}
        check_props(owner, props)
        clash = set(props) & set(common)
        if clash:
            warn("%s: redefines common properties %s" % (owner, sorted(clash)))
        if len(props) > MAX_PROPS:
            warn("%s: %d properties (> %d); split the event or drop rarely used ones" % (
                owner, len(props), MAX_PROPS))
        req = ev.get("required", [])
        if not isinstance(req, list):
            err("%s: required must be a list" % owner)
            req = []
        for r in req:
            if r not in props and r not in common:
                err("%s: required property '%s' is not declared" % (owner, r))

    if len(events) > MAX_EVENTS:
        warn("%d events (> %d): trim to what drives decisions" % (len(events), MAX_EVENTS))

    funnel = spec.get("funnel", [])
    if not isinstance(funnel, list):
        err("funnel must be a list of event names")
        funnel = []
    for f in funnel:
        if f not in seen:
            err("funnel references undeclared event '%s'" % f)
    if not funnel:
        warn("no 'funnel' declared (ordered core events for D0 funnel analysis)")
    for c in CORE_FUNNEL:
        if c not in seen:
            warn("recommended core event missing: %s" % c)
    return errors, warnings


def build_parser():
    ap = argparse.ArgumentParser(description="Lint a game telemetry spec JSON: snake_case names, "
                                             "required props, types, no PII keys.")
    ap.add_argument("spec", help="path to telemetry spec JSON")
    ap.add_argument("--strict", action="store_true", help="treat warnings as failures")
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    return ap


def main(argv=None):
    a = build_parser().parse_args(argv)
    try:
        with open(a.spec, "r", encoding="utf-8") as f:
            spec = json.load(f)
    except (OSError, ValueError) as e:
        sys.stderr.write("error: cannot read spec: %s\n" % e)
        return 2
    errors, warnings = lint(spec)
    failed = bool(errors) or (a.strict and bool(warnings))
    if a.json:
        print(json.dumps({"ok": not failed, "errors": errors, "warnings": warnings}, indent=2))
    else:
        for e in errors:
            print("ERROR  %s" % e)
        for w in warnings:
            print("WARN   %s" % w)
        n = len(spec.get("events", [])) if isinstance(spec, dict) and isinstance(spec.get("events"), list) else 0
        print("%s: %d events, %d errors, %d warnings" % ("FAIL" if failed else "OK", n, len(errors), len(warnings)))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
