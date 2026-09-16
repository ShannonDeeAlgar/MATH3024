"""Generate the exact six-site visual used to define pair-connectedness."""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

from figure_style import BLUE, GREY, INK, ORANGE, apply_course_figure_style


apply_course_figure_style()
output_dir = Path(__file__).resolve().parents[1] / "notebooks/week08/images"

names = list("ABCDEF")
cluster_labels = [1, 1, 0, 2, 2, 2]
colours = {0: GREY, 1: BLUE, 2: ORANGE}
pairs = [("A", "C", 0), ("B", "D", 0), ("C", "E", 0), ("D", "F", 1)]

fig = plt.figure(figsize=(12.5, 5.6), layout="constrained")
grid = fig.add_gridspec(2, 1, height_ratios=(1.05, 1.45))

ax_sites = fig.add_subplot(grid[0])
ax_sites.set(xlim=(-0.55, 5.55), ylim=(-0.75, 0.8))
ax_sites.axis("off")
ax_sites.set_title("Cluster labels identify connectivity", pad=3)
ax_sites.plot([0, 1], [0, 0], color=BLUE, linewidth=7, alpha=0.32, zorder=0)
ax_sites.plot([3, 5], [0, 0], color=ORANGE, linewidth=7, alpha=0.32, zorder=0)
for index, (name, label) in enumerate(zip(names, cluster_labels)):
    ax_sites.scatter(
        index,
        0,
        s=880,
        marker="s",
        facecolor=colours[label],
        edgecolor=INK,
        linewidth=1.5,
        zorder=2,
    )
    ax_sites.text(index, 0.47, name, ha="center", va="center", fontsize=17)
    description = "blocked" if label == 0 else f"cluster label ℓ = {label}"
    ax_sites.text(index, -0.53, description, ha="center", va="center", fontsize=13)

ax_pairs = fig.add_subplot(grid[1])
ax_pairs.set(xlim=(0, 9.8), ylim=(-1.35, 2.0))
ax_pairs.axis("off")
ax_pairs.set_title("At separation r = 2, examine each unordered pair", pad=6, fontsize=17)

for column, (left, right, connected) in enumerate(pairs):
    x0 = 0.25 + 2.35 * column
    card = FancyBboxPatch(
        (x0, 0.14),
        2.0,
        1.17,
        boxstyle="round,pad=0.08,rounding_size=0.08",
        facecolor="#F3F6FA",
        edgecolor="#C7CEDC",
        linewidth=1.2,
    )
    ax_pairs.add_patch(card)
    ax_pairs.text(x0 + 1.0, 1.58, f"{left}–{right}", ha="center", fontsize=15)
    ax_pairs.text(x0 + 1.0, 0.83, "same positive label?", ha="center", fontsize=13)
    ax_pairs.text(
        x0 + 1.0,
        0.42,
        "1  yes" if connected else "0  no",
        ha="center",
        fontsize=14,
        color="#16806A" if connected else INK,
        fontweight="bold" if connected else "normal",
    )

ax_pairs.text(
    4.9,
    -0.76,
    r"$C(2)=\dfrac{0+0+0+1}{4}=\dfrac{1}{4}$",
    ha="center",
    va="center",
    fontsize=19,
    color=INK,
)

for extension in ("svg", "png"):
    fig.savefig(output_dir / f"percolation_pair_connectedness.{extension}", dpi=170)
plt.close(fig)

print("Verified: four unordered pairs at r=2; one shares a positive cluster label.")
