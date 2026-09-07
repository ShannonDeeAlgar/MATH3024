"""Put qualitative observation before quantitative compression in Week 6 slides."""

import json
from pathlib import Path


path = Path(__file__).resolve().parents[1] / "notebooks/week06/L_Synchronisation.ipynb"
notebook = json.loads(path.read_text())
cells = notebook["cells"]


def first_line(cell):
    source = "".join(cell.get("source", []))
    return source.splitlines()[0] if source else ""


analysis_index = next(i for i, cell in enumerate(cells) if first_line(cell) == "# Analysis")
scope_index = next(i for i, cell in enumerate(cells[analysis_index + 1 :], analysis_index + 1)
                   if first_line(cell) == "# Scope and connections")

section = cells[analysis_index + 1 : scope_index]
qualitative_index = next(i for i, cell in enumerate(section)
                         if first_line(cell) == "## Qualitative analysis · watch phases organise")
quantitative_index = next(i for i, cell in enumerate(section)
                          if first_line(cell) == "## Quantitative analysis · collective coherence")

if quantitative_index < qualitative_index:
    qualitative_cell = section.pop(qualitative_index)
    quantitative_index = next(i for i, cell in enumerate(section)
                              if first_line(cell) == "## Quantitative analysis · collective coherence")
    section.insert(quantitative_index, qualitative_cell)
    cells[analysis_index + 1 : scope_index] = section

path.write_text(json.dumps(notebook, indent=1, ensure_ascii=False) + "\n")
