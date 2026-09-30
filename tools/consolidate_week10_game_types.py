"""Consolidate the Week 10 2x2 game comparison."""

from __future__ import annotations

import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from tools.check_equation_consistency import math_signature
from tools.rewrite_week10_axelrod_reader import TOURNAMENT_INTRO, TOURNAMENT_RESULTS


ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "notebooks/week10/L_Game_theory.ipynb"


COMPARISON = r'''## Comparing game types

These four $2\times2$ games use the same way of reading a payoff matrix. The compact matrices below use the ordinal ranks 1 to 4 for the first three games; Matching Pennies uses win/loss payoffs. Player 1 chooses a row, Player 2 a column, and each cell gives $(u_1,u_2)$.

<table class="game-type-comparison" style="width:100%;table-layout:fixed"><colgroup><col style="width:27%"><col style="width:43%"><col style="width:30%"></colgroup><thead><tr><th>Game</th><th>Structure and pure Nash equilibria</th><th>Wider application (illustrative)</th></tr></thead><tbody><tr><th scope="row"><strong>Prisoner’s Dilemma</strong></th><td><strong>Symmetric, non-zero-sum</strong> conflict; defection is strictly dominant; one equilibrium at (D, D). Mutual cooperation would give both players more.</td><td>Shared resources, arms races, price competition and congestion.</td></tr><tr><th scope="row"><strong>Stag Hunt</strong></th><td><strong>Symmetric coordination</strong>; best response follows the other action, giving two diagonal equilibria. Mutual Stag is best; mutual Hare is safer.</td><td>Collective action where a risky joint commitment gives the largest return: hunting, technology standards or climate action.</td></tr><tr><th scope="row"><strong>Chicken</strong></th><td><strong>Symmetric anti-coordination</strong>; best response is the opposite action, giving two off-diagonal equilibria. Mutual escalation is the costly non-equilibrium outcome.</td><td>Brinkmanship and contests in which each wants the other to back down: traffic, diplomatic crises or bargaining.</td></tr><tr><th scope="row"><strong>Matching Pennies</strong></th><td><strong>Asymmetric zero-sum</strong> conflict; switching is always profitable for one player, so there is no pure-strategy equilibrium. Equilibrium requires mixing.</td><td>Adversarial prediction and evasion, such as penalty kicks, inspections or cybersecurity.</td></tr></tbody></table>

Coordination games reward compatible choices; anti-coordination games reward different choices. Symmetry means that exchanging the players leaves the strategic structure unchanged. With two equilibria, the matrix does not predict which one occurs: expectations, history, risk and communication matter.

<div class="image-panel"><img src="images/game_type_best_response_arrows.svg" alt="Best-response arrows and stable or unstable profiles for the Prisoner's Dilemma, Stag Hunt, Chicken and Matching Pennies" style="width:100%;max-height:300px;object-fit:contain"><p class="figure-caption" id="fig-w10-4"><strong>Figure 10.4.</strong> Best-response arrows for four games. Filled circles mark stable pure-strategy Nash equilibria; open circles mark unstable profiles. Red arrows change Player 1's action; blue arrows change Player 2's.</p></div>

<p class="small-note"><strong>Geometry:</strong> Figure 10.4 uses a rectangle as a layout for the four action profiles, not as a payoff plane. Equal spacing and right angles carry no payoff meaning; the arrows and their directions do. Figure 10.2 uses numerical utilities, so its parallelogram reflects those particular payoffs. Other payoff assignments can give different quadrilaterals. With strict ordinal payoffs, each player's four outcomes have distinct ranks, so ties in either payoff coordinate are excluded.</p>

<div class="game-matrix-row" style="display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:0.35rem;align-items:start;width:100%;margin:0.8rem 0 0.35rem">
<div style="min-width:0"><p style="text-align:center;margin:0 0 0.25rem"><strong>Prisoner’s Dilemma</strong></p><table class="game-payoff-table" style="width:100%;font-size:0.68em;table-layout:fixed"><colgroup><col style="width:46%"><col style="width:27%"><col style="width:27%"></colgroup><thead><tr><th> P1\\P2 </th><th>C</th><th>D</th></tr></thead><tbody><tr><th>C</th><td>(3,3)</td><td>(1,4)</td></tr><tr><th>D</th><td>(4,1)</td><td>(2,2)</td></tr></tbody></table></div>
<div style="min-width:0"><p style="text-align:center;margin:0 0 0.25rem"><strong>Stag Hunt</strong></p><table class="game-payoff-table" style="width:100%;font-size:0.68em;table-layout:fixed"><colgroup><col style="width:46%"><col style="width:27%"><col style="width:27%"></colgroup><thead><tr><th> P1\\P2 </th><th>Stag</th><th>Hare</th></tr></thead><tbody><tr><th>Stag</th><td>(4,4)</td><td>(1,3)</td></tr><tr><th>Hare</th><td>(3,1)</td><td>(2,2)</td></tr></tbody></table></div>
<div style="min-width:0"><p style="text-align:center;margin:0 0 0.25rem"><strong>Chicken</strong></p><table class="game-payoff-table" style="width:100%;font-size:0.68em;table-layout:fixed"><colgroup><col style="width:46%"><col style="width:27%"><col style="width:27%"></colgroup><thead><tr><th> P1\\P2 </th><th>Yield</th><th>Escalate</th></tr></thead><tbody><tr><th>Yield</th><td>(3,3)</td><td>(2,4)</td></tr><tr><th>Escalate</th><td>(4,2)</td><td>(1,1)</td></tr></tbody></table></div>
<div style="min-width:0"><p style="text-align:center;margin:0 0 0.25rem"><strong>Matching Pennies</strong></p><table class="game-payoff-table" style="width:100%;font-size:0.68em;table-layout:fixed"><colgroup><col style="width:46%"><col style="width:27%"><col style="width:27%"></colgroup><thead><tr><th> P1\\P2 </th><th>Heads</th><th>Tails</th></tr></thead><tbody><tr><th>Heads</th><td>(1,−1)</td><td>(−1,1)</td></tr><tr><th>Tails</th><td>(−1,1)</td><td>(1,−1)</td></tr></tbody></table></div>
</div>
<p style="font-size:0.9em;margin-top:0.2rem"><strong>Normal-form comparison.</strong> Read across a fixed row or down a fixed column to compare one player’s unilateral choices. The arrows in Figure 10.4 show the same comparisons as profitable changes.</p>

Rock–paper–scissors is the earlier three-action cyclic example, so it is not part of this $2\times2$ comparison.
'''


