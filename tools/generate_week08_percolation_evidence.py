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
    # Keep this fixed-L porosity palette distinct from the size palette in
    # panel B so matching colours do not imply a cross-panel correspondence.
    example_colours = ["#44307A", "#A44A86", "#38A169"]
    examples = []
    for p, colour in zip(example_probabilities, example_colours):
        r, relative = measure_curve(128, p, 240, 48)
        xi, intercept, mask = fit_exponential(r, relative, 128)
        examples.append((p, r, relative, xi, intercept, mask, colour))
        axes[0].semilogy(r, relative, "o", ms=3.0, color=colour, alpha=.9)
        fit_r = r[mask]
        axes[0].semilogy(fit_r, np.exp(intercept - (fit_r - 1) / xi),
                        "-", lw=2.2, color=colour,
                        label=rf"$p={p:.2f}$: $\xi_{{\rm eff}}={xi:.1f}$")

    # Mark one e-folding distance: fitted value falls by a factor e.
    _, middle_r, _, middle_xi, middle_intercept, middle_mask, middle_colour = examples[1]
    r_start = float(middle_r[middle_mask][0])
    r_end = r_start + middle_xi
    assert r_end <= middle_r[middle_mask][-1]
    y_start = np.exp(middle_intercept - (r_start - 1) / middle_xi)
    y_end = y_start / np.e
    # Keep the distance marker and label in the clear lower-left region,
    # rather than beneath the fitted points where the purple curve crosses.
    bracket_y = 3e-4
    axes[0].plot([r_start, r_end], [y_start, y_end], 'o', color=middle_colour, ms=6)
    axes[0].vlines([r_start, r_end], bracket_y, [y_start, y_end],
                   color=middle_colour, ls=":", lw=1.2)
    axes[0].annotate("", xy=(r_start, bracket_y), xytext=(r_end, bracket_y),
                     arrowprops=dict(arrowstyle="|-|", color=middle_colour, lw=1.6))
    axes[0].text((r_start + r_end) / 2, bracket_y * 1.18,
                  r"$p=0.50$ example", ha="center", va="bottom", color=middle_colour,
                  fontsize=12,
                  bbox=dict(facecolor="white", edgecolor="none", alpha=.95, pad=1))
    axes[0].text((r_start + r_end) / 2, bracket_y * 0.65,
                  r"$\Delta r=\xi_{\rm eff}$", ha="center", va="top", color=middle_colour,
                  bbox=dict(facecolor="white", edgecolor="none", alpha=.95, pad=2))

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

    axes[0].set(
        xlabel="Separation, $r$ (lattice sites)",
        ylabel="$C(r)/C(1)$",
    )
    axes[1].axvline(PC, color=NAVY, lw=1.5, ls="--", label=rf"$p_c\approx{PC:.3f}$")
    axes[1].set(
        xlabel="Open-site probability (porosity), $p$",
        ylabel=r"Effective correlation length, $\xi_{\rm eff}$",
    )
    axes[0].legend(frameon=False, fontsize=12, title=r"fixed $L=128$")
    axes[1].legend(frameon=False, fontsize=12, ncol=2)
    for ax in axes:
        finish_axes(ax)
    fig.savefig(OUT / "critical_correlations.svg", transparent=True)
    fig.savefig(OUT / "critical_correlations.png", dpi=160)
    plt.close(fig)


def correlation_scaling_guide():
    """Show how nu appears on log-log axes and how finite size cuts off xi."""
    distance = np.logspace(-3, -0.55, 240)
    nu = 4 / 3
    amplitude = 0.16
    infinite_xi = amplitude * distance ** (-nu)

    fig, ax = plt.subplots(figsize=(8.1, 4.7), constrained_layout=True)
    ax.loglog(distance, infinite_xi, color=NAVY, lw=2.5,
              label=r"infinite-system law, $\nu=\frac{4}{3}$")

    # A smooth minimum shows the expected finite-size cutoff without
    # presenting the curves as measurements from the preceding simulation.
    cutoff_power = 5
    for size, colour in [(32, "#98A8BF"), (64, BLUE), (128, CORAL)]:
        cutoff = 0.42 * size
        finite_xi = (infinite_xi ** (-cutoff_power)
                     + cutoff ** (-cutoff_power)) ** (-1 / cutoff_power)
        ax.loglog(distance, finite_xi, color=colour, lw=2.0,
                  label=rf"finite-size guide, $L={size}$")

    ax.annotate(r"gradient $=-\nu$", xy=(0.045, 10), xytext=(0.10, 28),
                arrowprops=dict(arrowstyle="->", color="#5B6780", lw=1.3),
                color="#5B6780", ha="center", va="center")
    ax.set(
        xlabel=r"Distance from the threshold, $|p-p_c|$",
        ylabel=r"Correlation length, $\xi$",
    )
    ax.legend(frameon=False, fontsize=12, loc="lower left")
    finish_axes(ax)
    fig.savefig(OUT / "percolation_correlation_scaling_guide.svg", transparent=True)
    fig.savefig(OUT / "percolation_correlation_scaling_guide.png",
                dpi=180, transparent=True)
    plt.close(fig)


