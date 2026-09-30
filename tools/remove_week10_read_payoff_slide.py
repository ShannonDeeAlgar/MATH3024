"""Remove the redundant Week 10 payoff-entry slide."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK = ROOT / "notebooks/week10/L_Game_theory.ipynb"
MANIFEST = ROOT / "tools/equation_consistency.json"


def main() -> None:
    notebook = json.loads(NOTEBOOK.read_text())
    cell = next(c for c in notebook["cells"] if c.get("id") == "w10-read-payoff-slide")
    tags = set(cell.setdefault("metadata", {}).get("tags", []))
    tags.add("remove-cell")
    cell["metadata"]["tags"] = sorted(tags)
    NOTEBOOK.write_text(json.dumps(notebook, indent=1, ensure_ascii=False) + "\n")

    manifest = json.loads(MANIFEST.read_text())
    entry = manifest["notebooks"]["notebooks/week10/L_Game_theory.ipynb"]
    entry["math_signatures"].pop("w10-read-payoff-slide", None)
    entry["displays"] = [link for link in entry["displays"] if link.get("slide") != "w10-read-payoff-slide"]
    MANIFEST.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
