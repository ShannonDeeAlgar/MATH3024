"""Generate the Week 6 animation of natural-frequency heterogeneity."""

from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
import numpy as np


NAVY = "#192B52"
ORANGE = "#E35D34"
BLUE = "#2C7FB8"
GRID = "#D9E1EE"


def main():
    rng = np.random.default_rng(3024)
    n = 72
    # Use a non-zero laboratory-frame mean so a locked group visibly keeps rotating.
    # Subtracting this mean would give the equivalent co-rotating-frame description.
    population_rate = 3.0
    omega = np.sort(rng.normal(population_rate, 1.0, n))
    theta = rng.uniform(0, 2 * np.pi, n)
    coupling = 3.2
    dt = 0.0125
    frames = []

    for step in range(3200):
        z = np.mean(np.exp(1j * theta))
        r, psi = abs(z), np.angle(z)
        theta += dt * (omega + coupling * r * np.sin(psi - theta))
        # Store frames often enough that the common rotation is visually
        # continuous. Sampling every 80 steps advanced the locked group by
        # almost pi between frames and made smooth motion look like a flip.
        if step % 20 == 0:
            z_now = np.mean(np.exp(1j * theta))
            r_now, psi_now = abs(z_now), np.angle(z_now)
            realised = omega + coupling * r_now * np.sin(psi_now - theta)
            frames.append((theta.copy(), r_now, psi_now, realised.copy()))

    plt.rcParams.update({
        "font.family": "DejaVu Sans",
        "font.size": 13,
        "text.color": NAVY,
        "axes.labelcolor": NAVY,
        "axes.edgecolor": NAVY,
        "xtick.color": NAVY,
        "ytick.color": NAVY,
    })
    fig = plt.figure(figsize=(10.8, 5.2), constrained_layout=True)
    gs = fig.add_gridspec(1, 2, width_ratios=(1.0, 1.25))
    ax_circle = fig.add_subplot(gs[0, 0])
    ax_hist = fig.add_subplot(gs[0, 1])

    colours = plt.cm.coolwarm((omega - omega.min()) / np.ptp(omega))
    bins = np.linspace(omega.min() - 0.1, omega.max() + 0.1, 14)
    ax_hist.hist(omega, bins=bins, color=BLUE, alpha=0.78, edgecolor="white")
    common_rate = float(np.mean(omega))
    ax_hist.axvline(common_rate, color=ORANGE, lw=3, ls="--",
                    label=f"common realised frequency ≈ {common_rate:.1f}")
    ax_hist.annotate("slower clocks\nspeed up", xy=(common_rate - 0.05, 7.0), xytext=(omega.min() + 0.1, 9.5),
                     arrowprops=dict(arrowstyle="->", color=NAVY), color=NAVY, ha="left")
    ax_hist.annotate("faster clocks\nslow down", xy=(common_rate + 0.05, 7.0), xytext=(omega.max() - 0.1, 9.5),
                     arrowprops=dict(arrowstyle="->", color=NAVY), color=NAVY, ha="right")
    ax_hist.set(xlabel=r"natural frequency, $\omega_i$", ylabel="number of oscillators", title="Different internal clocks")
    ax_hist.legend(loc="upper center", bbox_to_anchor=(0.5, -0.18), frameon=False)
    ax_hist.spines[["top", "right"]].set_visible(False)
    ax_hist.grid(axis="y", color=GRID, alpha=0.7)

    circle = plt.Circle((0, 0), 1, fill=False, lw=3, color=NAVY)
    ax_circle.add_patch(circle)
    initial_phases = frames[0][0]
    points = ax_circle.scatter(
        np.cos(initial_phases), np.sin(initial_phases), s=52, c=colours,
        edgecolor="white", linewidth=0.5, zorder=3
    )
    mean_line, = ax_circle.plot([], [], color=ORANGE, lw=5)
    status = ax_circle.text(0, -1.26, "", ha="center", fontsize=13)
    ax_circle.set(xlim=(-1.18, 1.18), ylim=(-1.38, 1.18), aspect="equal", title="Phases coloured by natural frequency")
    ax_circle.axis("off")

    def update(frame):
        phases, r, psi, realised = frame
        points.set_offsets(np.column_stack((np.cos(phases), np.sin(phases))))
        mean_line.set_data([0, r * np.cos(psi)], [0, r * np.sin(psi)])
        status.set_text(
            rf"coherence $r={r:.2f}$; common realised frequency ≈ {np.mean(realised):.2f}"
        )
        return points, mean_line, status

    animation = FuncAnimation(fig, update, frames=frames, interval=85, blit=True)
    output = Path(__file__).resolve().parents[1] / "notebooks/week06/images/kuramoto_frequency_heterogeneity.gif"
    # Five frames per second gives enough time to follow recruitment into the group.
    animation.save(output, writer=PillowWriter(fps=12), dpi=82)
    plt.close(fig)


if __name__ == "__main__":
    main()
