"""Generate the Week 6 coupling--heterogeneity parameter map."""

from __future__ import annotations

import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.patheffects as pe
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from figure_style import INK, ORANGE, apply_course_figure_style  # noqa: E402


OUT = ROOT / "notebooks/week06/images/kuramoto_coupling_heterogeneity_map.svg"
DATA = ROOT / "notebooks/week06/images/kuramoto_coupling_heterogeneity_map.npz"


def simulate_map() -> tuple[np.ndarray, np.ndarray, np.ndarray, dict[str, float | int]]:
    """Return ensemble-mean long-time coherence over (sigma_omega, K)."""
    sigmas = np.linspace(0.2, 1.8, 15)
    couplings = np.linspace(0.4, 4.0, 16)
    n_oscillators = 120
    repeats = 6
    dt = 0.04
    transient_steps = 420
    observation_steps = 160

    rng = np.random.default_rng(302406)
    standard_rates = rng.normal(size=(repeats, n_oscillators))
    initial_phases = rng.uniform(0, 2 * np.pi, size=(repeats, n_oscillators))
    result = np.empty((couplings.size, sigmas.size))

    for sigma_index, sigma in enumerate(sigmas):
        omega = sigma * standard_rates
        for coupling_index, coupling in enumerate(couplings):
            theta = initial_phases.copy()
            accumulated = np.zeros(repeats)
            for step in range(transient_steps + observation_steps):
                order = np.mean(np.exp(1j * theta), axis=1)
                theta += dt * (
                    omega
                    + coupling
                    * np.imag(order[:, None] * np.exp(-1j * theta))
                )
                theta %= 2 * np.pi
                if step >= transient_steps:
                    accumulated += np.abs(np.mean(np.exp(1j * theta), axis=1))
            run_means = accumulated / observation_steps
            result[coupling_index, sigma_index] = np.mean(run_means)

    settings: dict[str, float | int] = {
        "n_oscillators": n_oscillators,
        "repeats": repeats,
        "dt": dt,
        "transient_time": transient_steps * dt,
        "observation_time": observation_steps * dt,
    }
    return sigmas, couplings, result, settings


def make_figure(
    sigmas: np.ndarray,
    couplings: np.ndarray,
    coherence: np.ndarray,
    settings: dict[str, float | int],
) -> None:
    apply_course_figure_style()
    fig, ax = plt.subplots(figsize=(9.4, 5.8), constrained_layout=True)
    mesh = ax.pcolormesh(
        sigmas,
        couplings,
        coherence,
        shading="nearest",
        cmap="cividis",
        vmin=0,
        vmax=1,
        rasterized=True,
    )

    sigma_line = np.linspace(sigmas.min(), sigmas.max(), 300)
    critical_line = np.sqrt(8 / np.pi) * sigma_line
    visible = critical_line <= couplings.max()
    (prediction,) = ax.plot(
        sigma_line[visible],
        critical_line[visible],
        color="white",
        linewidth=2.4,
        linestyle="--",
        label=r"continuum onset: $K_c=\sqrt{8/\pi}\,\sigma_\omega$",
        zorder=3,
    )
    prediction.set_path_effects([pe.Stroke(linewidth=4.2, foreground=INK), pe.Normal()])

    ax.set(
        xlabel=r"Natural-frequency standard deviation, $\sigma_\omega$",
        ylabel=r"Coupling strength, $K$",
        xlim=(sigmas.min() - 0.04, sigmas.max() + 0.04),
        ylim=(couplings.min() - 0.1, couplings.max() + 0.1),
    )
    ax.set_title("Coupling must overcome frequency spread", pad=28)
    ax.text(
        0.5,
        1.025,
        (
            f"ensemble mean from {settings['repeats']} simulations per parameter pair"
            f"  ·  N = {settings['n_oscillators']}  ·  Δt = {settings['dt']}"
        ),
        transform=ax.transAxes,
        ha="center",
        va="bottom",
        fontsize=12.5,
        color=INK,
    )
    ax.legend(loc="upper left", frameon=True, facecolor="white", framealpha=0.92)
    cbar = fig.colorbar(mesh, ax=ax, pad=0.025)
    cbar.set_label(r"Ensemble mean long-time coherence, $r_\infty$")
    cbar.outline.set_edgecolor(INK)
    ax.grid(False)
    ax.spines[["top", "right"]].set_visible(False)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT, transparent=False)
    fig.savefig("/tmp/kuramoto_coupling_heterogeneity_map.png", dpi=160)
    plt.close(fig)


def main() -> None:
    sigmas, couplings, coherence, settings = simulate_map()
    np.savez(
        DATA,
        sigmas=sigmas,
        couplings=couplings,
        coherence=coherence,
        **settings,
    )
    make_figure(sigmas, couplings, coherence, settings)


if __name__ == "__main__":
    main()
