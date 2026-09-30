"""Move the one-shot constraints to the preceding Prisoner's Dilemma slide."""

from __future__ import annotations

import json
from pathlib import Path


PATH = Path(__file__).resolve().parents[1] / "notebooks/week10/L_Game_theory.ipynb"


def main() -> None:
    notebook = json.loads(PATH.read_text())
    cells = {cell.get("id"): cell for cell in notebook["cells"]}
    cells["d9bf6664"]["source"] = [
        "## Prisoner's dilemma\n",
        "\n",
        "Two suspects are questioned separately after a burglary. If both stay silent, the police can pursue only a trespassing charge. If one testifies, they provide evidence of the burglary and the other faces the more serious charge. Each suspect’s sentence depends on both choices.\n",
        "\n",
        "A **one-shot game** gives each prisoner one choice. They are questioned separately, cannot communicate or make enforceable agreements, and there are no later rounds for reward or retaliation. An action is therefore also a **pure strategy**.\n",
    ]
    cells["8309b600-a5e3-4836-853a-d685bf85dd2f"]["source"] = [
        "### Set up the game\n",
        "\n",
        "| Component | Specification |\n",
        "|---|---|\n",
        "| **Players** | $P=\\{1,2\\}$ |\n",
        "| **Actions** | $A_1=A_2=\\{C,D\\}$; $C$ means stay silent and $D$ means testify |\n",
        "| **Payoffs (utilities)** | $u_1$ and $u_2$ are negative prison sentences; less negative is better |\n",
        "\n",
        "| Action pair | Sentences |\n",
        "|---|---|\n",
        "| **$(C,D)$** | Player 1 serves 3 years; Player 2 goes free |\n",
        "| **$(D,C)$** | Player 1 goes free; Player 2 serves 3 years |\n",
        "| **$(D,D)$** | 2 years each |\n",
        "| **$(C,C)$** | 1 year each |\n",
        "\n",
        "<p style=\"font-size:0.68em;color:#5B6780\"><strong>Notation:</strong> Subscripts identify the player: <em>A</em><sub>1</sub> and <em>u</em><sub>1</sub> belong to Player 1; <em>A</em><sub>2</sub> and <em>u</em><sub>2</sub> to Player 2. Here <em>C</em> means cooperate (stay silent) and <em>D</em> means defect (testify). Other sources may reverse these labels: <em>C</em> can mean confess (testify) and <em>D</em> can mean do not confess (stay silent). Always check the action definitions.</p>\n",
    ]
    PATH.write_text(json.dumps(notebook, indent=1, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
