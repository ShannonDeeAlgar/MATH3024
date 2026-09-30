#!/usr/bin/env python3
"""Generate the Week 5 Vicsek parameter-sweep evidence."""

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy.spatial import cKDTree

from figure_style import apply_course_figure_style, finish_axes


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "notebooks/week05/images"
INK = "#172A50"
BLUE = "#3C78A8"
CORAL = "#D95F3D"
YELLOW = "#F2CF4A"
GREY = "#8A94A6"

apply_course_figure_style()


def polarisation(headings):
    return np.abs(np.mean(np.exp(1j * headings)))


def simulate_vicsek(*, n_agents, density, noise, speed, steps, window, seed):
    """Return the late-time mean polarisation for angular-noise Vicsek particles."""
    rng = np.random.default_rng(seed)
    box_size = np.sqrt(n_agents / density)
    positions = rng.random((n_agents, 2)) * box_size
    headings = rng.uniform(-np.pi, np.pi, n_agents)
    late_phi = []

    for step in range(steps):
        directions = np.column_stack((np.cos(headings), np.sin(headings)))
        pairs = cKDTree(positions, boxsize=box_size).query_pairs(1.0, output_type="ndarray")

        summed = directions.copy()  # Each particle includes itself.
        if pairs.size:
            np.add.at(summed, pairs[:, 0], directions[pairs[:, 1]])
            np.add.at(summed, pairs[:, 1], directions[pairs[:, 0]])
        mean_headings = np.arctan2(summed[:, 1], summed[:, 0])
        new_headings = mean_headings + rng.uniform(-noise / 2, noise / 2, n_agents)

        # Retain the old-heading position update used in the course implementation.
        positions = (positions + speed * directions) % box_size
        headings = (new_headings + np.pi) % (2 * np.pi) - np.pi
        if step >= steps - window:
            late_phi.append(polarisation(headings))

    return float(np.mean(late_phi))


def ensemble(noise, density, speed, *, seeds, n_agents=120, steps=300, window=80):
    return np.asarray([
        simulate_vicsek(n_agents=n_agents, density=density, noise=noise,
                        speed=speed, steps=steps, window=window, seed=int(seed))
        for seed in seeds
    ])


def centre_and_iqr(values):
    values = np.asarray(values)
    return values.mean(axis=-1), *np.quantile(values, [.25, .75], axis=-1)


