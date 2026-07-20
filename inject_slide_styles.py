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

Two more blocks below are hardcoded here rather than derived from
style.css, since neither has a Reader equivalent to keep in sync with:

- jp-OutputArea/jp-OutputPrompt are nbconvert/Jupyter-only classes (the
  Reader uses MyST's {iframe} directive for embeds instead, which has
  no jp-OutputArea wrapper at all). Hides the literal "Out[1]:" prompt
  label and centers any code-cell output that contains an iframe
  (YouTube embeds), scoped with :has() so it doesn't affect other
  outputs like matplotlib figures.

- --jp-content-font-size1 is nbconvert's own base size for all rendered
  markdown (headings/body/lists all derive from it via fixed em
  multipliers -- confirmed live: bumping this one variable scaled h1
  through h5, body text, and list items all proportionally). nbconvert
  already sets it to 20px (up from Jupyter's own 14px default) for
  static HTML export, which was still too small read from the back of
  a lecture theatre. 28px was chosen empirically: legible at a
  projector's viewing distance without blowing up h1 past a sane title
  size (105px at 28px base vs 75px at 20px).

- img max-height caps figures so they don't push slide content past
  the 1280x720 canvas. Figures are generated at dpi=150, so a
  figsize=(12,5) figure alone is already 1800x750px -- taller than the
  whole slide before any heading/text above it. 350px was picked by
  headlessly walking every slide in week01 and measuring actual
  overflow: the worst offenders (Segregation, Complex Systems (the
  field)) needed the figure at or below ~358px to fit, so 350px clears
  that with a small margin. This is in px, not vh: reveal.js scales the
  whole 1280x720 canvas via a CSS transform, and vh inside a transformed
  box resolves against the real browser viewport, not the logical slide
  coordinate space, so it wouldn't reliably mean "% of slide height."

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
SHARED_COMPONENT_PREFIXES = (
    ".reader-",
    ".country-",
    ".slide-",
    ".assumption-",
    ".evidence-",
    ".meaning-",
    ".ladder-",
    ".group-",
    ".schelling-",
    ".figure-",
    ".unit-",
    ".model-",
    ".choice-",
    ".discussion-",
    ".process-",
    ".planet-",
    ".variable-",
    ".system-",
    ".qa-",
    ".simulation-",
    ".initialisation-",
    ".planet-",
    ".analysis-",
    ".aggregate-",
    ".parameter-",
    ".two-",
    ".transfer-",
)

SLIDES_ONLY_RULES = """
.jp-OutputArea-child:has(iframe) .jp-OutputPrompt,
.jp-Cell-outputWrapper:has(iframe) .jp-OutputCollapser {
  display: none;
}

.jp-Cell-outputWrapper:has(iframe) {
  display: flex;
  justify-content: center;
}

:root {
  --jp-content-font-size1: 28px !important;
  --reader-ink: #1B2A4C;
  --reader-ink-soft: #5A6685;
  --reader-line: #C7CEDC;
}

.reveal,
.reveal .slides,
.reveal .slides section {
  background: #fff;
  color: var(--reader-ink);
}

.reveal .jp-MarkdownOutput p,
.reveal .jp-MarkdownOutput li,
.reveal .jp-MarkdownOutput td,
.reveal .jp-MarkdownOutput th {
  font-family: Baskerville, Georgia, serif;
  line-height: 1.28;
}

.reveal .slides section h1 {
  font-size: 2.35em;
  line-height: 1.05;
}

.reveal .slides section h2,
.reveal .slides section h3,
.reveal .slides section h4,
.reveal .slides section h5 {
  font-size: 1.45em;
  line-height: 1.12;
}

.reveal .slides section h1,
.reveal .slides section h2,
.reveal .slides section h3,
.reveal .slides section h4,
.reveal .slides section h5 {
  margin-top: 0;
  margin-bottom: 0.55em;
  color: var(--reader-ink);
}

.reveal .slides section h3,
.reveal .slides section h4,
.reveal .slides section h5 {
  font-size: 1.15em;
}

.reveal .slides section a {
  color: var(--reader-ink);
  text-decoration-thickness: 1px;
  text-underline-offset: 0.12em;
}

.reveal .slides section table {
  border-collapse: collapse;
  margin: 0.7em auto;
  font-size: 0.82em;
}

.reveal .slides section th,
.reveal .slides section td {
  border-bottom: 1px solid var(--reader-line);
  padding: 0.3em 0.55em;
}

.reveal .slides section figcaption,
.reveal .slides section .figure-caption,
.reveal .slides section p:has(> em:first-child:last-child) {
  font-family: Arial, Helvetica, sans-serif;
  font-size: 0.58em;
  line-height: 1.25;
  color: var(--reader-ink-soft);
}

.reveal .slides section pre,
.reveal .slides section code,
.reveal .jp-CodeCell {
  font-family: "SFMono-Regular", Consolas, "Liberation Mono", monospace;
}

.reveal .slides section img {
  max-height: 350px;
  width: auto;
  height: auto;
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
        elif any(prefix in selector for prefix in SHARED_COMPONENT_PREFIXES):
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
