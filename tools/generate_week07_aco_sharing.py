from pathlib import Path
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from figure_style import apply_course_figure_style, finish_axes, BLUE, INK, ORANGE  # noqa: E402

apply_course_figure_style()

EDGES = [
    ("S", "A", 1.5), ("S", "B", 1.3),
    ("A", "C", 1.4), ("A", "D", 2.0), ("B", "C", 1.8), ("B", "D", 1.2),
    ("C", "E", 4.0), ("C", "F", 2.0), ("D", "E", 1.5), ("D", "F", 2.2),
    ("E", "T", 1.4), ("F", "T", 2.4),
]
OUT = {}
for index, edge in enumerate(EDGES):
    OUT.setdefault(edge[0], []).append(index)
BEST = (1, 5, 8, 10)


def enumerate_routes(node="S", route=()):
    if node == "T":
        return [route]
    routes = []
    for edge_index in OUT[node]:
        routes.extend(enumerate_routes(EDGES[edge_index][1], route + (edge_index,)))
    return routes


ROUTES = enumerate_routes()
ROUTE_COSTS = np.array([
    sum(EDGES[edge_index][2] for edge_index in route)
    for route in ROUTES
])
BEST_INDEX = ROUTES.index(BEST)


def experiment(seed, shared, generations=24, ants=30, record_routes=False):
    rng = np.random.default_rng(seed)
    tau = np.ones(len(EDGES))
    fractions = []
    route_use = []
    route_pheromone = []
    found = False
    for _ in range(generations):
        desirability = np.array([
            (tau[e] ** 1.25 if shared else 1.0) * (1 / EDGES[e][2]) ** 2
            for e in range(len(EDGES))
        ])
        route_probabilities = []
        for route in ROUTES:
            probability = 1.0
            for edge_index in route:
                node = EDGES[edge_index][0]
                choices = OUT[node]
                probability *= desirability[edge_index] / desirability[choices].sum()
            route_probabilities.append(probability)
        counts = rng.multinomial(ants, np.asarray(route_probabilities))
        fractions.append(counts[BEST_INDEX] / ants)
        route_use.append(counts / ants)
        found = found or counts[BEST_INDEX] > 0
        if shared:
            tau *= 0.72
            for route, cost, count in zip(ROUTES, ROUTE_COSTS, counts):
                for edge_index in route:
                    tau[edge_index] += count / cost
        route_pheromone.append([
            np.mean(tau[list(route)]) for route in ROUTES
        ])
    result = (np.asarray(fractions), found)
    if record_routes:
        return result + (np.asarray(route_use), np.asarray(route_pheromone))
    return result


runs = 120
shared_results = [experiment(seed, True) for seed in range(runs)]
independent_results = [experiment(seed, False) for seed in range(runs)]
shared = np.array([result[0] for result in shared_results])
independent = np.array([result[0] for result in independent_results])
shared_found = np.mean([result[1] for result in shared_results])
independent_found = np.mean([result[1] for result in independent_results])

generation = np.arange(1, shared.shape[1] + 1)
_, _, route_use, route_pheromone = experiment(11, True, record_routes=True)
route_order = np.argsort(ROUTE_COSTS)
route_use = route_use[:, route_order].T
route_pheromone = route_pheromone[:, route_order].T
route_pheromone /= route_pheromone.max(axis=0, keepdims=True)

route_names = []
for route_index in route_order:
    route = ROUTES[route_index]
    nodes = [EDGES[route[0]][0]] + [EDGES[edge_index][1] for edge_index in route]
    marker = "★ " if route_index == BEST_INDEX else ""
    route_names.append(f"{marker}{'–'.join(nodes)} ({ROUTE_COSTS[route_index]:.1f})")

