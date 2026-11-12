#!/usr/bin/env python3
"""技能库检查：frontmatter、命名、章节、行数、密钥扫描。

用法（在仓库根目录）:
    python3 scripts/lint-skills.py                  # 检查全部技能
    python3 scripts/lint-skills.py rebuild-recon    # 只检查指定技能
    python3 scripts/lint-skills.py --strict         # 把警告也当错误

错误（退出码 1）: 缺 SKILL.md / frontmatter / name / description、name 与目录名不一致、疑似密钥。
警告: SKILL.md 超过 200 行、缺「何时用」「相关 skill」「变更记录」章节。
"""
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SKILLS = ROOT / "skills"
MAX_LINES = 200
# 目录名与 frontmatter name 允许不同的历史例外（触发名与目录名分开）
NAME_ALIASES = {"taste-skill": "design-taste-frontend"}
# 大体量的第三方/导入技能，不做行数警告
SIZE_EXEMPT = {"taste-skill", "ai量化技能库"}
SECTION_HINTS = {
    "何时用": ("何时用", "何时使用", "When to use", "适用场景", "使用场景"),
    "相关 skill": ("相关 skill", "相关技能", "Related skill", "关联 skill"),
    "变更记录": ("变更记录", "Changelog", "Change log", "版本记录"),
}
SECRET_PATTERNS = [
    (re.compile(r"(?i)(api[_-]?key|secret|password|passwd|token)\s*[=:]\s*[\"'][A-Za-z0-9_\-]{16,}[\"']"), "疑似明文密钥"),
    (re.compile(r"AIza[0-9A-Za-z_\-]{35}"), "Google API Key"),
    (re.compile(r"sk-[A-Za-z0-9]{32,}"), "OpenAI 风格 Key"),
    (re.compile(r"-----BEGIN (RSA |EC |OPENSSH )?PRIVATE KEY-----"), "私钥"),
]
TEXT_EXT = {".md", ".py", ".gd", ".cfg", ".yaml", ".yml", ".json", ".ps1", ".sh", ".txt", ".html", ".js", ".tres", ".godot"}


def frontmatter(text):
    m = re.match(r"^---\r?\n(.*?)\r?\n---\r?\n", text, re.S)
    if not m:
        return None
    return dict(re.findall(r"^([\w-]+):\s*(.*)$", m.group(1), re.M))


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    strict = "--strict" in sys.argv
    errors, warnings = [], []
    dirs = [SKILLS / a for a in args] if args else sorted(p for p in SKILLS.iterdir() if p.is_dir())
    for skill in dirs:
        if not skill.is_dir():
            errors.append(f"{skill.name}: 目录不存在")
            continue
        f = skill / "SKILL.md"
        if not f.exists():
            errors.append(f"{skill.name}: 缺少 SKILL.md")
            continue
        text = f.read_text(encoding="utf-8", errors="ignore")
        fm = frontmatter(text)
        if fm is None:
            errors.append(f"{skill.name}: 缺少 frontmatter")
            continue
        for k in ("name", "description"):
            if not fm.get(k):
                errors.append(f"{skill.name}: frontmatter 缺 {k}")
        want = NAME_ALIASES.get(skill.name, skill.name)
        if fm.get("name") and fm["name"].strip("\"'") != want:
            errors.append(f"{skill.name}: name 与目录名不一致（{fm.get('name')}）")
        for label, hints in SECTION_HINTS.items():
            if not any(h in text for h in hints):
                warnings.append(f"{skill.name}: 缺少章节「{label}」")
        n = text.count("\n")
        if n > MAX_LINES and skill.name not in SIZE_EXEMPT:
            warnings.append(f"{skill.name}: SKILL.md {n} 行，超过 {MAX_LINES}，建议拆到 references/")
        for p in skill.rglob("*"):
            if not p.is_file() or p.suffix.lower() not in TEXT_EXT or p.stat().st_size > 2_000_000:
                continue
            for i, line in enumerate(p.read_text(encoding="utf-8", errors="ignore").splitlines(), 1):
                for pat, why in SECRET_PATTERNS:
                    if pat.search(line):
                        errors.append(f"{p.relative_to(ROOT)}:{i}: {why}")

    for w in warnings:
        print("WARN ", w)
    for e in errors:
        print("ERROR", e)
    bad = bool(errors) or (strict and bool(warnings))
    print(f"checked {len(dirs)} skills: {len(errors)} errors, {len(warnings)} warnings -> {'FAIL' if bad else 'OK'}")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
