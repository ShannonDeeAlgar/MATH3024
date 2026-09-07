"""Compare Abelian-sandpile avalanche tails across finite lattice sizes."""

from pathlib import Path
import sys

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from figure_style import apply_course_figure_style, finish_axes, BLUE, INK, ORANGE  # noqa: E402
from generate_week08_figures import add_and_relax  # noqa: E402

apply_course_figure_style()


def sample_sizes(L, additions, burn, seed):
    rng = np.random.default_rng(seed)
    pile = np.zeros((L, L), dtype=np.int64)
    values = []
    for step in range(additions):
        size, _, _, _ = add_and_relax(pile, rng)
        if step >= burn and size > 0:
            values.append(size)
    return np.asarray(values)


settings = [(24, 28_000, 6_000), (40, 48_000, 10_000), (64, 82_000, 18_000)]
colours = [BLUE, ORANGE, INK]

fig, ax = plt.subplots(figsize=(8.7, 5.5), constrained_layout=True)
for (L, additions, burn), colour in zip(settings, colours):
    sizes = np.sort(sample_sizes(L, additions, burn, 8000 + L))
    ccdf = (sizes.size - np.arange(sizes.size)) / sizes.size
    ax.loglog(sizes, ccdf, color=colour, lw=2.2,
              label=f"$L={L}$ ({sizes.size:,} non-zero events)")

ax.set(
    xlabel="Avalanche size, $S$ (topplings)",
    ylabel=r"CCDF, $\Pr(S\geq s)$",
    title="Avalanche tails extend as the lattice grows",
)
finish_axes(ax)
ax.legend(frameon=False)
ax.text(0.03, 0.06,
        "Open boundaries; random slow drive; every avalanche finishes before the next grain.",
        transform=ax.transAxes, color=INK, fontsize=10.5)

out = ROOT / "notebooks/week08/images/sandpile_finite_size_ccdf.png"
fig.savefig(out, dpi=210, facecolor="white", bbox_inches="tight")
plt.close(fig)
print(out)
