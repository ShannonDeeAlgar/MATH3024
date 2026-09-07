"""Place the Week 6 scene-setting Explorable before formal model details."""

import json
from pathlib import Path


path = Path(__file__).resolve().parents[1] / "notebooks/week06/L_Synchronisation.ipynb"
notebook = json.loads(path.read_text())
cells = notebook["cells"]


def heading(cell):
    source = "".join(cell.get("source", []))
    return source.splitlines()[0] if source else ""


def tags(cell):
    return set(cell.get("metadata", {}).get("tags", []))


def reorder_for(audience_tag):
    starts = [
        (index, heading(cell))
        for index, cell in enumerate(cells)
        if audience_tag in tags(cell) and heading(cell).startswith("# ")
    ]
    model_start = next(index for index, title in starts if title == "# Model details")
    explorable_start = next(index for index, title in starts if title == "# Explorable")
    analysis_start = next(index for index, title in starts if title == "# Analysis")

    if model_start < explorable_start:
        model_group = cells[model_start:explorable_start]
        explorable_group = cells[explorable_start:analysis_start]
        cells[model_start:analysis_start] = explorable_group + model_group


reorder_for("slides-only")
reorder_for("reader-only")

path.write_text(json.dumps(notebook, indent=1, ensure_ascii=False) + "\n")
