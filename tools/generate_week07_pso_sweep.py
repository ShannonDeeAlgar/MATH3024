from pathlib import Path
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from figure_style import apply_course_figure_style, finish_axes, INK  # noqa: E402

apply_course_figure_style()


def objective(x):
    x = np.asarray(x)
    dx = x[..., 0] - 1.3
    dy = x[..., 1] + 0.8
    return (
        .035 * (dx * dx + 1.15 * dy * dy)
        + (np.sin(1.15 * dx) + .42 * np.sin(2.05 * dy)) ** 2
        + .65 * (np.sin(.78 * dy) + .38 * np.sin(2.35 * dx + .2 * dy)) ** 2
    )


def run(seed, c1, c2, steps=100, n=28, inertia=.72, vmax=.55):
    rng = np.random.default_rng(seed)
    x = rng.uniform((-6, -5), (6, 5), (n, 2))
    v = rng.normal(0, .28, (n, 2))
    p = x.copy()
    ps = objective(p)
    for _ in range(steps):
        g = p[np.argmin(ps)].copy()
        raw = (inertia * v + c1 * rng.random(x.shape) * (p - x)
               + c2 * rng.random(x.shape) * (g - x))
        speed = np.linalg.norm(raw, axis=1, keepdims=True)
        v = raw * np.minimum(1.0, vmax / np.maximum(speed, 1e-12))
        x = np.clip(x + v, (-6, -5), (6, 5))
        score = objective(x)
        improved = score < ps
        p[improved] = x[improved]
        ps[improved] = score[improved]
    diversity = np.mean(np.linalg.norm(x - x.mean(axis=0), axis=1))
    return ps.min(), diversity


weights = np.array([0, .5, 1, 1.5, 2, 3, 4])
runs = 20
success = np.zeros((len(weights), len(weights)))
diversity = np.zeros_like(success)
for row, personal in enumerate(weights):
    for col, shared in enumerate(weights):
        outcomes = [run(seed, personal, shared) for seed in range(runs)]
        success[row, col] = np.mean([best < 1e-8 for best, _ in outcomes])
        diversity[row, col] = np.median([spread for _, spread in outcomes])

fig, axes = plt.subplots(1, 2, figsize=(13.5, 5.4), constrained_layout=True)
im = axes[0].imshow(success, origin="lower", vmin=0, vmax=1,
                    cmap="Blues", aspect="auto")
axes[0].set(title=f"A  Success within 100 iterations ({runs} runs)",
            xlabel=r"Shared weight, $c_2$", ylabel=r"Personal weight, $c_1$")
fig.colorbar(im, ax=axes[0], label=r"Success fraction, $F$")

im = axes[1].imshow(diversity, origin="lower",
                    cmap="YlGnBu", aspect="auto")
axes[1].set(title="B  Final spread of the particles",
            xlabel=r"Shared weight, $c_2$", ylabel=r"Personal weight, $c_1$")
fig.colorbar(im, ax=axes[1], label=r"Median final diversity, $\mathrm{median}\,D(K)$")

for ax in axes:
    ax.set_xticks(np.arange(len(weights)), labels=[f"{w:g}" for w in weights])
    ax.set_yticks(np.arange(len(weights)), labels=[f"{w:g}" for w in weights])
    finish_axes(ax, grid=False)

fig.suptitle("Search reliability and final convergence", color=INK)
out = ROOT / "notebooks/week07/images/pso_exploration_exploitation_sweep.png"
fig.savefig(out, dpi=180, facecolor="white")
plt.close(fig)
print(out)
