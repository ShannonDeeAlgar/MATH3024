#!/usr/bin/env python3
"""Injects the Reader's heading/body font-family rules into a generated
slides.html file.

Standalone nbconvert slides don't load style.css (confirmed: the slides
exporter produces a fully self-contained HTML file, no external
stylesheet link), so the Big Caslon/Baskerville typography set there for
the Reader never reaches slides on its own. Rather than hand-duplicating
those rules here (which would drift out of sync the next time style.css's
palette or type changes), this extracts the `.article`-scoped font-family
rule blocks directly from style.css and re-scopes them to
`.jp-MarkdownOutput`, the class nbconvert wraps rendered markdown cells in.

Usage: inject_slide_typography.py <slides.html>
Called from generate_slides.sh after the nbconvert step.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).parent
STYLE_CSS = ROOT / "style.css"

COMMENT_RE = re.compile(r"/\*.*?\*/", re.DOTALL)
RULE_RE = re.compile(r"([^{}]+)\{([^{}]*)\}")


def extract_typography_rules(css_text: str) -> str:
    css_text = COMMENT_RE.sub("", css_text)
    blocks = []
    for selector, body in RULE_RE.findall(css_text):
        selector = selector.strip()
        if not selector:
            continue
        if ".article" in selector and "font-family" in body:
            new_selector = selector.replace(".article", ".jp-MarkdownOutput")
            blocks.append(f"{new_selector.strip()} {{{body}}}")
    return "\n\n".join(blocks)


def main():
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <slides.html>", file=sys.stderr)
        sys.exit(1)

    slides_path = Path(sys.argv[1])
    css_text = STYLE_CSS.read_text()
    rules = extract_typography_rules(css_text)
    if not rules:
        print("WARNING: no .article font-family rules found in style.css -- slides typography not injected", file=sys.stderr)
        sys.exit(1)

    style_block = (
        "<style>\n"
        "/* Injected by inject_slide_typography.py -- keeps slide typography in\n"
        "   sync with style.css's Reader typography. Do not edit directly. */\n"
        f"{rules}\n"
        "</style>\n"
    )

    html = slides_path.read_text()
    if "</head>" not in html:
        print(f"ERROR: no </head> found in {slides_path}", file=sys.stderr)
        sys.exit(1)
    html = html.replace("</head>", style_block + "</head>", 1)
    slides_path.write_text(html)
    print(f"Injected slide typography into {slides_path}")


if __name__ == "__main__":
    main()