def sweep_evidence():
    seeds = np.arange(10) + 302450
    density = 2.0
    speed = 0.1

    coarse_noise = np.linspace(0, 2 * np.pi, 9)
    coarse_runs = np.asarray([ensemble(eta, density, speed, seeds=seeds)
                              for eta in coarse_noise])
    coarse_mean = coarse_runs.mean(axis=1)
    interval_change = np.abs(np.diff(coarse_mean) / np.diff(coarse_noise))
    steepest = int(np.argmax(interval_change))
    neighbours = [index for index in (steepest - 1, steepest + 1)
                  if 0 <= index < interval_change.size]
    adjacent = max(neighbours, key=interval_change.__getitem__)
    selected = sorted((steepest, adjacent))
    left = coarse_noise[selected[0]]
    right = coarse_noise[selected[-1] + 1]
    added_noise = np.linspace(left, right, 9)[1:-1]
    added_runs = np.asarray([ensemble(eta, density, speed, seeds=seeds + 100)
                             for eta in added_noise])
    all_noise = np.r_[coarse_noise, added_noise]
    all_runs = np.vstack((coarse_runs, added_runs))
    order = np.argsort(all_noise)
    all_noise, all_runs = all_noise[order], all_runs[order]
    noise_mean, noise_q1, noise_q3 = centre_and_iqr(all_runs)

    density_values = np.array([.15, .25, .4, .65, 1.0, 1.6, 2.5, 4.0, 6.0])
    density_noise = 2.0
    density_runs = np.asarray([ensemble(density_noise, rho, speed, seeds=seeds + 200)
                               for rho in density_values])
    density_mean, density_q1, density_q3 = centre_and_iqr(density_runs)

    map_density = np.array([.25, .45, .75, 1.2, 2.0, 3.2, 5.0])
    map_noise = np.linspace(.4, 5.8, 10)
    map_seeds = np.arange(6) + 302850
    response = np.empty((map_density.size, map_noise.size))
    spread = np.empty_like(response)
    for row, rho in enumerate(map_density):
        for column, eta in enumerate(map_noise):
            values = ensemble(eta, rho, speed, seeds=map_seeds, steps=260, window=70)
            response[row, column] = values.mean()
            spread[row, column] = np.subtract(*np.quantile(values, [.75, .25]))

    fig, axes = plt.subplots(1, 3, figsize=(17.0, 4.8), constrained_layout=True)

    axes[0].plot(coarse_noise, coarse_mean, "o--", color=GREY, lw=1.8,
                 ms=5, label="Coarse pilot")
    axes[0].plot(all_noise, noise_mean, "o-", color=INK, lw=2.3,
                 ms=4, label="After refinement")
    axes[0].fill_between(all_noise, noise_q1, noise_q3, color=BLUE, alpha=.22,
                         label="Middle 50% of runs")
    axes[0].axvspan(left, right, color=YELLOW, alpha=.16, zorder=-2,
                    label="Refined transition band")
    axes[0].set(title=rf"Noise sweep at fixed $\rho={density:g}$",
                xlabel=r"Angular-noise width, $\eta$", ylabel=r"Mean late-time polarisation, $\Phi$",
                xlim=(-.08, 2 * np.pi + .08), ylim=(-.03, 1.03))
    axes[0].legend(frameon=False, fontsize=8.5)

    axes[1].plot(density_values, density_mean, "o-", color=CORAL, lw=2.3)
    axes[1].fill_between(density_values, density_q1, density_q3,
                         color=CORAL, alpha=.2)
    axes[1].set_xscale("log")
    axes[1].set(title=rf"Density sweep at fixed $\eta={density_noise:g}$",
                xlabel=r"Density, $\rho=N/L^2$", ylabel=r"Mean late-time polarisation, $\Phi$",
                ylim=(-.03, 1.03))

    mesh = axes[2].pcolormesh(map_noise, map_density, response, shading="nearest",
                              cmap="cividis", vmin=0, vmax=1)
    axes[2].contour(map_noise, map_density, response, levels=[.5],
                    colors=[CORAL], linewidths=2)
    axes[2].axhline(density, color="white", lw=1.5, ls="--")
    axes[2].axvline(density_noise, color="white", lw=1.5, ls=":")
    axes[2].set_yscale("log")
    axes[2].set(title="Two-parameter response map",
                xlabel=r"Angular-noise width, $\eta$", ylabel=r"Density, $\rho$")
    colourbar = fig.colorbar(mesh, ax=axes[2], pad=.02, fraction=.06)
    colourbar.set_label(r"Mean late-time polarisation, $\Phi$")

    for ax in axes:
        finish_axes(ax)
    fig.savefig(OUT / "vicsek_parameter_sweep_design.svg", transparent=True)
    fig.savefig(OUT / "vicsek_parameter_sweep_design.png", dpi=180, transparent=True)
    plt.close(fig)

    return float(all_noise[np.argmin(np.abs(noise_mean - .5))])


def speed_screen(transition_noise):
    speeds = np.array([.003, .01, .03, .1, .3])
    seeds = np.arange(12) + 303150
    settings = [
        (1.2, "Ordered", BLUE),
        (transition_noise, "Near transition", CORAL),
        (5.2, "Disordered", GREY),
    ]
    density = 2.0
    results = {}
    for eta, label, colour in settings:
        results[label] = (colour, np.asarray([
            ensemble(eta, density, speed, seeds=seeds, steps=500, window=120)
            for speed in speeds
        ]))

    fig, ax = plt.subplots(figsize=(8.4, 4.8), constrained_layout=True)
    for label, (colour, values) in results.items():
        mean, q1, q3 = centre_and_iqr(values)
        ax.plot(speeds, mean, "o-", color=colour, lw=2.3, label=label)
        ax.fill_between(speeds, q1, q3, color=colour, alpha=.18)
    ax.set_xscale("log")
    ax.set(title=rf"Screen speed at fixed density $\rho={density:g}$",
           xlabel=r"Displacement per update, $v\Delta t/R$",
           ylabel=r"Mean late-time polarisation, $\Phi$", ylim=(-.03, 1.03))
    ax.legend(frameon=False, ncol=3, loc="upper center")
    finish_axes(ax)
    fig.savefig(OUT / "vicsek_speed_screen.svg", transparent=True)
    fig.savefig(OUT / "vicsek_speed_screen.png", dpi=180, transparent=True)
    plt.close(fig)


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    speed_screen(sweep_evidence())
