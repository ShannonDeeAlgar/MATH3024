"""Generate complementary ACO analysis figures for Week 7.

The benchmark is one fixed ten-city Euclidean travelling-salesperson instance.
Its exact optimum is calculated by enumeration and used only to score runs.
Each algorithm run receives the same budget of 100 completed tours.
"""

from itertools import permutations
from pathlib import Path
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from figure_style import (  # noqa: E402
    apply_course_figure_style,
    finish_axes,
    BLUE,
    INK,
    ORANGE,
)

apply_course_figure_style()

CITY_COUNT = 10
ANTS = 10
GENERATIONS = 10
RUNS = 80
BETA = 2.0
Q = 1.0
GOOD_GAP = 0.02

rng = np.random.default_rng(14)
coordinates = rng.random((CITY_COUNT, 2))
distances = np.linalg.norm(
    coordinates[:, None, :] - coordinates[None, :, :], axis=2
)


def exact_optimum() -> float:
    best = np.inf
    for middle in permutations(range(1, CITY_COUNT)):
        tour = np.asarray((0, *middle, 0))
        best = min(best, distances[tour[:-1], tour[1:]].sum())
    return float(best)


OPTIMUM = exact_optimum()
TARGET = (1.0 + GOOD_GAP) * OPTIMUM


def run_aco(seed: int, alpha: float, rho: float, beta: float = BETA, *, record_tours=False):
    """Return best-so-far tour cost after every completed-tour evaluation."""
    random = np.random.default_rng(seed)
    pheromone = np.ones((CITY_COUNT, CITY_COUNT))
    best = np.inf
    history = []
    generation_costs = []

    for _ in range(GENERATIONS):
        tours = np.zeros((ANTS, CITY_COUNT + 1), dtype=int)
        unvisited = np.ones((ANTS, CITY_COUNT), dtype=bool)
        unvisited[:, 0] = False
        costs = np.zeros(ANTS)

        for step in range(1, CITY_COUNT):
            current = tours[:, step - 1]
            local_distance = np.maximum(distances[current], 1e-12)
            scores = pheromone[current] ** alpha * (1 / local_distance) ** beta
            scores *= unvisited
            probabilities = scores / scores.sum(axis=1, keepdims=True)
            draws = random.random(ANTS)
            selected = (draws[:, None] > np.cumsum(probabilities, axis=1)).sum(axis=1)
            tours[:, step] = selected
            unvisited[np.arange(ANTS), selected] = False
            costs += distances[current, selected]

        costs += distances[tours[:, CITY_COUNT - 1], 0]
        if record_tours:
            generation_costs.append(costs.copy())

        for cost in costs:
            best = min(best, cost)
            history.append(best)

        pheromone *= 1 - rho
        for step in range(CITY_COUNT):
            start = tours[:, step]
            end = tours[:, step + 1]
            deposit = Q / costs
            np.add.at(pheromone, (start, end), deposit)
            np.add.at(pheromone, (end, start), deposit)

    if record_tours:
        return np.asarray(history), np.asarray(generation_costs)
    return np.asarray(history)


def progress_figure() -> None:
    history, costs = run_aco(0, alpha=1.0, rho=0.5, record_tours=True)
    assert costs.shape == (GENERATIONS, ANTS)
    np.testing.assert_array_equal(history, np.minimum.accumulate(costs.ravel()))
    np.testing.assert_array_equal(history, run_aco(0, alpha=1.0, rho=0.5))
    lower, median, upper = np.percentile(costs, [25, 50, 75], axis=1)
    generation = np.arange(1, GENERATIONS + 1)
    fig, ax = plt.subplots(figsize=(10.8, 5.4), constrained_layout=True)
    ax.fill_between(generation, lower, upper, color=BLUE, alpha=0.18, label="Middle 50% of tours in each generation")
    ax.plot(generation, median, color=BLUE, marker="o", label="Median tour length in each generation")
    ax.step(generation, history.reshape(GENERATIONS, ANTS)[:, -1], where="post", color=INK, lw=2.6, label="Best tour length found so far")
    ax.axhline(OPTIMUM, color=ORANGE, ls="-", label=f"Known optimum ({OPTIMUM:.4f})")
    ax.axhline(TARGET, color=ORANGE, ls="--", label=f"2% success threshold ({TARGET:.4f})")
    ax.set(xlabel="Generation (10 evaluated tours per generation)", ylabel="Tour length", xticks=generation, xlim=(1, GENERATIONS), title="One run: how tour quality changes")
    ax.legend(frameon=False, fontsize=10, loc="upper right")
    finish_axes(ax)
    fig.savefig(ROOT / "notebooks/week07/images/aco_tsp_progress.svg", facecolor="white", bbox_inches="tight")
    plt.close(fig)
    print(f"Progress run seed 0: final best={history[-1]:.6f}; target={TARGET:.6f}")


