#!/usr/bin/env python3
"""Generate course-owned conceptual figures for the Week 8 slides."""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from figure_style import BLUE, GRID, INK, ORANGE, YELLOW, apply_course_figure_style, finish_axes


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "notebooks/week08/images"
apply_course_figure_style()


def save(fig, name: str) -> None:
    fig.savefig(OUT / name, transparent=True, bbox_inches="tight", pad_inches=0.08)
    plt.close(fig)


def correlations() -> None:
    rng = np.random.default_rng(24)
    fig, axes = plt.subplots(1, 2, figsize=(10.8, 4.0), constrained_layout=True)
    x, y = np.meshgrid(np.arange(13), np.arange(8))

    # Away from criticality: many small, unrelated local patches.
    local = rng.integers(0, 7, size=x.shape)
    local[:, 1:] = np.where(rng.random((8, 12)) < 0.45, local[:, :-1], local[:, 1:])
    axes[0].scatter(x, y, c=local, cmap="Blues", s=95, edgecolor="white", linewidth=.6)
    axes[0].annotate("local fluctuation", (2, 5), xytext=(4.5, 6.7),
                     arrowprops={"arrowstyle": "->", "color": INK}, fontsize=11)

    # Near criticality: one correlated structure reaches across the system.
    phase = np.sin(.55*x + .75*y) + .45*np.sin(.25*x - .9*y)
    axes[1].scatter(x, y, c=phase, cmap="RdYlBu_r", s=95, edgecolor="white", linewidth=.6)
    axes[1].annotate("system-scale relationship", (9, 2), xytext=(4.2, 6.7),
                     arrowprops={"arrowstyle": "->", "color": INK}, fontsize=11)

    for ax, title in zip(
        axes,
        ["Away from the critical point", "Near the critical point"],
    ):
        ax.set_title(title, pad=12)
        ax.set_aspect("equal")
        ax.set_xlim(-.6, 12.6); ax.set_ylim(-.6, 7.6)
        ax.axis("off")
    save(fig, "critical_correlations.svg")


def finite_size() -> None:
    p = np.linspace(.40, .78, 500)
    pc = .5927
    fig, ax = plt.subplots(figsize=(7.8, 4.5), constrained_layout=True)
    for L, width, shift, colour in [
        (20, .040, .015, "#AAB5C8"),
        (40, .026, .008, BLUE),
        (80, .016, .003, ORANGE),
    ]:
        response = 1 / (1 + np.exp(-(p - (pc + shift))/width))
        ax.plot(p, response, linewidth=2.8, color=colour, label=f"$L={L}$")
    ax.axvline(pc, color=YELLOW, linewidth=2, linestyle="--", label="infinite-system $p_c$")
    ax.set(
        xlabel="Occupation probability, $p$",
        ylabel="Spanning probability",
        xlim=(.40, .78), ylim=(-.02, 1.03),
    )
    ax.legend(frameon=False, loc="lower right")
    finish_axes(ax)
    ax.text(.02, .96, "Illustrative finite-size response", transform=ax.transAxes,
            va="top", fontsize=11.5, color="#5A6685")
    save(fig, "percolation_finite_size.svg")


if __name__ == "__main__":
    # These were once hand-shaped schematics. Generate measured outputs from
    # the site-percolation model instead, using the shared reproducible script.
    from generate_week08_percolation_evidence import correlation_figure, finite_size_figure

    OUT.mkdir(parents=True, exist_ok=True)
    correlation_figure()
    finite_size_figure()
