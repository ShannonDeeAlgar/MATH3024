import json
from pathlib import Path


path = Path("notebooks/week05/L_ABM.ipynb")
notebook = json.loads(path.read_text())
seen = set()
for cell in notebook["cells"]:
    cell_id = cell.get("id")
    if cell_id in seen and "vectorial noise" in "".join(cell.get("source", [])).lower():
        cell["id"] = "week05-vectorial-noise"
    seen.add(cell.get("id"))

path.write_text(json.dumps(notebook, indent=1, ensure_ascii=False) + "\n")
