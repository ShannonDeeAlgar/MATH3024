"""Compare ensemble summaries using the Week 8 site-percolation model."""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy import ndimage

from figure_style import (
    GREY,
    INK,
    LIGHT_BLUE,
    ORANGE,
    apply_course_figure_style,
    finish_axes,
    style_figure,
)


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "notebooks/week08/images/ensemble_summary_comparison.svg"
PC = 0.592746
STRUCTURE = ndimage.generate_binary_structure(2, 1)


def percolation_ensemble(size=64, number=160, seed=3024):
    """Measure the largest-cluster fraction in independent site-percolation lattices."""
    rng = np.random.default_rng(seed)
    probabilities = np.unique(np.r_[np.linspace(0.48, 0.70, 12), PC])
    fractions = np.empty((probabilities.size, number))
    for p_index, probability in enumerate(probabilities):
        for run in range(number):
            occupied = rng.random((size, size)) < probability
            labels, clusters = ndimage.label(occupied, structure=STRUCTURE)
            if clusters:
                sizes = np.bincount(labels.ravel(), minlength=clusters + 1)[1:]
                fractions[p_index, run] = sizes.max() / size**2
            else:
                fractions[p_index, run] = 0.0
    return probabilities, fractions


def draw_raw(ax, probabilities, fractions):
    jitter = np.linspace(-0.0015, 0.0015, fractions.shape[1])
    for probability, values in zip(probabilities, fractions):
        ax.scatter(
            probability + jitter,
            values,
            color=GREY,
            alpha=0.24,
            s=7,
            linewidths=0,
        )
    ax.plot(probabilities, fractions.mean(axis=1), color=INK, linewidth=2.4)
    ax.set_title("Individual realisations + mean")


def draw_band(ax, probabilities, centre, lower, upper, title, colour=INK):
    ax.fill_between(probabilities, lower, upper, color=LIGHT_BLUE, alpha=0.45)
    ax.plot(probabilities, centre, color=colour, linewidth=2.4, marker="o", ms=3.5)
    ax.set_title(title)


def main():
    apply_course_figure_style()
    probabilities, fractions = percolation_ensemble()
    mean = fractions.mean(axis=1)
    median = np.median(fractions, axis=1)
    standard_deviation = fractions.std(axis=1, ddof=1)
    standard_error = standard_deviation / np.sqrt(fractions.shape[1])
    q25, q75 = np.quantile(fractions, [0.25, 0.75], axis=1)

    fig, axes = plt.subplots(2, 3, figsize=(14.2, 8.2), sharex=True, sharey=True)
    draw_raw(axes[0, 0], probabilities, fractions)
    draw_band(
        axes[0, 1], probabilities, mean, fractions.min(axis=1),
        fractions.max(axis=1), "Mean + observed min–max",
    )
    draw_band(
        axes[0, 2], probabilities, median, q25, q75,
        "Median + middle 50%", ORANGE,
    )
    draw_band(
        axes[1, 0], probabilities, mean, mean - standard_deviation,
        mean + standard_deviation, "Mean ± 1 standard deviation",
    )
    draw_band(
        axes[1, 1], probabilities, mean, mean - 1.96 * standard_error,
        mean + 1.96 * standard_error, "Mean + approximate 95% CI",
    )
    axes[1, 2].errorbar(
        probabilities,
        mean,
        yerr=standard_deviation,
        color=INK,
        marker="o",
        markersize=4.5,
        linewidth=1.8,
        capsize=4,
    )
    axes[1, 2].set_title("Mean ± SD as error bars")

    for row in axes:
        for ax in row:
            label = rf"$p_c\approx {PC:.3f}$" if ax is axes[0, 0] else None
            ax.axvline(PC, color="#F2CF4A", linewidth=1.7, linestyle="--", label=label)
            ax.set(xlim=(0.475, 0.705), ylim=(-0.02, 0.82))
            finish_axes(ax)
    axes[0, 0].legend(frameon=False, loc="upper left")
    for ax in axes[1, :]:
        ax.set_xlabel("Open-site probability (porosity), $p$")
    for ax in axes[:, 0]:
        ax.set_ylabel(r"Largest-cluster fraction, $f_{\max}$")

    fig.subplots_adjust(
        left=0.075,
        right=0.99,
        bottom=0.09,
        top=0.97,
        wspace=0.18,
        hspace=0.30,
    )
    style_figure(fig)
    fig.savefig(OUTPUT)
    plt.close(fig)
    print(f"Wrote {OUTPUT}")


if __name__ == "__main__":
    main()
