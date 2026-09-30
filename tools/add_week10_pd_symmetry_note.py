"""Add the symmetry bridge to the Week 10 Player 1 analysis slide."""

from __future__ import annotations

import json
from pathlib import Path


PATH = Path(__file__).resolve().parents[1] / "notebooks/week10/L_Game_theory.ipynb"


def main() -> None:
    notebook = json.loads(PATH.read_text())
    cell = next(c for c in notebook["cells"] if c.get("id") == "e902a40e-5ac1-4db4-ad7c-a606d1f0f688")
    source = "".join(cell["source"])
    old = "### What should Player 1 do?\n\n<!-- reader-equation: c1cd393a-fb79-4969-886d-91559cef052a:0 -->"
    new = "### What should Player 1 do?\n\nBecause the Prisoner’s Dilemma is symmetric, this is the same comparison as for Player 2, with rows and columns exchanged.\n\n<!-- reader-equation: c1cd393a-fb79-4969-886d-91559cef052a:0 -->"
    if old not in source:
        raise SystemExit("Player 1 slide text not found")
    cell["source"] = source.replace(old, new, 1).splitlines(keepends=True)
    PATH.write_text(json.dumps(notebook, indent=1, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
