#!/usr/bin/env python3
"""Order and nest the Week 7 biological motivation in the Reader."""

from pathlib import Path

import nbformat


ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "notebooks/week07/L_Intelligent_systems.ipynb"

nb = nbformat.read(PATH, as_version=4)
by_id = {cell.get("id"): cell for cell in nb.cells}


def set_heading(cell_id: str, old: str | None, new: str) -> None:
    cell = by_id[cell_id]
    text = cell.source
    if old is None:
        # The superorganism introduction previously had no heading.
        if not text.lstrip().startswith(new):
            cell.source = new + "\n\n" + text.lstrip()
    elif text.lstrip().startswith(old):
        cell.source = text.replace(old, new, 1)
    elif not text.lstrip().startswith(new):
        raise ValueError(f"Unexpected heading in {cell_id}: {text.splitlines()[:1]}")


set_heading("5aa96f13", None, "## Superorganisms")
set_heading("9012fd46", "## Ants", "### Ants")
set_heading("302edd47", "## Ants communicate through the environment", "#### Ants communicate through the environment")
set_heading("e454bccc", "## Shortest paths", "#### Shortest paths")
set_heading("3110c932", "## Lane formation", "#### Lane formation")
set_heading("9120f58a", "## Lesson: Be like ants", "#### Lesson: Be like ants")
set_heading("9133eb16", "## Lesson: Don't be like ants", "#### Lesson: Don't be like ants")

# Move complete conceptual blocks rather than isolated heading cells.  All
# cells between each listed anchor and the next anchor belong to that block.
reader_start = nb.cells.index(by_id["w7-reader-real-banner"]) + 1
reader_end = nb.cells.index(by_id["w7-optimisation-reader"])
region = nb.cells[reader_start:reader_end]

starts = {
    "framing": region.index(by_id["f0d0beff"]),
    "superorganisms": region.index(by_id["5aa96f13"]),
    "biomimicry": region.index(by_id["ce2ba53c"]),
}

framing = region[starts["framing"]:starts["superorganisms"]]
superorganisms = region[starts["superorganisms"]:starts["biomimicry"]]
biomimicry = region[starts["biomimicry"]:]

# Biological design first; biological collectives second; abstraction into
# engineered swarm computation last.
nb.cells[reader_start:reader_end] = biomimicry + superorganisms + framing

nbformat.write(nb, PATH)
print(f"Updated {PATH.relative_to(ROOT)}")
