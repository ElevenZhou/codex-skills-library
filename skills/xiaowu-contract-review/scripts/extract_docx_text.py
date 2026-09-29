#!/usr/bin/env python3
"""Extract full text from a .docx file (paragraphs in document order).

Usage:
    python extract_docx_text.py <input.docx> [output.txt]

Prints to stdout if no output path is given. Handles only body paragraphs
and table cells; headers/footers are skipped (usually boilerplate).
"""
import sys
import zipfile
from xml.etree import ElementTree as ET

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"


def extract(docx_path: str) -> str:
    with zipfile.ZipFile(docx_path) as z:
        xml = z.read("word/document.xml")
    root = ET.fromstring(xml)
    lines = []
    for p in root.iter(W + "p"):
        text = "".join(t.text or "" for t in p.iter(W + "t"))
        lines.append(text)
    return "\n".join(lines)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("usage: extract_docx_text.py <input.docx> [output.txt]")
    result = extract(sys.argv[1])
    if len(sys.argv) >= 3:
        with open(sys.argv[2], "w", encoding="utf-8") as f:
            f.write(result)
        print(f"wrote {sys.argv[2]} ({len(result)} chars)")
    else:
        print(result)
