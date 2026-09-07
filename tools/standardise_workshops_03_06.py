#!/usr/bin/env python3
"""Make the Week 3–6 LMS workshop notebooks render without custom assets."""

from pathlib import Path
import re

import nbformat


ROOT = Path(__file__).resolve().parents[1]
NOTEBOOKS = (
    "week03/WS_Reaction_diffusion.ipynb",
    "week04/WS_Cellular_automata.ipynb",
    "week04/WS_Cellular_automata_revised.ipynb",
    "week05/WS_ABM.ipynb",
    "week06/WS_Synchronisation.ipynb",
)

TITLES = {
    "week04/WS_Cellular_automata.ipynb": "Week 4 workshop · Rules, states, consequences",
    "week05/WS_ABM.ipynb": "Week 5 workshop · Agents, alignment, collective motion",
    "week06/WS_Synchronisation.ipynb": "Week 6 workshop · From oscillators to synchronisation",
}


def plain_markdown(source: str) -> str:
    """Replace presentation-only HTML callouts with portable Markdown."""
    callouts = (
        ("ladder-marker", "The ladder of abstraction"),
        ("discussion-marker", "Discuss"),
        ("choice-marker", "Modelling choice"),
    )
    for class_name, label in callouts:
        source = re.sub(
            rf'<div class="{class_name}"><img[^>]*><span>(.*?)</span></div>',
            rf'> **{label}:** \1',
            source,
            flags=re.DOTALL,
        )
    source = source.replace("<strong>", "**").replace("</strong>", "**")
    source = re.sub(
        r'<div class="reader-route">\s*'
        r'<div class="reader-route-label">(.*?)</div>\s*'
        r'<div class="reader-route-body">(.*?)</div>\s*</div>',
        r'> **\1:** \2',
        source,
        flags=re.DOTALL,
    )
    return source


for relative in NOTEBOOKS:
    path = ROOT / "notebooks" / relative
    notebook = nbformat.read(path, as_version=4)
    notebook.metadata.pop("author", None)
    notebook.metadata.pop("authors", None)

    notebook.cells = [
        cell
        for cell in notebook.cells
        if not (cell.cell_type == "markdown" and not cell.source.strip())
    ]
    for cell in notebook.cells:
        if cell.cell_type == "markdown":
            cell.source = plain_markdown(cell.source)

    title = TITLES.get(relative)
    if title:
        focus = next(
            (cell for cell in notebook.cells if cell.get("id") == "workshop-focus"),
            None,
        )
        if focus is not None:
            focus.source = re.sub(
                r"^# Workshop focus",
                f"# {title}\n\n## Workshop focus",
                focus.source,
            )

    nbformat.write(notebook, path)
    print(path)
