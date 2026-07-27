#!/usr/bin/env python3
"""Generate the paired Mandelbrot scale-symmetry image used in Week 2."""

from pathlib import Path

import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt


OUTPUT = Path(__file__).resolve().parents[1] / "notebooks/week02/images/mandelbrot_scale_symmetry.png"


def render(ax, centre_x, centre_y, width, iterations=400, pixels=600):
    height = 0.72 * width
    x = np.linspace(centre_x - width / 2, centre_x + width / 2, pixels)
    y = np.linspace(centre_y - height / 2, centre_y + height / 2, int(0.72 * pixels))
    c = x[None, :] + 1j * y[:, None]
    z = np.zeros_like(c)
    active = np.ones(c.shape, dtype=bool)
    escape_time = np.full(c.shape, iterations, dtype=float)
    for step in range(iterations):
        z[active] = z[active] ** 2 + c[active]
        escaped = active & (np.abs(z) > 2)
        escape_time[escaped] = step
        active[escaped] = False
    ax.imshow(
        escape_time,
        extent=[x[0], x[-1], y[0], y[-1]],
        origin="lower",
        cmap="gray_r",
        interpolation="bilinear",
    )
    ax.axis("off")


figure, axes = plt.subplots(1, 2, figsize=(12, 4.7))
render(axes[0], -0.5, 0.0, 3.2, iterations=350)
render(axes[1], -1.75838878220982, -0.0184883097807565, 0.00000048, iterations=1600)
axes[0].set_title("The familiar set", color="#1B2A4C", fontsize=15, fontweight="bold")
axes[1].set_title(
    "A miniature copy after deep magnification",
    color="#1B2A4C",
    fontsize=15,
    fontweight="bold",
)
figure.tight_layout(pad=0.5)
figure.savefig(OUTPUT, dpi=180, bbox_inches="tight", facecolor="white")
plt.close(figure)
print(f"Wrote {OUTPUT}")
