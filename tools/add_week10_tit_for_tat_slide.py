"""Add a concise Tit for Tat strategy slide to the Axelrod sequence."""

from pathlib import Path
import json


NOTEBOOK = Path("notebooks/week10/L_Game_theory.ipynb")
AFTER_ID = "w10-repeated-play-slide"
SLIDE_ID = "w10-tit-for-tat-slide"


SOURCE = [
    "### Tit for Tat\n",
    "\n",
    '<div class="two-panel compact-panels" style="grid-template-columns:minmax(0,0.95fr) minmax(0,1.05fr);gap:1.15em;align-items:start">\n',
    '<div class="text-panel" style="font-size:0.80em;line-height:1.18"><p style="margin:0 0 0.35em"><strong>Rule</strong></p><ol style="margin-top:0"><li>Start with C.</li><li>Copy the opponent’s previous action.</li></ol><table class="game-payoff-table" style="width:100%;table-layout:fixed;font-size:0.90em"><thead><tr><th>Round</th><th>1</th><th>2</th><th>3</th></tr></thead><tbody><tr><th>Opponent</th><td>C</td><td>D</td><td>C</td></tr><tr><th>Tit for Tat</th><td>C</td><td>D</td><td>C</td></tr></tbody></table></div>\n',
    '<div class="text-panel" style="font-size:0.80em;line-height:1.18"><p style="margin:0 0 0.35em"><strong>Why it can work well</strong></p><table class="game-payoff-table" style="width:100%;table-layout:fixed;font-size:0.92em"><thead><tr><th style="width:30%">Property</th><th>Behaviour</th></tr></thead><tbody><tr><th>Nice</th><td>Starts with C.</td></tr><tr><th>Retaliatory</th><td>Answers D with D.</td></tr><tr><th>Forgiving</th><td>Returns to C after C.</td></tr><tr><th>Non-envious</th><td>Seeks a good joint score.</td></tr></tbody></table></div>\n',
    '</div>\n',
    '\n',
    '<p class="small-note">These properties describe why the rule can do well against a varied opponent field. Its ranking still depends on the opponents, match length and noise.</p>\n',
    '<p class="small-note"><strong>Variants:</strong> <em>Tit for Two Tats</em> defects only after two consecutive defections. <em>Two Tits for Tat</em> answers one defection with two defections.</p>\n',
]


def main() -> None:
    notebook = json.loads(NOTEBOOK.read_text())
    cells = notebook["cells"]
    existing = next((cell for cell in cells if cell.get("id") == SLIDE_ID), None)
    if existing is not None:
        source = "".join(existing.get("source", []))
        variant = '<p class="small-note"><strong>Variants:</strong> <em>Tit for Two Tats</em> defects only after two consecutive defections. <em>Two Tits for Tat</em> answers one defection with two defections.</p>\n'
        if "Tit for Two Tats" not in source:
            existing["source"].append(variant)
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
