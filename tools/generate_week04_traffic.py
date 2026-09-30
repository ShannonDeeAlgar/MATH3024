#!/usr/bin/env python3
"""Generate the Week 4 Nagel--Schreckenberg teaching figures."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from matplotlib.patches import Patch
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "notebooks/week04/images"
NAVY = "#1b2d52"
BLUE = "#5f82b5"
YELLOW = "#f3cf4f"


def initialise_road(length: int, density: float, rng: np.random.Generator):
    number = int(round(length * density))
    positions = np.sort(rng.choice(length, number, replace=False))
    velocities = np.zeros(number, dtype=int)
    return positions, velocities


def update(positions, velocities, length, vmax, braking_probability, rng):
    """One synchronous Nagel--Schreckenberg update on a periodic single lane."""
    velocities = np.minimum(velocities + 1, vmax)
    gaps = (np.roll(positions, -1) - positions - 1) % length
    velocities = np.minimum(velocities, gaps)
    random_brake = (velocities > 0) & (rng.random(len(velocities)) < braking_probability)
    velocities = velocities - random_brake
    positions = (positions + velocities) % length
    order = np.argsort(positions)
    return positions[order], velocities[order]


def simulate(length, density, steps, *, vmax=5, p=0.25, seed=0, burn_in=0):
    rng = np.random.default_rng(seed)
    positions, velocities = initialise_road(length, density, rng)
    for _ in range(burn_in):
        positions, velocities = update(positions, velocities, length, vmax, p, rng)
    states = np.zeros((steps, length), dtype=np.uint8)
    flows = np.empty(steps)
    for t in range(steps):
        positions, velocities = update(positions, velocities, length, vmax, p, rng)
        states[t, positions] = np.where(velocities == 0, 2, 1)
        flows[t] = velocities.sum() / length
    return states, flows


def make_modern_figure():
    OUT.mkdir(parents=True, exist_ok=True)
    states, _ = simulate(120, 0.28, 170, seed=16, burn_in=100)

    densities = np.linspace(0.02, 0.92, 19)
    all_flows = []
    for density in densities:
        runs = []
        for seed in range(8):
            _, flow = simulate(180, float(density), 220, seed=1000 + seed, burn_in=180)
            runs.append(flow.mean())
        all_flows.append(runs)
    all_flows = np.asarray(all_flows)
    mean = all_flows.mean(axis=1)
    lower, upper = np.quantile(all_flows, [0.25, 0.75], axis=1)

    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 11})
    fig, axes = plt.subplots(1, 2, figsize=(11.2, 4.5), gridspec_kw={"width_ratios": [1.08, 1]})

    cmap = ListedColormap(["#ffffff", NAVY, YELLOW])
    axes[0].imshow(states, origin="upper", aspect="auto", interpolation="nearest", cmap=cmap, vmin=0, vmax=2)
    axes[0].set_xlabel("Position on the periodic road")
    axes[0].set_ylabel("Time step")
    axes[0].set_title("A traffic jam moves backwards")
    axes[0].legend(
        handles=[Patch(facecolor=NAVY, label="moving car"), Patch(facecolor=YELLOW, label="stopped car")],
        frameon=False,
        ncol=2,
        loc="upper center",
        bbox_to_anchor=(0.5, -0.16),
    )

    axes[1].fill_between(densities, lower, upper, color=BLUE, alpha=0.22, label="middle 50% of runs")
    axes[1].plot(densities, mean, "o-", color=NAVY, lw=2.2, ms=5, label="mean flow")
    axes[1].set_xlabel("Density (cars per site)")
    axes[1].set_ylabel("Flow (cars per site per step)")
    axes[1].set_title("The fundamental diagram")
    axes[1].set_xlim(0, 0.95)
    axes[1].set_ylim(bottom=0)
    axes[1].grid(color="#dbe2ee", linewidth=0.8)
    axes[1].legend(frameon=False)
    for ax in axes:
        ax.spines[["top", "right"]].set_visible(False)

    fig.tight_layout(w_pad=2.8)
    fig.savefig(OUT / "nagel_schreckenberg_redesign.png", dpi=180, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def make_original_excerpt(pdf_path: Path):
    """Create a small, cited comparison excerpt from Figures 1 and 2 of the paper."""
    import fitz

    doc = fitz.open(pdf_path)
    crops = []
    for page_number in (3, 4):
        page = doc[page_number]
        rect = fitz.Rect(38, 72, 558, 430)
        pix = page.get_pixmap(matrix=fitz.Matrix(2.2, 2.2), clip=rect, alpha=False)
        crops.append(np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, pix.n)[..., :3])

    fig, axes = plt.subplots(1, 2, figsize=(11.2, 4.1))
    for ax, crop, label in zip(axes, crops, ("Low density", "Congested traffic")):
        ax.imshow(crop)
        ax.set_title(label, fontsize=12, color=NAVY)
        ax.axis("off")
    fig.tight_layout(pad=0.4)
    fig.savefig(OUT / "nagel_schreckenberg_original_excerpt.png", dpi=170, bbox_inches="tight", facecolor="white")
    plt.close(fig)


if __name__ == "__main__":
    make_modern_figure()
    source_pdf = Path("/private/tmp/Nagel_Schreckenberg_1992.pdf")
    if source_pdf.exists():
        make_original_excerpt(source_pdf)
    print("Generated Week 4 traffic figures.")
