"""Add the Reader's tournament/evolution figure and renumber later figures."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK = ROOT / "notebooks/week10/L_Game_theory.ipynb"


SOURCE = """#### Tournament scores can feed an evolutionary model

The tournament keeps the four strategy rules fixed. The model in Figure 10.8 uses the same strategies in a finite, well-mixed population of 2,000 agents, starting in equal shares. One round is one Prisoner’s Dilemma encounter; 50 rounds make one repeated match. For each pair of strategies, 80 independent matches are used to estimate the mean payoff per round. Those pairwise means are then used to update the population for 60 generations.

An agent keeps its strategy throughout a repeated game; it does not jump to another strategy after an individual round. Between generations, strategies with higher mean payoff are copied more often, using selection strength 0.08 and no mutation. The coloured bands show population shares, not individual actions. In this run Tit for Tat becomes the largest share, but that outcome depends on the opponent field, payoff ordering, match length and update rule.

<div class="image-panel"><img src="images/axelrod_evolution_dynamics.svg" alt="Population shares of Always Cooperate, Always Defect, Tit for Tat and Random over generations when copying success depends on mean payoff." style="width:100%;max-height:430px;object-fit:contain"><p class="figure-caption" id="fig-w10-8"><strong>Figure 10.8.</strong> One 60-generation population run with 2,000 agents. Each strategy pairing is first estimated from 80 independent 50-round matches; higher mean payoff then gives a strategy more copies between generations.</p></div>

For scale, the linked [Axelrod-Python pairwise payoff results](https://axelrod-tournament.readthedocs.io/en/stable/standard/all_strategies.html#payoffs) extend the tournament to the library's 243 strategies. The page also shows a separate [evolutionary-dynamics plot](https://axelrod-tournament.readthedocs.io/en/stable/standard/all_strategies.html#evolutionary-dynamics), where strategy frequencies change. These full-library plots are useful reference views, but their labels are too dense to serve as the main teaching figures here.
"""


def main() -> None:
    notebook = json.loads(NOTEBOOK.read_text())
    cells = notebook["cells"]

    for cell in cells:
        source = "".join(cell.get("source", []))
        if "pd_replicator_dynamics.svg" in source:
            source = source.replace('fig-w10-8', 'fig-w10-9').replace('<strong>Figure 10.8.</strong>', '<strong>Figure 10.9.</strong>')
            cell["source"] = source.splitlines(keepends=True)

    field_cell = next((cell for cell in cells if cell.get("id") == "w10-tournament-field-distribution"), None)
    if field_cell is not None:
        field_cell["source"] = SOURCE.splitlines(keepends=True)
    else:
        insert_at = next(i for i, cell in enumerate(cells) if cell.get("id") == "w10-tournament-scores-slide")
        cells.insert(insert_at, {
            "cell_type": "markdown",
            "id": "w10-tournament-field-distribution",
            "metadata": {
                "slideshow": {"slide_type": "subslide"},
                "tags": ["reader-only"],
            },
            "source": SOURCE.splitlines(keepends=True),
        })

    NOTEBOOK.write_text(json.dumps(notebook, ensure_ascii=False, indent=1) + "\n")


if __name__ == "__main__":
    main()
