#!/usr/bin/env python3
"""Generate the Week 2 scale-free and Zipf-law teaching figures."""

from __future__ import annotations

import re
from collections import Counter
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle, Polygon


ROOT = Path(__file__).resolve().parents[1]
IMAGES = ROOT / "notebooks/week02/images"
TEXT = Path("/private/tmp/pride_and_prejudice.txt")

NAVY = "#1d3158"
BLUE = "#5d7fae"
YELLOW = "#f3cf52"
GREY = "#68758c"


def save_zipf() -> None:
    text = TEXT.read_text(encoding="utf-8")
    start = text.find("*** START OF THE PROJECT GUTENBERG EBOOK")
    end = text.find("*** END OF THE PROJECT GUTENBERG EBOOK")
    if start >= 0 and end > start:
        text = text[start:end]
    words = re.findall(r"[a-z]+(?:'[a-z]+)?", text.lower())
    counts = np.array(sorted(Counter(words).values(), reverse=True), dtype=float)
    rank = np.arange(1, len(counts) + 1)

    fit_mask = (rank >= 10) & (rank <= 1000)
    slope, intercept = np.polyfit(
        np.log10(rank[fit_mask]), np.log10(counts[fit_mask]), 1
    )
    reference = 10 ** intercept * rank**slope

    shown = np.unique(
        np.concatenate(
            [np.arange(min(500, len(rank))), np.geomspace(500, len(rank), 900)]
        ).astype(int)
    )
    shown = shown[shown < len(rank)]

    fig, ax = plt.subplots(figsize=(8.4, 4.8))
    ax.loglog(
        rank[shown],
        counts[shown],
        ".",
        color=BLUE,
        ms=3.5,
        alpha=0.55,
        label="observed",
    )
    ax.loglog(
        rank,
        reference,
        color=NAVY,
        lw=2.4,
        label=rf"illustrative fit, slope {slope:.2f}",
    )
    ax.set_xlabel("Word rank, $r$")
    ax.set_ylabel("Frequency, $f(r)$")
    ax.set_title("Word frequencies in Pride and Prejudice")
    ax.grid(True, which="major", color="#d9e0ea", linewidth=0.8)
    ax.spines[["top", "right"]].set_visible(False)
    ax.legend(frameon=False)
    fig.tight_layout()
    fig.savefig(IMAGES / "zipf_pride_prejudice.svg", transparent=True)
    plt.close(fig)


def save_circle_contrast() -> None:
    """Contrast scaling a family of circles with self-similarity of one set."""
    fig, axes = plt.subplots(1, 2, figsize=(10.8, 4.45))

    ax = axes[0]
    ax.set_title("A family of circles", fontsize=14, color=NAVY, pad=8)
    centres = (-1.25, 1.25)
    radii = (0.72, 1.02)
    colours = (NAVY, YELLOW)
    for centre, radius, colour in zip(centres, radii, colours):
        ax.add_patch(
            Circle(
                (centre, 0.08),
                radius,
                facecolor="none",
                edgecolor=colour,
                linewidth=3,
            )
        )
        ax.plot(
            [centre, centre + radius],
            [0.08, 0.08],
            color=colour,
            linewidth=2,
        )
    ax.text(centres[0], 1.27, r"$x^2+y^2=R^2$", ha="center", fontsize=13)
    ax.text(
        centres[1],
        1.27,
        r"$x^2+y^2=(aR)^2$",
        ha="center",
        fontsize=13,
    )
    ax.text(centres[0] + 0.34, 0.17, r"$R$", ha="center", color=NAVY)
    ax.text(centres[1] + 0.51, 0.17, r"$aR$", ha="center", color="#856600")
    ax.text(
        0,
        -1.22,
        r"$A(R)=\pi R^2,\qquad A(aR)=a^2A(R)$",
        ha="center",
        fontsize=13,
        color=NAVY,
    )
    ax.text(
        0,
        -1.57,
        r"$R$ remains a characteristic length; changing it selects a different circle.",
        ha="center",
        fontsize=10.5,
        color=GREY,
    )
    ax.set_xlim(-2.45, 2.45)
    ax.set_ylim(-1.78, 1.62)
    ax.set_aspect("equal")
    ax.axis("off")

    ax = axes[1]
    ax.set_title("One self-similar fractal", fontsize=14, color=NAVY, pad=8)

    root = np.array([[0.0, 0.0], [1.0, 0.0], [0.5, np.sqrt(3) / 2]])

    def sierpinski(triangle: np.ndarray, depth: int) -> None:
        if depth == 0:
            ax.add_patch(
                Polygon(
                    triangle,
                    closed=True,
                    facecolor=NAVY,
                    edgecolor="none",
                )
            )
            return
        a, b, c = triangle
        ab, ac, bc = (a + b) / 2, (a + c) / 2, (b + c) / 2
        sierpinski(np.array([a, ab, ac]), depth - 1)
        sierpinski(np.array([ab, b, bc]), depth - 1)
        sierpinski(np.array([ac, bc, c]), depth - 1)

    sierpinski(root, 4)
    ax.add_patch(
        Polygon(root, closed=True, fill=False, edgecolor=GREY, linewidth=1.2)
    )
    first_copy = np.array(
        [[0.0, 0.0], [0.5, 0.0], [0.25, np.sqrt(3) / 4]]
    )
    ax.add_patch(
        Polygon(
            first_copy,
            closed=True,
            fill=False,
            edgecolor=YELLOW,
            linewidth=3,
        )
    )
    ax.annotate(
        "one half-scale copy",
        xy=(0.24, 0.19),
        xytext=(0.92, 0.17),
        ha="left",
        va="center",
        fontsize=10.5,
        color=GREY,
        arrowprops={"arrowstyle": "->", "color": GREY, "lw": 1.4},
    )
    ax.text(
        0.5,
        -0.17,
        r"$L=2,\quad N=3,\quad N=L^D$",
        ha="center",
        fontsize=13,
        color=NAVY,
    )
    ax.text(
        0.5,
        -0.34,
        r"$D=\log N/\log L=\log 3/\log 2$",
        ha="center",
        fontsize=12.5,
    )
    ax.text(
        0.5,
        -0.50,
        "Magnifying a retained copy recovers the same construction.",
        ha="center",
        fontsize=10.5,
        color=GREY,
    )
    ax.set_xlim(-0.08, 1.42)
    ax.set_ylim(-0.58, 1.02)
    ax.set_aspect("equal")
    ax.axis("off")

    fig.tight_layout(w_pad=2.2)
    fig.savefig(IMAGES / "circle_vs_scale_free.svg", transparent=True)
    plt.close(fig)


