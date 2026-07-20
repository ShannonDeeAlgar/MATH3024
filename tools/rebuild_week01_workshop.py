#!/usr/bin/env python3
"""Rebuild the Week 1 workshop as a tested continuation of the lecture."""

from pathlib import Path

import nbformat as nbf


ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "notebooks/week01/WS_Introduction_to_complex_systems.ipynb"


def md(source: str, cell_id: str):
    cell = nbf.v4.new_markdown_cell(source.strip() + "\n")
    cell["id"] = cell_id
    return cell


def code(source: str, cell_id: str):
    cell = nbf.v4.new_code_cell(source.strip() + "\n")
    cell["id"] = cell_id
    return cell


def main():
    nb = nbf.v4.new_notebook()
    nb["metadata"] = {
        "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
        "language_info": {"name": "python", "version": "3"},
    }
    nb["cells"] = [
        md(r"""
# Week 1 workshop · Build, inspect, generalise

<div class="reader-route">
  <div class="reader-route-label">Route through the workshop</div>
  <div class="reader-route-body">Specify → initialise → inspect one agent → update once → simulate → measure → repeat as an ensemble</div>
</div>

## Learning outcomes

By the end of the workshop, you should be able to:

- implement a reproducible one-dimensional Schelling model;
- distinguish states, parameters, update rules, and observables;
- test local rules on small cases before iterating them;
- move between agent-level mechanisms and system-level summaries;
- explain why a stochastic model needs an ensemble of runs.

## How to work

At each checkpoint: **predict first**, run the smallest useful test, inspect what changed, then explain the result to someone else. Code that runs is evidence, not yet an explanation.
""", "week01-workshop-guide"),

        md(r"""
# From the lecture to the workshop

In the lecture we built a two-dimensional model to expose the modelling choices. Here we deliberately move to one dimension. The simpler geometry lets us inspect every neighbourhood and test every part of the algorithm.

<div class="ladder-marker"><img src="images/ladder_marker.svg" alt="Ladder of abstraction"><span><strong>Down the ladder:</strong> reduce the geometry so that one update can be checked by hand. <strong>Up the ladder:</strong> recover trajectories, observables, and ensembles.</span></div>

This implementation is inspired by Schelling's one-dimensional model, but it uses the lecture update rule: a randomly selected dissatisfied agent moves to a randomly selected empty site. Schelling's original 1971 rule used no empty sites and moved agents in a prescribed order to the nearest acceptable location. These are different models.

Original source: T. C. Schelling, [“Dynamic Models of Segregation”](https://doi.org/10.1080/0022250X.1971.9989794), *Journal of Mathematical Sociology* 1 (1971), 143–186.
""", "lecture-connection"),

        md(r"""
## What goes into our model?

<div class="discussion-marker"><img src="images/discussion_marker.svg" alt="Discussion prompt"><span>Which entries are states, parameters, rules, and observables?</span></div>

| Ingredient | Choice for this workshop |
|---|---|
| World | A bounded line of 70 sites |
| Site state | Empty, yellow agent, or blue agent |
| Initialisation | Independent draws with probabilities $[0.2,0.4,0.4]$ |
| Neighbourhood | Up to four sites on each side; boundaries have fewer neighbours |
| Local observable | Fraction of occupied neighbours belonging to the same group |
| Dissatisfaction | Similarity ratio below threshold $\theta$ |
| Update | Move one randomly chosen dissatisfied agent to a random empty site |
| Stopping condition | No dissatisfied agents, no empty sites, or the time budget is exhausted |
| System observables | Mean similarity ratio and fraction dissatisfied |

<div class="choice-marker"><img src="images/choice_marker.svg" alt="Modelling choice"><span>Every row is a modelling choice</span></div>
""", "model-specification"),

        md(r"""
## Set up a reproducible experiment

The random seed is part of the experimental record. We use `numpy.random.Generator` rather than global random state, so functions are reproducible without silently affecting one another.
""", "setup-intro"),

        code(r'''
from dataclasses import dataclass
from typing import Optional, Sequence

import json
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from IPython.display import HTML, display

EMPTY, YELLOW, BLUE = 0, 1, 2
STATE_PROBABILITIES = (0.2, 0.4, 0.4)
N_SITES = 70
RADIUS = 4
THRESHOLD = 0.5
MAX_STEPS = 500
ENSEMBLE_SIZE = 12
SWEEP_MAX_STEPS = 250
SEED = 3024

COLOURS = ["white", "#EDCC55", "#5879AA"]
CMAP = ListedColormap(COLOURS)

rng = np.random.default_rng(SEED)
print(f"NumPy {np.__version__} · seed {SEED}")
''', "imports-and-parameters"),

        md(r"""
### Initialisation

<div class="discussion-marker"><img src="images/discussion_marker.svg" alt="Discussion prompt"><span>Before running: approximately how many empty, yellow, and blue sites do you expect?</span></div>

Changing the seed changes the particular initial state, not the probabilities that define the initialisation procedure.
""", "initialisation-prompt"),

        code(r'''
def initialise_line(
    n_sites: int,
    probabilities: Sequence[float],
    rng: np.random.Generator,
) -> np.ndarray:
    """Return a reproducible line with states 0 (empty), 1, and 2."""
    probabilities = np.asarray(probabilities, dtype=float)
    if n_sites <= 0:
        raise ValueError("n_sites must be positive")
    if probabilities.shape != (3,) or np.any(probabilities < 0):
        raise ValueError("probabilities must contain three non-negative values")
    if not np.isclose(probabilities.sum(), 1.0):
        raise ValueError("probabilities must sum to one")
    return rng.choice([EMPTY, YELLOW, BLUE], size=n_sites, p=probabilities)


initial_line = initialise_line(N_SITES, STATE_PROBABILITIES, rng)
counts = np.bincount(initial_line, minlength=3)
print(dict(zip(["empty", "yellow", "blue"], counts)))
''', "initialise-line"),

        code(r'''
def plot_line(line: np.ndarray, ax=None, title: str = "", mark=None):
    """Plot a one-dimensional configuration using the lecture palette."""
    if ax is None:
        _, ax = plt.subplots(figsize=(11, 1.25))
    ax.imshow(line[np.newaxis, :], cmap=CMAP, vmin=0, vmax=2, aspect="auto")
    ax.set(yticks=[], xlabel="Site")
    ax.set_title(title, loc="left", color="#1B2A4C")
    if mark is not None:
        ax.scatter([mark], [0], marker="x", s=85, linewidths=2, color="#1B2A4C")
    for spine in ax.spines.values():
        spine.set_color("#C7CEDC")
        spine.set_linewidth(0.6)
    return ax


plot_line(initial_line, title="Initial one-dimensional world")
plt.show()
''', "plot-initial-line"),

        md(r"""
# Stay low: inspect one agent

For an occupied focal site $i$, remove empty sites and the focal agent from its neighbourhood. Its similarity ratio is

$$s_i=\frac{\text{similar occupied neighbours}}{\text{occupied neighbours}}.$$

At a boundary the neighbourhood is truncated. If an occupied agent has no occupied neighbours, we assign similarity zero. That convention is another modelling choice.

<div class="discussion-marker"><img src="images/discussion_marker.svg" alt="Discussion prompt"><span>What should an isolated agent's similarity ratio be? What would change if we used one instead of zero?</span></div>
""", "one-agent-intro"),

        code(r'''
def neighbourhood_indices(index: int, n_sites: int, radius: int) -> np.ndarray:
    """Indices within `radius` of `index`, excluding the focal site."""
    if not 0 <= index < n_sites:
        raise IndexError("index is outside the line")
    if radius < 1:
        raise ValueError("radius must be at least one")
    start, stop = max(0, index - radius), min(n_sites, index + radius + 1)
    return np.array([j for j in range(start, stop) if j != index], dtype=int)


def similarity_ratio(line: np.ndarray, index: int, radius: int) -> float:
    """Similarity among occupied neighbours; NaN for an empty focal site."""
    focal_state = line[index]
    if focal_state == EMPTY:
        return np.nan
    neighbours = line[neighbourhood_indices(index, len(line), radius)]
    occupied = neighbours[neighbours != EMPTY]
    if occupied.size == 0:
        return 0.0
    return float(np.mean(occupied == focal_state))


def similarity_ratios(line: np.ndarray, radius: int) -> np.ndarray:
    """One ratio per site, with NaN at empty sites."""
    return np.array([similarity_ratio(line, i, radius) for i in range(len(line))])


def dissatisfied_indices(line: np.ndarray, radius: int, threshold: float) -> np.ndarray:
    """Occupied sites whose local similarity lies below the threshold."""
    ratios = similarity_ratios(line, radius)
    return np.flatnonzero((line != EMPTY) & (ratios < threshold))
''', "local-observables"),

        md(r"""
### Test before iterating

These small cases are executable specifications. If a later edit breaks a boundary rule, excludes the wrong sites, or treats empty sites as agents, an assertion fails immediately.
""", "tests-intro"),

        code(r'''
test_line = np.array([YELLOW, YELLOW, EMPTY, BLUE, BLUE])

assert np.array_equal(neighbourhood_indices(0, 5, radius=2), np.array([1, 2]))
assert np.array_equal(neighbourhood_indices(2, 5, radius=2), np.array([0, 1, 3, 4]))
assert similarity_ratio(test_line, 0, radius=1) == 1.0
assert np.isnan(similarity_ratio(test_line, 2, radius=1))
assert similarity_ratio(np.array([YELLOW, BLUE, YELLOW]), 1, radius=1) == 0.0
assert set(dissatisfied_indices(np.array([YELLOW, BLUE, YELLOW]), 1, 0.5)) == {0, 1, 2}

print("All local-rule tests passed.")
''', "local-tests"),

        md(r"""
### Inspect a real neighbourhood

Choose the focal agent deliberately while debugging. Random selection is useful for simulation, but it makes mistakes harder to reproduce.
""", "inspect-prompt"),

        code(r'''
occupied_sites = np.flatnonzero(initial_line != EMPTY)
focal_index = int(occupied_sites[len(occupied_sites) // 2])
neighbours = neighbourhood_indices(focal_index, len(initial_line), RADIUS)
ratio = similarity_ratio(initial_line, focal_index, RADIUS)

print(f"focal site: {focal_index}")
print(f"neighbour sites: {neighbours.tolist()}")
print(f"similarity ratio: {ratio:.3f}")
print("dissatisfied" if ratio < THRESHOLD else "satisfied")

plot_line(initial_line, title="The × marks the focal agent", mark=focal_index)
plt.show()
''', "inspect-agent"),

        md(r"""
# Apply one update

Our update selects from the dissatisfied agents directly. If everyone is satisfied, or if there is nowhere to move, it returns without changing the state.

<div class="choice-marker"><img src="images/choice_marker.svg" alt="Modelling choice"><span>Random dissatisfied agent → random empty site</span></div>
""", "one-update-intro"),

        code(r'''
def update_once(
    line: np.ndarray,
    radius: int,
    threshold: float,
    rng: np.random.Generator,
) -> tuple[np.ndarray, Optional[tuple[int, int]]]:
    """Return a new line and `(origin, destination)`, or `None` if no move is possible."""
    unhappy = dissatisfied_indices(line, radius, threshold)
    empty = np.flatnonzero(line == EMPTY)
    if unhappy.size == 0 or empty.size == 0:
        return line.copy(), None

    origin = int(rng.choice(unhappy))
    destination = int(rng.choice(empty))
    updated = line.copy()
    updated[destination] = updated[origin]
    updated[origin] = EMPTY
    return updated, (origin, destination)


step_rng = np.random.default_rng(SEED + 1)
line_after_one_step, move = update_once(initial_line, RADIUS, THRESHOLD, step_rng)
print("move:", move)

fig, axes = plt.subplots(2, 1, figsize=(11, 2.5), sharex=True)
plot_line(initial_line, axes[0], "Before", None if move is None else move[0])
plot_line(line_after_one_step, axes[1], "After", None if move is None else move[1])
fig.tight_layout()
plt.show()
''', "one-update"),

        md(r"""
<div class="discussion-marker"><img src="images/discussion_marker.svg" alt="Discussion prompt"><span>Did the move necessarily improve the destination neighbourhood? Is that assumed by our update rule?</span></div>

The lecture model moves a dissatisfied agent to a random empty site. It does **not** require the destination to make that agent satisfied. This is why aggregate quantities can oscillate.
""", "one-update-discussion"),

        md(r"""
# Iterate to a stopping condition

We now package the evolving state and observables together. The simulation records its initial condition at time zero, then records each successful update. It stops early when no move is possible.
""", "simulation-intro"),

        code(r'''
def mean_similarity_ratio(line: np.ndarray, radius: int) -> float:
    """Mean local similarity across occupied agents only."""
    ratios = similarity_ratios(line, radius)
    return float(np.nanmean(ratios)) if np.any(~np.isnan(ratios)) else np.nan


def dissatisfied_fraction(line: np.ndarray, radius: int, threshold: float) -> float:
    """Fraction of occupied agents that are dissatisfied."""
    occupied = np.count_nonzero(line)
    return len(dissatisfied_indices(line, radius, threshold)) / occupied if occupied else np.nan


@dataclass(frozen=True)
class SimulationResult:
    frames: tuple[np.ndarray, ...]
    moves: tuple[tuple[int, int], ...]
    msr: np.ndarray
    dissatisfied_fraction: np.ndarray
    settled: bool


def run_simulation(
    initial: np.ndarray,
    radius: int,
    threshold: float,
    rng: np.random.Generator,
    max_steps: int = 500,
) -> SimulationResult:
    """Run the model without mutating `initial`."""
    line = initial.copy()
    frames = [line.copy()]
    moves = []
    msr_history = [mean_similarity_ratio(line, radius)]
    dissatisfied_history = [dissatisfied_fraction(line, radius, threshold)]

    for _ in range(max_steps):
        line, move = update_once(line, radius, threshold, rng)
        if move is None:
            break
        moves.append(move)
        frames.append(line.copy())
        msr_history.append(mean_similarity_ratio(line, radius))
        dissatisfied_history.append(dissatisfied_fraction(line, radius, threshold))

    settled = len(dissatisfied_indices(line, radius, threshold)) == 0
    return SimulationResult(
        frames=tuple(frames),
        moves=tuple(moves),
        msr=np.asarray(msr_history),
        dissatisfied_fraction=np.asarray(dissatisfied_history),
        settled=settled,
    )


simulation_rng = np.random.default_rng(SEED + 2)
result = run_simulation(initial_line, RADIUS, THRESHOLD, simulation_rng, MAX_STEPS)
print(f"{len(result.moves)} steps · settled={result.settled} · final MSR={result.msr[-1]:.3f}")
''', "run-simulation"),

        md(r"""
## Pause the process

Use play/pause and the time slider to inspect individual state changes. The player is deliberately separate from the model logic, so changing the visualisation cannot change the simulation.
""", "player-intro"),

        code(r'''
def simulation_player(frames: Sequence[np.ndarray], element_id: str = "schelling-1d") -> HTML:
    """Return a dependency-free HTML player for a sequence of 1D states."""
    frame_data = json.dumps([frame.tolist() for frame in frames])
    return HTML(f"""
    <div id="{element_id}" style="font-family:Arial,sans-serif;color:#1B2A4C">
      <canvas width="1000" height="90" style="width:100%;border:1px solid #C7CEDC"></canvas>
      <div style="display:flex;gap:12px;align-items:center;margin-top:8px">
        <button type="button">Play</button>
        <input type="range" min="0" max="{len(frames)-1}" value="0" style="flex:1;accent-color:#1B2A4C">
        <span>0 / {len(frames)-1}</span>
      </div>
    </div>
    <script>
    (() => {{
      const root=document.getElementById('{element_id}');
      const frames={frame_data}, canvas=root.querySelector('canvas'), ctx=canvas.getContext('2d');
      const slider=root.querySelector('input'), button=root.querySelector('button'), label=root.querySelector('span');
      const colours=['#ffffff','#EDCC55','#5879AA']; let timer=null;
      function draw(k) {{
        const frame=frames[k], w=canvas.width/frame.length;
        frame.forEach((state,j)=>{{ctx.fillStyle=colours[state];ctx.fillRect(j*w,0,w,canvas.height);}});
        label.textContent=`${{k}} / ${{frames.length-1}}`;
      }}
      function stop() {{clearInterval(timer);timer=null;button.textContent='Play';}}
      button.onclick=()=>{{if(timer){{stop();return;}}button.textContent='Pause';timer=setInterval(()=>{{let k=+slider.value;if(k>=frames.length-1){{stop();return;}}slider.value=k+1;draw(k+1);}},250);}};
      slider.oninput=()=>draw(+slider.value); draw(0);
    }})();
    </script>
    """)


display(simulation_player(result.frames))
''', "simulation-player"),

        md(r"""
# Analyse one run

Qualitative and quantitative views answer different questions. Keep them connected to the same sequence of states.
""", "analyse-one-run"),

        code(r'''
fig, axes = plt.subplots(2, 1, figsize=(9, 5), sharex=True)
time = np.arange(len(result.frames))

axes[0].plot(time, result.dissatisfied_fraction, color="#1B2A4C", linewidth=2)
axes[0].set_ylabel("Dissatisfied\nfraction")
axes[0].set_ylim(0, 1)

axes[1].plot(time, result.msr, color="#1B2A4C", linewidth=2)
axes[1].axhline(0.5, color="#5A6685", linestyle="--", linewidth=1, label="random 50:50 benchmark")
axes[1].set(xlabel="Simulation time step", ylabel="MSR", ylim=(0, 1))
axes[1].legend(frameon=False)

for ax in axes:
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(axis="y", color="#C7CEDC", linewidth=0.6, alpha=0.6)

fig.tight_layout()
plt.show()
''', "one-run-observables"),

        md(r"""
<div class="discussion-marker"><img src="images/discussion_marker.svg" alt="Discussion prompt"><span>Where does the aggregate curve hide individual agents? Find a time step worth inspecting in the player.</span></div>

- Did MSR increase monotonically?
- Did the dissatisfied fraction decrease monotonically?
- Did the run reach a steady state, or merely use its time budget?
- Which claim is supported by this one run? Which claim is not?
""", "one-run-discussion"),

        md(r"""
# One run is not enough

An **ensemble** repeats the same model and parameter values with independent initial states and random update sequences. It replaces one possible history with a distribution of possible histories.

An ensemble contributes:

- an estimate of typical behaviour;
- run-to-run variation;
- the probability of settling within a specified time budget;
- evidence about whether a conclusion is robust to stochastic choices.

<div class="ladder-marker"><img src="images/ladder_marker.svg" alt="Ladder of abstraction"><span><strong>Up the ladder:</strong> one history → a distribution over histories.</span></div>
""", "ensemble-intro"),

        code(r'''
def run_ensemble(
    threshold: float,
    seeds: Sequence[int],
    *,
    n_sites: int = N_SITES,
    radius: int = RADIUS,
    probabilities: Sequence[float] = STATE_PROBABILITIES,
    max_steps: int = MAX_STEPS,
) -> list[SimulationResult]:
    """Independent runs at one fixed threshold."""
    ensemble = []
    for seed in seeds:
        initial_rng = np.random.default_rng(seed)
        update_rng = np.random.default_rng(seed + 10_000)
        initial = initialise_line(n_sites, probabilities, initial_rng)
        ensemble.append(run_simulation(initial, radius, threshold, update_rng, max_steps))
    return ensemble


ensemble = run_ensemble(THRESHOLD, seeds=range(ENSEMBLE_SIZE))
final_msr = np.array([run.msr[-1] for run in ensemble])
settled = np.array([run.settled for run in ensemble])

print(f"mean final MSR: {final_msr.mean():.3f}")
print(f"middle 50%: {np.quantile(final_msr, [0.25, 0.75])}")
print(f"settled within budget: {settled.mean():.0%}")
''', "run-ensemble"),

        md(r"""
# Vary one modelling choice

Now repeat the ensemble at several similarity thresholds. This is a **parameter sweep of ensembles**: each threshold receives its own collection of independent runs.

For a responsive workshop, each threshold uses 12 runs and a 250-step budget. These computational choices affect the precision of our estimates and the meaning of “settled within budget”.

<div class="discussion-marker"><img src="images/discussion_marker.svg" alt="Discussion prompt"><span>Predict the shape of each curve before running the sweep.</span></div>
""", "parameter-sweep-intro"),

        code(r'''
thresholds = np.array([0.2, 0.35, 0.5, 0.65, 0.8])
seeds = range(ENSEMBLE_SIZE)

summary = []
for threshold in thresholds:
    runs = run_ensemble(threshold, seeds, max_steps=SWEEP_MAX_STEPS)
    summary.append({
        "threshold": threshold,
        "mean_final_msr": np.mean([run.msr[-1] for run in runs]),
        "mean_final_dissatisfied": np.mean([run.dissatisfied_fraction[-1] for run in runs]),
        "settled_fraction": np.mean([run.settled for run in runs]),
    })

mean_msr = np.array([row["mean_final_msr"] for row in summary])
mean_dissatisfied = np.array([row["mean_final_dissatisfied"] for row in summary])
settled_fraction = np.array([row["settled_fraction"] for row in summary])

fig, axes = plt.subplots(1, 3, figsize=(12, 3.6), sharex=True)
axes[0].plot(thresholds, mean_msr, "o-", color="#1B2A4C")
axes[0].set_ylabel("Mean final MSR")
axes[1].plot(thresholds, mean_dissatisfied, "o-", color="#1B2A4C")
axes[1].set_ylabel("Mean final dissatisfied fraction")
axes[2].plot(thresholds, settled_fraction, "o-", color="#1B2A4C")
axes[2].set_ylabel("Fraction of runs settled")

for ax in axes:
    ax.set(xlabel="Similarity threshold", ylim=(0, 1))
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(axis="y", color="#C7CEDC", linewidth=0.6, alpha=0.6)

fig.tight_layout()
plt.show()
''', "parameter-sweep"),

        md(r"""
## Interpret, do not optimise

<div class="discussion-marker"><img src="images/discussion_marker.svg" alt="Discussion prompt"><span>What does each panel contribute that the other two do not?</span></div>

The sweep does not reveal a universally “best” threshold. The threshold represents an assumed preference. A best value exists only after an objective and acceptable trade-offs have been specified.

Discuss:

1. At which thresholds is satisfaction easy to achieve? Does that imply strong segregation?
2. At which thresholds does the model struggle to settle?
3. Is final MSR alone an adequate outcome measure?
4. Which result appears robust across initialisations, and which remains variable?
""", "interpret-sweep"),

        md(r"""
# Choose an extension

Work on one extension deeply. State your prediction before editing code and preserve the baseline result for comparison.

### A · Challenge an assumption

Change exactly one of the following: neighbourhood radius, empty-site probability, boundary rule, destination rule, or isolated-agent convention. Explain which question the change helps answer.

### B · Challenge an observable

Design a more global segregation measure. Test it on at least three deliberately constructed configurations, including a mixed line and a line split into two domains.

### C · Challenge robustness

Increase the ensemble size. Decide what it would mean for a summary to have “stabilised”, then justify a sufficient number of runs.

### D · Move back up in geometry

Identify the smallest changes needed to apply the same function structure to a two-dimensional grid. Separate changes to state representation from changes to neighbourhood calculation.
""", "extensions"),

        code(r'''
# Your extension goes here. Keep the baseline functions unchanged where possible.

''', "student-extension"),

        md(r"""
# Exit ticket

In three sentences:

1. Name one local modelling choice.
2. Describe one system-level pattern or observable it affected.
3. Explain why an ensemble supported a stronger claim than a single run.

<div class="ladder-marker"><img src="images/ladder_marker.svg" alt="Ladder of abstraction"><span>Agent → update rule → trajectory → observable → ensemble.</span></div>
""", "exit-ticket"),
    ]

    nbf.write(nb, TARGET)
    print(f"Wrote {TARGET} ({len(nb['cells'])} cells)")


if __name__ == "__main__":
    main()
