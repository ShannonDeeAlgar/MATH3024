#!/usr/bin/env python3
"""Restructure Workshop 7 as a progressively independent investigation."""

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "notebooks/week07/WS_Intelligent_systems.ipynb"
notebook = json.loads(PATH.read_text())


def markdown(cell_id, source):
    return {
        "cell_type": "markdown",
        "id": cell_id,
        "metadata": {},
        "source": source.strip() + "\n",
    }


def code(cell_id, source, tags=None):
    metadata = {}
    if tags:
        metadata["tags"] = tags
    return {
        "cell_type": "code",
        "execution_count": None,
        "id": cell_id,
        "metadata": metadata,
        "outputs": [],
        "source": source.strip() + "\n",
    }


notebook["cells"] = [
    markdown("w7-title", """
# Week 7 workshop · Collective search with ACO and PSO

<span class="workshop-download-enabled" aria-hidden="true"></span>
"""),
    markdown("workshop-stage-week07-context", """
# Context
"""),
    markdown("week07-context-summary", """
**Canonical models:** ant colony optimisation and particle swarm optimisation.  
**Modelling practice:** represent a search problem, validate inherited code and design a controlled investigation.  
**New toolkit:** environmental memory, personal memory, globally shared information, repeated stochastic runs and search diversity.

ACO is used here to compare model architectures. The computational investigation develops PSO.

The central question is:

> How does the weight given to globally shared information affect the reliability and concentration of a particle swarm search?

Your final record should contain a model comparison, validation evidence, an experimental design, results from repeated runs and one appropriately limited conclusion.
"""),
    markdown("workshop-stage-week07-specify", """
# Specify the models
"""),
    markdown("week07-architecture-comparison", r"""
## Compare the search architectures

Complete or annotate this table before working with the code. Use a complete route for an ACO candidate and a vector $\mathbf{x}$ for a PSO candidate.

| Component | ACO | PSO |
|---|---|---|
| candidate solution |  |  |
| value of a solution |  |  |
| information retained by one agent |  |  |
| information shared by the population |  |  |
| update after evaluation |  |  |

Then explain how pheromone changes later route construction in ACO and how the global best-so-far position changes later motion in PSO.
"""),
    markdown("week07-pso-specification", r"""
## PSO baseline

For a minimisation problem, each particle stores a candidate $\mathbf{x}_i$, a velocity $\mathbf{v}_i$ and its personal-best position $\mathbf{p}_i$. Every particle can use the best-so-far position $\mathbf{g}$ shared globally.

At one iteration,

$$
\mathbf v_i(t+1)=w\mathbf v_i(t)
+c_1\mathbf r_1[\mathbf p_i-\mathbf x_i(t)]
+c_2\mathbf r_2[\mathbf g-\mathbf x_i(t)],
$$

followed by $\mathbf{x}_i(t+1)=\mathbf{x}_i(t)+\mathbf{v}_i(t+1)$. Here $w$ is inertia, $c_1$ and $c_2$ weight personal and shared information, and the components of $\mathbf r_1$ and $\mathbf r_2$ are independent uniform random draws on $[0,1]$.

The supplied boundary rule clips positions to the stated bounds and retains the calculated velocity. PSO advances through algorithmic iterations rather than physical time.
"""),
    markdown("week07-pso-pseudocode", """
### Pseudocode

```text
INPUT objective, bounds, particle count, iteration budget, update parameters and seed
INITIALISE positions, velocities and personal-best records
EVALUATE the initial positions and identify the global best-so-far position

FOR each iteration
    DRAW the personal and shared random coefficients
    UPDATE every velocity using inertia, personal memory and the global record
    UPDATE every position and apply the declared boundary rule
    EVALUATE every new position
    UPDATE personal and global best-so-far records
    RECORD solution quality and swarm diversity
END FOR

RETURN the recorded histories and final memories
```
"""),
    markdown("workshop-stage-week07-implement", """
# Validate the implementation

The following two cells provide the PSO implementation. Treat it as inherited code: identify its assumptions and establish that it behaves as specified before using it for an investigation.
"""),
    code("week07-pso-imports-objective", """
import numpy as np
import matplotlib.pyplot as plt

def rastrigin(x):
    x = np.asarray(x, dtype=float)
    n_dims = x.shape[-1]
    return 10 * n_dims + np.sum(x**2 - 10 * np.cos(2 * np.pi * x), axis=-1)
""", ["supplied-code"]),
    code("week07-pso-implementation", """
def initialise_swarm(n_particles, n_dims, bounds, objective, rng):
    lower = np.broadcast_to(np.asarray(bounds[0], dtype=float), (n_dims,))
    upper = np.broadcast_to(np.asarray(bounds[1], dtype=float), (n_dims,))
    positions = rng.uniform(lower, upper, size=(n_particles, n_dims))
    velocities = np.zeros_like(positions)
    personal_best = positions.copy()
    personal_scores = objective(personal_best)
    return positions, velocities, personal_best, personal_scores


def pso_step(positions, velocities, personal_best, personal_scores,
             objective, bounds, rng, inertia=0.72,
             personal_weight=1.49, shared_weight=1.49, max_speed=None):
    global_best = personal_best[np.argmin(personal_scores)]
    r_personal = rng.random(positions.shape)
    r_shared = rng.random(positions.shape)
    velocities = (
        inertia * velocities
        + personal_weight * r_personal * (personal_best - positions)
        + shared_weight * r_shared * (global_best - positions)
    )
    if max_speed is not None:
        speed = np.linalg.norm(velocities, axis=1, keepdims=True)
        velocities *= np.minimum(1.0, max_speed / np.maximum(speed, 1e-12))

    # Boundary rule: clip the position and retain the calculated velocity.
    positions = np.clip(positions + velocities, bounds[0], bounds[1])
    scores = personal_scores.copy()
    improved = scores < personal_scores
    personal_best[improved] = positions[improved]
    personal_scores[improved] = scores[improved]
    return positions, velocities, personal_best, personal_scores, scores


def run_pso(objective=rastrigin, seed=7, n_particles=30, n_dims=2,
            bounds=(-5.12, 5.12), steps=100, **update_parameters):
    rng = np.random.default_rng(seed)
    initial = initialise_swarm(n_particles, n_dims, bounds, objective, rng)
    positions, velocities, personal_best, personal_scores = initial
    scores = objective(positions)

    position_history = [positions.copy()]
    best_scores = [personal_scores.min()]
    diversity = [np.mean(np.linalg.norm(positions - positions.mean(axis=0), axis=1))]

    for _ in range(steps):
        positions, velocities, personal_best, personal_scores, scores = pso_step(
            positions, velocities, personal_best, personal_scores,
            objective, bounds, rng, **update_parameters,
        )
        position_history.append(positions.copy())
        best_scores.append(personal_scores.min())
        diversity.append(np.mean(np.linalg.norm(
            positions - positions.mean(axis=0), axis=1
        )))

    return {
        "positions": np.asarray(position_history),
        "best_scores": np.asarray(best_scores),
        "diversity": np.asarray(diversity),
        "personal_best": personal_best.copy(),
        "personal_scores": personal_scores.copy(),
        "objective_evaluations": n_particles * (steps + 1),
    }
""", ["supplied-code"]),
    markdown("week07-validation-task", """
## Establish that the baseline is valid

Design and run checks for:

1. the known Rastrigin minimum at the origin;
2. reproducibility under a fixed seed;
3. a best-so-far score that never increases; and
4. positions that remain within the declared bounds.

Record what each check tests. Add another check if your investigation depends on an assumption not covered here.
"""),
    code("week07-student-validation", """
# Write and run the validation checks here.
"""),
    markdown("workshop-stage-week07-analyse", """
# Investigate
"""),
    markdown("week07-investigation-design", r"""
## Design the shared-information experiment

Investigate how `shared_weight` affects:

- **reliability:** the fraction of repeated runs reaching a success criterion you define; and
- **search concentration:** the distribution of final swarm diversity,

$$
D(t)=\frac{1}{N}\sum_{i=1}^{N}\lVert\mathbf{x}_i(t)-\bar{\mathbf{x}}(t)\rVert.
$$

A small $D(t)$ means that particles occupy a concentrated region. Solution quality is measured by the best objective value found.

Before running the experiment, record:

| Decision | Your choice and justification |
|---|---|
| prediction |  |
| shared-information weights |  |
| controlled PSO settings |  |
| success criterion |  |
| number of repeated seeds |  |
| outputs and summaries |  |

Keep the objective, initialisation method, seeds, particle count, inertia, personal-memory weight, move limit and iteration budget fixed across conditions.
"""),
    markdown("week07-ensemble-helper-heading", """
### Supplied ensemble helper

The helper runs one condition across a declared collection of seeds. Choose the conditions and construct the comparison yourself.
"""),
    code("week07-ensemble-helper", """
def run_ensemble(shared_weight, seeds, **fixed_settings):
    runs = [
        run_pso(seed=int(seed), shared_weight=shared_weight, **fixed_settings)
        for seed in seeds
    ]
    return {
        "final_best": np.array([run["best_scores"][-1] for run in runs]),
        "final_diversity": np.array([run["diversity"][-1] for run in runs]),
        "evaluations": np.array([run["objective_evaluations"] for run in runs]),
        "runs": runs,
    }
""", ["supplied-code"]),
    code("week07-student-investigation", """
# Choose the shared-information weights, repeated seeds and fixed settings.
# Run the ensembles, summarise reliability and diversity, and produce a comparison.
"""),
    markdown("week07-evidence-checkpoint", """
## Evidence checkpoint

Report:

1. the experimental settings and success criterion;
2. reliability and final diversity for every condition;
3. one figure that permits a direct comparison;
4. whether greater concentration coincided with better solutions; and
5. one conclusion supported by the repeated runs.

Convergence can concentrate local search around a useful region. The objective value determines whether that region contains a good solution.
"""),
    markdown("workshop-stage-week07-transfer", """
# Transfer
"""),
    markdown("week07-terrain-task", """
## Represent a summit search

The Maunga Whau data contain elevations on an $87\times61$ grid with 10 m spacing. Load and inspect the grid below. Then specify a summit-search model by deciding:

- whether a candidate is a discrete grid cell or a continuous map position;
- how a candidate is evaluated;
- how maximisation is represented by the minimising PSO implementation;
- how positions outside the measured region are treated; and
- how the PSO result will be checked against the available grid.

Implement the choices you make. Repeat the search across seeds and report the validation comparison. Directly scanning this complete grid is simpler; the task practises constructing and checking an objective from data that could instead be costly to evaluate.
"""),
    code("week07-load-terrain", """
from pathlib import Path

data_path = Path("maunga_whau_elevation.csv")
if not data_path.exists():
    data_path = Path("notebooks/week07/maunga_whau_elevation.csv")
elevation = np.loadtxt(data_path, delimiter=",", skiprows=1)

print(f"Grid shape: {elevation.shape}; elevation range: {elevation.min():.1f}–{elevation.max():.1f} m")
plt.figure(figsize=(5.5, 4.2))
plt.imshow(elevation, origin="lower", cmap="terrain")
plt.colorbar(label="Elevation (m)")
plt.xlabel("Column")
plt.ylabel("Row")
plt.show()
""", ["supplied-code"]),
    code("week07-student-terrain", """
# Define the candidate representation, objective and boundary treatment.
# Run and validate the summit search here.
"""),
    markdown("workshop-stage-week07-exit", """
# Exit
"""),
    markdown("week07-exit-prompt", """
## Investigation record

Before leaving, record:

- how ACO and PSO store shared information differently;
- which validation checks passed;
- one conclusion about shared-information weight supported by repeated runs;
- the distinction between solution quality and search concentration; and
- one modelling choice required to turn the elevation grid into a PSO problem.
"""),
]

PATH.write_text(json.dumps(notebook, ensure_ascii=False, indent=1) + "\n")
print(PATH)
