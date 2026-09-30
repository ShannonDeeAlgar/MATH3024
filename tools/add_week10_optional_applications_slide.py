"""Add a concise slide summarising applications of the PD payoff ordering."""

from pathlib import Path
import json


NOTEBOOK = Path("notebooks/week10/L_Game_theory.ipynb")
AFTER_ID = "w10-comparing-game-types"
SLIDE_ID = "w10-optional-applications-slide"


def main() -> None:
    notebook = json.loads(NOTEBOOK.read_text())
    cells = notebook["cells"]
    if any(cell.get("id") == SLIDE_ID for cell in cells):
        return

    slide = {
        "cell_type": "markdown",
        "id": SLIDE_ID,
        "metadata": {
            "slideshow": {"slide_type": "subslide"},
            "tags": ["slides", "slides-only"],
        },
        "source": [
            "### Optional applications beyond prison\n",
            "\n",
            "The same payoff ordering can arise in other one-shot settings, if the incentives have the same form.\n",
            "\n",
            "| Setting | Cooperate | Defect |\n",
            "|---|---|---|\n",
            "| Shared water | Keep to a quota | Take extra water |\n",
            "| Weapons build-up | Limit weapons | Build up weapons |\n",
            "| Price competition | Keep the higher price | Offer a discount |\n",
            "| Road use | Avoid a shared shortcut | Use the shortcut |\n",
            "\n",
            "The labels are illustrative: check the actual payoffs before calling a situation a Prisoner’s Dilemma.",
        ],
    }

    for index, cell in enumerate(cells):
        if cell.get("id") == AFTER_ID:
            cells.insert(index + 1, slide)
            break
    else:
        raise SystemExit(f"Could not find cell {AFTER_ID}")

    NOTEBOOK.write_text(json.dumps(notebook, indent=1, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
