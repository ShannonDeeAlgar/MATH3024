"""Combine the Week 10 Axelrod heading and result figure into one slide."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "notebooks/week10/L_Game_theory.ipynb"


def main() -> None:
    notebook = json.loads(PATH.read_text())
    cells = {cell.get("id"): cell for cell in notebook["cells"]}
    heading = cells["w10-repeated-play-slide"]
    source = "".join(heading["source"]).rstrip()
    if 'id="fig-w10-7"' not in source:
        source += '''

<div class="image-panel"><img src="images/axelrod_tournament_random_opponents.svg" alt="Pairwise payoff heatmap and running mean payoffs for four fixed strategies in a random-opponent Prisoner’s Dilemma tournament." style="width:100%;max-height:330px;object-fit:contain"><p class="figure-caption" id="fig-w10-7"><strong>Figure 10.7.</strong> Pairwise payoffs and random-opponent tournament trajectories.</p></div>
'''
    heading["source"] = source.splitlines(keepends=True)
    cell = cells["w10-tournament-scores-slide"]
    tags = set(cell.setdefault("metadata", {}).get("tags", []))
    tags.add("remove-cell")
    cell["metadata"]["tags"] = sorted(tags)
    PATH.write_text(json.dumps(notebook, indent=1, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
