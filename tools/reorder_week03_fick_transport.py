#!/usr/bin/env python3
"""Tighten the Week 3 Reader sequence around diffusion and transport."""

import json
from pathlib import Path


NOTEBOOK = Path("notebooks/week03/L_Reaction_diffusion.ipynb")


def source(cell):
    return "".join(cell.get("source", []))


def set_source(cell, value):
    cell["source"] = value.splitlines(keepends=True)


def index_by_id(cells, cell_id):
    return next(i for i, cell in enumerate(cells) if cell.get("id") == cell_id)


def move_before(cells, moving_id, target_id):
    moving = cells.pop(index_by_id(cells, moving_id))
    cells.insert(index_by_id(cells, target_id), moving)


def move_after(cells, moving_id, target_id):
    moving = cells.pop(index_by_id(cells, moving_id))
    cells.insert(index_by_id(cells, target_id) + 1, moving)


nb = json.loads(NOTEBOOK.read_text())
cells = nb["cells"]

# The historical explanation continues directly from the Gray–Scott introduction.
history = cells[index_by_id(cells, "week03-gray-scott-history-reader")]
set_source(history, source(history).replace("## Why Gray–Scott?\n\n", "", 1))

# Fick's laws supply the macroscopic equation before the field interpretation.
fick_id = "57d73b10-bd0c-4326-b40d-50a7e9eb7c03"
field_id = "1c111a8d-516f-4637-95c0-080efdec3d90"
move_before(cells, fick_id, field_id)

# Do not state the diffusion equation for a second time on the field slide.
field = cells[index_by_id(cells, field_id)]
set_source(
    field,
    source(field).replace(
        "\n$$\n\\frac{\\partial C}{\\partial t}=D\\nabla^2C.\n$$\n",
        "\n",
        1,
    ),
)

# Keep the optional transport extension beside the general reaction–diffusion model,
# immediately before the specific Gray–Scott construction.
transport_id = "4fad79e4-e78d-468c-be71-d70d8c4c711e"
general_rd_id = "week03-turing-paper-scope"
move_after(cells, transport_id, general_rd_id)

NOTEBOOK.write_text(json.dumps(nb, ensure_ascii=False, indent=1) + "\n")
print(NOTEBOOK.resolve())
