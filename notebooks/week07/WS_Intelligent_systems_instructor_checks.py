"""Instructor checks and reference analysis for the Week 7 PSO workshop.

Run this file from any working directory. It loads the implementation directly
from the student notebook, so the checks exercise the version students receive.

%run WS_Intelligent_systems_instructor_checks.py

"""

from pathlib import Path
import json

import matplotlib.pyplot as plt
from matplotlib import animation
import numpy as np
from IPython.display import HTML, display


HERE = Path(__file__).resolve().parent
NOTEBOOK = HERE / "WS_Intelligent_systems.ipynb"


def load_workshop_code():
    notebook = json.loads(NOTEBOOK.read_text())
    namespace = {}
    required_cells = [
        "week07-pso-imports-objective",
        "week07-pso-engine",
        "week07-ensemble-helper",
    ]
    for cell_id in required_cells:
        cell = next(cell for cell in notebook["cells"] if cell.get("id") == cell_id)
        exec("".join(cell["source"]), namespace)
    return namespace


workshop = load_workshop_code()
objective_landscape = workshop["objective_landscape"]
initialise_swarm = workshop["initialise_swarm"]
pso_step = workshop["pso_step"]
run_pso = workshop["run_pso"]
run_ensemble = workshop["run_ensemble"]


# ---------------------------------------------------------------------------
# Reference answer for "Establish that the baseline is valid"
# ---------------------------------------------------------------------------

known_minimum = np.array([1.3, -0.8])
assert np.isclose(objective_landscape(known_minimum), 0.0)

# The objective is a sum of non-negative terms, so zero is a global minimum.
rng = np.random.default_rng(3024)
sample = rng.uniform([-6.0, -5.0], [6.0, 5.0], size=(100_000, 2))
assert np.all(objective_landscape(sample) >= 0.0)

run_a = run_pso(seed=19, steps=40)
run_b = run_pso(seed=19, steps=40)
for key in ("positions", "best_scores", "diversity", "personal_best"):
    assert np.array_equal(run_a[key], run_b[key])

lower = np.array([-6.0, -5.0])
upper = np.array([6.0, 5.0])
assert np.all(run_a["positions"] >= lower)
assert np.all(run_a["positions"] <= upper)

# A controlled update checks that an improvement is retained and a worse visit
# does not replace the previous record.
def sphere(x):
    return np.sum(np.asarray(x, dtype=float) ** 2, axis=-1)


positions = np.array([[2.0, 0.0], [0.0, 0.0]])
velocities = np.array([[-1.0, 0.0], [1.0, 0.0]])
personal_best = positions.copy()
personal_scores = sphere(personal_best)

_, _, new_best, new_scores, visited_scores = pso_step(
    positions,
    velocities,
    personal_best,
    personal_scores,
    objective=sphere,
    bounds=((-3.0, -3.0), (3.0, 3.0)),
    rng=np.random.default_rng(5),
    inertia=1.0,
    personal_weight=0.0,
    shared_weight=0.0,
)
assert visited_scores[0] < personal_scores[0]
assert np.array_equal(new_best[0], np.array([1.0, 0.0]))
assert new_scores[0] == 1.0
assert visited_scores[1] > personal_scores[1]
assert np.array_equal(new_best[1], np.array([0.0, 0.0]))
assert new_scores[1] == 0.0

n_particles = 17
n_updates = 23
counted_run = run_pso(n_particles=n_particles, steps=n_updates, seed=8)
assert counted_run["objective_evaluations"] == n_particles * (n_updates + 1)

print("All five workshop validation checks passed.")


# ---------------------------------------------------------------------------
# Full reference animation
# ---------------------------------------------------------------------------

