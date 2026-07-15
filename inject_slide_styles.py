#!/usr/bin/env python3
"""Injects the Reader's typography and .reader-* component styles into a
generated slides.html file.

Standalone nbconvert slides don't load style.css (confirmed: the slides
exporter produces a fully self-contained HTML file, no external
stylesheet link), so nothing set there for the Reader reaches slides on
its own. Rather than hand-duplicating those rules here (which would
drift out of sync the next time style.css changes), this extracts two
kinds of rule directly from style.css:

- `.article`-scoped font-family rules (headings/body copy), re-scoped to
  `.jp-MarkdownOutput`, the class nbconvert wraps rendered markdown
  cells in.
- `.reader-*`-prefixed component rules (Voice/Prompt/Emphasis etc, see
  reskin templates), copied verbatim -- these are literal class="..."
  attributes on raw HTML in notebook cells, present identically in both
  the Reader and slides, so no re-scoping needed. Their colours read
  through var(--reader-ink, #hex); the fallback hex is what applies
  here, since --reader-ink is never defined outside `.article`.

A third block below is hardcoded here rather than derived from
style.css: jp-OutputArea/jp-OutputPrompt are nbconvert/Jupyter-only
classes with no Reader equivalent to keep in sync with (the Reader
uses MyST's {iframe} directive for embeds instead, which has no
jp-OutputArea wrapper at all), so there's nothing for style.css to
define. It hides the literal "Out[1]:" prompt label and centers any
code-cell output that contains an iframe (YouTube embeds), scoped with
:has() so it doesn't affect other outputs like matplotlib figures.

Usage: inject_slide_styles.py <slides.html>
Called from generate_slides.sh after the nbconvert step.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).parent
STYLE_CSS = ROOT / "style.css"

COMMENT_RE = re.compile(r"/\*.*?\*/", re.DOTALL)
RULE_RE = re.compile(r"([^{}]+)\{([^{}]*)\}")

SLIDES_ONLY_RULES = """
.jp-OutputArea-child:has(iframe) .jp-OutputPrompt,
.jp-Cell-outputWrapper:has(iframe) .jp-OutputCollapser {
  display: none;
}

.jp-Cell-outputWrapper:has(iframe) {
  display: flex;
  justify-content: center;
}
""".strip()


def extract_rules(css_text: str) -> str:
    css_text = COMMENT_RE.sub("", css_text)
    blocks = []
    for selector, body in RULE_RE.findall(css_text):
        selector = selector.strip()
        if not selector:
            continue
        if ".article" in selector and "font-family" in body:
            new_selector = selector.replace(".article", ".jp-MarkdownOutput")
            blocks.append(f"{new_selector.strip()} {{{body}}}")
        elif ".reader-" in selector:
            blocks.append(f"{selector} {{{body}}}")
    return "\n\n".join(blocks)


def main():
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <slides.html>", file=sys.stderr)
        sys.exit(1)

    slides_path = Path(sys.argv[1])
    css_text = STYLE_CSS.read_text()
    rules = extract_rules(css_text)
    if not rules:
        print("WARNING: no rules extracted from style.css -- slide styling not injected", file=sys.stderr)
        sys.exit(1)

    style_block = (
        "<style>\n"
        "/* Injected by inject_slide_styles.py -- keeps slide styling in\n"
        "   sync with style.css. Do not edit directly. */\n"
        f"{rules}\n\n"
        f"{SLIDES_ONLY_RULES}\n"
        "</style>\n"
    )

    html = slides_path.read_text()
    if "</head>" not in html:
        print(f"ERROR: no </head> found in {slides_path}", file=sys.stderr)
        sys.exit(1)
    html = html.replace("</head>", style_block + "</head>", 1)
    slides_path.write_text(html)
    print(f"Injected slide styles into {slides_path}")


if __name__ == "__main__":
    main()
