"""Generate the Week 10 figure for payoff-dependent strategy frequencies.

The plotted trajectories come from ``evolve_population`` in the small
Axelrod-style engine.  This is deliberately a four-strategy teaching model,
not a reconstruction of the full historical Axelrod library.
"""

from __future__ import annotations

import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "notebooks" / "week10"))

from axelrod_tournament import evolve_population
from figure_style import CB_BLUE, CB_GREEN, CB_ORANGE, CB_PURPLE, apply_course_figure_style, finish_axes


PLAYERS = ("Always Cooperate", "Always Defect", "Tit for Tat", "Random")
LABELS = {
    "Always Cooperate": "Always Cooperate",
    "Always Defect": "Always Defect",
    "Tit for Tat": "Tit for Tat",
    "Random": "Random",
}
COLOURS = (CB_BLUE, CB_ORANGE, CB_GREEN, CB_PURPLE)


def main() -> None:
    apply_course_figure_style()
    result = evolve_population(
        players=PLAYERS,
        initial_shares=np.full(len(PLAYERS), 1 / len(PLAYERS)),
        generations=60,
        population_size=2000,
        selection_strength=0.08,
        mutation=0.0,
        rounds=50,
        repetitions=80,
        noise=0.0,
        seed=3024,
    )

    generations = np.arange(result["shares"].shape[0])
    shares = result["shares"]
    fig, ax = plt.subplots(figsize=(10.5, 5.4))
    ax.stackplot(
        generations,
        shares.T,
        labels=[LABELS[player] for player in PLAYERS],
        colors=COLOURS,
        alpha=0.88,
        edgecolor="white",
        linewidth=0.55,
    )
    ax.set(
        xlim=(0, generations[-1]),
        ylim=(0, 1),
        xlabel="Generation",
        ylabel="Share of population",
        title="Payoff-dependent evolution of four fixed strategies",
        yticks=(0, 0.25, 0.5, 0.75, 1),
        yticklabels=("0", "0.25", "0.50", "0.75", "1"),
    )
    ax.legend(
        loc="upper center",
        bbox_to_anchor=(0.5, -0.14),
        ncol=4,
        frameon=False,
        handlelength=1.7,
        columnspacing=1.25,
    )
    finish_axes(ax)
    fig.subplots_adjust(left=0.09, right=0.98, bottom=0.25, top=0.85)
    output = ROOT / "notebooks" / "week10" / "images" / "axelrod_evolution_dynamics.svg"
    fig.savefig(output)
    plt.close(fig)


if __name__ == "__main__":
    main()
