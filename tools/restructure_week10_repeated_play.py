"""Clarify the Week 10 repeated-play and strategy-update hierarchy."""

from __future__ import annotations

import json
import copy
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "notebooks/week10/L_Game_theory.ipynb"


def replace_heading(source: str, old: str, new: str) -> str:
    if old not in source:
        raise ValueError(f"missing heading {old!r}")
    return source.replace(old, new, 1)


def main() -> None:
    notebook = json.loads(PATH.read_text())
    cells = notebook["cells"]
    by_id = {cell.get("id"): cell for cell in cells}

    bridge = by_id["w10-evolution-bridge"]
    bridge["source"] = [
        "## Repeated play and evolving strategy\n",
        "\n",
        "A repeated game and an evolutionary population are different extensions of a pairwise game. In repeated play, a strategy can respond to earlier actions but its rule stays fixed during the tournament. In an evolutionary model, payoff-dependent copying or reproduction changes the strategy frequencies, so later encounters come from a different population.\n",
        "\n",
        "We first compare fixed strategies in an Axelrod-style tournament. We then look at two population models in which types can change: copying by successful neighbours in a static population, and conversion after a loss in a moving population. Finally, we let tournament strategies enter an evolutionary population model.\n",
    ]
    slide_bridge = by_id["w10-evolution-bridge-slide"]
    slide_bridge["source"] = [
        "## Repeated play and evolving strategy\n",
        "\n",
        "A repeated game can use history while the strategy rule stays fixed. Evolutionary game dynamics changes strategy frequencies through payoff-dependent copying or reproduction.\n",
        "\n",
        "We compare fixed strategies first, then examine strategy updating in static and moving populations, and finally let tournament strategies change in a population model.\n",
    ]

    fixed = by_id["w10-payoff-to-fitness"]
    fixed["source"] = [
        "### In a heterogeneous population: Axelrod tournament\n",
        "\n",
        "In a **repeated game**, the same players meet over several rounds. A strategy can use earlier actions to choose the next one. The relevant payoff is usually the sum of round payoffs across the match (or a discounted sum when later rounds count less), not one round in isolation.\n",
        "\n",
        "An Axelrod-style tournament compares a heterogeneous set of fixed strategy rules. Each strategy receives a cumulative score across a declared opponent field and repeated matches, so its ranking depends on who it plays. A strategy may give up an immediate gain for a later one, but its rule does not change during the tournament.\n",
        "\n",
        "Always Cooperate and Always Defect choose the same action every round, while Tit for Tat cooperates first and then copies its opponent's previous action.\n",
    ]
    fixed_slide = by_id["w10-repeated-play-slide"]
    fixed_slide["source"] = [
        "### In a heterogeneous population: Axelrod tournament\n",
        "\n",
        "A repeated match lets a strategy respond to earlier actions. The strategy rule remains fixed while the tournament compares cumulative scores across a declared opponent field.\n",
        "\n",
        "- Always Cooperate and Always Defect choose the same action every round.\n",
        "- Tit for Tat cooperates first, then copies its opponent's previous action.\n",
        "\n",
        "A defection can bring an immediate gain and trigger retaliation in later rounds.\n",
    ]

    pathway = by_id["week10-pathway"]
    pathway["source"] = [
        """### Tournament comparison

A single repeated match has two players and therefore two score lines. Figure 10.7 first shows Tit for Tat against Always Defect. The second panel holds Tit for Tat fixed and changes the opponent; each line is its cumulative score against one opponent, averaged over 30 matches. The comparison includes Always Cooperate, Always Defect and a Random action rule. The three lines are separate two-player comparisons, not a three-player game.

A tournament combines results across a declared opponent field. The cumulative score and the opponent field both matter, so a strategy can rank differently when the field changes. Cumulative scores may look roughly linear once the per-round payoff settles; the slopes differ because the opponents differ. Only after this fixed-field comparison do we ask how strategy frequencies might change in a population.

<div class="image-panel"><img src="images/axelrod_tournament_scores.svg" alt="Left: cumulative scores for Tit for Tat and Always Defect in one repeated Prisoner’s Dilemma match. Right: Tit for Tat’s mean cumulative score against Always Cooperate, Always Defect and Random." style="width:100%;max-height:360px;object-fit:contain"><p class="figure-caption" id="fig-w10-7"><strong>Figure 10.7.</strong> One repeated match and one focal strategy against several opponents. The right panel averages 30 independent matches for each opponent.</p></div>

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
"""
    ]
    pathway_text = "".join(pathway["source"])
    evolution_marker = "### Evolution in action: tracking strategy frequencies"
    evolution_cell = by_id.get("w10-evolution-action")
    if evolution_cell is None and evolution_marker in pathway_text:
        fixed_text, evolution_text = pathway_text.split(evolution_marker, 1)
        pathway["source"] = [fixed_text.rstrip() + "\n"]
        evolution_cell = copy.deepcopy(pathway)
        evolution_cell["id"] = "w10-evolution-action"
        evolution_cell["metadata"] = {"tags": ["reader-only"]}
        evolution_cell["source"] = [evolution_marker + evolution_text]

    static_reader = by_id["a7e5e594"]
    static_reader["source"][0] = "### In a static population: Prisoner's Kaleidoscope\n"
    static_slide = by_id["w10-prisoners-kaleidoscope-slide"]
    static_slide["source"][0] = "### In a static population: Prisoner's Kaleidoscope\n"

    moving = by_id["w10-rps-population"]
    moving["source"][0] = "### In a moving population: rock–paper–scissors\n"
    arena = by_id["w10-rps-arena"]
    arena["source"] = [
        "<div class=\"two-panel wide-left compact-panels\">\n",
        "<div class=\"image-panel\"><iframe src=\"https://konloch.com/demos/rock-paper-scissors\" title=\"Rock paper scissors moving-agent simulation\" style=\"width:100%;height:430px;border:0\"></iframe></div>\n",
        "<div class=\"text-panel\"><p><a href=\"https://konloch.com/demos/rock-paper-scissors\" target=\"_blank\">Open the simulation in a new tab</a>.</p></div>\n",
        "</div>\n",
    ]

    explorable_banner = by_id["w10-explorable-banner"]
    explorable_banner["source"] = ["### Explorable\n"]

    evolving = by_id["w10-evolutionary-ipd"]
    evolving["source"] = [
        """### Letting tournament strategies change

After the fixed-strategy comparison, let payoff-dependent copying or reproduction change the shares of those strategies. The population then supplies a changing opponent field.

Evolution changes strategy frequencies, so the opponents encountered also change. **Fitness** means expected reproductive or copying success. We specify how payoff affects fitness and how the population updates.

| Process | Model decision |
|---|---|
| **Selection** | how payoff changes the expected number of descendants or copies |
| **Inheritance** | how strategies pass to descendants |
| **Mutation** | whether copied strategies can change, and how often |
"""
    ]
    evolving_slide = by_id["w10-tournament-evolution-slide"]
    evolving_slide["source"][0] = "### Letting tournament strategies change\n"

    tournament_slide = by_id["w10-tournament-scores-slide"]
    tournament_slide["source"][0] = "### Tournament comparison\n"

    spatial = by_id["w10-spatial-evolution"]
    spatial["source"] = [
        re.sub(r"^#+ Evolution of strategy frequencies", "#### Evolution of strategy frequencies", line)
        for line in spatial["source"]
    ]

    evolution_slide = by_id["w10-axelrod-slide"]
    evolution_slide["source"] = [
        line.replace(
            "What would you expect the frequencies to do in rock–paper–scissors: converge, or cycle?",
            "What would happen if a tournament strategy could be copied into the next generation? Which strategies might rise or fall, and why?",
        )
        for line in evolution_slide["source"]
    ]

    # Keep the biological RPS example with the original familiar game.
    lizard = by_id["w10-lizard-morphs"]
    lizard_slide = by_id["w10-real-games-slide"]

    ids_before = [cell.get("id") for cell in cells]
    ids_to_move = {
        "w10-lizard-morphs", "w10-real-games-slide",
        "w10-evolution-bridge", "w10-evolution-bridge-slide",
        "w10-payoff-to-fitness", "w10-repeated-play-slide", "week10-pathway",
        "w10-evolution-action",
        "w10-tournament-scores-slide", "w10-axelrod-slide",
        "a7e5e594", "w10-prisoners-kaleidoscope-slide", "w10-rps-population",
        "w10-rps-arena", "w10-rps-population-behaviour", "w10-evolution-not-optimisation",
        "w10-explorable-banner", "w10-population-terms-slide",
        "w10-evolutionary-ipd", "w10-tournament-evolution-slide",
        "w10-payoff-fitness-link-slide", "w10-selection-inheritance-mutation-slide",
        "w10-spatial-evolution", "w10-spatial-evolution-notation-slide",
    }
    moved = [by_id[cell_id] for cell_id in ids_before if cell_id in ids_to_move]
    remaining = [cell for cell in cells if cell.get("id") not in ids_to_move]

    def insert_after(target_id: str, new_cells: list[dict]) -> None:
        index = next(i for i, cell in enumerate(remaining) if cell.get("id") == target_id) + 1
        remaining[index:index] = new_cells

    # Familiar RPS -> biological RPS, before the general game-theory setup.
    insert_after("w10-rps-local-game-slide", [lizard, lizard_slide])

    ordered = [
        by_id["w10-evolution-bridge"], by_id["w10-evolution-bridge-slide"],
        by_id["w10-payoff-to-fitness"], by_id["w10-repeated-play-slide"],
        by_id["week10-pathway"], by_id["w10-tournament-scores-slide"],
        by_id["a7e5e594"], by_id["w10-prisoners-kaleidoscope-slide"],
        by_id["w10-rps-population"], by_id["w10-rps-arena"],
        by_id["w10-rps-population-behaviour"], by_id["w10-evolution-not-optimisation"],
        by_id["w10-explorable-banner"], by_id["w10-population-terms-slide"],
        by_id["w10-evolutionary-ipd"], by_id["w10-tournament-evolution-slide"],
        by_id["w10-payoff-fitness-link-slide"], by_id["w10-selection-inheritance-mutation-slide"],
        by_id["w10-axelrod-slide"], by_id["w10-spatial-evolution"],
        by_id["w10-spatial-evolution-notation-slide"],
    ]
    if evolution_cell is not None:
        evolution_cell["source"] = [
            re.sub(
                r"^#+ Evolution in action: tracking strategy frequencies",
                "#### Evolution in action: tracking strategy frequencies",
                line,
            ).replace(
                "Before looking at rock–paper–scissors, what would you expect its strategy frequencies to do? Would one strategy take over, or would the shares cycle?",
                "What would happen if a tournament strategy could be copied into the next generation? Which strategies might rise or fall, and why?",
            )
            for line in evolution_cell["source"]
        ]
        ordered.insert(15, evolution_cell)
    # Use the bridge's existing location as the anchor for the reordered run.
    anchor = next(i for i, cell in enumerate(remaining) if cell.get("id") == "w10-comparing-game-types")
    remaining[anchor + 1:anchor + 1] = ordered
    notebook["cells"] = remaining
    PATH.write_text(json.dumps(notebook, indent=1, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
