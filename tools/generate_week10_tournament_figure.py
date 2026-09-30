"""Generate the Week 10 fixed-strategy tournament figure.

The figure uses the same simultaneous-match engine as the tested Axelrod-style
model.  A tournament match is one repeated 50-round Prisoner's Dilemma match;
the running x-axis counts completed tournament matches, not individual rounds.
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

from axelrod_tournament import play_match
from figure_style import CB_BLUE, CB_GREEN, CB_ORANGE, CB_PURPLE, apply_course_figure_style


STRATEGIES = ("Always Cooperate", "Always Defect", "Tit for Tat", "Random")
ROUNDS = 50
PAIRWISE_REPETITIONS = 30
TOURNAMENT_MATCHES = 300
SEED = 3024
COLOURS = {
    "Always Cooperate": CB_BLUE,
    "Always Defect": CB_ORANGE,
    "Tit for Tat": CB_GREEN,
    "Random": CB_PURPLE,
}


def pairwise_payoffs(*, rounds: int = ROUNDS, repetitions: int = PAIRWISE_REPETITIONS) -> np.ndarray:
    """Mean focal payoff per round for each focal/opponent pair."""
    values = np.zeros((len(STRATEGIES), len(STRATEGIES)))
    for i, focal in enumerate(STRATEGIES):
        for j, opponent in enumerate(STRATEGIES):
            matches = [
                play_match(
                    focal,
                    opponent,
                    rounds=rounds,
                    seed=SEED + 10000 * i + 100 * j + repetition,
                )["mean_scores"][0]
                for repetition in range(repetitions)
            ]
            values[i, j] = np.mean(matches)
    return values


def random_opponent_tournament(*, matches: int = TOURNAMENT_MATCHES, rounds: int = ROUNDS):
    """Return running focal means using one shared random opponent sequence."""
    rng = np.random.default_rng(SEED)
    opponent_indices = rng.integers(0, len(STRATEGIES), size=matches)
    match_seeds = rng.integers(0, 2**32 - 1, size=matches, dtype=np.uint32)
    results = {}
    for focal_index, focal in enumerate(STRATEGIES):
        scores = []
        for opponent_index, match_seed in zip(opponent_indices, match_seeds):
            opponent = STRATEGIES[int(opponent_index)]
            match = play_match(
                focal,
                opponent,
                rounds=rounds,
                seed=int(match_seed) + 100000 * focal_index,
            )
            scores.append(match["mean_scores"][0])
        scores = np.asarray(scores)
        results[focal] = np.cumsum(scores) / np.arange(1, matches + 1)
    return results


def main() -> None:
    apply_course_figure_style()
    payoff_matrix = pairwise_payoffs()
    trajectories = random_opponent_tournament()

    fig, axes = plt.subplots(
        1,
        2,
        figsize=(13, 4.8),
        gridspec_kw={"width_ratios": [1, 1.25], "wspace": 0.36},
    )
    heat = axes[0].imshow(payoff_matrix, cmap="viridis", vmin=0, vmax=5)
    axes[0].set(
        title="Pairwise payoff per round",
        xlabel="Opponent strategy",
        ylabel="Focal strategy",
        xticks=np.arange(len(STRATEGIES)),
        xticklabels=STRATEGIES,
        yticks=np.arange(len(STRATEGIES)),
        yticklabels=STRATEGIES,
    )
    axes[0].tick_params(axis="x", rotation=35, labelsize=11)
    axes[0].tick_params(axis="y", labelsize=11)
    for i in range(len(STRATEGIES)):
        for j in range(len(STRATEGIES)):
            colour = "white" if payoff_matrix[i, j] < 2.7 else "#1B2A4C"
            axes[0].text(j, i, f"{payoff_matrix[i, j]:.2f}", ha="center", va="center", color=colour)
    fig.colorbar(heat, ax=axes[0], label="Mean payoff per round", fraction=0.046, pad=0.04)

    for name, trajectory in trajectories.items():
        axes[1].plot(
            np.arange(1, len(trajectory) + 1),
            trajectory,
            label=name,
            linewidth=2,
            color=COLOURS[name],
        )
    axes[1].set(
        title="Random-opponent tournament",
        xlabel="Completed tournament matches (m)",
        ylabel="Running mean payoff per round",
    )
    axes[1].legend(loc="upper right", frameon=False)
    for ax in axes:
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
    fig.subplots_adjust(left=0.08, right=0.98, bottom=0.25, top=0.86, wspace=0.36)
    output = ROOT / "notebooks" / "week10" / "images" / "axelrod_tournament_random_opponents.svg"
    fig.savefig(output)
    plt.close(fig)


if __name__ == "__main__":
    main()