def benchmark_figure() -> None:
    """Show the exact coordinates and an independently enumerated reference tour."""
    best_tour = min(
        ((0, *middle, 0) for middle in permutations(range(1, CITY_COUNT))),
        key=lambda tour: sum(distances[a, b] for a, b in zip(tour[:-1], tour[1:])),
    )
    assert np.isclose(sum(distances[a, b] for a, b in zip(best_tour[:-1], best_tour[1:])), OPTIMUM)
    fig, axes = plt.subplots(1, 2, figsize=(10.8, 4.8))
    fig.subplots_adjust(left=0.07, right=0.98, bottom=0.14, top=0.86, wspace=0.27)
    for ax in axes:
        ax.scatter(*coordinates.T, s=85, color=INK, zorder=3)
        for i, (x, y) in enumerate(coordinates):
            ax.annotate(str(i + 1), (x, y), xytext=(7, 7), textcoords="offset points", color=INK, fontsize=12)
        ax.set(xlim=(0, 1), ylim=(0, 1), xlabel="Horizontal coordinate", ylabel="Vertical coordinate", aspect="equal")
        finish_axes(ax)
    axes[0].set_title("Ten fixed city locations")
    tour_coordinates = coordinates[list(best_tour)]
    axes[1].plot(*tour_coordinates.T, color=ORANGE, lw=2.3, zorder=2)
    axes[1].set_title(f"Shortest tour: cost {OPTIMUM:.4f}")
    fig.savefig(ROOT / "notebooks/week07/images/aco_tsp_benchmark.svg", facecolor="white", bbox_inches="tight")
    plt.close(fig)


def discovery_figure() -> None:
    shared = np.asarray([run_aco(seed, alpha=1.0, rho=0.5) for seed in range(RUNS)])
    independent = np.asarray([run_aco(seed, alpha=0.0, rho=0.5) for seed in range(RUNS)])
    evaluations = np.arange(1, ANTS * GENERATIONS + 1)

    fig, ax = plt.subplots(figsize=(10.8, 5.9))
    fig.subplots_adjust(left=0.11, right=0.97, top=0.80, bottom=0.22)
    for values, colour, label in [
        (shared, ORANGE, r"stigmergic ants ($\alpha=1$, $\beta=2$, $\rho=0.5$, $Q=1$)"),
        (independent, BLUE, r"independent ants ($\alpha=0$, $\beta=2$)"),
    ]:
        success = (values <= TARGET).mean(axis=0)
        ax.plot(evaluations, success, color=colour, lw=2.8, label=label)

    ax.set(
        xlabel=r"Completed tours evaluated, $E$",
        ylabel=r"Success fraction, $F$",
        xlim=(1, ANTS * GENERATIONS),
        ylim=(-0.02, 1.02),
    )
    finish_axes(ax)
    ax.legend(frameon=False, loc="upper left")
    fig.suptitle("A separate problem: does stigmergy improve discovery?", y=0.97)
    fig.text(
        0.5,
        0.88,
        "Unlike the S–T shortest-path explorable, this benchmark asks for a complete tour of 10 cities.",
        ha="center",
        color=INK,
        fontsize=11.5,
    )
    fig.text(
        0.5,
        0.035,
        f"Travelling-salesperson benchmark (not the explorable network): {RUNS} seeded runs; 10 ants × 10 generations; "
        r"$\beta=2$. The known shortest tour is used only to assess performance.",
        ha="center",
        color=INK,
        fontsize=10.5,
    )
    fig.savefig(
        ROOT / "notebooks/week07/images/aco_discovery_efficiency.png",
        dpi=190,
        facecolor="white",
    )
    plt.close(fig)


