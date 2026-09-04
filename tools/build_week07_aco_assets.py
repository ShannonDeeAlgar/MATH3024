"""Build the Week 7 ACO animation used by the Reader."""

from pathlib import Path

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation, PillowWriter

from figure_style import (
    BLUE,
    GRID as PALE,
    INK,
    ORANGE,
    YELLOW as GOLD,
    apply_course_figure_style,
    style_animation_frame,
)


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "notebooks/week07/images/aco_network_learning.gif"

NODES = ["S", "A", "B", "C", "D", "T"]
POS = {
    "S": (0.0, 0.5), "A": (1.2, 1.3), "B": (1.2, -0.3),
    "C": (2.6, 1.3), "D": (2.6, -0.3), "T": (3.8, 0.5),
}
EDGES = {
    ("S", "A"): 2.0, ("A", "C"): 2.0, ("C", "T"): 2.0,
    ("S", "B"): 2.6, ("B", "D"): 2.8, ("D", "T"): 2.6,
    ("A", "D"): 3.1, ("B", "C"): 3.1,
}
ROUTES = [
    (["S", "A", "C", "T"], 6.0),
    (["S", "B", "D", "T"], 8.0),
    (["S", "A", "D", "T"], 7.7),
    (["S", "B", "C", "T"], 7.7),
]


def route_edges(route):
    return [tuple(sorted(e)) for e in zip(route[:-1], route[1:])]


def simulate(seed=7, generations=32, ants=24):
    rng = np.random.default_rng(seed)
    pheromone = {tuple(sorted(e)): 1.0 for e in EDGES}
    records = []
    for generation in range(generations):
        desirability = []
        for route, length in ROUTES:
            trail = np.prod([pheromone[e] for e in route_edges(route)])
            desirability.append(trail ** 1.0 * (1 / length) ** 3.0)
        probabilities = np.asarray(desirability) / np.sum(desirability)
        choices = rng.choice(len(ROUTES), size=ants, p=probabilities)
        counts = np.bincount(choices, minlength=len(ROUTES))
        records.append((generation, pheromone.copy(), probabilities.copy(), counts.copy()))
        pheromone = {e: 0.78 * value for e, value in pheromone.items()}
        for choice in choices:
            route, length = ROUTES[choice]
            for e in route_edges(route):
                pheromone[e] += 2.2 / length
    return records


def main():
    apply_course_figure_style()
    records = simulate()

    fig = plt.figure(figsize=(10.2, 5.5), facecolor="white")
    grid = fig.add_gridspec(2, 2, width_ratios=(1.55, 1), height_ratios=(1, 1),
                           wspace=0.24, hspace=0.38)
    ax_graph = fig.add_subplot(grid[:, 0])
    ax_routes = fig.add_subplot(grid[0, 1])
    ax_history = fig.add_subplot(grid[1, 1])
    history = []

    def draw(frame):
        generation, pheromone, probabilities, counts = records[frame]
        history.append(probabilities[0])
        ax_graph.clear(); ax_routes.clear(); ax_history.clear()

        graph_edges = list(EDGES)
        edge_keys = [tuple(sorted(e)) for e in graph_edges]
        values = np.array([pheromone[e] for e in edge_keys])
        scaled = (values - values.min()) / max(np.ptp(values), 1e-9)
        widths = 1.2 + 8.0 * scaled
        colours = [ORANGE if e in route_edges(ROUTES[0][0]) else PALE for e in edge_keys]
        alphas = [0.45 + 0.55 * s for s in scaled]
        for (a, b), width, colour, alpha in zip(graph_edges, widths, colours, alphas):
            xa, ya = POS[a]; xb, yb = POS[b]
            ax_graph.plot([xa, xb], [ya, yb], lw=width, color=colour,
                          alpha=alpha, solid_capstyle="round", zorder=1)
            ax_graph.text((xa + xb) / 2, (ya + yb) / 2 + 0.08,
                          f"{EDGES[(a, b)]:g}", ha="center", va="center",
                          fontsize=9, color=INK,
                          bbox={"facecolor": "white", "edgecolor": "none", "pad": 0.5},
                          zorder=3)
        for node in NODES:
            x, y = POS[node]
            ax_graph.scatter(x, y, s=900, facecolor="white", edgecolor=INK,
                             linewidth=2, zorder=4)
            ax_graph.text(x, y, node, ha="center", va="center", color=INK,
                          fontweight="bold", fontsize=12, zorder=5)
        ax_graph.set_title("Pheromone accumulates on useful edges", color=INK, pad=10)
        ax_graph.text(0.02, 0.03, "edge width = pheromone   ·   labels = fixed cost",
                      transform=ax_graph.transAxes, color=INK, fontsize=10)
        ax_graph.set_xlim(-0.35, 4.15); ax_graph.set_ylim(-0.75, 1.75); ax_graph.axis("off")

        labels_short = ["S–A–C–T", "S–B–D–T", "S–A–D–T", "S–B–C–T"]
        bars = ax_routes.barh(np.arange(4), counts, color=[ORANGE, BLUE, GOLD, "#7A6FAC"])
        ax_routes.set_yticks(np.arange(4), labels_short)
        ax_routes.invert_yaxis(); ax_routes.set_xlabel("ants choosing route")
        ax_routes.set_title(f"Generation {generation + 1}: current choices", color=INK)
        ax_routes.set_xlim(0, max(24, counts.max() + 2))
        ax_routes.spines[["top", "right"]].set_visible(False)
        ax_routes.grid(axis="x", color=PALE, lw=0.8)
        for bar, n in zip(bars, counts):
            ax_routes.text(bar.get_width() + 0.35, bar.get_y() + bar.get_height()/2,
                           str(n), va="center", fontsize=9, color=INK)

        ax_history.plot(np.arange(1, len(history) + 1), history, color=ORANGE, lw=2.6)
        ax_history.set(xlabel="generation", ylabel="probability of\nshortest route", ylim=(0, 1.03))
        ax_history.set_xlim(1, len(records)); ax_history.set_title("The solution emerges", color=INK)
        ax_history.spines[["top", "right"]].set_visible(False)
        ax_history.grid(color=PALE, lw=0.8)
        fig.suptitle("Ant colony optimisation on a weighted graph", color=INK,
                     fontsize=18, fontweight="bold", y=0.99)
        style_animation_frame(fig, (ax_routes, ax_history))
        matplotlib.rcParams["savefig.bbox"] = "standard"

    animation = FuncAnimation(fig, draw, frames=len(records), interval=280, repeat=True)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with matplotlib.rc_context({"savefig.bbox": "standard"}):
        animation.save(OUT, writer=PillowWriter(fps=4), dpi=105)
    plt.close(fig)
    print(OUT)


if __name__ == "__main__":
    main()
