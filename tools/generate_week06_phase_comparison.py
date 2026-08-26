"""Generate the Week 6 comparison of uncoupled and coupled phase oscillators."""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


BLUE = "#2C7FB8"
ORANGE = "#F5A300"
NAVY = "#192B52"
GRID = "#D9E1EE"


def simulate_one_way_coupling(t, omega_1, omega_2, coupling):
    theta_1 = np.empty_like(t)
    theta_2 = omega_2 * t
    theta_1[0] = 0.0
    dt = t[1] - t[0]
    for n in range(len(t) - 1):
        theta_1[n + 1] = theta_1[n] + dt * (
            omega_1 + coupling * np.sin(theta_2[n] - theta_1[n])
        )
    return theta_1, theta_2


def add_column(axes, t, theta_1, theta_2, title):
    x_1, x_2 = np.cos(theta_1), np.cos(theta_2)
    # Phase is a circular variable.  Plot the relative phase modulo one turn
    # rather than implying that values such as -15 radians are distinct states.
    phi = np.mod(theta_1 - theta_2, 2 * np.pi)

    axes[0].plot(t, x_1, color=BLUE, lw=1.7, label=r"oscillator 1: $\cos\theta_1$")
    axes[0].plot(t, x_2, color=ORANGE, lw=1.7, label=r"oscillator 2: $\cos\theta_2$")
    axes[0].set_title(title, loc="left", fontweight="bold", pad=58, fontsize=16)
    axes[0].set_ylabel("signal")
    axes[0].legend(
        frameon=True,
        facecolor="white",
        edgecolor="none",
        framealpha=1,
        ncol=2,
        fontsize=12,
        loc="lower center",
        bbox_to_anchor=(0.5, 1.015),
        borderaxespad=0,
    )

    axes[1].plot(t, x_1 + x_2, color=NAVY, lw=1.8)
    axes[1].axhline(0, color=GRID, lw=1)
    axes[1].set_ylabel("sum")

    axes[2].plot(t, phi, color=NAVY, lw=1.8)
    axes[2].set_ylabel(r"$\phi=(\theta_1-\theta_2)\;\mathrm{mod}\;2\pi$")
    axes[2].set_yticks([0, np.pi, 2 * np.pi], ["0", r"$\pi$", r"$2\pi$"])
    axes[2].set_ylim(-0.12, 2 * np.pi + 0.12)
    axes[2].set_xlabel("time")

    for ax in axes:
        ax.spines[["top", "right"]].set_visible(False)
        ax.grid(axis="x", color=GRID, lw=0.7, alpha=0.8)


def main():
    # A longer interval shows more than two complete beat envelopes.
    t = np.linspace(0, 130, 13001)
    omega_1, omega_2 = 1.0, 1.12

    uncoupled_1 = omega_1 * t
    uncoupled_2 = omega_2 * t
    coupled_1, coupled_2 = simulate_one_way_coupling(t, omega_1, omega_2, 0.30)

    plt.rcParams.update({
        "font.family": "DejaVu Sans",
        "font.size": 14,
        "axes.labelcolor": NAVY,
        "axes.edgecolor": NAVY,
        "xtick.color": NAVY,
        "ytick.color": NAVY,
        "text.color": NAVY,
    })
    fig, ax = plt.subplots(3, 2, figsize=(14, 8), sharex="col", constrained_layout=True)
    add_column(ax[:, 0], t, uncoupled_1, uncoupled_2, "Uncoupled: nearby frequencies create beats")
    add_column(ax[:, 1], t, coupled_1, coupled_2, "Coupled: oscillator 1 is recruited into phase locking")
    fig.suptitle("The same two oscillators, viewed three ways", fontsize=18, fontweight="bold")

    output = Path(__file__).resolve().parents[1] / "notebooks/week06/images/phase_signal_comparison.svg"
    fig.savefig(output, transparent=True, bbox_inches="tight")
    plt.close(fig)

    for stem, title, theta_1, theta_2 in (
        ("phase_signals_uncoupled", "Uncoupled: nearby frequencies create beats", uncoupled_1, uncoupled_2),
        ("phase_signals_coupled", "Coupled: oscillator 1 is recruited into phase locking", coupled_1, coupled_2),
    ):
        fig, axes = plt.subplots(3, 1, figsize=(11.5, 7.2), sharex=True, constrained_layout=True)
        add_column(axes, t, theta_1, theta_2, title)
        fig.savefig(output.with_name(f"{stem}.svg"), transparent=True, bbox_inches="tight")
        plt.close(fig)


if __name__ == "__main__":
    main()