def sweep_figure() -> None:
    alphas = np.asarray([0.0, 0.25, 0.5, 1.0, 1.5, 2.0, 3.0])
    betas = np.asarray([0.0, 0.5, 1.0, 2.0, 3.0, 5.0])
    rhos = np.asarray([0.05, 0.15, 0.3, 0.5, 0.7, 0.9])
    success_alpha_beta = np.empty((len(betas), len(alphas)))
    success_alpha_rho = np.empty((len(rhos), len(alphas)))

    fixed_rho = 0.5
    for row, beta in enumerate(betas):
        for column, alpha in enumerate(alphas):
            final_costs = np.asarray([
                run_aco(
                    seed,
                    alpha=float(alpha),
                    beta=float(beta),
                    rho=fixed_rho,
                )[-1]
                for seed in range(RUNS)
            ])
            success_alpha_beta[row, column] = np.mean(final_costs <= TARGET)

    fixed_beta = 2.0
    for row, rho in enumerate(rhos):
        for column, alpha in enumerate(alphas):
            final_costs = np.asarray(
                [
                    run_aco(
                        seed,
                        alpha=float(alpha),
                        beta=fixed_beta,
                        rho=float(rho),
                    )[-1]
                    for seed in range(RUNS)
                ]
            )
            success_alpha_rho[row, column] = np.mean(final_costs <= TARGET)

    fig, axes = plt.subplots(1, 2, figsize=(14.2, 5.8))
    fig.subplots_adjust(left=0.08, right=0.91, top=0.82, bottom=0.22, wspace=0.28)

    panels = [
        (
            axes[0], success_alpha_beta, betas,
            r"Heuristic weight, $\beta$",
            rf"A  Shared versus local information ($\rho={fixed_rho:g}$)",
        ),
        (
            axes[1], success_alpha_rho, rhos,
            r"Evaporation fraction, $\rho$",
            rf"B  Influence versus persistence ($\beta={fixed_beta:g}$)",
        ),
    ]
    for ax, success, y_values, y_label, title in panels:
        image = ax.imshow(
            success, origin="lower", aspect="auto", vmin=0, vmax=1, cmap="YlGnBu"
        )
        ax.set(
            xlabel=r"Pheromone weight, $\alpha$",
            ylabel=y_label,
            xticks=np.arange(len(alphas)),
            yticks=np.arange(len(y_values)),
            xticklabels=[f"{value:g}" for value in alphas],
            yticklabels=[f"{value:g}" for value in y_values],
            title=title,
        )
        for row in range(len(y_values)):
            for column in range(len(alphas)):
                colour = "white" if success[row, column] >= 0.58 else INK
                ax.text(
                    column, row, f"{success[row, column]:.0%}",
                    ha="center", va="center", color=colour, fontsize=9.5,
                )
    colourbar = fig.colorbar(image, ax=axes, fraction=0.035, pad=0.025)
    colourbar.set_label(r"Success fraction, $F$")
    fig.suptitle("Useful sharing requires a balance", y=0.95)
    fig.text(
        0.5,
        0.045,
        f"The same travelling-salesperson benchmark (not the explorable network): {RUNS} seeded runs per setting; "
        r"100 completed tours per run. At $\alpha=0$, pheromone has no influence. Read broad regions, not one best cell.",
        ha="center",
        color=INK,
        fontsize=10.5,
    )
    fig.savefig(
        ROOT / "notebooks/week07/images/aco_parameter_sweep.png",
        dpi=190,
        facecolor="white",
    )
    plt.close(fig)


if __name__ == "__main__":
    if "--progress-only" in sys.argv:
        progress_figure()
    elif "--benchmark-only" in sys.argv:
        benchmark_figure()
    else:
        benchmark_figure()
        progress_figure()
        discovery_figure()
        sweep_figure()
    print(ROOT / "notebooks/week07/images/aco_tsp_benchmark.svg")
