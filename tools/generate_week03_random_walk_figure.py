from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


root = Path(__file__).resolve().parents[1]
out = root / "notebooks/week03/images/random_walk_types_stats.svg"
rng = np.random.default_rng(3024)
n = 45

fig, axes = plt.subplots(1, 3, figsize=(11.4, 3.45), constrained_layout=True)
navy = "#1b2a4c"
blue = "#2878a8"
orange = "#c65b17"

# All three walks choose from the same eight unit vectors. Only the rule for
# choosing a direction changes. Store the paths so every panel can use the
# same spatial scale.
walks = []
direction_angles = np.arange(8) * np.pi / 4
unit_vectors = np.column_stack((np.cos(direction_angles), np.sin(direction_angles)))

# Unbiased walk: every direction is equally likely and successive choices are
# independent.
dirs = rng.integers(0, 8, n)
steps = unit_vectors[dirs]
walk = np.vstack(([0, 0], np.cumsum(steps, axis=0)))
walks.append(walk)
axes[0].plot(walk[:, 0], walk[:, 1], color=navy, lw=1.45, marker="o", ms=3.6,
             markerfacecolor="white", markeredgewidth=0.75)
axes[0].set_title("Unbiased · 45 unit steps")
axes[0].text(0.03, 0.04, "independent directions\nzero mean step", transform=axes[0].transAxes)

# Biased walk: the same directions and step length, but eastward directions
# receive more probability.
weights = np.exp(1.2 * np.cos(direction_angles))
weights /= weights.sum()
dirs = rng.choice(8, size=n, p=weights)
steps = unit_vectors[dirs]
walk = np.vstack(([0, 0], np.cumsum(steps, axis=0)))
walks.append(walk)
axes[1].plot(walk[:, 0], walk[:, 1], color=orange, lw=1.45, marker="o", ms=3.6,
             markerfacecolor="white", markeredgewidth=0.75)
axes[1].set_title("Biased · 45 unit steps")
axes[1].text(0.03, 0.04, "non-zero mean step\nmean displacement grows", transform=axes[1].transAxes)

# Persistent walk: retain the previous direction most of the time; otherwise
# turn by one eighth-turn left or right. Step length remains one.
dirs = np.empty(n, dtype=int)
dirs[0] = 0
for i in range(1, n):
    dirs[i] = (dirs[i - 1] + rng.choice([-1, 0, 1], p=[0.17, 0.66, 0.17])) % 8
steps = unit_vectors[dirs]
walk = np.vstack(([0, 0], np.cumsum(steps, axis=0)))
walks.append(walk)
axes[2].plot(walk[:, 0], walk[:, 1], color=blue, lw=1.6, marker="o", ms=3.6,
             markerfacecolor="white", markeredgewidth=0.75)
axes[2].set_title("Persistent · 45 unit steps")
axes[2].text(0.03, 0.04, "correlated directions\nturning angles carry memory", transform=axes[2].transAxes)

all_points = np.vstack(walks)
xmin, ymin = all_points.min(axis=0)
xmax, ymax = all_points.max(axis=0)
span = max(xmax - xmin, ymax - ymin)
cx, cy = (xmin + xmax) / 2, (ymin + ymax) / 2
pad = 0.08 * span

for ax, path in zip(axes, walks):
    ax.scatter(path[0, 0], path[0, 1], s=36, color=navy, zorder=3)
    ax.set_xlim(cx - span / 2 - pad, cx + span / 2 + pad)
    ax.set_ylim(cy - span / 2 - pad, cy + span / 2 + pad)
    ax.set_aspect("equal", adjustable="box")
    ax.set_xticks(np.arange(np.floor(cx - span / 2), np.ceil(cx + span / 2) + 1, 5))
    ax.set_yticks(np.arange(np.floor(cy - span / 2), np.ceil(cy + span / 2) + 1, 5))
    ax.tick_params(labelsize=7, colors="#72809a", length=2)
    ax.grid(color="#dfe5ef", linewidth=0.6, alpha=0.8)
    ax.plot([0.07, 0.17], [0.91, 0.91], transform=ax.transAxes, color="#4f607f", lw=2)
    ax.text(0.12, 0.84, "one unit step", ha="center", transform=ax.transAxes, fontsize=8, color="#4f607f")
    # Revisited locations can hide several steps. Number common checkpoints so
    # the equal step count remains visible even where the path retraces itself.
    for checkpoint in (0, 10, 20, 30, 40, 45):
        ax.scatter(path[checkpoint, 0], path[checkpoint, 1], s=18, color="white",
                   edgecolor=navy, linewidth=0.7, zorder=4)
        ax.annotate(str(checkpoint), path[checkpoint], xytext=(3, 3),
                    textcoords="offset points", fontsize=6.5, color=navy,
                    zorder=5)
    for spine in ax.spines.values():
        spine.set_color("#bcc8dc")
    ax.title.set_color(navy)

fig.patch.set_alpha(0)
for ax in axes:
    ax.set_facecolor("none")
fig.savefig(out, transparent=True, bbox_inches="tight")
print(out)
