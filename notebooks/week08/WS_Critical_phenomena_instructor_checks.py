"""Instructor checks and reference analysis for the Week 8 workshop.

Run this file from any working directory. It loads the implementation directly
from the student notebook, so the checks exercise the version students receive.

%run WS_Critical_phenomena_instructor_checks.py

"""

from pathlib import Path
import json

import matplotlib.pyplot as plt
from matplotlib import animation
import numpy as np
from IPython.display import HTML, display


HERE = Path(__file__).resolve().parent
NOTEBOOK = HERE / "WS_Critical_phenomena.ipynb"


def load_workshop_code():
    notebook = json.loads(NOTEBOOK.read_text())
    namespace = {}
    required_cells = [
        "week08-sandpile-implementation",
        "week08-analysis-helpers",
    ]
    for cell_id in required_cells:
        cell = next(cell for cell in notebook["cells"] if cell.get("id") == cell_id)
        exec("".join(cell["source"]), namespace)
    return namespace


workshop = load_workshop_code()
relax_pile = workshop["relax_pile"]
add_grain_and_relax = workshop["add_grain_and_relax"]
prepare_active_pile = workshop["prepare_active_pile"]
run_sandpile = workshop["run_sandpile"]
empirical_ccdf = workshop["empirical_ccdf"]
log_binned_density = workshop["log_binned_density"]


# ---------------------------------------------------------------------------
# Reference answer for "Establish that the inherited code is valid"
# ---------------------------------------------------------------------------

# 1. One interior toppling conserves grains.
interior = np.zeros((5, 5), dtype=np.int64)
interior[2, 2] = 4
before = int(interior.sum())
event = relax_pile(interior)
assert int(interior.sum()) == before
assert event["size"] == event["area"] == event["duration"] == 1
assert interior[2, 2] == 0
assert np.all(interior[[1, 2, 2, 3], [2, 1, 3, 2]] == 1)

# 2. A boundary toppling loses one grain at an edge and two at a corner.
edge = np.zeros((5, 5), dtype=np.int64)
edge[0, 2] = 4
before = int(edge.sum())
relax_pile(edge)
assert before - int(edge.sum()) == 1

corner = np.zeros((5, 5), dtype=np.int64)
corner[0, 0] = 4
before = int(corner.sum())
relax_pile(corner)
assert before - int(corner.sum()) == 2

# 3. A completed relaxation contains no unstable site.
rng = np.random.default_rng(3024)
unstable = rng.integers(0, 8, size=(18, 18), dtype=np.int64)
relax_pile(unstable)
assert np.all(unstable < 4)
assert np.all(unstable >= 0)

# 4. Changing processing order within a parallel step gives the same stable state.
initial = np.random.default_rng(81).integers(0, 8, size=(18, 18), dtype=np.int64)
forward = initial.copy()
reverse = initial.copy()
forward_event = relax_pile(forward, site_order="forward")
reverse_event = relax_pile(reverse, site_order="reverse")
assert np.array_equal(forward, reverse)
assert forward_event["size"] == reverse_event["size"]
assert forward_event["area"] == reverse_event["area"]

print("All four advertised workshop validation checks passed.")


# ---------------------------------------------------------------------------
# Additional protocol and measurement checks
# ---------------------------------------------------------------------------

run_a = run_sandpile(L=16, additions=800, burn_in=200, seed=19)
run_b = run_sandpile(L=16, additions=800, burn_in=200, seed=19)
for key in ("pile", "size", "area", "duration"):
    assert np.array_equal(run_a[key], run_b[key])

assert run_a["recorded_additions"] == 600
assert all(len(run_a[key]) == 600 for key in ("size", "area", "duration"))
assert np.all(run_a["size"] >= run_a["area"])
assert np.all(run_a["size"] >= run_a["duration"])
assert np.array_equal(run_a["size"] == 0, run_a["area"] == 0)
assert np.array_equal(run_a["size"] == 0, run_a["duration"] == 0)
assert np.all(run_a["pile"] < 4)

print("Reproducibility, recording and event-measurement checks passed.")


# ---------------------------------------------------------------------------
# Full reference animation with the event quantities tracked
# ---------------------------------------------------------------------------


def find_visible_event(L=32, seed=3024, minimum_size=30, maximum_tries=20_000):
    """Return a stable pile and a recorded avalanche large enough to inspect."""
    pile, _ = prepare_active_pile(L=L, seed=seed)
    rng = np.random.default_rng(seed + 1)
    for _ in range(maximum_tries):
        starting_pile = pile.copy()
        event = add_grain_and_relax(pile, rng, record_frames=True)
        if event["size"] >= minimum_size:
            return starting_pile, event
    raise RuntimeError("No suitably visible avalanche was found; try another seed.")


