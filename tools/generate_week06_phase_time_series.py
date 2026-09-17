#!/usr/bin/env python3
"""Generate the qualitative wrapped-phase time-series figure for Week 6."""

from __future__ import annotations

from pathlib import Path
import sys

import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from figure_style import apply_course_figure_style  # noqa: E402


NAVY = "#1B2A4C"
BLUE = "#3B8BC2"
GRID = "#D7E0EF"


def main() -> None:
    apply_course_figure_style()
    rng = np.random.default_rng(3024)
    n = 12
    dt = 0.02
    steps = 900
    coupling = 1.9
    omega = rng.normal(3.0, 0.42, n)
    theta = rng.uniform(0, 2 * np.pi, n)
    history = np.empty((steps + 1, n))
    history[0] = theta
    for k in range(steps):
        z = np.mean(np.exp(1j * theta))
        interaction = np.imag(z * np.exp(-1j * theta))
        theta = np.mod(theta + dt * (omega + coupling * interaction), 2 * np.pi)
        history[k + 1] = theta

    time = np.arange(steps + 1) * dt
    fig, ax = plt.subplots(figsize=(8.2, 3.3))
    colours = plt.cm.Blues(np.linspace(0.38, 0.88, n))
    for j in range(n):
        ax.plot(time, history[:, j], color=colours[j], lw=1.05, alpha=0.82)
    ax.set(
        xlabel="Simulation time",
        ylabel="Wrapped phase",
        yticks=[0, np.pi, 2 * np.pi],
        yticklabels=["0", r"$\pi$", r"$2\pi$"],
        ylim=(-0.12, 2 * np.pi + 0.12),
    )
    ax.grid(color=GRID, linewidth=0.8, alpha=0.8)
    ax.spines[["top", "right"]].set_visible(False)
    for spine in ("bottom", "left"):
        ax.spines[spine].set_color(NAVY)
    fig.tight_layout()
    out = ROOT / "notebooks/week06/images/kuramoto_phase_time_series.svg"
    fig.savefig(out, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    main()
