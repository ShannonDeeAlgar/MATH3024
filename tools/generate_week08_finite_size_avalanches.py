"""Compare Abelian-sandpile avalanche tails across finite lattice sizes."""

from pathlib import Path
import sys
from collections import deque
from concurrent.futures import ProcessPoolExecutor

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from figure_style import apply_course_figure_style, finish_axes, BLUE, INK, ORANGE  # noqa: E402

apply_course_figure_style()


def add_and_relax_size(pile, rng):
    """Add one grain and return the order-independent toppling count."""
    L = pile.shape[0]
    i, j = (int(x) for x in rng.integers(0, L, size=2))
    pile[i, j] += 1
    queue = deque([(i, j)]) if pile[i, j] == 4 else deque()
    size = 0
    while queue:
        i, j = queue.popleft()
        while pile[i, j] >= 4:
            pile[i, j] -= 4
            size += 1
            for di, dj in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                u, v = i + di, j + dj
                if 0 <= u < L and 0 <= v < L:
                    pile[u, v] += 1
                    if pile[u, v] == 4:
                        queue.append((u, v))
    return size


def sample_sizes(L, recorded, burn, seed):
    rng = np.random.default_rng(seed)
    pile = np.zeros((L, L), dtype=np.int64)
    values = []
    mean_load = []
    for step in range(burn + recorded):
        size = add_and_relax_size(pile, rng)
        if step >= burn and size > 0:
            values.append(size)
        if step >= burn:
            mean_load.append(pile.mean())
    return np.asarray(values), np.asarray(mean_load)


def sample_run(args):
    return sample_sizes(*args)


def main():
    # Starting from empty requires a burn-in that grows with lattice area.
    # Twenty independent runs expose run-to-run variation. Only five thin
    # curves per size are drawn to keep the figure legible; bold curves pool
    # all runs after each run has been checked for residual load drift.
    lattice_sizes = [24, 40, 64]
    recorded = 3_000
    runs = 20
    colours = [BLUE, ORANGE, INK]
    single_run_floors = []

    fig, ax = plt.subplots(figsize=(8.7, 5.5), constrained_layout=True)
    for L, colour in zip(lattice_sizes, colours):
        burn = 8 * L**2
        samples = []
        jobs = [
            (L, recorded, burn, 8000 + 100 * L + run)
            for run in range(runs)
        ]
        with ProcessPoolExecutor(max_workers=8) as pool:
            results = list(pool.map(sample_run, jobs))
        for run, (sizes, mean_load) in enumerate(results):
            # Compare the two halves of the measurement window. This is a
            # diagnostic, not a proof of stationarity.
            half = mean_load.size // 2
            drift = abs(mean_load[:half].mean() - mean_load[half:].mean())
            if drift > 0.035:
                raise RuntimeError(
                    f"Residual mean-load drift for L={L}, run={run}: {drift:.3f}"
                )
            sizes = np.sort(sizes)
            samples.append(sizes)
            ccdf = (sizes.size - np.arange(sizes.size)) / sizes.size
            single_run_floors.append(1 / sizes.size)
            ax.loglog(sizes, ccdf, color=colour, lw=0.55, alpha=0.09)
        pooled = np.sort(np.concatenate(samples))
        pooled_ccdf = (pooled.size - np.arange(pooled.size)) / pooled.size
        ax.loglog(
            pooled,
            pooled_ccdf,
            color=colour,
            lw=2.2,
            label=f"$L={L}$ ({runs} runs; {pooled.size:,} events)",
        )

    typical_floor = float(np.median(single_run_floors))
    ax.axhline(
        typical_floor, color="#7A8496", lw=1.0, ls=":", alpha=0.9,
    )
    ax.text(
        1.15, typical_floor * 1.18,
        "one event in a typical run",
        color="#5B6780", fontsize=9, ha="left", va="bottom",
    )

    ax.set(
        xlabel="Avalanche size, $S$ (topplings)",
        ylabel=r"Fraction with $S\geq s$ (CCDF)",
    )
    finish_axes(ax)
    ax.legend(frameon=False)

    out = ROOT / "notebooks/week08/images/sandpile_finite_size_ccdf.png"
    fig.savefig(out, dpi=210, facecolor="white", bbox_inches="tight")
    plt.close(fig)
    print(out)


if __name__ == "__main__":
    main()
