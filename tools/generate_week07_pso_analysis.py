from pathlib import Path
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from figure_style import apply_course_figure_style, finish_axes, BLUE, INK, ORANGE  # noqa: E402

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


def initialise(rng, n=28):
    x = rng.uniform((-6, -5), (6, 5), (n, 2))
    v = rng.normal(0, 0.28, (n, 2))
    p = x.copy()
    ps = objective(p)
    return x, v, p, ps


def components(state, rng, w=.72, c1=1.3, c2=1.3):
    x, v, p, ps = state
    g = p[np.argmin(ps)].copy()
    retained = w * v
    personal = c1 * rng.random(x.shape) * (p - x)
    shared = c2 * rng.random(x.shape) * (g - x)
    return retained, personal, shared


def step(state, rng, vmax=.55):
    x, v, p, ps = state
    retained, personal, shared = components(state, rng)
    raw = retained + personal + shared
    norm = np.linalg.norm(raw, axis=1, keepdims=True)
    scale = np.minimum(1.0, vmax / np.maximum(norm, 1e-12))
    v = raw * scale
    x = np.clip(x + v, (-6, -5), (6, 5))
    score = objective(x)
    improved = score < ps
    p = p.copy(); ps = ps.copy()
    p[improved] = x[improved]; ps[improved] = score[improved]
    return x, v, p, ps


def run(seed, steps=100):
    rng = np.random.default_rng(seed)
    state = initialise(rng)
    best, diversity = [], []
    for _ in range(steps):
        state = step(state, rng)
        best.append(state[3].min())
        diversity.append(np.mean(np.linalg.norm(state[0] - state[0].mean(0), axis=1)))
    return state, np.asarray(best), np.asarray(diversity)


fig, axes = plt.subplots(1, 3, figsize=(17, 5.5), constrained_layout=True)

# A--B: one run.
_, best, diversity = run(6)
ax = axes[0]
ax.semilogy(np.arange(1, 101), best, color=INK, lw=2.4)
ax.axhline(1e-8, color=ORANGE, ls="--", label="success target")
ax.set(xlabel=r"Iteration, $n$", ylabel=r"Best objective, $f_{\rm best}(n)$", title="A  One swarm: progress")
ax.legend(frameon=False)
finish_axes(ax)

ax = axes[1]
ax.plot(np.arange(1, 101), diversity, color=ORANGE, lw=2.4)
ax.set(xlabel=r"Iteration, $n$", ylabel=r"Swarm diversity, $D(n)$",
       title="B  One swarm: diversity")
finish_axes(ax)

# C: repeated runs summarised as an ensemble, rather than ranked one by one.
final = np.asarray([run(seed)[1][-1] for seed in range(40)])
successes = int(np.sum(final < 1e-8))
ax = axes[2]
safe = np.maximum(final, 1e-12)
ax.boxplot(safe, vert=True, widths=.34, patch_artist=True,
           boxprops=dict(facecolor="#d9eaf4", edgecolor=INK),
           medianprops=dict(color=ORANGE, linewidth=2.4),
           whiskerprops=dict(color=INK), capprops=dict(color=INK),
           flierprops=dict(marker="o", markerfacecolor=BLUE, markeredgecolor=INK))
ax.axhline(1e-8, color=ORANGE, ls="--")
ax.set_yscale("log")
ax.set_xticks([1], ["40 seeded runs"])
ax.set(ylabel=r"Final best objective, $f_{\rm best}(K)$",
       title=f"C  Ensemble: {successes}/40 reached the target")
ax.annotate("success target", xy=(1.46, 1e-8), xytext=(0, -5),
            textcoords="offset points", ha="right", va="top", color=INK)
finish_axes(ax)

out = ROOT / "notebooks/week07/images/pso_analysis_levels.png"
fig.savefig(out, dpi=180, facecolor="white")
plt.close(fig)
print(out)
