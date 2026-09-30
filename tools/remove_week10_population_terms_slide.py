"""Remove the standalone Week 10 population-terms slide."""

from __future__ import annotations

import json
from pathlib import Path


PATH = Path(__file__).resolve().parents[1] / "notebooks/week10/L_Game_theory.ipynb"


def main() -> None:
    notebook = json.loads(PATH.read_text())
    cell = next(c for c in notebook["cells"] if c.get("id") == "w10-population-terms-slide")
    tags = set(cell.setdefault("metadata", {}).get("tags", []))
    tags.add("remove-cell")
    cell["metadata"]["tags"] = sorted(tags)
    PATH.write_text(json.dumps(notebook, indent=1, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
