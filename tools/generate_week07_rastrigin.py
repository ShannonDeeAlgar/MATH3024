#!/usr/bin/env python3
"""Generate the Week 7 Rastrigin objective-landscape figure."""

from pathlib import Path
import sys

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from figure_style import apply_course_figure_style, style_figure  # noqa: E402


def main():
    apply_course_figure_style()
    x = np.linspace(-5.12, 5.12, 500)
    X, Y = np.meshgrid(x, x)
    Z = 20 + X**2 + Y**2 - 10 * (np.cos(2 * np.pi * X) + np.cos(2 * np.pi * Y))

    fig, ax = plt.subplots(figsize=(8.8, 5.2))
    levels = np.linspace(0, 70, 29)
    contour = ax.contourf(X, Y, np.minimum(Z, levels[-1]), levels=levels, cmap="Blues")
    ax.contour(X, Y, Z, levels=np.arange(5, 66, 10), colors="#5479A3", linewidths=0.45, alpha=0.55)
    ax.scatter([0], [0], marker="*", s=180, color="#E3A51A", edgecolor="#172A52", linewidth=0.8, zorder=5)
    ax.annotate("global minimum", (0, 0), xytext=(0.55, 0.65), color="#172A52", fontsize=11,
                arrowprops={"arrowstyle": "->", "color": "#172A52", "lw": 1.2})
    ax.set(xlabel=r"candidate coordinate, $x_1$", ylabel=r"candidate coordinate, $x_2$",
           xlim=(-5.12, 5.12), ylim=(-5.12, 5.12), aspect="equal")
    colourbar = fig.colorbar(contour, ax=ax, pad=0.025, shrink=0.92)
    colourbar.set_label("objective value")
    style_figure(fig)
    fig.tight_layout()
    output = ROOT / "notebooks/week07/images/rastrigin_landscape.png"
    fig.savefig(output, dpi=190, bbox_inches="tight", facecolor="white")
    plt.close(fig)


if __name__ == "__main__":
    main()
