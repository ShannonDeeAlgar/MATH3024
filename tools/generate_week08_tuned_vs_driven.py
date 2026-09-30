#!/usr/bin/env python3
"""Generate separate Week 8 fixed-energy and driven-sandpile figures."""

from pathlib import Path
from collections import deque

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from figure_style import apply_course_figure_style


ROOT = Path(__file__).resolve().parents[1]
OUT_TUNED = ROOT / "notebooks/week08/images/sandpile_fixed_energy.svg"
OUT_DRIVEN = ROOT / "notebooks/week08/images/sandpile_driven_stationarity.svg"
OUT_PREPARATION = ROOT / "notebooks/week08/images/sandpile_overfull_preparation.svg"


def relax_open(heights, record=False):
    """Topple each unstable site once per parallel step; optionally record it."""
    heights = np.asarray(heights, dtype=np.int32).copy()
    density = [float(heights.mean())]
    active = [int(np.count_nonzero(heights >= 4))]
    loss = []
    while np.any(heights >= 4):
        before = int(heights.sum())
        topplings = (heights >= 4).astype(np.int32)
        heights -= 4 * topplings
        heights[1:, :] += topplings[:-1, :]
        heights[:-1, :] += topplings[1:, :]
        heights[:, 1:] += topplings[:, :-1]
        heights[:, :-1] += topplings[:, 1:]
        loss.append(before - int(heights.sum()))
        density.append(float(heights.mean()))
        active.append(int(np.count_nonzero(heights >= 4)))
    if record:
        return heights, np.asarray(density), np.asarray(active), np.asarray(loss)
    return heights


def preparation_figure(density, active, loss):
    """Display relaxation before the first driven trial, using its own clock."""
    purple, orange = "#76538C", "#df6238"
    k = np.arange(density.size)
    fig, axes = plt.subplots(
        3, 1, figsize=(8.4, 6.4), sharex=True,
        gridspec_kw={"height_ratios": [2, 1.25, 1.25], "hspace": 0.18},
    )
    axes[0].plot(k, density, color=purple, lw=2)
    axes[0].set_ylabel("mean load per site", fontsize=13)
    axes[0].annotate(
        "no grain additions", xy=(0.04, 0.15), xycoords="axes fraction",
        fontsize=13, color="#172b52",
    )
    axes[1].plot(k, active, color=purple, lw=1.7)
    axes[1].plot(k[-1], 0, "o", color=purple, ms=6)
    axes[1].annotate(
        f"stable after {k[-1]} steps: no active sites",
        xy=(k[-1], 0), xytext=(0.25, 0.7), textcoords="axes fraction",
        fontsize=12, color=purple,
        arrowprops={"arrowstyle": "->", "color": purple},
    )
    axes[1].set_ylabel("active sites", fontsize=13)
    axes[2].plot(k[1:], loss, color=orange, lw=1.7)
    axes[2].set_ylabel("grains lost\nper step", fontsize=13)
    axes[2].set_xlabel("Preparatory parallel steps, $k$", fontsize=14)
    axes[2].set_xlim(0, k[-1] + 3)
    for ax in axes:
        ax.spines[["top", "right"]].set_visible(False)
        ax.grid(axis="y", alpha=0.22, color="#9babc5")
        ax.tick_params(labelsize=12)
    fig.subplots_adjust(left=0.16, right=0.98, top=0.97, bottom=0.10)
    fig.savefig(OUT_PREPARATION, bbox_inches="tight")
    fig.savefig(OUT_PREPARATION.with_suffix(".png"), dpi=160, bbox_inches="tight")
    plt.close(fig)


def driven_sandpile(L=16, additions=4000, seed=3024, initial=None):
    rng = np.random.default_rng(seed)
    heights = (np.zeros((L, L), dtype=np.int32)
               if initial is None else np.asarray(initial, dtype=np.int32).copy())
    density = np.empty(additions)
    grains_lost = np.zeros(additions, dtype=np.int32)

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

        grains_lost[step] = before - int(heights.sum())
        density[step] = heights.mean()

    return density, grains_lost


def rolling_mean(values, width=200):
    kernel = np.ones(width) / width
    return np.convolve(values, kernel, mode="valid")


