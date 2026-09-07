"""Assign unique stable IDs to Week 6 notebook cells."""

import hashlib
import json
from pathlib import Path


path = Path(__file__).resolve().parents[1] / "notebooks/week06/L_Synchronisation.ipynb"
nb = json.loads(path.read_text())
used: set[str] = set()

for index, cell in enumerate(nb["cells"]):
    candidate = cell.get("id")
    if not candidate or candidate in used:
        seed = f"week06:{index}:" + "".join(cell.get("source", []))
        candidate = "w6-" + hashlib.sha1(seed.encode()).hexdigest()[:10]
        suffix = 1
        base = candidate
        while candidate in used:
            suffix += 1
            candidate = f"{base}-{suffix}"
        cell["id"] = candidate
    used.add(candidate)

path.write_text(json.dumps(nb, indent=1, ensure_ascii=False) + "\n")