def animate_avalanche(starting_pile, event, interval=260):
    """Animate one relaxation and track size, area and active sites by parallel step."""
    frames = event["frames"]
    active_counts = np.array([active.sum() for _, active in frames], dtype=int)
    cumulative_size = np.cumsum(active_counts)

    cumulative_area = []
    toppled = np.zeros_like(starting_pile, dtype=bool)
    for _, active in frames:
        toppled |= active
        cumulative_area.append(int(toppled.sum()))
    cumulative_area = np.asarray(cumulative_area)
    steps = np.arange(len(frames))

    fig, (pile_ax, measurement_ax) = plt.subplots(
        1, 2, figsize=(10.8, 4.6), gridspec_kw={"width_ratios": [1.05, 1.0]}
    )
    image = pile_ax.imshow(frames[0][0], cmap="viridis", vmin=0, vmax=3)
    active_points = pile_ax.scatter([], [], marker="s", s=18, facecolors="none",
                                    edgecolors="#F5C242", linewidths=1.1)
    pile_ax.set(title="Pile and active sites", xlabel=r"$y$", ylabel=r"$x$")
    fig.colorbar(image, ax=pile_ax, label="Height, $h_{xy}$", shrink=0.86)

    measurement_ax.plot(steps, cumulative_size, color="#D95F35", lw=2,
                        label=r"Size so far, $S$")
    measurement_ax.plot(steps, cumulative_area, color="#2878B5", lw=2,
                        label=r"Area so far, $A$")
    measurement_ax.step(steps, active_counts, where="mid", color="#6A51A3", lw=1.6,
                        label="Active sites in step")
    cursor = measurement_ax.axvline(0, color="#182B52", lw=1.2)
    measurement_ax.set(
        xlim=(0, max(1, steps[-1])),
        ylim=(0, max(1, cumulative_size.max()) * 1.08),
        xlabel="Avalanche time step", ylabel="Count", title="Event measurements",
    )
    measurement_ax.grid(alpha=0.2)
    measurement_ax.legend(frameon=False)
    heading = fig.suptitle("")
    fig.tight_layout()

    def update(frame):
        pile, active = frames[frame]
        image.set_data(pile)
        sites = np.argwhere(active)
        active_points.set_offsets(sites[:, ::-1] if sites.size else np.empty((0, 2)))
        cursor.set_xdata([frame, frame])
        heading.set_text(
            f"Step {frame} · S = {cumulative_size[frame]} · "
            f"A = {cumulative_area[frame]} · active = {active_counts[frame]}"
        )
        return image, active_points, cursor, heading

    result = animation.FuncAnimation(
        fig, update, frames=len(frames), interval=interval,
        blit=False, repeat=False,
    )
    plt.close(fig)
    return result


animation_start, animated_event = find_visible_event()
reference_animation = animate_avalanche(animation_start, animated_event)
display(HTML(reference_animation.to_jshtml(default_mode="once")))
print(
    "Animated event: "
    f"S={animated_event['size']}, A={animated_event['area']}, "
    f"T={animated_event['duration']}."
)


# ---------------------------------------------------------------------------
# Reference distribution analysis
# ---------------------------------------------------------------------------

lattice_sizes = (16, 32, 48)
additions = 8_000
burn_in = 2_000
seeds = (3024, 3025)

results = {
    L: [
        run_sandpile(L=L, additions=additions, burn_in=burn_in, seed=seed)
        for seed in seeds
    ]
    for L in lattice_sizes
}

print("\nReference protocol")
print(f"L = {lattice_sizes}; additions = {additions}; burn-in = {burn_in}; seeds = {seeds}")
print(" L   recorded events   zero-event fraction   largest S")
for L in lattice_sizes:
    sizes = np.concatenate([run["size"] for run in results[L]])
    print(f"{L:2d}      {len(sizes):6d}             {np.mean(sizes == 0):6.3f}       {sizes.max():7d}")

fig, axes = plt.subplots(1, 3, figsize=(13.4, 3.8))

reference_sizes = np.concatenate([run["size"] for run in results[32]])
positive_reference = reference_sizes[reference_sizes > 0]
linear_limit = int(np.percentile(positive_reference, 95))
axes[0].hist(positive_reference, bins=np.arange(1, linear_limit + 2),
             color="#2878B5", alpha=0.85)
axes[0].set(
    xlabel=r"Avalanche size, $S$", ylabel="Number of events",
    title=r"Linear view ($L=32$, to 95th percentile)",
)

for L in lattice_sizes:
    sizes = np.concatenate([run["size"] for run in results[L]])
    x, ccdf = empirical_ccdf(sizes)
    axes[1].loglog(x, ccdf, lw=2, label=fr"$L={L}$")
axes[1].set(
    xlabel=r"Avalanche size, $S$", ylabel=r"$P(S'\geq S)$",
    title="Empirical CCDF",
)
axes[1].legend(frameon=False)

x, ccdf = empirical_ccdf(reference_sizes)
mean_size = positive_reference.mean()
exponential = np.exp(-(x - x.min()) / mean_size)
axes[2].loglog(x, ccdf, color="#2878B5", lw=2, label="Sandpile")
axes[2].loglog(x, exponential, "--", color="#D95F35", lw=2,
               label="Exponential comparator")
axes[2].set(
    xlabel=r"Avalanche size, $S$", ylabel=r"$P(S'\geq S)$",
    title=r"Tail shape ($L=32$)",
)
axes[2].legend(frameon=False)

for axis in axes:
    axis.grid(alpha=0.2)
fig.suptitle("Week 8 reference diagnostics")
fig.tight_layout()
plt.show()


# The cutoff comparison is descriptive rather than a pass/fail test: finite
# samples fluctuate, while the plot lets the instructor inspect the claimed
# movement of the upper tail with lattice size.
fig, axes = plt.subplots(1, 2, figsize=(9.2, 3.8))
for L in lattice_sizes:
    sizes = np.concatenate([run["size"] for run in results[L]])
    areas = np.concatenate([run["area"] for run in results[L]])
    durations = np.concatenate([run["duration"] for run in results[L]])
    nonzero = sizes > 0
    axes[0].scatter(areas[nonzero], sizes[nonzero], s=7, alpha=0.18, label=fr"$L={L}$")
    axes[1].scatter(durations[nonzero], sizes[nonzero], s=7, alpha=0.18,
                    label=fr"$L={L}$")
axes[0].set(xlabel=r"Area, $A$", ylabel=r"Size, $S$", title="Size and area")
axes[1].set(xlabel=r"Duration, $T$", ylabel=r"Size, $S$", title="Size and duration")
for axis in axes:
    axis.set_xscale("log")
    axis.set_yscale("log")
    axis.grid(alpha=0.2)
    axis.legend(frameon=False)
fig.tight_layout()
plt.show()
