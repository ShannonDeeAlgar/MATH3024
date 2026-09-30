"""Split the Week 10 game comparison into concise slides."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK = ROOT / "notebooks/week10/L_Game_theory.ipynb"
MANIFEST = ROOT / "tools/equation_consistency.json"


DESCRIPTION = r'''## Comparing game types

These two-action games use the same row/column convention. The first three use ordinal ranks; Matching Pennies uses win/loss payoffs.

<table class="game-type-comparison" style="width:100%;table-layout:fixed"><colgroup><col style="width:20%"><col style="width:48%"><col style="width:32%"></colgroup><thead><tr><th>Game</th><th>Structure and pure equilibria</th><th>Illustrative application</th></tr></thead><tbody><tr><th scope="row">Prisoner’s Dilemma</th><td>Conflict; defection is strictly dominant; one pure equilibrium at (D, D).</td><td>Shared resources, arms races, congestion.</td></tr><tr><th scope="row">Stag Hunt</th><td>Coordination; two diagonal pure equilibria.</td><td>Collective action, standards, climate action.</td></tr><tr><th scope="row">Chicken</th><td>Anti-coordination; two off-diagonal pure equilibria.</td><td>Brinkmanship, traffic, bargaining.</td></tr><tr><th scope="row">Matching Pennies</th><td>Asymmetric zero-sum conflict; no pure equilibrium.</td><td>Prediction and evasion, inspections, cybersecurity.</td></tr></tbody></table>

Coordination rewards compatible choices; anti-coordination rewards different choices. With two equilibria, expectations and communication can affect which one occurs.
'''


DIAGRAMS = r'''### Best-response diagrams

<div class="image-panel"><img src="images/game_type_best_response_arrows.svg" alt="Best-response arrows and stable or unstable profiles for the Prisoner's Dilemma, Stag Hunt, Chicken and Matching Pennies" style="width:100%;max-height:390px;object-fit:contain"><p class="figure-caption" id="fig-w10-4"><strong>Figure 10.4.</strong> Best-response arrows for four games. Filled circles mark pure-strategy Nash equilibria; open circles mark other profiles. Red arrows change Player 1’s action; blue arrows change Player 2’s.</p></div>

<p class="small-note"><strong>Geometry:</strong> The rectangles lay out action profiles; their spacing is not a payoff scale. Figure 10.2 is different: its parallelogram reflects the numerical utilities used there.</p>
'''


MATRICES = r'''### Normal-form matrices

<div class="game-matrix-row" style="display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:0.35rem;align-items:start;width:100%;margin:0.8rem 0 0.35rem">
<div style="min-width:0"><p style="text-align:center;margin:0 0 0.25rem"><strong>Prisoner’s Dilemma</strong></p><table class="game-payoff-table" style="width:100%;font-size:0.68em;table-layout:fixed"><colgroup><col style="width:46%"><col style="width:27%"><col style="width:27%"></colgroup><thead><tr><th> P1\\P2 </th><th>C</th><th>D</th></tr></thead><tbody><tr><th>C</th><td>(3,3)</td><td>(1,4)</td></tr><tr><th>D</th><td>(4,1)</td><td>(2,2)</td></tr></tbody></table></div>
<div style="min-width:0"><p style="text-align:center;margin:0 0 0.25rem"><strong>Stag Hunt</strong></p><table class="game-payoff-table" style="width:100%;font-size:0.68em;table-layout:fixed"><colgroup><col style="width:46%"><col style="width:27%"><col style="width:27%"></colgroup><thead><tr><th> P1\\P2 </th><th>Stag</th><th>Hare</th></tr></thead><tbody><tr><th>Stag</th><td>(4,4)</td><td>(1,3)</td></tr><tr><th>Hare</th><td>(3,1)</td><td>(2,2)</td></tr></tbody></table></div>
<div style="min-width:0"><p style="text-align:center;margin:0 0 0.25rem"><strong>Chicken</strong></p><table class="game-payoff-table" style="width:100%;font-size:0.68em;table-layout:fixed"><colgroup><col style="width:46%"><col style="width:27%"><col style="width:27%"></colgroup><thead><tr><th> P1\\P2 </th><th>Yield</th><th>Escalate</th></tr></thead><tbody><tr><th>Yield</th><td>(3,3)</td><td>(2,4)</td></tr><tr><th>Escalate</th><td>(4,2)</td><td>(1,1)</td></tr></tbody></table></div>
<div style="min-width:0"><p style="text-align:center;margin:0 0 0.25rem"><strong>Matching Pennies</strong></p><table class="game-payoff-table" style="width:100%;font-size:0.68em;table-layout:fixed"><colgroup><col style="width:46%"><col style="width:27%"><col style="width:27%"></colgroup><thead><tr><th> P1\\P2 </th><th>Heads</th><th>Tails</th></tr></thead><tbody><tr><th>Heads</th><td>(1,−1)</td><td>(−1,1)</td></tr><tr><th>Tails</th><td>(−1,1)</td><td>(1,−1)</td></tr></tbody></table></div>
</div>

<p class="small-note">Read across a fixed row or down a fixed column to compare one player’s unilateral choices. The arrows show the same comparisons as profitable changes.</p>
'''


def cell(cell_id: str, source: str) -> dict:
    return {
        "cell_type": "markdown",
        "id": cell_id,
        "metadata": {"editable": True, "slideshow": {"slide_type": "subslide"}},
        "source": source.splitlines(keepends=True),
    }


def main() -> None:
    notebook = json.loads(NOTEBOOK.read_text())
    cells = notebook["cells"]
    existing = {c.get("id"): c for c in cells}

    comparison = existing["w10-comparing-game-types"]
    comparison["source"] = DESCRIPTION.splitlines(keepends=True)
    comparison.setdefault("metadata", {}).setdefault("slideshow", {})["slide_type"] = "slide"

    additions = [
        cell("w10-game-comparison-diagrams", DIAGRAMS),
        cell("w10-game-comparison-matrices", MATRICES),
    ]
    cells[:] = [c for c in cells if c.get("id") not in {a["id"] for a in additions}]
    index = next(i for i, c in enumerate(cells) if c.get("id") == "w10-comparing-game-types")
    cells[index + 1:index + 1] = additions
    NOTEBOOK.write_text(json.dumps(notebook, indent=1, ensure_ascii=False) + "\n")

    manifest = json.loads(MANIFEST.read_text())
    signatures = manifest["notebooks"]["notebooks/week10/L_Game_theory.ipynb"]["math_signatures"]
    signatures.pop("w10-comparing-game-types", None)
    MANIFEST.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
