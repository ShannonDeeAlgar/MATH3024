"""Place the Week 10 rock-paper-scissors figure and matrix side by side."""

from __future__ import annotations

import json
from pathlib import Path


PATH = Path(__file__).resolve().parents[1] / "notebooks/week10/L_Game_theory.ipynb"


def main() -> None:
    notebook = json.loads(PATH.read_text())
    cells = {cell.get("id"): cell for cell in notebook["cells"]}
    cells["w10-rps-local-game-slide"]["source"] = r'''## Familiar example: rock–paper–scissors

Two players simultaneously choose rock, paper or scissors; a win gives $+1$, a loss $-1$, and a draw $0$.

<div class="two-panel equal-panels compact-panels" style="align-items:start">
<div class="image-panel rps-cycle"><img src="images/rps_cyclic_dominance.svg" alt="Rock, paper and scissors icons arranged in a compact cyclic dominance diagram; arrows point from each winner to the action it defeats." style="max-width:380px;width:100%;"><p class="figure-caption" id="fig-w10-1"><strong>Figure 10.1.</strong> Rock–paper–scissors as cyclic dominance. Arrows point from the winning action to the action it defeats.</p></div>
<div class="text-panel">

| Player 1 \ Player 2 | Rock | Paper | Scissors |
|---|---:|---:|---:|
| **Rock** | $(0,0)$ | $(-1,+1)$ | $(+1,-1)$ |
| **Paper** | $(+1,-1)$ | $(0,0)$ | $(-1,+1)$ |
| **Scissors** | $(-1,+1)$ | $(+1,-1)$ | $(0,0)$ |
</div>
</div>

Rock–paper–scissors is **zero-sum**, **symmetric**, and **cyclic**: each action defeats one alternative and loses to the other.

<p style="font-size:0.68em;color:#5B6780">The table is the payoff matrix. Each payoff pair is ordered (player 1, player 2); player 1 selects the row and player 2 the column.</p>
'''.splitlines(keepends=True)
    PATH.write_text(json.dumps(notebook, indent=1, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
