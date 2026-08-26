"""Generate Week 6 figures for controlled Kuramoto heterogeneity experiments."""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

NAVY = "#192B52"
BLUE = "#2C7FB8"
ORANGE = "#E35D34"
GOLD = "#F4C84A"
GRID = "#D9E1EE"


def simulate(omega, coupling, steps=12000, dt=0.02, seed=12):
    rng = np.random.default_rng(seed)
    theta = rng.uniform(-np.pi, np.pi, len(omega))
    tail = []
    for step in range(steps):
        z = np.mean(np.exp(1j * theta))
        theta += dt * (omega + coupling * np.imag(z * np.exp(-1j * theta)))
        if step >= steps - 1000:
            tail.append(theta.copy())
    tail = np.asarray(tail)
    realised = np.mean(np.diff(tail, axis=0), axis=0) / dt
    return theta, realised


def main():
    root = Path(__file__).resolve().parents[1]
    out = root / "notebooks/week06/images"
    rng = np.random.default_rng(8)
    n = 220
    # Work in the laboratory frame.  A mean frequency of 3 makes it clear that
    # frequency locking does not mean that the oscillators stop rotating.
    population_rate = 3.0
    omega = rng.normal(population_rate, 0.65, n)

    # Model specification: show the assigned natural-frequency distribution
    # before interpreting any realised rates from a simulation.
    fig, ax = plt.subplots(figsize=(7.4, 4.2), constrained_layout=True)
    ax.hist(omega, bins=20, color=BLUE, alpha=0.82, edgecolor="white")
    ax.set(
        xlabel=r"natural frequency, $\omega_i$",
        ylabel="number of oscillators",
        title=r"Natural frequencies: $\omega_i\sim\mathcal{N}(3,0.65^2)$",
    )
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(axis="y", color=GRID, lw=0.8)
    fig.savefig(out / "kuramoto_natural_frequency_distribution.svg", transparent=True, bbox_inches="tight")
    plt.close(fig)

    theta, realised = simulate(omega, coupling=1.8)
    order = np.abs(np.mean(np.exp(1j * theta)))
    mean_rate = np.median(realised[np.abs(realised - np.median(realised)) < 0.08])

    plt.rcParams.update({
        "font.family": "DejaVu Sans", "font.size": 13,
        "axes.labelcolor": NAVY, "axes.edgecolor": NAVY,
        "xtick.color": NAVY, "ytick.color": NAVY, "text.color": NAVY,
    })
    fig, axes = plt.subplots(1, 2, figsize=(12.5, 5.4), constrained_layout=True)
    ax = axes[0]
    circle = plt.Circle((0, 0), 1, fill=False, color=NAVY, lw=2.5)
    ax.add_patch(circle)
    sc = ax.scatter(np.cos(theta), np.sin(theta), c=omega, cmap="coolwarm", s=32,
                    edgecolor="white", linewidth=0.35,
                    vmin=population_rate - 1.5, vmax=population_rate + 1.5)
    z = np.mean(np.exp(1j * theta))
    ax.arrow(0, 0, z.real, z.imag, width=0.018, head_width=0.09,
             length_includes_head=True, color=GOLD)
    ax.set(xlim=(-1.18, 1.18), ylim=(-1.18, 1.18), aspect="equal",
           title=f"Phases after coupling ($r={order:.2f}$)")
    ax.axis("off")
    cb = fig.colorbar(sc, ax=ax, fraction=0.047, pad=0.03)
    cb.set_label(r"natural frequency, $\omega_i$")

    ax = axes[1]
    ax.hist(omega, bins=24, color=BLUE, alpha=0.78, edgecolor="white")
    ax.axvline(mean_rate, color=GOLD, lw=3,
               label=rf"common realised frequency $\approx {mean_rate:.2f}$")
    ax.annotate("slower clocks\nare accelerated", xy=(population_rate - 0.55, 17),
                xytext=(population_rate - 1.45, 29),
                arrowprops=dict(arrowstyle="->", color=NAVY), ha="center")
    ax.annotate("faster clocks\nare slowed", xy=(population_rate + 0.55, 17),
                xytext=(population_rate + 1.45, 29),
                arrowprops=dict(arrowstyle="->", color=NAVY), ha="center")
    ax.set(xlabel=r"natural frequency, $\omega_i$", ylabel="number of oscillators",
           title="The population remains heterogeneous")
    ax.legend(frameon=False, loc="upper center", bbox_to_anchor=(0.5, -0.18))
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(axis="y", color=GRID, lw=0.8)
    fig.savefig(out / "kuramoto_frequency_heterogeneity.svg", transparent=True, bbox_inches="tight")
    plt.close(fig)

    # Isolate heterogeneous responsiveness before combining sources of variation.
    # This is a direct finite-population simulation with equal natural frequencies.
    rng = np.random.default_rng(27)
    k_values = np.array([0.25, 0.6, 1.0, 1.8])
    per_group = 40
    k_agents = np.repeat(k_values, per_group)
    theta = rng.uniform(-np.pi, np.pi, len(k_agents))
    dt = 0.025
    steps = 800
    t = np.arange(steps) * dt
    offsets = np.empty((steps, len(k_values)))
    for step in range(steps):
        z = np.mean(np.exp(1j * theta))
        psi = np.angle(z)
        wrapped = np.angle(np.exp(1j * (theta - psi)))
        for group in range(len(k_values)):
            offsets[step, group] = np.mean(np.abs(wrapped[group * per_group:(group + 1) * per_group]))
        theta += dt * k_agents * abs(z) * np.sin(psi - theta)

    fig, ax = plt.subplots(figsize=(9.5, 5.2), constrained_layout=True)
    for group, (k, colour) in enumerate(zip(k_values, plt.cm.viridis(np.linspace(0.15, 0.9, len(k_values))))):
        ax.plot(t, offsets[:, group], color=colour, lw=2.5, label=rf"$K_i={k:g}$")
    ax.axhline(0, color=GRID, lw=1)
    ax.set(xlabel="time", ylabel=r"group mean $|\mathrm{wrap}(\theta_i-\psi)|$",
           title=r"One deterministic simulation: equal $\omega_i$, heterogeneous $K_i$")
    ax.legend(frameon=False, ncol=4, loc="upper center", bbox_to_anchor=(0.5, -0.17))
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(axis="x", color=GRID, lw=0.8)
    fig.savefig(out / "kuramoto_coupling_heterogeneity.svg", transparent=True, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    main()
