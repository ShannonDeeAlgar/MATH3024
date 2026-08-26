"""Generate the Week 6 synchronisation taxonomy in the unit style."""

from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "notebooks/week06/images/synchronisation_types.svg"
PANEL_DIR = ROOT / "notebooks/week06/images/synchronisation_types"
NAVY = "#192B52"
BLUE = "#3F8FC5"
ORANGE = "#E7653B"
PALE = "#DCE7F3"

t = np.linspace(0, 8 * np.pi, 500)
cases = [
    ("In phase", np.vstack([t, t])),
    ("Anti-phase", np.vstack([t, t + np.pi])),
    ("Phase locked", np.vstack([t, t + 0.75])),
    ("Frequency entrained", np.vstack([t + 0.18*np.sin(.35*t), t + .9 - .18*np.sin(.35*t)])),
    ("Two clusters", np.vstack([t, t+.12, t+np.pi, t+np.pi+.12])),
    ("Partial synchrony", np.vstack([t, t+.15, t-.12, 1.25*t+1.3])),
    ("Chimera-like", np.vstack([t, t+.08, t-.1, t+.16, .72*t+.3, 1.22*t+1.0, .9*t+2.2, 1.38*t+.5])),
]

PANEL_DIR.mkdir(parents=True, exist_ok=True)


def draw_case(name, theta, output):
    """Write one compact phase-circle/time-series pair for inline definitions."""
    panel = plt.figure(figsize=(5.2, 2.15), facecolor="white")
    grid = panel.add_gridspec(1, 2, width_ratios=[1, 1.85], wspace=.22)
    axc = panel.add_subplot(grid[0, 0], projection="polar")
    axt = panel.add_subplot(grid[0, 1])
    colors = [BLUE, ORANGE, "#79B7D9", "#8C5AA5", "#43AA8B", "#D99A2B", "#BF5B78", "#567D46"]
    for j in range(theta.shape[0]):
        axc.scatter(theta[j, -1] % (2*np.pi), 1, s=48,
                    color=colors[j % len(colors)], edgecolor="white",
                    linewidth=.5, zorder=3)
        axt.plot(t/(2*np.pi), np.cos(theta[j]),
                 color=colors[j % len(colors)], lw=1.55, alpha=.9)
    axc.set_ylim(0, 1.08)
    axc.set_xticks([]); axc.set_yticks([])
    axc.spines["polar"].set_color(NAVY); axc.spines["polar"].set_linewidth(1.3)
    axc.grid(False)
    axt.set_xlim(0, 4); axt.set_ylim(-1.1, 1.1)
    axt.set_xticks([0, 2, 4]); axt.set_yticks([-1, 0, 1])
    axt.tick_params(labelsize=8, colors=NAVY, length=2)
    axt.grid(color=PALE, lw=.7)
    for spine in ("top", "right"):
        axt.spines[spine].set_visible(False)
    axt.spines["left"].set_color(NAVY); axt.spines["bottom"].set_color(NAVY)
    axt.set_xlabel("time", fontsize=8, color=NAVY)
    panel.savefig(output, bbox_inches="tight", pad_inches=.08)
    plt.close(panel)


for slug, (name, theta) in zip(
    ["in_phase", "anti_phase", "phase_locked", "frequency_entrained",
     "two_clusters", "partial_synchrony", "chimera_like"],
    cases,
):
    draw_case(name, theta, PANEL_DIR / f"{slug}.svg")

fig = plt.figure(figsize=(14, 6.25), facecolor="white")
outer = fig.add_gridspec(2, 4, wspace=.35, hspace=.55)

for idx, (name, theta) in enumerate(cases):
    cell = outer[idx // 4, idx % 4].subgridspec(1, 2, width_ratios=[1, 1.7], wspace=.20)
    axc = fig.add_subplot(cell[0, 0], projection="polar")
    axt = fig.add_subplot(cell[0, 1])
    colors = [BLUE, ORANGE, "#79B7D9", "#8C5AA5", "#43AA8B", "#D99A2B", "#BF5B78", "#567D46"]
    for j in range(theta.shape[0]):
        axc.scatter(theta[j, -1] % (2*np.pi), 1, s=38, color=colors[j % len(colors)], edgecolor="white", linewidth=.5, zorder=3)
        axt.plot(t/(2*np.pi), np.cos(theta[j]), color=colors[j % len(colors)], lw=1.35, alpha=.9)
    axc.set_ylim(0, 1.08)
    axc.set_xticks([]); axc.set_yticks([])
    axc.spines["polar"].set_color(NAVY); axc.spines["polar"].set_linewidth(1.3)
    axc.grid(False)
    axt.set_xlim(0, 4); axt.set_ylim(-1.1, 1.1)
    # A short trace panel reads as a time series and visually matches the
    # compact phase circle; the previous near-square panel was too tall.
    axt.set_box_aspect(.46)
    axt.set_xticks([0, 2, 4]); axt.set_yticks([-1, 0, 1])
    axt.tick_params(labelsize=7, colors=NAVY, length=2)
    axt.grid(color=PALE, lw=.7)
    for spine in ("top", "right"):
        axt.spines[spine].set_visible(False)
    axt.spines["left"].set_color(NAVY); axt.spines["bottom"].set_color(NAVY)
    axt.set_title(name, fontsize=12, color=NAVY, fontweight="semibold", pad=7)
    if idx // 4 == 1:
        axt.set_xlabel("time", fontsize=8, color=NAVY)
    # The meaning of the traces is stated in the key; repeated y labels crowd
    # the adjoining phase circles.

ax = fig.add_subplot(outer[1, 3]); ax.axis("off")
ax.text(.02, .72, "Circle", color=NAVY, fontsize=12, fontweight="semibold")
ax.text(.02, .58, "phase-space snapshot", color=NAVY, fontsize=11)
ax.text(.02, .35, "Traces", color=NAVY, fontsize=12, fontweight="semibold")
ax.text(.02, .21, r"observable $y_i(t)=\cos\theta_i(t)$", color=NAVY, fontsize=11)

fig.savefig(OUT, bbox_inches="tight", pad_inches=.16)
plt.close(fig)
