"""Reflow the Week 10 Prisoner's Dilemma setup and payoff slides."""

from __future__ import annotations

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from tools.check_equation_consistency import math_signature, resolved_source

PATH = ROOT / "notebooks/week10/L_Game_theory.ipynb"
MANIFEST = ROOT / "tools/equation_consistency.json"


SETUP = r'''### Set up the game

| Component | Specification |
|---|---|
| **Players** | $P=\{1,2\}$ |
| **Actions** | $A_1=A_2=\{C,D\}$; $C$ means stay silent and $D$ means testify |
| **Payoffs (utilities)** | $u_1$ and $u_2$ are negative prison sentences; less negative is better |

<p style="font-size:0.68em;color:#5B6780"><strong>Notation:</strong> Subscripts identify the player: <em>A</em><sub>1</sub> and <em>u</em><sub>1</sub> belong to Player 1; <em>A</em><sub>2</sub> and <em>u</em><sub>2</sub> to Player 2. Here <em>C</em> means cooperate (stay silent) and <em>D</em> means defect (testify). Other sources may reverse these labels: <em>C</em> can mean confess (testify) and <em>D</em> can mean do not confess (stay silent). Always check the action definitions.</p>
'''


ACTION_PROFILES = r'''#### Action profiles

<!-- reader-equation: 185e0fc7-41d0-47a3-b5e9-cdedc9619297:0 -->

The sentence outcomes for these action profiles are:

| Action pair | Sentences |
|---|---|
| **$(C,D)$** | Player 1 serves 3 years; Player 2 goes free |
| **$(D,C)$** | Player 1 goes free; Player 2 serves 3 years |
| **$(D,D)$** | 2 years each |
| **$(C,C)$** | 1 year each |

<p style="font-size:0.68em;color:#5B6780"><strong>Notation:</strong> $S$ is the set of action pairs; $\times$ forms the Cartesian product. The first entry is Player 1's action.</p>
'''


PAYOFFS = r'''#### Payoffs

The set of **action profiles** contains all possible action pairs. For each profile in $S$, $u_1$ and $u_2$ give the two prisoners' utilities.

Using negative years in prison as utility gives

<!-- reader-equation: e190c160-09b7-46d5-8983-6aa6f397daf4:0 -->

<table style="width:100%;table-layout:fixed"><colgroup><col style="width:40%"><col style="width:40%"><col style="width:20%"></colgroup><thead><tr><th>Quantity shown</th><th>Objective</th><th>1-year sentence</th></tr></thead><tbody><tr><td>Prison years $t_i$</td><td>Minimise</td><td>$1$</td></tr><tr><td>Payoff $u_i=-t_i$</td><td>Maximise</td><td>$-1$</td></tr><tr><td>Payoff $u_i=3-t_i$</td><td>Maximise</td><td>$2$</td></tr></tbody></table>

<p style="font-size:0.64em;color:#5B6780"><strong>Convention:</strong> All three rank the outcomes identically. This chapter uses $u_i=-t_i$. Prison time is a cost to minimise; payoff or utility is maximised, so the larger utility is preferred.</p>
'''


def main() -> None:
    notebook = json.loads(PATH.read_text())
    cells = {cell.get("id"): cell for cell in notebook["cells"]}
    cells["8309b600-a5e3-4836-853a-d685bf85dd2f"]["source"] = SETUP.splitlines(keepends=True)
    cells["185e0fc7-41d0-47a3-b5e9-cdedc9619297-notation-slide"]["source"] = ACTION_PROFILES.splitlines(keepends=True)
    cells["e190c160-09b7-46d5-8983-6aa6f397daf4-notation-slide"]["source"] = PAYOFFS.splitlines(keepends=True)
    PATH.write_text(json.dumps(notebook, indent=1, ensure_ascii=False) + "\n")

    manifest = json.loads(MANIFEST.read_text())
    entry = manifest["notebooks"]["notebooks/week10/L_Game_theory.ipynb"]
    for cell_id in ("8309b600-a5e3-4836-853a-d685bf85dd2f", "185e0fc7-41d0-47a3-b5e9-cdedc9619297-notation-slide", "e190c160-09b7-46d5-8983-6aa6f397daf4-notation-slide"):
        entry["math_signatures"][cell_id] = math_signature(
            resolved_source(cells[cell_id], cells)
        )
    MANIFEST.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
