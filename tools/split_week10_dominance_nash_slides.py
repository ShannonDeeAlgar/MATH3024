"""Split the crowded Week 10 dominance/Nash slide."""

from __future__ import annotations

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from tools.check_equation_consistency import math_signature, resolved_source

PATH = ROOT / "notebooks/week10/L_Game_theory.ipynb"
MANIFEST = ROOT / "tools/equation_consistency.json"


DOMINANCE = r'''#### Dominance

A **dominant strategy** is a best response to every action of the other player. It is **weakly dominant** if it is never worse than an alternative in any comparison, and **strictly dominant** if it is better in every comparison. Equality therefore gives weak, rather than strict, dominance.

In the Prisoner’s Dilemma, comparing the entries shows that $D$ gives a higher payoff than $C$ against either action. Defection is therefore strictly dominant for both players.
'''


NASH_SLIDE = r'''#### Nash equilibrium

An action profile $(a_1^*,a_2^*)$ is a Nash equilibrium when both inequalities hold.

<!-- reader-equation: b091f920-71fa-423d-bcca-802cdfc18199:0 -->

<!-- reader-equation: b091f920-71fa-423d-bcca-802cdfc18199:1 -->

In the Prisoner’s Dilemma, a Nash equilibrium has no profitable **unilateral deviation**. At $(D,D)$, switching alone changes $-2$ to $-3$, so $(D,D)$ is the equilibrium.

<p style="font-size:0.68em;color:#5B6780"><strong>Notation:</strong> $A_i$ is player $i$’s action set; $a_i^*$ is the proposed equilibrium action. Each inequality compares a player’s payoff with every unilateral alternative while the other player stays fixed.</p>
'''


def main() -> None:
    notebook = json.loads(PATH.read_text())
    cells = {cell.get("id"): cell for cell in notebook["cells"]}
    cells["894680c8-6d78-4117-b994-6b42b5c64ffe"]["source"] = DOMINANCE.splitlines(keepends=True)
    cells["b091f920-71fa-423d-bcca-802cdfc18199-notation-slide"]["source"] = NASH_SLIDE.splitlines(keepends=True)
    cells["b091f920-71fa-423d-bcca-802cdfc18199-notation-slide"].setdefault("metadata", {}).setdefault("slideshow", {})["slide_type"] = "subslide"
    PATH.write_text(json.dumps(notebook, indent=1, ensure_ascii=False) + "\n")

    manifest = json.loads(MANIFEST.read_text())
    entry = manifest["notebooks"]["notebooks/week10/L_Game_theory.ipynb"]
    for cell_id in ("894680c8-6d78-4117-b994-6b42b5c64ffe", "b091f920-71fa-423d-bcca-802cdfc18199-notation-slide"):
        entry["math_signatures"][cell_id] = math_signature(resolved_source(cells[cell_id], cells))
    MANIFEST.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
