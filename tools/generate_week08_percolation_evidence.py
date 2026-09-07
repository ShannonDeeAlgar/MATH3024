#!/usr/bin/env python3
"""Generate Week 8 figures from reproducible site-percolation experiments."""

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy import ndimage

from figure_style import apply_course_figure_style, finish_axes


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "notebooks/week08/images"
PC = 0.592746
NAVY = "#172A50"
BLUE = "#3C78A8"
PALE = "#DCE8F3"
CORAL = "#D95F3D"
YELLOW = "#F2CF4A"
STRUCTURE = ndimage.generate_binary_structure(2, 1)

apply_course_figure_style()


def labelled_lattice(L, p, rng):
    occupied = rng.random((L, L)) < p
    labels, number = ndimage.label(occupied, structure=STRUCTURE)
    return occupied, labels, number


def cluster_sizes(labels, number):
    if number == 0:
        return np.empty(0, dtype=int)
    return np.bincount(labels.ravel(), minlength=number + 1)[1:]


def spans(labels):
    top = set(labels[0, :]) - {0}
    bottom = set(labels[-1, :]) - {0}
    left = set(labels[:, 0]) - {0}
    right = set(labels[:, -1]) - {0}
    return bool((top & bottom) or (left & right))


def pair_connectedness(labels, distances):
    values = []
    for r in distances:
        horizontal = (labels[:, :-r] == labels[:, r:]) & (labels[:, :-r] > 0)
        vertical = (labels[:-r, :] == labels[r:, :]) & (labels[:-r, :] > 0)
        values.append((horizontal.sum() + vertical.sum()) / (horizontal.size + vertical.size))
    return np.asarray(values)


def snapshot_colours(labels, number):
    image = np.zeros(labels.shape + (4,), dtype=float)
    image[:] = matplotlib.colors.to_rgba("#F7F9FC")
    image[labels > 0] = matplotlib.colors.to_rgba(PALE)
    if number:
        sizes = cluster_sizes(labels, number)
        largest = 1 + int(np.argmax(sizes))
        image[labels == largest] = matplotlib.colors.to_rgba(BLUE)
    return image


