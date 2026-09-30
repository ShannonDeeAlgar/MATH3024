"""Generate the Week 10 Reader figure for tournament ranking and field sensitivity."""

from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "notebooks" / "week10"))

from figure_style import CB_BLUE, CB_GREEN, CB_ORANGE, CB_PURPLE, INK, apply_course_figure_style, finish_axes
from axelrod_tournament import play_match


STRATEGIES = ("Always Cooperate", "Always Defect", "Tit for Tat", "Random")
COLOURS = (CB_BLUE, CB_ORANGE, CB_GREEN, CB_PURPLE)
SHORT = ("Always Cooperate", "Always Defect", "Tit for Tat", "Random")


def field_scores(*, fields: int = 180, opponents_per_field: int = 8, rounds: int = 50) -> np.ndarray:
    """Return mean payoff per round for each focal strategy and random field."""
    scores = np.empty((fields, len(STRATEGIES)))
    master = np.random.default_rng(3024108)
    for field in range(fields):
        opponents = master.choice(STRATEGIES, size=opponents_per_field, replace=True)
        for focal_index, focal in enumerate(STRATEGIES):
            match_scores = []
            for match_index, opponent in enumerate(opponents):
                seed = int(master.integers(0, 2**32 - 1))
                match_scores.append(play_match(focal, opponent, rounds=rounds, seed=seed)["mean_scores"][0])
            scores[field, focal_index] = np.mean(match_scores)
    return scores


def tft_payoffs(*, repetitions: int = 120, rounds: int = 50) -> np.ndarray:
    values = np.empty((repetitions, len(STRATEGIES)))
    for repetition in range(repetitions):
        for opponent_index, opponent in enumerate(STRATEGIES):
            seed = 400000 + repetition * 10 + opponent_index
            values[repetition, opponent_index] = play_match(
                "Tit for Tat", opponent, rounds=rounds, seed=seed
            )["mean_scores"][0]
    return values.mean(axis=0)


def main() -> None:
    apply_course_figure_style()
    scores = field_scores()
    pairwise = tft_payoffs()
    means = scores.mean(axis=0)
    order = np.argsort(-means, kind="stable")

    fig, (ax0, ax1) = plt.subplots(
        1,
        2,
        figsize=(12, 4.7),
        gridspec_kw={"width_ratios": (1.55, 1), "wspace": 0.42},
    )

    distributions = [scores[:, index] for index in order]
    parts = ax0.violinplot(
        distributions,
        positions=np.arange(len(order)),
        vert=False,
        showmeans=False,
        showmedians=False,
        showextrema=False,
        widths=0.72,
    )
    for body, index in zip(parts["bodies"], order):
        body.set_facecolor(COLOURS[index])
        body.set_edgecolor(COLOURS[index])
        body.set_alpha(0.32)

    jitter_rng = np.random.default_rng(3024109)
    for position, index in enumerate(order):
        jitter = jitter_rng.uniform(-0.13, 0.13, size=len(scores))
        ax0.scatter(scores[:, index], position + jitter, s=4, color=COLOURS[index], alpha=0.28, linewidths=0, zorder=2)
        q25, q75 = np.quantile(scores[:, index], [0.25, 0.75])
        ax0.plot([q25, q75], [position, position], color=INK, lw=5, solid_capstyle="butt", zorder=3)
        ax0.scatter(means[index], position, s=44, facecolor="white", edgecolor=INK, linewidth=1.5, zorder=4)
        ax0.text(5.02, position, f"rank {position + 1}", va="center", ha="left", fontsize=10, color=INK)

    ax0.set(
        yticks=np.arange(len(order)),
        yticklabels=[SHORT[index] for index in order],
        xlabel="Mean payoff per round",
        title="Randomized opponent fields",
        xlim=(0, 5.9),
    )
    ax0.invert_yaxis()
    ax0.set_title("Randomized opponent fields", pad=12)

    heat = ax1.imshow(pairwise[None, :], cmap="Blues", vmin=0, vmax=5, aspect="auto")
    ax1.set(
        xticks=np.arange(len(STRATEGIES)),
        xticklabels=["Cooperate", "Defect", "Tit for Tat", "Random"],
        yticks=[0],
        yticklabels=["Tit for Tat"],
        title="Tit for Tat against each opponent",
        xlabel="Opponent strategy",
    )
    ax1.tick_params(axis="x", labelrotation=25, labelsize=10, pad=4)
    for label in ax1.get_xticklabels():
        label.set_horizontalalignment("right")
    for index, value in enumerate(pairwise):
        ax1.text(index, 0, f"{value:.2f}", ha="center", va="center", color=INK, fontsize=12, fontweight="bold")
    fig.colorbar(heat, ax=ax1, shrink=0.78, pad=0.04, label="Mean payoff")

    for ax in (ax0, ax1):
        finish_axes(ax)
    fig.subplots_adjust(left=0.08, right=0.90, bottom=0.22, top=0.86, wspace=0.42)
    fig.savefig(ROOT / "notebooks" / "week10" / "images" / "axelrod_tournament_field_distributions.svg")
    plt.close(fig)


if __name__ == "__main__":
    main()