def main() -> None:
    notebook = json.loads(PATH.read_text())
    cells = {cell.get("id"): cell for cell in notebook["cells"]}
    cells["w10-comparing-game-types"]["source"] = COMPARISON.splitlines(keepends=True)
    for cell_id in ("w10-stag-hunt-normal-form", "w10-chicken-normal-form", "w10-matching-pennies-normal-form"):
        cell = cells[cell_id]
        tags = set(cell.setdefault("metadata", {}).get("tags", []))
        tags.add("remove-cell")
        cell["metadata"]["tags"] = sorted(tags)

    # Keep one heading for the heterogeneous-population tournament section.
    cells["w10-payoff-to-fitness"]["source"][0] = "### In a heterogeneous population: Axelrod Prisoner’s Dilemma tournament\n"
    cells["w10-repeated-play-slide"]["source"][0] = "### In a heterogeneous population: Axelrod Prisoner’s Dilemma tournament\n"
    cells["week10-pathway"]["source"] = r'''A tournament keeps the strategy rules fixed and compares their payoffs against a declared opponent field. The heatmap shows the mean payoff per round for each focal strategy against each opponent. The second panel samples one opponent uniformly before each repeated match and plots the running mean payoff over 300 tournament matches. The same opponent sequence is used for every focal strategy, so the trajectories are directly comparable.

Under this payoff matrix and opponent field, Always Defect finishes highest, followed by Tit for Tat and Random; Always Cooperate scores lowest. The individual matches are random, but the ranking settles as the tournament gets longer. This is tournament performance, not evolution: no strategy is copied, removed or introduced.

<div class="image-panel"><img src="images/axelrod_tournament_random_opponents.svg" alt="Pairwise payoff heatmap and running mean payoffs for four fixed strategies in a random-opponent Prisoner’s Dilemma tournament." style="width:100%;max-height:390px;object-fit:contain"><p class="figure-caption" id="fig-w10-7"><strong>Figure 10.7.</strong> Pairwise payoffs and random-opponent tournament trajectories. Each trajectory shows the running mean payoff per round over 300 repeated matches.</p></div>

#### Axelrod strategy comparisons

Axelrod’s tournaments compared many submitted strategies in repeated Prisoner’s Dilemma matches. Each strategy received a cumulative score across a fixed opponent field, so its ranking depended on who it played. The table gives four reference rules.

| Strategy | Rule | What it shows |
|---|---|---|
| **Always Cooperate** | Cooperate every round. | Can do well with cooperators but is exploited by defectors. |
| **Always Defect** | Defect every round. | Avoids exploitation but gives up mutual cooperation. |
| **Tit for Tat** | Cooperate first, then copy the opponent’s previous move. | Reciprocates cooperation and defection. |
| **Random** | Choose cooperate or defect independently each round. | Provides a memory-free comparison. |

Later analyses summarised the behaviour of successful strategies using four descriptors:

| Property | Behaviour in the tournament | Trade-off |
|---|---|---|
| **Nice** | Cooperate on the first move; do not exploit an unprovoked opponent. | Can be exploited by a population of persistent defectors. |
| **Retaliatory** | Respond to defection rather than allowing repeated exploitation. | Excessive punishment can destroy future cooperation. |
| **Forgiving** | Resume cooperation after the opponent returns to cooperation. | Too much forgiveness can invite repeated exploitation. |
| **Non-envious** | Seek a good score rather than needing to outscore the opponent in every match. | The ranking depends on the opponent field, horizon and noise. |

Tit for Tat illustrates the combination: cooperate first, copy the opponent’s previous move, and return to cooperation after cooperation. It can perform well in a friendly, low-noise field, but a single error can trigger echoing retaliation.

The tournament ends with this comparison: the strategies and opponent field are fixed, and we rank cumulative scores. No strategy is copied, removed or introduced.
'''.splitlines(keepends=True)
    cells["w10-tournament-scores-slide"]["source"] = r'''A tournament scores a declared set of fixed strategies against a declared opponent field. Figure 10.7 first shows pairwise mean payoffs, then the running mean payoff when each repeated match samples one opponent at random. The lines are separate focal strategies, not a changing population.

<div class="image-panel"><img src="images/axelrod_tournament_random_opponents.svg" alt="Pairwise payoff heatmap and running mean payoffs for four fixed strategies in a random-opponent Prisoner’s Dilemma tournament." style="width:100%;max-height:330px;object-fit:contain"><p class="figure-caption" id="fig-w10-7"><strong>Figure 10.7.</strong> Pairwise payoffs and random-opponent tournament trajectories.</p></div>
'''.splitlines(keepends=True)

    # Keep the Reader's tournament explanation in its dedicated updater so it
    # is not regressed when this comparison script is rerun.
    cells["w10-payoff-to-fitness"]["source"] = TOURNAMENT_INTRO.splitlines(keepends=True)
    cells["week10-pathway"]["source"] = TOURNAMENT_RESULTS.splitlines(keepends=True)

    PATH.write_text(json.dumps(notebook, indent=1, ensure_ascii=False) + "\n")

    manifest_path = ROOT / "tools/equation_consistency.json"
    manifest = json.loads(manifest_path.read_text())
    signatures = manifest["notebooks"]["notebooks/week10/L_Game_theory.ipynb"]["math_signatures"]
    signatures["w10-comparing-game-types"] = math_signature(COMPARISON)
    signatures["week10-pathway"] = math_signature(TOURNAMENT_RESULTS)
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
