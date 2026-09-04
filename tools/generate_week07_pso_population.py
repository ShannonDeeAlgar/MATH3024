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


def run(seed, n, evaluation_budget=3000, inertia=.72, personal=1.3,
        shared=1.3, max_move=.55):
    """Run global-best PSO with approximately the same evaluation budget."""
    rng = np.random.default_rng(seed)
    x = rng.uniform((-6, -5), (6, 5), (n, 2))
    v = rng.normal(0, .28, (n, 2))
    p = x.copy()
    ps = objective(p)
    # Initial positions are objective evaluations too. Reserve their cost before
    # deciding how many complete swarm updates fit within the budget.
    steps = max(0, evaluation_budget // n - 1)
    for _ in range(steps):
        g = p[np.argmin(ps)].copy()
        raw = (inertia * v
               + personal * rng.random(x.shape) * (p - x)
               + shared * rng.random(x.shape) * (g - x))
        speed = np.linalg.norm(raw, axis=1, keepdims=True)
        v = raw * np.minimum(1.0, max_move / np.maximum(speed, 1e-12))
        x = np.clip(x + v, (-6, -5), (6, 5))
        score = objective(x)
        improved = score < ps
        p[improved] = x[improved]
        ps[improved] = score[improved]
    return ps.min(), steps


sizes = np.array([1, 3, 8, 15, 30, 60])
runs = 30
budget = 3000
final = np.zeros((len(sizes), runs))
steps = []
for row, n in enumerate(sizes):
    for seed in range(runs):
        final[row, seed], n_steps = run(seed, int(n), budget)
    steps.append(n_steps)

success = np.mean(final < 1e-8, axis=1)
median = np.median(final, axis=1)
q25, q75 = np.quantile(final, [.25, .75], axis=1)

fig, axes = plt.subplots(1, 2, figsize=(12.5, 4.8), constrained_layout=True)
axes[0].plot(sizes, success, marker="o", color=INK, lw=2.2)
axes[0].set(xlabel="Number of particles, $N$", ylabel=r"Success fraction, $F$",
            ylim=(-.03, 1.03), title="Reliability")
finish_axes(axes[0])

axes[1].plot(sizes, np.maximum(median, 1e-12), marker="o", color=ORANGE, lw=2.2,
             label="median")
axes[1].fill_between(sizes, np.maximum(q25, 1e-12), np.maximum(q75, 1e-12),
                     color=BLUE, alpha=.16, label="middle 50%")
axes[1].axhline(1e-8, color=INK, ls="--", lw=1.5, label="success target")
axes[1].set_yscale("log")
axes[1].set(xlabel="Number of particles, $N$", ylabel=r"Final best objective, $f_{\rm best}(K)$",
            title="Ensemble outcome")
axes[1].legend(frameon=False)
finish_axes(axes[1])

fig.suptitle(rf"Population size at fixed evaluation budget, $E_{{\max}}={budget}$" "\n"
             f"{runs} seeded runs per population size", color=INK)
fig.text(.5, -.01,
         "A larger swarm samples more positions per iteration but therefore receives fewer iterations at fixed cost.",
         ha="center", color=INK, fontsize=11)
out = ROOT / "notebooks/week07/images/pso_population_size_sweep.png"
fig.savefig(out, dpi=180, facecolor="white", bbox_inches="tight")
plt.close(fig)
print(out)
