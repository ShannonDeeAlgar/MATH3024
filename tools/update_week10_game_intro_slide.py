"""Align the Week 10 opening game-definition slide with the Reader."""

from __future__ import annotations

import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from tools.check_equation_consistency import math_signature, resolved_source


ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK = ROOT / "notebooks/week10/L_Game_theory.ipynb"
MANIFEST = ROOT / "tools/equation_consistency.json"


def main() -> None:
    notebook = json.loads(NOTEBOOK.read_text())
    cells = {cell.get("id"): cell for cell in notebook["cells"]}
    cells["w10-shared-conflicting-objectives-slide"]["source"] = [
        "## What is a game?\n",
        "\n",
        "A game represents strategic interaction: players choose actions, and each payoff depends on the combination of choices.\n",
        "\n",
        "A one-shot game specifies the players, their available actions, and a payoff for every action profile. In standard normal form,\n",
        "\n",
        "<!-- reader-equation: w10-game-basics-reader:0 -->\n",
        "\n",
        "A normal-form table records these possibilities without a sequence-of-moves diagram.\n",
    ]
    data = json.loads(MANIFEST.read_text())
    entry = data["notebooks"]["notebooks/week10/L_Game_theory.ipynb"]
    link = {
        "slide": "w10-shared-conflicting-objectives-slide",
        "index": 0,
        "mode": "exact",
        "reader": "w10-game-basics-reader",
        "reader_index": 0,
    }
    if link not in entry["displays"]:
        entry["displays"].append(link)
    entry["math_signatures"]["w10-shared-conflicting-objectives-slide"] = math_signature(
        resolved_source(cells["w10-shared-conflicting-objectives-slide"], cells)
    )
    NOTEBOOK.write_text(json.dumps(notebook, indent=1, ensure_ascii=False) + "\n")
    MANIFEST.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
