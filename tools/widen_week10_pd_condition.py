"""Give the explanation more room on the Prisoner's Dilemma condition slide."""

from pathlib import Path
import json


NOTEBOOK = Path("notebooks/week10/L_Game_theory.ipynb")
CELL_ID = "a8733185-a037-45a2-b04e-75ac43cedb98-notation-slide"


def main() -> None:
    notebook = json.loads(NOTEBOOK.read_text())
    for cell in notebook["cells"]:
        if cell.get("id") == CELL_ID:
            source = "".join(cell.get("source", []))
            source = source.replace(
                '<div class="figure-interpretation-layout">',
                '<div class="figure-interpretation-layout" style="grid-template-columns:minmax(0,0.8fr) minmax(0,1.2fr);">',
                1,
            )
            cell["source"] = source.splitlines(keepends=True)
            break
    else:
        raise SystemExit(f"Could not find cell {CELL_ID}")

    NOTEBOOK.write_text(json.dumps(notebook, indent=1, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