def correlation_figure():
    rng = np.random.default_rng(302408)
    L = 128
    distances = np.arange(1, 49)
    snapshot_settings = [(0.45, "Below the threshold"), (PC, "Near the threshold")]
    snapshots = []
    for p, _ in snapshot_settings:
        for sample in range(1):
            _, labels, number = labelled_lattice(L, p, rng)
            snapshots.append(snapshot_colours(labels, number))

    # Keep the fixed-p lattice examples separate from the distance sweep.
    fig, axes = plt.subplots(1, 2, figsize=(10.8, 4.0), constrained_layout=True)
    for col, ((p, title), image) in enumerate(zip(snapshot_settings, snapshots)):
        ax = axes[col]
        ax.imshow(image, interpolation="nearest")
        ax.set_title(f"{title}: $p={p:.3f}$")
        ax.set_xticks([]); ax.set_yticks([])
    fig.savefig(OUT / "percolation_cluster_snapshots.svg", transparent=True)
    plt.close(fig)

    def measure_curve(size, p, samples, max_distance):
        r = np.arange(1, max_distance + 1)
        accumulated = np.zeros(r.size)
        for _ in range(samples):
            _, labels, _ = labelled_lattice(size, p, rng)
            accumulated += pair_connectedness(labels, r)
        relative = accumulated / samples
        return r, relative / relative[0]

    def fit_exponential(r, relative, size):
        mask = ((r >= 2) & (r <= min(36, size // 3)) &
                (relative < 0.88) & (relative > 1e-2))
        slope, intercept = np.polyfit(r[mask] - 1, np.log(relative[mask]), 1)
        return -1.0 / slope, intercept, mask

    fig, axes = plt.subplots(1, 2, figsize=(12.4, 4.9), constrained_layout=True)

    # Panel A: make the extraction of xi visible for three subcritical cases.
    example_probabilities = [0.42, 0.50, 0.56]
    example_colours = ["#44307A", BLUE, "#38A169"]
    examples = []
    for p, colour in zip(example_probabilities, example_colours):
        r, relative = measure_curve(128, p, 240, 48)
        xi, intercept, mask = fit_exponential(r, relative, 128)
        examples.append((p, r, relative, xi, intercept, mask, colour))
        axes[0].semilogy(r, relative, "o", ms=3.0, color=colour, alpha=.9)
        fit_r = r[mask]
        axes[0].semilogy(fit_r, np.exp(intercept - (fit_r - 1) / xi),
                        "-", lw=2.2, color=colour,
                        label=rf"$p={p:.2f}$: $\xi={xi:.1f}$")

    # Mark one e-folding distance: fitted value falls by a factor e.
    _, _, _, middle_xi, middle_intercept, _, middle_colour = examples[1]
    y_start = np.exp(middle_intercept)
    axes[0].vlines(1 + middle_xi, y_start / np.e, y_start,
                   color=middle_colour, ls="--", lw=1.5)
    axes[0].annotate(r"one fitted $\xi$", xy=(1 + middle_xi, y_start / np.e),
                     xytext=(14, .13), color=middle_colour,
                     arrowprops=dict(arrowstyle="->", color=middle_colour, lw=1.2))

    # Panel B: repeat the extraction for several finite lattice sizes.
    sweep_probabilities = np.array([0.38, 0.42, 0.46, 0.50, 0.53,
                                    0.55, 0.565, 0.575, 0.584, 0.589])
    for size, colour in [(32, "#98A8BF"), (64, BLUE), (128, CORAL)]:
        estimates = []
        max_distance = min(48, size // 2 - 1)
        for p in sweep_probabilities:
            r, relative = measure_curve(size, p, 120, max_distance)
            xi, _, _ = fit_exponential(r, relative, size)
            estimates.append(xi)
        axes[1].plot(sweep_probabilities, estimates, "o-", color=colour,
                     lw=2.1, ms=4.2, label=rf"$L={size}$")

    axes[0].set(title="How correlation length is extracted",
                xlabel="Separation, $r$ (lattice sites)", ylabel="$C(r)/C(1)$")
    axes[1].axvline(PC, color=NAVY, lw=1.5, ls="--", label=rf"$p_c\approx{PC:.3f}$")
    axes[1].set(title="Finite lattices limit the measured growth",
                xlabel="Occupation probability, $p$", ylabel=r"Fitted correlation length, $\xi$")
    axes[0].legend(frameon=False, fontsize=9)
    axes[1].legend(frameon=False, fontsize=9, ncol=2)
    for ax in axes:
        finish_axes(ax)
    fig.savefig(OUT / "critical_correlations.svg", transparent=True)
    plt.close(fig)


def finite_size_figure():
    rng = np.random.default_rng(302409)
    probabilities = np.linspace(.48, .70, 23)
    trials = 450
    fig, ax = plt.subplots(figsize=(8.2, 4.8), constrained_layout=True)
    for L, colour in [(16, "#98A8BF"), (32, BLUE), (64, CORAL)]:
        estimates = []
        errors = []
        for p in probabilities:
            successes = 0
            for _ in range(trials):
                _, labels, _ = labelled_lattice(L, p, rng)
                successes += spans(labels)
            estimate = successes / trials
            estimates.append(estimate)
            errors.append(np.sqrt(estimate * (1 - estimate) / trials))
        estimates = np.asarray(estimates)
        errors = np.asarray(errors)
        ax.plot(probabilities, estimates, "o-", ms=4, lw=2.2, color=colour, label=f"$L={L}$")
        ax.fill_between(probabilities, np.maximum(0, estimates - 1.96 * errors),
                        np.minimum(1, estimates + 1.96 * errors), color=colour, alpha=.14)
    ax.axvline(PC, color=YELLOW, lw=2.2, ls="--",
               label=rf"$p_c\approx {PC:.3f}$")
    ax.set(xlabel="Occupation probability, $p$", ylabel="Estimated spanning probability",
           xlim=(probabilities.min(), probabilities.max()), ylim=(-.02, 1.02),
           title=f"Site percolation: {trials} independent lattices per point")
    ax.legend(frameon=False, loc="lower right", ncol=2)
    finish_axes(ax)
    fig.savefig(OUT / "percolation_finite_size.svg", transparent=True)
    plt.close(fig)


def empirical_ccdf(values):
    values = np.sort(np.asarray(values))
    unique, first = np.unique(values, return_index=True)
    survival = (values.size - first) / values.size
    return unique, survival


def tails_figure():
    rng = np.random.default_rng(302410)
    L = 128
    settings = [(0.45, "Below threshold, $p=0.45$", BLUE),
                (PC, f"Near threshold, $p={PC:.3f}$", CORAL)]
    samples = []
    for p, label, colour in settings:
        sizes = []
        for _ in range(600):
            _, labels, number = labelled_lattice(L, p, rng)
            sizes.extend(cluster_sizes(labels, number))
        samples.append((np.asarray(sizes), label, colour))

    fig, axes = plt.subplots(1, 2, figsize=(11.4, 4.8), constrained_layout=True)
    for values, label, colour in samples:
        x, y = empirical_ccdf(values)
        axes[0].plot(x, y, lw=2.6, color=colour, label=label)
        axes[1].loglog(x, y, lw=2.6, color=colour, label=label)
    axes[0].set(xlim=(1, 180), ylim=(0, 1.02), title="Linear axes")
    axes[1].set(title="Log–log axes")
    for ax in axes:
        ax.set(xlabel="Cluster size, $s$", ylabel="$\Pr(S\geq s)$")
        ax.legend(frameon=False)
        finish_axes(ax)
    fig.suptitle("Cluster-size tails measured in site percolation", fontsize=17)
    fig.savefig(OUT / "Tails_comparison.png", dpi=220, transparent=True)
    plt.close(fig)


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    correlation_figure()
    finite_size_figure()
    tails_figure()
