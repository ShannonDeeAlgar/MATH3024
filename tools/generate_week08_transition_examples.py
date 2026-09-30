#!/usr/bin/env python3
"""Generate the schematic continuous and discontinuous transition comparison."""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from figure_style import BLUE, INK, ORANGE, SECONDARY, apply_course_figure_style, finish_axes


OUT = (
    Path(__file__).resolve().parents[1]
    / "notebooks"
    / "week08"
    / "images"
    / "phase_transition_examples.svg"
)


def main() -> None:
    apply_course_figure_style()
    fig, axes = plt.subplots(1, 2, figsize=(10.8, 4.2), constrained_layout=True)

    temperature = np.linspace(0.55, 1.25, 500)
    magnetisation = np.zeros_like(temperature)
    below = temperature < 1
    magnetisation[below] = (1 - temperature[below]) ** 0.33

    ax = axes[0]
    ax.plot(temperature, magnetisation, color=BLUE, linewidth=3)
    ax.axvline(1, color=SECONDARY, linestyle="--", linewidth=1.8)
    ax.text(1.015, 0.68, "$T_c$", color=SECONDARY)
    ax.text(0.62, 0.58, "ordered", color=INK)
    ax.text(1.08, 0.10, "disordered", color=INK)
    ax.set(
        title="Continuous · ferromagnet",
        xlabel="Temperature, $T$",
        ylabel="Magnetisation, $m$",
        xlim=(0.55, 1.25),
        ylim=(-0.02, 0.82),
    )
    ax.set_xticks([])
    ax.set_yticks([])
    finish_axes(ax)

    low = np.linspace(0.55, 1, 260, endpoint=False)
    high = np.linspace(1, 1.25, 180)
    liquid_density = 0.91 - 0.07 * (low - 0.55)
    vapour_density = 0.12 - 0.025 * (high - 1)

    ax = axes[1]
    ax.plot(low, liquid_density, color=BLUE, linewidth=3)
    ax.plot(high, vapour_density, color=ORANGE, linewidth=3)
    ax.plot([1, 1], [vapour_density[0], liquid_density[-1]], color=SECONDARY,
            linestyle="--", linewidth=1.8)
    ax.scatter([1], [liquid_density[-1]], s=55, facecolor="white", edgecolor=BLUE,
               linewidth=2, zorder=3)
    ax.scatter([1], [vapour_density[0]], s=55, facecolor="white", edgecolor=ORANGE,
               linewidth=2, zorder=3)
    ax.text(1.015, 0.68, "$T_b$", color=SECONDARY)
    ax.text(0.67, 0.82, "liquid", color=BLUE)
    ax.text(1.08, 0.17, "vapour", color=ORANGE)
    ax.set(
        title="Discontinuous · boiling",
        xlabel="Temperature, $T$",
        ylabel="Density, $\\rho$",
        xlim=(0.55, 1.25),
        ylim=(-0.02, 1.02),
    )
    ax.set_xticks([])
    ax.set_yticks([])
    finish_axes(ax)

    fig.savefig(OUT, transparent=False)
    fig.savefig(OUT.with_suffix(".png"), dpi=180, transparent=False)
    plt.close(fig)


if __name__ == "__main__":
    main()