def finite_size_figure():
    rng = np.random.default_rng(302409)
    probabilities = np.linspace(.48, .70, 23)
    trials = 450
    joint_L = 128
    joint_probabilities = np.array([.54, .57, .584, .592, .600, .62])
    joint_p = []
    joint_fractions = []
    joint_spanning = []
    fig, axes = plt.subplots(1, 3, figsize=(17.2, 5.2), constrained_layout=True)
    fig.get_layout_engine().set(rect=(0, 0, 1, .90))
    ax, fraction_ax, joint_ax = axes
    for L, colour in [(16, "#98A8BF"), (32, BLUE), (64, CORAL),
                      (128, "#209582"), (256, "#8C4CB5"), (512, NAVY)]:
        # Retain the original three series; resolve the narrower transition
        # with additional open-site probabilities for the larger lattices.
        if L >= 128:
            probabilities = np.unique(np.round(np.r_[np.linspace(.48, .70, 23),
                                                      np.arange(.582, .606, .002)], 6))
        estimates = []
        lower_errors = []
        upper_errors = []
        fractions = []
        fraction_errors = []
        for p in probabilities:
            successes = 0
            largest_fractions = []
            spanning_flags = []
            for _ in range(trials):
                _, labels, number = labelled_lattice(L, p, rng)
                did_span = spans(labels)
                successes += did_span
                spanning_flags.append(did_span)
                sizes = cluster_sizes(labels, number)
                largest_fractions.append(sizes.max() / L**2 if number else 0.0)
            if L == joint_L and np.any(np.isclose(p, joint_probabilities)):
                joint_p.extend(np.full(trials, p))
                joint_fractions.extend(largest_fractions)
                joint_spanning.extend(spanning_flags)
            estimate = successes / trials
            estimates.append(estimate)
            # Wilson intervals remain informative when every sampled lattice
            # gives the same binary spanning outcome.
            z = 1.96
            denominator = 1 + z**2 / trials
            centre = (estimate + z**2 / (2 * trials)) / denominator
            half_width = (
                z
                * np.sqrt(
                    estimate * (1 - estimate) / trials
                    + z**2 / (4 * trials**2)
                )
                / denominator
            )
            lower_bound = max(0.0, centre - half_width)
            upper_bound = min(1.0, centre + half_width)
            lower_errors.append(max(0.0, estimate - lower_bound))
            upper_errors.append(max(0.0, upper_bound - estimate))
            fractions.append(np.mean(largest_fractions))
            fraction_errors.append(np.std(largest_fractions, ddof=1) / np.sqrt(trials))
        estimates = np.asarray(estimates)
        spanning_errors = np.vstack([lower_errors, upper_errors])
        ax.fill_between(
            probabilities,
            estimates - spanning_errors[0],
            estimates + spanning_errors[1],
            color=colour,
            alpha=0.16,
            linewidth=0,
        )
        ax.plot(
            probabilities,
            estimates,
            "o-",
            ms=4,
            lw=2.0,
            color=colour,
            alpha=0.92,
            label=f"$L={L}$",
        )
        fractions = np.asarray(fractions)
        fraction_errors = np.asarray(fraction_errors)
        fraction_ax.fill_between(
            probabilities,
            np.clip(fractions - 1.96 * fraction_errors, 0, 1),
            np.clip(fractions + 1.96 * fraction_errors, 0, 1),
            color=colour,
            alpha=0.16,
            linewidth=0,
        )
        fraction_ax.plot(
            probabilities,
            fractions,
            "o-",
            ms=4,
            lw=2.0,
            color=colour,
            alpha=0.92,
            label=f"$L={L}$",
        )
    ax.set(xlabel="Open-site probability (porosity), $p$", ylabel="Estimated spanning probability",
           xlim=(probabilities.min(), probabilities.max()), ylim=(-.02, 1.02),
           title="Does a cluster span?")
    fraction_ax.set(xlabel="Open-site probability (porosity), $p$",
                    ylabel=r"Mean largest-cluster fraction, $\langle f_{\max}\rangle$",
                    title="How much of the lattice does it occupy?", ylim=(0, .75))
    for panel in (ax, fraction_ax):
        panel.axvline(PC, color=YELLOW, lw=2.2, ls="--", label=rf"$p_c\approx {PC:.3f}$")
        finish_axes(panel)
    handles, labels = ax.get_legend_handles_labels()
    fig.legend(handles, labels, loc="upper center", bbox_to_anchor=(.5, 1),
               frameon=False, fontsize=13, ncol=7)

    # The third panel retains the joint outcome for individual L=128 lattices.
    # Vertical jitter separates coincident binary outcomes; it is not data.
    jitter_rng = np.random.default_rng(302411)
    joint_spanning = np.asarray(joint_spanning, dtype=float)
    vertical_jitter = jitter_rng.uniform(-.075, .075, joint_spanning.size)
    points = joint_ax.scatter(joint_fractions, joint_spanning + vertical_jitter,
                              c=joint_p, cmap="cividis", vmin=.54, vmax=.62,
                              s=10, alpha=.48, linewidths=0, rasterized=True)
    joint_ax.set(xlabel=r"Largest-cluster fraction, $f_{\max}$",
                 ylabel="Does this lattice span?",
                 yticks=[0, 1], yticklabels=["No", "Yes"], ylim=(-.18, 1.18),
                 title=rf"Do the measures agree? ($L={joint_L}$)")
    colourbar = fig.colorbar(points, ax=joint_ax, pad=.02, fraction=.06)
    colourbar.set_label("Porosity, $p$")
    finish_axes(joint_ax)
    fig.savefig(OUT / "percolation_finite_size.svg", transparent=True)
    fig.savefig(OUT / "percolation_finite_size.png", dpi=160, transparent=True)
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
                (PC, f"Near threshold, $p={PC:.3f}$", CORAL),
                (0.65, "Above threshold, $p=0.65$", "#209582")]
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
        ax.set(xlabel="Cluster size, $s$", ylabel=r"Fraction of clusters with $S\geq s$")
        ax.legend(frameon=False)
        finish_axes(ax)
    fig.savefig(OUT / "Tails_comparison.png", dpi=220, transparent=True)
    plt.close(fig)


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    correlation_figure()
    correlation_scaling_guide()
    finite_size_figure()
    tails_figure()
