#!/usr/bin/env python3
"""Apply the shared Week 1 presentation grammar to all lecture notebooks.

This script deliberately limits itself to repeatable structural changes. It does
not rewrite topic content or alter executable code.
"""

from __future__ import annotations

import re
import shutil
from pathlib import Path

import nbformat


ROOT = Path(__file__).resolve().parents[1]
NOTEBOOKS = ROOT / "notebooks"
MARKER_SOURCE = NOTEBOOKS / "week01" / "images"
MARKERS = ("ladder_marker.svg", "discussion_marker.svg", "choice_marker.svg")
BROKEN_WEEK10_ASSETS = (
    "DarwinsFinches.jpeg",
    "Evolution_ApeMan_Linear.png",
    "Evolution_ApeMan_Proper.jpeg",
    "Axelrod_PD.png",
    "Axelrod_TournamentResults.png",
)

QUOTE_RE = re.compile(
    r'''<div\s+style="margin:\s*1\.5em 0;\s*border-right:\s*4px solid #888;'''
    r'''\s*padding-right:\s*1em;\s*text-align:\s*right;">\s*'''
    r'''<div\s+style="font-style:\s*italic;[^\"]*">\s*(.*?)\s*</div>\s*'''
    r'''<div\s+style="font-style:\s*normal;[^\"]*">\s*[—-]?\s*(.*?)\s*</div>\s*'''
    r'''</div>''',
    re.DOTALL,
)

DISCUSSION_RE = re.compile(
    r'''<div\s+style="border-left:\s*4px solid #1e70bf;[^\"]*">\s*'''
    r'''<strong>Pause and consider:</strong><br>\s*(.*?)\s*</div>''',
    re.DOTALL | re.IGNORECASE,
)

EMPTY_ALT_RE = re.compile(r"!\[\]\((images/[^)\s]+)([^)]*)\)")

LEGACY_QUOTE_OPEN = (
    '<div style="margin: 1.5em 0; border-right: 4px solid #888; '
    'padding-right: 1em; text-align: right;">'
)
LEGACY_QUOTE_TEXT_OPEN = (
    '<div style="font-style: italic; font-family: \'Comic Neue\', '
    '\'Segoe Script\', cursive; font-size: 1.2em;">'
)
LEGACY_QUOTE_ATTR_OPEN = (
    '<div style="font-style: normal; font-size: 0.95em; margin-top: 0.5em;">'
)


def quote_component(match: re.Match[str]) -> str:
    quote = match.group(1).strip()
    attribution = match.group(2).strip()
    return (
        '<div class="reader-voice">\n'
        f'  <div class="reader-voice-quote">{quote}</div>\n'
        f'  <div class="reader-voice-attr">{attribution}</div>\n'
        '</div>'
    )


def discussion_component(match: re.Match[str]) -> str:
    prompt = match.group(1).strip()
    return (
        '<div class="discussion-marker">'
        '<img src="images/discussion_marker.svg" alt="Discussion prompt">'
        f'<span>{prompt}</span></div>'
    )


def image_alt(match: re.Match[str]) -> str:
    path, suffix = match.groups()
    stem = Path(path).stem.replace("_", " ").replace("-", " ")
    label = stem[:1].upper() + stem[1:]
    return f"![{label}]({path}{suffix})"


def finish_legacy_quote_markup(source: str) -> str:
    """Handle legacy quote blocks whose imperfect HTML defeated the full regex."""
    source = source.replace(LEGACY_QUOTE_OPEN, '<div class="reader-voice">')
    source = source.replace(LEGACY_QUOTE_TEXT_OPEN, '<div class="reader-voice-quote">')
    source = source.replace(LEGACY_QUOTE_ATTR_OPEN, '<div class="reader-voice-attr">')
    source = re.sub(
        r'(<div class="reader-voice-attr">\s*)[—-]\s*',
        r"\1",
        source,
    )
    return source


