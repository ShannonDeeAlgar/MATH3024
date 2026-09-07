"""Place the Week 6 modelling pause before analysis and restore the end summary."""

import json
from pathlib import Path


path = Path(__file__).resolve().parents[1] / "notebooks/week06/L_Synchronisation.ipynb"
notebook = json.loads(path.read_text())
cells = notebook["cells"]


def move_before(cell_id, target_id):
    cell = next(item for item in cells if item.get("id") == cell_id)
    cells.remove(cell)
    target_index = next(i for i, item in enumerate(cells) if item.get("id") == target_id)
    cells.insert(target_index, cell)


# The modelling pause closes the model-building sequence and leads into analysis.
move_before("w6-specify", "w6-66a5febb56")
move_before("firefly-model", "w6-e3d28ed62b")

# The standard summary and pseudocode remain the final Reader section.
canonical = next(item for item in cells if item.get("id") == "canonical-pseudocode")
cells.remove(canonical)
cells.append(canonical)

path.write_text(json.dumps(notebook, indent=1, ensure_ascii=False) + "\n")