fig = plt.figure(figsize=(16.2, 6.6))
outer = fig.add_gridspec(
    1, 2, width_ratios=(1.18, 1), left=0.065, right=0.97,
    top=0.79, bottom=0.22, wspace=0.28,
)
ax = fig.add_subplot(outer[0])
right = outer[1].subgridspec(2, 1, hspace=0.18)
ax_use = fig.add_subplot(right[0])
ax_tau = fig.add_subplot(right[1], sharex=ax_use)
for values, colour, label in [
    (shared, ORANGE, r"stigmergic ants ($\alpha=1.25$, $\beta=2$, $\rho=0.28$, $Q=1$)"),
    (independent, BLUE, "independent ants; no pheromone memory"),
]:
    mean = values.mean(axis=0)
    lo, hi = np.quantile(values, [0.1, 0.9], axis=0)
    ax.plot(generation, mean, color=colour, lw=2.5, label=label)
    ax.fill_between(generation, lo, hi, color=colour, alpha=0.13)

ax.set(
    xlabel=r"Generation, $k$",
    ylabel=r"Shortest-route fraction, $f_{\rm short}(k)$",
    ylim=(-0.02, 1.02),
)
finish_axes(ax)
ax.set_title("A  Ensemble route allocation", loc="left", fontsize=14, pad=11)
fig.suptitle("Shared pheromone concentrates later route construction", y=0.96)
if shared_found == 1 and independent_found == 1:
    success_summary = (
        "The shortest route was found at least once in every run, with or without "
        "pheromone sharing."
    )
else:
    success_summary = (
        "Runs finding the shortest route at least once within 24 generations: "
        f"shared pheromone {shared_found:.0%}; no pheromone memory {independent_found:.0%}."
    )
fig.text(
    0.5, 0.875,
    success_summary,
    ha="center", color=INK, fontsize=11,
)
ax.legend(
    frameon=False,
    loc="upper center",
    bbox_to_anchor=(0.5, -0.22),
    ncol=2,
)

use_image = ax_use.imshow(
    route_use, aspect="auto", interpolation="nearest", origin="upper",
    extent=(0.5, 24.5, len(ROUTES) - 0.5, -0.5),
    cmap="YlOrRd", vmin=0, vmax=1,
)
tau_image = ax_tau.imshow(
    route_pheromone, aspect="auto", interpolation="nearest", origin="upper",
    extent=(0.5, 24.5, len(ROUTES) - 0.5, -0.5),
    cmap="Blues", vmin=0, vmax=1,
)
ax_use.set_title("B  One shared-pheromone run", loc="left", fontsize=14, pad=11)
ax_use.set_ylabel("Route (cost)")
ax_tau.set_ylabel("Route (cost)")
ax_tau.set_xlabel(r"Generation, $k$")
ax_use.set_yticks(np.arange(len(route_names)), labels=route_names, fontsize=8.5)
ax_tau.set_yticks(np.arange(len(route_names)), labels=route_names, fontsize=8.5)
ax_use.tick_params(axis="x", labelbottom=False)
ax_tau.set_xticks([1, 5, 10, 15, 20, 24])
ax_use.text(
    0.01, 0.98, "Fraction of ants using each route", transform=ax_use.transAxes,
    ha="left", va="top", fontsize=10, color=INK,
    bbox={"facecolor": "white", "edgecolor": "none", "alpha": 0.82, "pad": 2},
)
ax_tau.text(
    0.01, 0.98, "Relative pheromone strength", transform=ax_tau.transAxes,
    ha="left", va="top", fontsize=10, color=INK,
    bbox={"facecolor": "white", "edgecolor": "none", "alpha": 0.82, "pad": 2},
)
for heat_ax in (ax_use, ax_tau):
    heat_ax.spines[["top", "right"]].set_visible(False)
    heat_ax.grid(False)
fig.colorbar(use_image, ax=ax_use, fraction=0.035, pad=0.025, label="Route fraction")
fig.colorbar(tau_image, ax=ax_tau, fraction=0.035, pad=0.025, label="Relative strength")
fig.text(
    0.5, 0.025,
    "A: mean and 10th–90th percentile across 120 seeded runs.  "
    "B: one seeded run; route strength is mean edge pheromone, normalised within each generation.  "
    "30 ants per generation.",
    ha="center", color=INK, fontsize=10.5,
)
out = ROOT / "notebooks/week07/images/aco_sharing_comparison.png"
fig.savefig(out, dpi=190, facecolor="white", bbox_inches="tight")
plt.close(fig)
print(out)