def standardise_title(source: str, week: int) -> str:
    """Give every deck the same title hierarchy without changing its topic."""
    lines = source.splitlines()
    if not lines:
        return source
    match = re.match(rf"#\s+Week\s+{week}\s*:\s*(.+)", lines[0], re.IGNORECASE)
    if not match:
        return source
    topic = match.group(1).strip()
    lines[0] = f"# {topic}"
    lines.insert(1, f"## MATH3024 · Week {week}")
    return "\n".join(lines)


def split_title_content(nb: nbformat.NotebookNode) -> None:
    """Keep title slides minimal and move explanatory prose to a subslide."""
    first = nb.cells[0]
    if any(cell.get("id") == "standardised-title-context" for cell in nb.cells):
        return
    lines = first.source.splitlines()
    content_start = 2
    while content_start < len(lines) and not lines[content_start].strip():
        content_start += 1
    if content_start < len(lines) and lines[content_start].startswith("## "):
        content_start += 1
        while content_start < len(lines) and not lines[content_start].strip():
            content_start += 1
    remainder = "\n".join(lines[content_start:]).strip()
    if not remainder:
        return
    first.source = "\n".join(lines[:content_start]).strip()
    context = nbformat.v4.new_markdown_cell(f"## Starting point\n\n{remainder}\n")
    context["id"] = "standardised-title-context"
    context.metadata["slideshow"] = {"slide_type": "subslide"}
    nb.cells.insert(1, context)


def remove_broken_week10_images(nb: nbformat.NotebookNode) -> int:
    removed = 0
    for cell in nb.cells:
        if cell.cell_type != "markdown":
            continue
        for filename in BROKEN_WEEK10_ASSETS:
            pattern = re.compile(
                rf'''\s*<center>\s*<img\s+src="images/{re.escape(filename)}"[^>]*?/?>\s*</center>\s*''',
                re.IGNORECASE,
            )
            cell.source, count = pattern.subn("\n", cell.source)
            removed += count
    return removed


def main() -> None:
    totals = {
        "notebooks": 0,
        "quotes": 0,
        "discussions": 0,
        "alt_text": 0,
        "broken_assets": 0,
    }
    for week in range(2, 11):
        week_dir = NOTEBOOKS / f"week{week:02d}"
        paths = sorted(week_dir.glob("L_*.ipynb"))
        if not paths:
            continue
        images = week_dir / "images"
        images.mkdir(exist_ok=True)
        for marker in MARKERS:
            shutil.copy2(MARKER_SOURCE / marker, images / marker)

        for path in paths:
            nb = nbformat.read(path, as_version=4)
            nb.metadata["math3024_slide_format"] = "blue-period-v3"
            first = nb.cells[0]
            first.metadata.setdefault("slideshow", {})["slide_type"] = "slide"
            first.metadata["tags"] = [
                tag for tag in first.metadata.get("tags", []) if tag != "reader-only"
            ]
            first.source = standardise_title(first.source, week)
            split_title_content(nb)

            for cell in nb.cells:
                if cell.cell_type != "markdown":
                    continue
                source, quote_count = QUOTE_RE.subn(quote_component, cell.source)
                source, discussion_count = DISCUSSION_RE.subn(discussion_component, source)
                source = finish_legacy_quote_markup(source)
                source, alt_count = EMPTY_ALT_RE.subn(image_alt, source)
                cell.source = source
                totals["quotes"] += quote_count
                totals["discussions"] += discussion_count
                totals["alt_text"] += alt_count

            if week == 10:
                totals["broken_assets"] += remove_broken_week10_images(nb)

            nbformat.write(nb, path)
            totals["notebooks"] += 1
            print(f"Standardised {path.relative_to(ROOT)}")

    print(
        f"Updated {totals['notebooks']} notebooks, "
        f"{totals['quotes']} quote blocks, and "
        f"{totals['discussions']} discussion prompts; "
        f"added {totals['alt_text']} image descriptions and removed "
        f"{totals['broken_assets']} broken image calls."
    )


if __name__ == "__main__":
    main()
