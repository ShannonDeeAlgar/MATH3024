#!/usr/bin/env python3
"""Place the representation sequence at the transition and resize the grid diagram."""

import json
from pathlib import Path


NOTEBOOK = Path("notebooks/week03/L_Reaction_diffusion.ipynb")
TRANSITION_ID = "954ca579-6444-4529-9190-05fb00912d11"
SEQUENCE_ID = "088466bd-70cc-484f-ac97-e85a5a7255f4"
GRID_ID = "09eb9036-81a5-4e05-8806-69d16664865b"

nb = json.loads(NOTEBOOK.read_text())
cells = nb["cells"]


def index(cell_id):
    return next(i for i, cell in enumerate(cells) if cell.get("id") == cell_id)


# The three representations explain why the continuous-to-discrete transition occurs,
# so keep them together before the detailed indexing begins.
sequence = cells.pop(index(SEQUENCE_ID))
cells.insert(index(TRANSITION_ID) + 1, sequence)

grid = cells[index(GRID_ID)]
grid_text = "".join(grid.get("source", []))
grid_text = grid_text.replace(
    "style=\"display:block;width:100%;height:auto;max-height:330px;object-fit:contain;margin:0 auto;\"",
    "style=\"display:block;width:84%;height:auto;max-height:255px;object-fit:contain;margin:0 auto;\"",
)
grid["source"] = grid_text.splitlines(keepends=True)

NOTEBOOK.write_text(json.dumps(nb, ensure_ascii=False, indent=1) + "\n")
print(NOTEBOOK.resolve())