def save_power_law_data_types() -> None:
    """Contrast empirical discrete and continuous power-law observations."""
    rng = np.random.default_rng(3024)
    alpha = 2.5
    sample_size = 1800

    # Zipf supplies integer-valued observations with a power-law tail.
    discrete = rng.zipf(alpha, sample_size)
    discrete = discrete[discrete <= 1000]
    x_discrete = np.unique(discrete)
    survival_discrete = np.array([(discrete >= value).mean() for value in x_discrete])
    reference_discrete = x_discrete.astype(float) ** (1 - alpha)

    # NumPy's Pareto variable starts at zero, so add one to set x_min = 1.
    continuous = rng.pareto(alpha - 1, sample_size) + 1
    continuous.sort()
    x_continuous = continuous
    survival_continuous = (
        np.arange(sample_size, 0, -1, dtype=float) / sample_size
    )
    reference_continuous = x_continuous ** (1 - alpha)

    fig, axes = plt.subplots(2, 1, figsize=(8.6, 5.8), sharex=False)

    axes[0].loglog(
        x_discrete,
        survival_discrete,
        "o",
        ms=4.2,
        markerfacecolor="white",
        markeredgecolor=BLUE,
        label="integer observations",
    )
    axes[0].loglog(
        x_discrete,
        reference_discrete,
        color=NAVY,
        lw=2.2,
        label="power-law reference",
    )
    axes[0].set_title("Discrete data")
    axes[0].set_ylabel(r"$P(X\geq x)$")

    shown = np.unique(
        np.geomspace(1, sample_size, 260).astype(int) - 1
    )
    axes[1].loglog(
        x_continuous[shown],
        survival_continuous[shown],
        "o",
        ms=3.8,
        markerfacecolor="white",
        markeredgecolor=YELLOW,
        label="continuous observations",
    )
    axes[1].loglog(
        x_continuous,
        reference_continuous,
        color=NAVY,
        lw=2.2,
        label="power-law reference",
    )
    axes[1].set_title("Continuous data")
    axes[1].set_xlabel("Observed value, $x$")
    axes[1].set_ylabel(r"$P(X\geq x)$")

    for ax in axes:
        ax.grid(True, which="major", color="#d9e0ea", linewidth=0.8)
        ax.spines[["top", "right"]].set_visible(False)
        ax.legend(frameon=False, fontsize=9, loc="upper right")

    fig.tight_layout()
    fig.savefig(IMAGES / "power_law_discrete_continuous.svg", transparent=True)
    plt.close(fig)


if __name__ == "__main__":
    IMAGES.mkdir(parents=True, exist_ok=True)
    save_zipf()
    save_circle_contrast()
    save_power_law_data_types()
    print("Generated Week 2 scale-free figures.")
