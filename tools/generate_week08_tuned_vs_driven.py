#!/usr/bin/env python3
"""Generate the Week 8 fixed-energy versus driven-sandpile comparison."""

from pathlib import Path
from collections import deque

import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "notebooks/week08/images/sandpile_tuned_vs_driven.svg"


def driven_sandpile(L=16, additions=4000, seed=3024):
    rng = np.random.default_rng(seed)
    heights = np.zeros((L, L), dtype=np.int32)
    density = np.empty(additions)
    loss = np.zeros(additions, dtype=bool)

    for step in range(additions):
        i, j = rng.integers(0, L, size=2)
        heights[i, j] += 1
        before = int(heights.sum())

        queue = deque([(int(i), int(j))]) if heights[i, j] >= 4 else deque()
        while queue:
            x, y = queue.popleft()
            if heights[x, y] < 4:
                continue
            heights[x, y] -= 4
            for nx, ny in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)):
                if 0 <= nx < L and 0 <= ny < L:
                    heights[nx, ny] += 1
                    if heights[nx, ny] == 4:
                        queue.append((nx, ny))
            if heights[x, y] >= 4:
                queue.append((x, y))

        loss[step] = int(heights.sum()) < before
        density[step] = heights.mean()

    return density, loss


def main():
    plt.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "font.size": 11,
            "axes.titlesize": 14,
            "axes.labelsize": 12,
            "axes.edgecolor": "#172b52",
            "axes.labelcolor": "#172b52",
            "xtick.color": "#172b52",
            "ytick.color": "#172b52",
            "text.color": "#172b52",
        }
    )

    navy, orange, blue = "#172b52", "#df6238", "#347caf"
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12.4, 4.2))

    # Conceptual order-parameter curve for the related fixed-energy construction.
    z = np.linspace(0, 1, 400)
    zc = 0.56
    activity = 0.72 * np.maximum((z - zc) / (1 - zc), 0) ** 0.55
    ax1.plot(z, activity, color=orange, lw=3)
    ax1.axvline(zc, color=navy, ls="--", lw=1.6)
    ax1.text(zc, -0.075, r"$\zeta_c$", ha="center", va="top", fontsize=12)
    ax1.text(0.25, 0.09, "absorbing\nactivity stops", ha="center")
    ax1.text(0.79, 0.46, "active\ntoppling persists", ha="center")
    ax1.set(xlim=(0, 1), ylim=(-0.01, 0.78), xlabel=r"fixed mean grain density, $\zeta$", ylabel=r"long-run active-site fraction, $\rho_a$")
    ax1.set_xticks([])
    ax1.set_yticks([0])
    ax1.set_title("A  Tuned: fixed-energy sandpile", loc="left")

    density, loss = driven_sandpile()
    steps = np.arange(1, density.size + 1)
    ax2.plot(steps, density, color=blue, lw=1.25)
    steady = density[2200:]
    lo, hi = np.quantile(steady, [0.02, 0.98])
    ax2.axhspan(lo, hi, color=orange, alpha=0.14, label="stationary range")
    ax2.axvline(2200, color=navy, ls=":", lw=1.4)
    ax2.text(900, 1.02, "slow loading", color=blue, ha="center")
    drop_step = np.flatnonzero(loss & (steps > 2500))[12]
    ax2.annotate(
        "boundary loss\nduring an avalanche",
        xy=(steps[drop_step], density[drop_step]),
        xytext=(3150, 1.48),
        arrowprops={"arrowstyle": "->", "color": orange, "lw": 1.5},
        color=orange,
        ha="center",
    )
    ax2.text(3100, hi + 0.035, "fluctuating stationary regime", color=orange, ha="center")
    ax2.set(xlim=(1, density.size), ylim=(0, max(2.35, density.max() + 0.08)), xlabel="completed grain additions", ylabel="mean grains per site")
    ax2.set_title("B  Self-organised: slow drive and boundary loss", loc="left")

    for ax in (ax1, ax2):
        ax.spines[["top", "right"]].set_visible(False)
        ax.grid(alpha=0.22, color="#9babc5")

    fig.suptitle("Two ways to reach the sandpile transition", fontsize=17, fontweight="bold", color=navy)
    fig.tight_layout(rect=(0, 0, 1, 0.94), w_pad=3.0)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    main()