def main():
    apply_course_figure_style()

    navy, orange, blue = "#172b52", "#df6238", "#347caf"

    # Conceptual order-parameter curve for the related fixed-energy construction.
    fig, ax = plt.subplots(figsize=(6.3, 4.2))
    z = np.linspace(0, 1, 400)
    zc = 0.56
    activity = 0.72 * np.maximum((z - zc) / (1 - zc), 0) ** 0.55
    ax.axvspan(0, zc, color=blue, alpha=0.07, zorder=0)
    ax.axvspan(zc, 1, color=orange, alpha=0.055, zorder=0)
    ax.plot(z, activity, color=orange, lw=3)
    ax.axvline(zc, color=navy, ls="--", lw=1.6)
    ax.text(zc, -0.025, r"$\zeta_c$", transform=ax.get_xaxis_transform(),
            ha="center", va="top", fontsize=13)
    ax.text(0.25, 0.09, "absorbing phase\nactivity eventually stops", ha="center")
    ax.text(0.82, 0.24, "active phase\ntoppling persists", ha="center")
    ax.set(
        xlim=(0, 1),
        ylim=(-0.01, 0.78),
        xlabel=r"fixed mean grain density, $\zeta$",
        ylabel=r"long-run active-site fraction, $\rho_a$",
    )
    ax.set_xticks([])
    ax.xaxis.labelpad = 22
    ax.set_yticks([0])
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(alpha=0.22, color="#9babc5")
    fig.tight_layout()
    OUT_TUNED.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT_TUNED, bbox_inches="tight")
    fig.savefig(OUT_TUNED.with_suffix(".png"), dpi=160, bbox_inches="tight")
    plt.close(fig)

    density_empty, loss_empty = driven_sandpile(seed=3024)
    initial_rng = np.random.default_rng(8031)
    prepared, prep_density, prep_active, prep_loss = relax_open(
        initial_rng.integers(0, 8, size=(16, 16)), record=True,
    )
    assert prep_active[-1] == 0
    assert np.isclose(
        (prep_density[0] - prep_density[-1]) * prepared.size, prep_loss.sum(),
    )
    preparation_figure(prep_density, prep_active, prep_loss)
    density_prepared, loss_prepared = driven_sandpile(
        seed=8032, initial=prepared
    )
    steps = np.arange(1, density_empty.size + 1)
    analysis_start = 2200
    fig, (ax_density, ax_loss) = plt.subplots(
        2,
        1,
        figsize=(8.4, 5.4),
        sharex=True,
        gridspec_kw={"height_ratios": [3.0, 1.15], "hspace": 0.16},
    )

    purple = "#76538C"
    ax_density.plot(
        steps, density_empty, color=blue, lw=1.15,
        label="start empty",
    )
    ax_density.plot(
        steps, density_prepared, color=purple, lw=1.05, alpha=0.9,
        label="prepared high-load state; then drive",
    )
    steady = np.concatenate(
        [density_empty[analysis_start:], density_prepared[analysis_start:]]
    )
    lo, hi = np.quantile(steady, [0.02, 0.98])
    ax_density.axhspan(
        lo, hi, color=orange, alpha=0.12,
        label="late-run 2–98% load range",
    )
    ax_density.annotate(
        "empty-start loading transient",
        xy=(520, density_empty[519]), xytext=(760, 1.35),
        color=blue, ha="center", fontsize=11,
        arrowprops={"arrowstyle": "->", "color": blue, "lw": 1.0},
    )
    ax_density.set(
        xlim=(1, density_empty.size),
        ylim=(0, max(2.55, density_empty.max() + 0.3,
                     density_prepared.max() + 0.3)),
        ylabel="mean load per site",
    )
    ax_density.set_ylabel("mean load per site", fontsize=12, labelpad=5)
    ax_density.legend(frameon=False, fontsize=11, loc="lower right")

    width = 200
    rolling_steps = np.arange(width, steps.size + 1)
    ax_loss.plot(
        rolling_steps, rolling_mean(loss_empty, width),
        color=blue, lw=1.2,
    )
    ax_loss.plot(
        rolling_steps, rolling_mean(loss_prepared, width),
        color=purple, lw=1.2,
    )
    ax_loss.axhline(1, color=orange, ls="--", lw=1.25,
                    label="one-grain input")
    ax_loss.set(
        ylim=(0, 1.75),
        xlabel="Completed trials, $n$",
        ylabel="mean boundary loss\n(200-trial window)",
    )
    ax_loss.set_ylabel(
        "mean boundary loss\n(200-trial window)", fontsize=11, labelpad=5,
    )
    ax_loss.legend(frameon=False, fontsize=10, loc="upper right")

    for panel in (ax_density, ax_loss):
        panel.spines[["top", "right"]].set_visible(False)
        panel.grid(axis="y", alpha=0.22, color="#9babc5")

    fig.subplots_adjust(left=0.12, right=0.98, top=0.91, bottom=0.12)
    fig.savefig(OUT_DRIVEN, bbox_inches="tight")
    fig.savefig(OUT_DRIVEN.with_suffix(".png"), dpi=160, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    main()