def animate_pso_run(run, objective, bounds=((-6.0, -5.0), (6.0, 5.0)),
                    interval=90):
    """Animate the swarm together with the two quantities tracked by run_pso."""
    positions = run["positions"]
    best_scores = run["best_scores"]
    diversity = run["diversity"]
    iterations = np.arange(len(positions))
    best_position_history = []
    best_position = None
    best_value = np.inf
    for frame_positions in positions:
        frame_scores = objective(frame_positions)
        frame_index = int(np.argmin(frame_scores))
        if frame_scores[frame_index] < best_value:
            best_value = float(frame_scores[frame_index])
            best_position = frame_positions[frame_index].copy()
        best_position_history.append(best_position.copy())
    best_position_history = np.asarray(best_position_history)

    x_grid = np.linspace(bounds[0][0], bounds[1][0], 220)
    y_grid = np.linspace(bounds[0][1], bounds[1][1], 190)
    xx, yy = np.meshgrid(x_grid, y_grid)
    zz = objective(np.stack([xx, yy], axis=-1))

    fig, axes = plt.subplots(
        1, 3, figsize=(13.2, 4.2),
        gridspec_kw={"width_ratios": [1.2, 1.0, 1.0]},
    )
    landscape_ax, score_ax, diversity_ax = axes

    landscape_ax.contourf(xx, yy, zz, levels=32, cmap="viridis_r")
    particles = landscape_ax.scatter([], [], s=28, color="#F4C542",
                                     edgecolor="#1B2A4C", linewidth=0.5)
    current_best = landscape_ax.scatter([], [], marker="*", s=150,
                                        color="#DF6338", edgecolor="white",
                                        linewidth=0.8, label="Best found")
    landscape_ax.scatter(1.3, -0.8, marker="x", s=75, color="white",
                         linewidth=2, label="Known optimum")
    landscape_ax.set(
        xlim=(bounds[0][0], bounds[1][0]),
        ylim=(bounds[0][1], bounds[1][1]),
        xlabel=r"$x_1$", ylabel=r"$x_2$", title="Candidate positions",
    )
    landscape_ax.legend(frameon=True, fontsize=8, loc="upper right")

    score_ax.plot(iterations, best_scores, color="#1B2A4C", lw=2)
    score_cursor = score_ax.axvline(0, color="#DF6338", lw=1.5)
    score_point, = score_ax.plot([], [], "o", color="#DF6338")
    score_ax.set_yscale("log")
    positive_scores = best_scores[best_scores > 0]
    score_floor = positive_scores.min() * 0.5 if positive_scores.size else 1e-14
    score_ax.set(
        xlim=(0, iterations[-1]),
        ylim=(score_floor, max(best_scores.max() * 1.4, score_floor * 10)),
        xlabel="Iteration", ylabel="Best-so-far objective",
        title="Solution quality",
    )

    diversity_ax.plot(iterations, diversity, color="#5879AA", lw=2)
    diversity_cursor = diversity_ax.axvline(0, color="#DF6338", lw=1.5)
    diversity_point, = diversity_ax.plot([], [], "o", color="#DF6338")
    diversity_ax.set(
        xlim=(0, iterations[-1]),
        ylim=(0, max(diversity.max() * 1.12, 1e-6)),
        xlabel="Iteration", ylabel="Swarm diversity",
        title="Search concentration",
    )

    for axis in (score_ax, diversity_ax):
        axis.grid(alpha=0.2)

    iteration_label = fig.suptitle("")
    fig.tight_layout()

    def update(frame):
        xy = positions[frame]
        particles.set_offsets(xy)
        current_best.set_offsets(best_position_history[[frame]])
        score_cursor.set_xdata([frame, frame])
        diversity_cursor.set_xdata([frame, frame])
        score_point.set_data([frame], [best_scores[frame]])
        diversity_point.set_data([frame], [diversity[frame]])
        iteration_label.set_text(
            f"PSO iteration {frame} · best objective {best_scores[frame]:.3g} "
            f"· diversity {diversity[frame]:.3g}"
        )
        return (
            particles, current_best, score_cursor, diversity_cursor,
            score_point, diversity_point, iteration_label,
        )

    anim = animation.FuncAnimation(
        fig, update, frames=len(positions), interval=interval,
        blit=False, repeat=False,
    )
    plt.close(fig)
    return anim


animated_run = run_pso(
    seed=19,
    n_particles=30,
    steps=100,
    inertia=0.72,
    personal_weight=1.49,
    shared_weight=1.49,
)
reference_animation = animate_pso_run(animated_run, objective_landscape)
display(HTML(reference_animation.to_jshtml(default_mode="once")))


# ---------------------------------------------------------------------------
# Reference shared-information investigation
# ---------------------------------------------------------------------------

shared_weights = np.array([0.0, 0.4, 0.8, 1.2, 1.49, 2.0, 2.8])
seeds = np.arange(120) + 10_000
success_threshold = 1e-3
fixed_settings = {
    "n_particles": 30,
    "steps": 100,
    "inertia": 0.72,
    "personal_weight": 1.49,
}

ensembles = {
    weight: run_ensemble(weight, seeds, **fixed_settings)
    for weight in shared_weights
}

success_fraction = np.array([
    np.mean(ensembles[weight]["final_best"] <= success_threshold)
    for weight in shared_weights
])
median_best = np.array([
    np.median(ensembles[weight]["final_best"])
    for weight in shared_weights
])
median_diversity = np.array([
    np.median(ensembles[weight]["final_diversity"])
    for weight in shared_weights
])

print("\nShared-information sweep")
print("weight  success fraction  median best value  median final diversity")
for weight, success, best, diversity in zip(
    shared_weights, success_fraction, median_best, median_diversity
):
    print(f"{weight:5.2f}       {success:6.3f}          {best:10.4g}          {diversity:10.4g}")

fig, axes = plt.subplots(1, 3, figsize=(12.5, 3.6))
axes[0].plot(shared_weights, success_fraction, "o-")
axes[0].set(ylabel="Fraction successful", ylim=(-0.03, 1.03))

best_data = [ensembles[weight]["final_best"] for weight in shared_weights]
axes[1].boxplot(best_data, tick_labels=[f"{w:g}" for w in shared_weights], showfliers=False)
axes[1].set_yscale("log")
axes[1].set(ylabel="Final best objective")

diversity_data = [ensembles[weight]["final_diversity"] for weight in shared_weights]
axes[2].boxplot(
    diversity_data,
    tick_labels=[f"{w:g}" for w in shared_weights],
    showfliers=False,
)
axes[2].set(ylabel="Final swarm diversity")

for axis in axes:
    axis.set_xlabel("Shared-information weight")
    axis.grid(alpha=0.2)
fig.suptitle(
    f"PSO comparison across {len(seeds)} paired seeds; success ≤ {success_threshold:g}"
)
fig.tight_layout()
plt.show()
