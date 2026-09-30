"""Add a side-by-side atlas-reading guide for the Prisoner's Dilemma and Stag Hunt."""

from pathlib import Path
import json


NOTEBOOK = Path("notebooks/week10/L_Game_theory.ipynb")
AFTER_ID = "09fa3a4f"
SLIDE_ID = "w10-atlas-reading-slide"


SOURCE = [
    "### Reading the atlas\n",
    "\n",
    "Figure 10.5 shows the rank pairs. Figure 10.6 shows profitable unilateral changes. Find the same game in both views.\n",
    "\n",
    '<p class="small-note"><strong>Legend:</strong> rank pairs are (Player 1, Player 2). Red arrows improve Player 1’s payoff; blue arrows improve Player 2’s payoff.</p>\n',
    '<div class="two-panel atlas-reading-pair" style="grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:1em;align-items:start">\n',
    '<div class="atlas-reading-column"><p class="atlas-game-label">Prisoner’s Dilemma</p>\n',
    '<div class="atlas-reading-blocks" style="display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:0.55em">\n',
    '<img src="images/atlas_pd_105.svg" alt="Clean vector rank block for the Prisoner’s Dilemma" style="width:100%;height:auto">\n',
    '<img src="images/atlas_pd_106.svg" alt="Clean vector arrow block for the Prisoner’s Dilemma" style="width:100%;height:auto">\n',
    '</div>\n',
    '<p class="small-note">Both improving paths lead to mutual defection.</p></div>\n',
    '<div class="atlas-reading-column"><p class="atlas-game-label">Stag Hunt</p>\n',
    '<div class="atlas-reading-blocks" style="display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:0.55em">\n',
    '<img src="images/atlas_stag_105.svg" alt="Clean vector rank block for Stag Hunt" style="width:100%;height:auto">\n',
    '<img src="images/atlas_stag_106.svg" alt="Clean vector arrow block for Stag Hunt" style="width:100%;height:auto">\n',
    '</div>\n',
    '<p class="small-note">Improving paths lead to either diagonal profile.</p></div>\n',
    '</div>\n',
]


def main() -> None:
    notebook = json.loads(NOTEBOOK.read_text())
    cells = notebook["cells"]
    existing = next((cell for cell in cells if cell.get("id") == SLIDE_ID), None)
    if existing is not None:
        existing["source"] = SOURCE
        NOTEBOOK.write_text(json.dumps(notebook, indent=1, ensure_ascii=False) + "\n")
        return

    slide = {
        "cell_type": "markdown",
        "id": SLIDE_ID,
        "metadata": {
            "slideshow": {"slide_type": "subslide"},
            "tags": ["slides", "slides-only"],
        },
        "source": SOURCE,
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
