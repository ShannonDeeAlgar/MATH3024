"""Clarify the Axelrod tournament and its standard summary measures in the Reader."""

from pathlib import Path
import json
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from tools.check_equation_consistency import math_signature


NOTEBOOK = Path("notebooks/week10/L_Game_theory.ipynb")


TOURNAMENT_INTRO = r'''### In a heterogeneous population: Axelrod Prisoner’s Dilemma tournament

In a **repeated game**, the same two players meet for several rounds. A strategy can use earlier actions to choose the next one. The score for a match is the sum of its round payoffs (or their discounted sum if later rounds count less).

An Axelrod-style tournament keeps the strategy rules fixed and compares them over many opponents. For each pair of strategies:

1. play repeated matches;
2. add the round payoffs within each match;
3. average over repeated matches;
4. average across the declared opponent field and rank the strategies.

This is tournament performance, not evolution: no strategy is copied, removed or introduced. The ranking depends on the strategies entered, the match length, the payoff matrix, errors and how opponents are weighted. If match lengths differ, report mean payoff per round rather than cumulative score.
'''


TOURNAMENT_RESULTS = r'''A small example makes the summaries concrete. Use four fixed strategies: Always Cooperate, Always Defect, Tit for Tat and Random. One round is one Prisoner’s Dilemma encounter; 50 rounds make one repeated match. For each focal strategy, sample an opponent before each of 300 matches and plot the running mean payoff. The payoffs are the Prisoner’s Dilemma values $(T,R,P,S)=(5,3,1,0)$.

In the heatmap, each cell is the focal strategy’s **mean payoff per round** against the named opponent, averaged over the repeated matches. Rows are focal strategies; columns are opponents. The second panel samples an opponent before each match and plots the running mean payoff as the tournament proceeds. The same opponent sequence is used for every focal strategy, so the trajectories can be compared directly.

The overall tournament result is a ranking by mean payoff across the opponent field. A violin plot, boxplot or jittered points can show the spread across opponents or repetitions; a single average can hide that a strategy is excellent against some opponents and poor against others. The Axelrod-Python documentation reports these standard summaries: ranked mean utilities, pairwise payoffs, wins and payoff differences. It also gives a larger set of strategies to explore: <a href="https://axelrod-tournament.readthedocs.io/en/stable/standard/all_strategies.html" target="_blank" rel="noopener">All Strategies</a>.

<div class="image-panel"><img src="images/axelrod_tournament_random_opponents.svg" alt="Pairwise payoff heatmap and running mean payoffs for four fixed strategies in a random-opponent Prisoner’s Dilemma tournament." style="width:100%;max-height:390px;object-fit:contain"><p class="figure-caption" id="fig-w10-7"><strong>Figure 10.7.</strong> Pairwise mean payoffs and random-opponent trajectories. Each match lasts 50 rounds; each trajectory contains 300 matches.</p></div>

Use the Tit for Tat row as a guide. It does well when cooperation is available and responds to defection, but its score changes with the opponent field and with errors. In this example Always Defect finishes highest, followed by Tit for Tat and Random; Always Cooperate scores lowest. That is a result for this field and these settings, not a universal ranking.

#### Axelrod strategy comparisons

The table gives four reference rules.

| Strategy | Rule | What it shows |
|---|---|---|
| **Always Cooperate** | Cooperate every round. | Can do well with cooperators but is exploited by defectors. |
| **Always Defect** | Defect every round. | Avoids exploitation but gives up mutual cooperation. |
| **Tit for Tat** | Cooperate first, then copy the opponent’s previous move. | Reciprocates cooperation and defection. |
| **Random** | Choose cooperate or defect independently each round. | Provides a memory-free comparison. |

Later analyses highlighted four properties often found in strong tournament strategies:

| Property | Behaviour in the tournament | Trade-off |
|---|---|---|
| **Nice** | Cooperate on the first move; do not exploit an unprovoked opponent. | Can be exploited by persistent defectors. |
| **Retaliatory** | Respond to defection rather than allowing repeated exploitation. | Excessive punishment can destroy future cooperation. |
| **Forgiving** | Resume cooperation after the opponent returns to cooperation. | Too much forgiveness can invite repeated exploitation. |
| **Non-envious** | Seek a good score rather than needing to outscore the opponent in every match. | The ranking depends on the opponent field, horizon and noise. |

Tit for Tat has the four properties in their simplest form: it starts cooperatively, answers defection, returns to cooperation when the opponent does, and does not try to beat a cooperative opponent. Its tournament score still depends on the opponents, match length and noise.
'''


def main() -> None:
    notebook = json.loads(NOTEBOOK.read_text())
    by_id = {cell.get("id"): cell for cell in notebook["cells"]}
    for cell_id, source in (
        ("w10-payoff-to-fitness", TOURNAMENT_INTRO),
        ("week10-pathway", TOURNAMENT_RESULTS),
    ):
        if cell_id not in by_id:
            raise SystemExit(f"Could not find cell {cell_id}")
        by_id[cell_id]["source"] = source.splitlines(keepends=True)

    NOTEBOOK.write_text(json.dumps(notebook, indent=1, ensure_ascii=False) + "\n")

    manifest_path = NOTEBOOK.parents[2] / "tools/equation_consistency.json"
    manifest = json.loads(manifest_path.read_text())
    signatures = manifest["notebooks"][str(NOTEBOOK.relative_to(NOTEBOOK.parents[2]))]["math_signatures"]
    signatures["week10-pathway"] = math_signature(TOURNAMENT_RESULTS)
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
