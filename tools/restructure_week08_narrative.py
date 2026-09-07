"""Reorder Week 8 around tuned criticality and the Abelian sandpile.

This is deliberately assertion-heavy: it should stop rather than silently edit a
different version of the notebook.
"""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "notebooks/week08/L_Critical_phenomena.ipynb"


def text(cell: dict) -> str:
    return "".join(cell.get("source", []))


def set_text(cell: dict, value: str) -> None:
    cell["source"] = value.splitlines(keepends=True)


def find(cells: list[dict], prefix: str) -> dict:
    matches = [cell for cell in cells if text(cell).lstrip().startswith(prefix)]
    if len(matches) != 1:
        raise RuntimeError(f"Expected one cell beginning {prefix!r}; found {len(matches)}")
    return matches[0]


def find_all(cells: list[dict], prefix: str) -> list[dict]:
    return [cell for cell in cells if text(cell).lstrip().startswith(prefix)]


def tags(cell: dict) -> list[str]:
    return cell.setdefault("metadata", {}).setdefault("tags", [])


def add_tag(cell: dict, tag: str) -> None:
    if tag not in tags(cell):
        tags(cell).append(tag)


def remove_tag(cell: dict, tag: str) -> None:
    if tag in tags(cell):
        tags(cell).remove(tag)


def main() -> None:
    notebook = json.loads(PATH.read_text())
    cells = notebook["cells"]

    title = find(cells, "# Critical behaviour")
    real_world = find(cells, "# Real-world motivation")
    starting = find(cells, "## Starting point")
    routes = find(cells, "## Two routes to critical behaviour")
    critical_change = find(cells, "## What changes at a critical point?")
    explorable = find(cells, "# Explorable")
    return_perc = find(cells, "# Return to percolation")
    model_details = find(cells, "# Model details")
    soc = find(cells, "## Self-organised criticality")
    from_btw = find(cells, "### From BTW to the Abelian sandpile")
    abelian_details = find(cells, "### Abelian sandpile · model details")
    qualitative = find(cells, "### Qualitative behaviour")
    quantitative = find(cells, "### Quantitative behaviour")
    analysis = find(cells, "# Analysis")
    analytical = find(cells, "## Analytical change of scale")
    rga = find(cells, "## Renormalisation Group Analysis (RGA)")
    scope = find(cells, "# Scope and connections")

    borrow = find_all(cells, "### Borrow code; audit the model")
    sandpile = find_all(cells, "## Sandpile models")
    if len(borrow) != 2 or len(sandpile) != 2:
        raise RuntimeError("Expected paired Reader/slide cells for borrowing code and sandpiles")

    set_text(return_perc, "## Tuned criticality · percolation\n")
    set_text(soc, text(soc).replace("## Self-organised criticality", "## Self-organised criticality · sandpile", 1))
    set_text(from_btw, text(from_btw).replace("### From BTW to the Abelian sandpile", "### Canonical model · the Abelian sandpile", 1))
    set_text(abelian_details, text(abelian_details).replace("### Abelian sandpile · model details", "### Specify the model", 1))
    set_text(qualitative, "## Qualitative analysis\n")
    set_text(quantitative, text(quantitative).replace("### Quantitative behaviour", "## Quantitative analysis", 1))
    set_text(analysis, "# Optional reader extension · changing scale\n")
    set_text(analytical, text(analytical).replace("## Analytical change of scale", "## Why coarse-grain?", 1))
    set_text(rga, text(rga).replace("## Renormalisation Group Analysis (RGA)", "## Renormalisation-group example · forest fire", 1))

    # The changing-scale material is valuable context but not part of the core
    # lecture route. Keep it in the Reader and out of generated slides.
    start_optional = cells.index(analysis)
    end_optional = cells.index(scope)
    for cell in cells[start_optional:end_optional]:
        add_tag(cell, "reader-only")
        remove_tag(cell, "slides")
        remove_tag(cell, "slides-only")

    # Remove empty separator cells left by an earlier export, but retain every
    # substantive explanation, figure and calculation.
    cells = [cell for cell in cells if text(cell).strip() or cell.get("cell_type") == "code"]

    # Re-fetch indices after removing empty markdown cells.
    def idx(cell: dict) -> int:
        return cells.index(cell)

    # Move the critical-point explanation so it follows the visible percolation
    # example, rather than asking students to absorb the abstractions first.
    cells.remove(critical_change)
    insert_after_perc = idx(return_perc) + 1
    # Include the percolation prose cells that originally followed its heading.
    while insert_after_perc < len(cells) and not text(cells[insert_after_perc]).lstrip().startswith("# Model details"):
        insert_after_perc += 1
    cells.insert(insert_after_perc, critical_change)

    # Borrowing code belongs immediately before the model specification: it is
    # the modelling practice used to implement this canonical model, not part of
    # the opening definition of criticality.
    for cell in borrow:
        cells.remove(cell)
    model_index = cells.index(abelian_details)
    for offset, cell in enumerate(borrow):
        cells.insert(model_index + offset, cell)

    # Put the physical sandpile and historical bridge before the formal model.
    # The paired headings remain because one is Reader-only and one is slide-only.
    for cell in sandpile:
        cells.remove(cell)
    soc_index = cells.index(soc) + 1
    for offset, cell in enumerate(sandpile):
        cells.insert(soc_index + offset, cell)

    notebook["cells"] = cells
    PATH.write_text(json.dumps(notebook, ensure_ascii=False, indent=1) + "\n")


if __name__ == "__main__":
    main()
