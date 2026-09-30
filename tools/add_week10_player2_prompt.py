"""Add the Player 2 discussion prompt to the Week 10 analysis slide."""

from __future__ import annotations

import json
from pathlib import Path


PATH = Path(__file__).resolve().parents[1] / "notebooks/week10/L_Game_theory.ipynb"


def main() -> None:
    notebook = json.loads(PATH.read_text())
    cells = {cell.get("id"): cell for cell in notebook["cells"]}
    cell = cells["5cddb19c"]
    source = "".join(cell["source"])
    marker = '<div class="discussion-marker"><img src="images/discussion_marker.svg" alt="Discussion prompt"><span>What outcome would Player 2 prefer?</span></div>\n'
    if marker not in source:
        source = source.rstrip() + "\n\n" + marker
    cell["source"] = source.splitlines(keepends=True)
    PATH.write_text(json.dumps(notebook, indent=1, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
