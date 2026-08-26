"""Generate the Week 6 natural-versus-realised frequency figure."""

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from figure_style import BLUE, GREY, INK, YELLOW, apply_course_figure_style, finish_axes

rng = np.random.default_rng(3024)
n, coupling, dt, steps = 120, 1.15, 0.035, 2400
omega = rng.normal(3.0, 0.48, n)
theta = rng.uniform(0, 2 * np.pi, n)
unwrapped = np.empty((steps, n))
raw = theta.copy()
for step in range(steps):
    unwrapped[step] = raw
    phase = raw % (2 * np.pi)
    z = np.mean(np.exp(1j * phase))
    raw += dt * (omega + coupling * np.imag(z * np.exp(-1j * phase)))

mid = steps // 2
realised = (unwrapped[-1] - unwrapped[mid]) / ((steps - 1 - mid) * dt)
group_rate = float(np.median(realised))
locked = np.abs(realised - group_rate) < 0.06

apply_course_figure_style()
fig, ax = plt.subplots(figsize=(9.2, 5.2), constrained_layout=True)
bounds = [float(omega.min()) - 0.15, float(omega.max()) + 0.15]
ax.plot(bounds, bounds, color=GREY, lw=2,
        label=r"without coupling: $\omega_i^\infty=\omega_i$")
ax.axhline(group_rate, color=INK, ls="--", lw=2,
           label=rf"locked-group rate $\Omega\approx{group_rate:.2f}$")
ax.scatter(omega[~locked], realised[~locked], s=105, color=YELLOW, edgecolor=INK,
           linewidth=1.5, zorder=4, label="drifting oscillator")
ax.scatter(omega[locked], realised[locked], s=55, color=BLUE, edgecolor="white",
           label="frequency-locked oscillators")
ax.set(xlabel=r"Natural frequency, $\omega_i$",
       ylabel=r"Realised long-time frequency, $\omega_i^\infty$")
finish_axes(ax)
ax.legend(frameon=False, loc="upper left", ncol=1,
          handlelength=2.4, labelspacing=0.45)
if (~locked).any():
    index = np.flatnonzero(~locked)[0]
    ax.annotate(
        "continues to drift",
        (omega[index], realised[index]),
        xytext=(-80, -36),
        textcoords="offset points",
        arrowprops={"arrowstyle": "->", "color": INK, "lw": 1.2},
        ha="right",
        va="top",
    )
ax.text(0.98, 0.04, rf"$N={n}$, $K={coupling}$", transform=ax.transAxes,
        ha="right", va="bottom")
out = Path(__file__).resolve().parents[1] / "notebooks/week06/images/kuramoto_realised_frequency_drifter.svg"
fig.savefig(out, transparent=True, bbox_inches="tight")
