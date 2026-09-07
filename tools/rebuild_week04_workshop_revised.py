#!/usr/bin/env python3
"""Build a revised, branched Week 4 cellular-automata workshop."""

from pathlib import Path
import re

import nbformat as nbf


ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "notebooks/week04/WS_Cellular_automata.ipynb"


def md(source: str, cell_id: str):
    callouts = (
        ("ladder-marker", "The ladder of abstraction"),
        ("discussion-marker", "Discuss"),
        ("choice-marker", "Modelling choice"),
    )
    for class_name, label in callouts:
        source = re.sub(
            rf'<div class="{class_name}"><img[^>]*><span>(.*?)</span></div>',
            rf'> **{label}:** \1',
            source,
            flags=re.DOTALL,
        )
    source = source.replace("<strong>", "**").replace("</strong>", "**")
    source = re.sub(
        r'<div class="reader-route">\s*'
        r'<div class="reader-route-label">(.*?)</div>\s*'
        r'<div class="reader-route-body">(.*?)</div>\s*</div>',
        r'> **\1:** \2',
        source,
        flags=re.DOTALL,
    )
    cell = nbf.v4.new_markdown_cell(source.strip() + "\n")
    cell["id"] = cell_id
    return cell


def code(source: str, cell_id: str):
    cell = nbf.v4.new_code_cell(source.strip() + "\n")
    cell["id"] = cell_id
    return cell


def main() -> None:
    nb = nbf.v4.new_notebook()
    nb.metadata = {
        "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
        "language_info": {"name": "python", "version": "3"},
        "math3024_workshop_format": "blue-period-v3-revised-branch",
    }
    nb.cells = [
        md(r"""
# Week 4 workshop · Rules, states, consequences

<div class="reader-route">
  <div class="reader-route-label">Route through the workshop</div>
  <div class="reader-route-body">Decode a rule → test one update → iterate → compare fairly → move to two dimensions → test known objects → investigate</div>
</div>

## Workshop focus

The lecture and Reader introduce cellular automata. Here you will actively reconstruct and test them by:

- decoding a Wolfram rule number into local transitions;
- implementing and testing a synchronous update;
- comparing rules under controlled initial and boundary conditions;
- challenging density, entropy, and activity as descriptions of visual structure;
- implementing Conway's Game of Life and testing it against known still lifes,
  oscillators, and spaceships.
""", "week04-revised-guide"),

        md(r"""
# From the lecture to the workshop

The lecture moves from elementary cellular automata to Conway's Game of Life, then asks how cellular automata can be compared and classified. We begin in one dimension so that every neighbourhood and update can be inspected, then carry the same modelling choices into a two-dimensional world.

Rule 90 links back to the Sierpiński triangle from Week 2. Rule 110 supplies persistent structure, and Rule 204 gives a useful counterexample when we test proposed summary statistics. The same modelling choices carry into Game of Life: state, neighbourhood, boundary, initial condition, and update schedule.

**Canonical models used here:** elementary cellular automata and Conway's Game of Life.

This notebook needs Python 3.10 or later, NumPy, Matplotlib, and IPython. It does not need the lecture repository or any separate data or image files. Run the cells in order from a fresh kernel before beginning an extension.
""", "lecture-to-workshop"),

        code(r'''
from typing import Sequence

import json
import numpy as np
import matplotlib.pyplot as plt
from IPython.display import HTML, display

SEED = 3024
INK = "#1B2A4C"
BLUE = "#5879AA"
YELLOW = "#EDCC55"

rng = np.random.default_rng(SEED)
print(f"NumPy {np.__version__} · seed {SEED}")
''', "setup"),

        md(r"""
# What goes into an elementary cellular automaton?

| Ingredient | Workshop choice |
|---|---|
| World | A one-dimensional lattice |
| State | Each cell is 0 or 1 |
| Neighbourhood | Left, centre, and right cells |
| Boundary | Periodic wrap-around |
| Dynamics | One deterministic rule applied synchronously |
| Initial condition | A single central cell or a reproducible random state |
| Clock | One simultaneous update of every cell |

<div class="choice-marker"><img src="images/choice_marker.svg" alt="Modelling choice"><span>State, neighbourhood, boundary, initialisation, and update schedule are separate choices.</span></div>
""", "model-specification"),

        md(r"""
# Decode a rule number

Three binary cells form eight possible neighbourhoods. Reading $111,110,\ldots,000$ as binary numbers gives indices $7,6,\ldots,0$.

Rule 90 is

$$90=01011010_2.$$

The bit at index $n$ gives the output for the neighbourhood whose binary value is $n$.
""", "decode-intro"),

        code(r'''
def rule_table(rule: int) -> np.ndarray:
    """Return outputs indexed by neighbourhood values 0,...,7."""
    if not isinstance(rule, (int, np.integer)) or not 0 <= rule <= 255:
        raise ValueError("rule must be an integer from 0 to 255")
    return np.array([(rule >> index) & 1 for index in range(8)], dtype=np.uint8)


def neighbourhood_bits(value: int) -> tuple[int, int, int]:
    """Return the left, centre, and right bits encoded by a value from 0 to 7."""
    if not isinstance(value, (int, np.integer)) or not 0 <= value <= 7:
        raise ValueError("value must be an integer from 0 to 7")
    return (value >> 2 & 1, value >> 1 & 1, value & 1)


assert np.array_equal(rule_table(90), [0, 1, 0, 1, 1, 0, 1, 0])
assert neighbourhood_bits(6) == (1, 1, 0)

rule = 90
table = rule_table(rule)
for value in range(7, -1, -1):
    print("".join(map(str, neighbourhood_bits(value))), "→", table[value])
''', "rule-table"),

        md(r"""
<div class="discussion-marker"><img src="images/discussion_marker.svg" alt="Discussion prompt"><span>For Rule 90, which part of the neighbourhood determines the next state? Does the centre matter?</span></div>

Rule 90 outputs one exactly when the left and right states differ. It is the exclusive-or of the two neighbours.
""", "rule90-discussion"),

        md(r"""
# Apply one synchronous update

All outputs must be calculated from the same previous state. Updating cells in place from left to right would define a different, asynchronous model.
""", "step-intro"),

        code(r'''
def validate_state(state: np.ndarray) -> np.ndarray:
    """Validate and return a one-dimensional binary state array."""
    state = np.asarray(state)
    if state.ndim != 1 or state.size < 1:
        raise ValueError("state must be a non-empty one-dimensional array")
    if not np.all((state == 0) | (state == 1)):
        raise ValueError("state must contain only zeros and ones")
    return state.astype(np.uint8, copy=False)


def elementary_ca_step(state: np.ndarray, rule: int) -> np.ndarray:
    """Apply one synchronous elementary-CA update with periodic boundaries."""
    state = validate_state(state)
    left = np.roll(state, 1)
    right = np.roll(state, -1)
    neighbourhood_value = 4 * left + 2 * state + right
    return rule_table(rule)[neighbourhood_value]
''', "step-function"),

        md(r"""
## Test rules whose behaviour is known

Tests make the bit ordering and periodic boundary convention explicit.
""", "step-tests-intro"),

        code(r'''
test_state = np.array([0, 1, 1, 0, 1], dtype=np.uint8)

assert np.array_equal(elementary_ca_step(test_state, 0), np.zeros_like(test_state))
assert np.array_equal(elementary_ca_step(test_state, 255), np.ones_like(test_state))
assert np.array_equal(elementary_ca_step(test_state, 204), test_state)  # identity rule
assert np.array_equal(
    elementary_ca_step(test_state, 90),
    np.bitwise_xor(np.roll(test_state, 1), np.roll(test_state, -1)),
)
assert np.array_equal(test_state, [0, 1, 1, 0, 1])  # input was not mutated

print("All one-step tests passed.")
''', "step-tests"),

        md(r"""
# Iterate the rule

The returned history includes the initial state at time zero. Rows are time steps and columns are cells.
""", "simulate-intro"),

        code(r'''
def simulate_elementary_ca(
    initial_state: np.ndarray,
    rule: int,
    steps: int,
) -> np.ndarray:
    """Return a state history with shape `(steps + 1, n_cells)`."""
    state = validate_state(initial_state).copy()
    if not isinstance(steps, (int, np.integer)) or steps < 0:
        raise ValueError("steps must be a non-negative integer")
    history = np.empty((steps + 1, state.size), dtype=np.uint8)
    history[0] = state
    for time in range(1, steps + 1):
        state = elementary_ca_step(state, rule)
        history[time] = state
    return history


def single_seed(n_cells: int) -> np.ndarray:
    if not isinstance(n_cells, (int, np.integer)) or n_cells < 1:
        raise ValueError("n_cells must be a positive integer")
    state = np.zeros(n_cells, dtype=np.uint8)
    state[n_cells // 2] = 1
    return state


def random_state(n_cells: int, density: float, rng: np.random.Generator) -> np.ndarray:
    if n_cells < 1 or not 0 <= density <= 1:
        raise ValueError("n_cells must be positive and density must lie in [0,1]")
    return (rng.random(n_cells) < density).astype(np.uint8)
''', "simulate-functions"),

        code(r'''
def plot_history(history: np.ndarray, rule: int, ax=None, title: str | None = None):
    """Plot time vertically and cells horizontally."""
    if ax is None:
        _, ax = plt.subplots(figsize=(8, 5))
    ax.imshow(history, cmap="binary", vmin=0, vmax=1, interpolation="nearest", aspect="auto")
    ax.set(xlabel="Cell", ylabel="Time step", title=title or f"Rule {rule}")
    return ax


initial_single = single_seed(201)
history_90 = simulate_elementary_ca(initial_single, rule=90, steps=100)
plot_history(history_90, rule=90)
plt.show()
''', "rule90-history"),

        md(r"""
<div class="ladder-marker"><img src="images/ladder_marker.svg" alt="Ladder of abstraction"><span><strong>Down:</strong> eight local transitions. <strong>Up:</strong> a two-dimensional history produced by repeating them.</span></div>

The vertical direction in this image is time, not a second spatial dimension.
""", "history-ladder"),

        md(r"""
# Compare rules fairly

Changing both the rule and the random initial state prevents us from attributing differences to the rule. Generate one initial state, then reuse it.

<div class="discussion-marker"><img src="images/discussion_marker.svg" alt="Discussion prompt"><span>Predict which rule will become uniform, periodic, nested, or persistently irregular.</span></div>
""", "fair-comparison-intro"),

        code(r'''
shared_initial = random_state(240, density=0.5, rng=np.random.default_rng(SEED))
rules = [0, 4, 30, 90, 110, 204]

fig, axes = plt.subplots(2, 3, figsize=(11, 7), sharex=True, sharey=True)
for ax, rule in zip(axes.flat, rules):
    history = simulate_elementary_ca(shared_initial, rule, steps=160)
    plot_history(history, rule, ax=ax)
fig.tight_layout()
plt.show()
''', "compare-rules"),

        md(r"""
## Pause one process

Use play/pause and the slider to inspect Rule 110 one synchronous update at a time.
""", "player-intro"),

        code(r'''
def ca_player(history: np.ndarray, element_id: str = "ca-player") -> HTML:
    """Return a dependency-free player for a one-dimensional CA history."""
    history = np.asarray(history, dtype=np.uint8)
    data = json.dumps(history.tolist())
    return HTML(f"""
    <div id="{element_id}" style="font-family:Arial,sans-serif;color:#1B2A4C">
      <canvas width="1000" height="90" style="width:100%;border:1px solid #C7CEDC;image-rendering:pixelated"></canvas>
      <div style="display:flex;gap:12px;align-items:center;margin-top:8px">
        <button type="button">Play</button>
        <input type="range" min="0" max="{len(history)-1}" value="0" style="flex:1;accent-color:#1B2A4C">
        <span></span>
      </div>
    </div>
    <script>
    (() => {{
      const root=document.getElementById('{element_id}'), states={data};
      const canvas=root.querySelector('canvas'), ctx=canvas.getContext('2d');
      const slider=root.querySelector('input'), button=root.querySelector('button'), label=root.querySelector('span');
      let timer=null;
      function draw(k) {{
        const state=states[k], width=canvas.width/state.length;
        state.forEach((value,j)=>{{ctx.fillStyle=value?'#1B2A4C':'#ffffff';ctx.fillRect(j*width,0,width+.5,canvas.height);}});
        label.textContent=`t = ${{k}}`;
      }}
      function stop() {{clearInterval(timer);timer=null;button.textContent='Play';}}
      button.onclick=()=>{{if(timer){{stop();return;}}button.textContent='Pause';timer=setInterval(()=>{{let k=+slider.value;if(k>=states.length-1){{stop();return;}}slider.value=k+1;draw(k+1);}},180);}};
      slider.oninput=()=>draw(+slider.value); draw(0);
    }})();
    </script>
    """)


player_initial = random_state(240, density=0.5, rng=np.random.default_rng(SEED))
history_110 = simulate_elementary_ca(player_initial, rule=110, steps=160)
display(ca_player(history_110))
''', "ca-player"),

        md(r"""
# Small periodic worlds change the neighbourhood

With only three cells, the left and right neighbours of a focal cell are the same two sites in opposite order. With two cells, left and right refer to the same site. The code still runs, but the intended three-cell neighbourhood has collapsed.

<div class="discussion-marker"><img src="images/discussion_marker.svg" alt="Discussion prompt"><span>What is the smallest periodic world in which left, centre, and right are three distinct sites?</span></div>
""", "small-world-intro"),

        code(r'''
for n_cells in [2, 3, 4]:
    labels = np.arange(n_cells)
    focal = 0
    neighbourhood = (labels[(focal - 1) % n_cells], labels[focal], labels[(focal + 1) % n_cells])
    print(f"n={n_cells}: focal-site neighbourhood labels = {neighbourhood}")
''', "small-world-check"),

        md(r"""
# Quantitative views

For a binary state $x$:

- **density** $\rho=\langle x\rangle$ is the fraction of cells in state one;
- **binary entropy** $H(\rho)$ measures uncertainty in the state of a randomly sampled cell;
- **activity** is the fraction of cells that change between consecutive steps.

These compress different features. None is a complete measure of spatial complexity.
""", "observables-intro"),

        code(r'''
def binary_entropy_from_density(density: np.ndarray) -> np.ndarray:
    """Binary Shannon entropy in bits, with 0 log 0 defined as zero."""
    density = np.asarray(density, dtype=float)
    if np.any((density < 0) | (density > 1)):
        raise ValueError("density must lie in [0,1]")
    entropy = np.zeros_like(density)
    interior = (density > 0) & (density < 1)
    p = density[interior]
    entropy[interior] = -(p * np.log2(p) + (1 - p) * np.log2(1 - p))
    return entropy


def ca_observables(history: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Return density, single-cell entropy, and between-step activity."""
    history = np.asarray(history)
    density = history.mean(axis=1)
    entropy = binary_entropy_from_density(density)
    activity = np.r_[np.nan, np.mean(history[1:] != history[:-1], axis=1)]
    return density, entropy, activity


density, entropy, activity = ca_observables(history_110)
fig, axes = plt.subplots(3, 1, figsize=(8, 6), sharex=True)
for ax, values, label in zip(axes, (density, entropy, activity), ("Density", "Single-cell entropy", "Activity")):
    ax.plot(values, color=INK, linewidth=1.6)
    ax.set_ylabel(label)
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(axis="y", color="#C7CEDC", linewidth=0.6)
axes[-1].set_xlabel("Time step")
fig.tight_layout()
plt.show()
''', "calculate-observables"),

        md(r"""
<div class="discussion-marker"><img src="images/discussion_marker.svg" alt="Discussion prompt"><span>Can a static configuration and a rapidly changing configuration have the same density and entropy? Which observable notices the difference?</span></div>

Rule 204 is a useful counterexample: it can retain high single-cell entropy while having zero activity after initialisation.
""", "measure-discussion"),

        md(r"""
# Survey rule space

Apply every rule to the same initial state. The scatter plot is a map of finite experiments, not a universal classification of rules.
""", "rule-space-intro"),

        code(r'''
summary = []
for rule in range(256):
    history = simulate_elementary_ca(shared_initial, rule, steps=160)
    density, entropy, activity = ca_observables(history)
    summary.append((rule, density[-1], entropy[-1], np.nanmean(activity[-40:])))

summary = np.asarray(summary)
fig, ax = plt.subplots(figsize=(7, 5))
scatter = ax.scatter(
    summary[:, 2], summary[:, 3], c=summary[:, 1], cmap="cividis", s=24, alpha=0.85
)
for rule in [0, 30, 90, 110, 204, 255]:
    row = summary[rule]
    ax.annotate(str(rule), (row[2], row[3]), xytext=(4, 3), textcoords="offset points", fontsize=8)
ax.set(xlabel="Final single-cell entropy", ylabel="Recent mean activity")
ax.spines[["top", "right"]].set_visible(False)
fig.colorbar(scatter, ax=ax, label="Final density")
plt.show()
''', "rule-space-summary"),

        md(r"""
<div class="ladder-marker"><img src="images/ladder_marker.svg" alt="Ladder of abstraction"><span><strong>Up the ladder:</strong> one local rule → one history → three observables → a finite survey of rule space.</span></div>

The survey depends on lattice size, boundary condition, initial condition, runtime, and chosen observables. A different experiment can move a rule elsewhere in this plot.
""", "rule-space-ladder"),

        md(r"""
# Canonical model 2 · Conway's Game of Life

Game of Life keeps binary states and synchronous updates, but moves to a
two-dimensional square lattice. Each cell reads its eight-cell **Moore
neighbourhood**.

| Ingredient | Workshop choice |
|---|---|
| World | A two-dimensional square lattice |
| State | Dead (0) or alive (1) |
| Neighbourhood | Eight surrounding cells; the focal cell is not counted |
| Boundary | Periodic wrap-around for the baseline |
| Update | Synchronous B3/S23 rule |

**B3/S23** means that a dead cell is **born** with exactly three live
neighbours, while a live cell **survives** with two or three. Every other cell
is dead in the next state.
""", "life-model"),

        code(r'''
def validate_life_grid(grid: np.ndarray) -> np.ndarray:
    """Validate and return a two-dimensional binary grid."""
    grid = np.asarray(grid)
    if grid.ndim != 2 or min(grid.shape) < 1:
        raise ValueError("grid must be a non-empty two-dimensional array")
    if not np.all((grid == 0) | (grid == 1)):
        raise ValueError("grid must contain only zeros and ones")
    return grid.astype(np.uint8, copy=False)


def moore_neighbour_count(grid: np.ndarray) -> np.ndarray:
    """Count live Moore neighbours using periodic boundaries."""
    grid = validate_life_grid(grid)
    count = np.zeros_like(grid, dtype=np.uint8)
    for row_shift in (-1, 0, 1):
        for col_shift in (-1, 0, 1):
            if row_shift == 0 and col_shift == 0:
                continue
            count += np.roll(grid, shift=(row_shift, col_shift), axis=(0, 1))
    return count


def game_of_life_step(grid: np.ndarray) -> np.ndarray:
    """Apply one synchronous B3/S23 update with periodic boundaries."""
    grid = validate_life_grid(grid)
    neighbours = moore_neighbour_count(grid)
    born = (grid == 0) & (neighbours == 3)
    survives = (grid == 1) & ((neighbours == 2) | (neighbours == 3))
    return (born | survives).astype(np.uint8)


def simulate_game_of_life(initial_grid: np.ndarray, steps: int) -> np.ndarray:
    """Return a Game-of-Life history including the initial configuration."""
    grid = validate_life_grid(initial_grid).copy()
    if not isinstance(steps, (int, np.integer)) or steps < 0:
        raise ValueError("steps must be a non-negative integer")
    history = np.empty((steps + 1, *grid.shape), dtype=np.uint8)
    history[0] = grid
    for time in range(1, steps + 1):
        grid = game_of_life_step(grid)
        history[time] = grid
    return history
''', "life-functions"),

        md(r"""
## Test the rule using known objects

A visual resemblance is not enough to validate the code. Still lifes,
oscillators and spaceships provide executable checks with known periods and
motions.
""", "life-tests-intro"),

        code(r'''
def place_pattern(shape: tuple[int, int], pattern: np.ndarray, top: int, left: int) -> np.ndarray:
    """Place a binary pattern on an otherwise empty periodic grid."""
    grid = np.zeros(shape, dtype=np.uint8)
    pattern = validate_life_grid(pattern)
    rows, cols = pattern.shape
    if top < 0 or left < 0 or top + rows > shape[0] or left + cols > shape[1]:
        raise ValueError("pattern must fit inside the grid")
    grid[top:top + rows, left:left + cols] = pattern
    return grid


BLOCK = np.array([[1, 1], [1, 1]], dtype=np.uint8)
BLINKER = np.array([[1, 1, 1]], dtype=np.uint8)
GLIDER = np.array([[0, 1, 0],
                   [0, 0, 1],
                   [1, 1, 1]], dtype=np.uint8)

block = place_pattern((12, 12), BLOCK, 5, 5)
assert np.array_equal(game_of_life_step(block), block)

blinker = place_pattern((12, 12), BLINKER, 5, 4)
assert not np.array_equal(game_of_life_step(blinker), blinker)
assert np.array_equal(simulate_game_of_life(blinker, 2)[-1], blinker)

glider = place_pattern((20, 20), GLIDER, 5, 5)
after_four = simulate_game_of_life(glider, 4)[-1]
assert np.array_equal(after_four, np.roll(glider, shift=(1, 1), axis=(0, 1)))

print("Block, blinker, and glider tests passed.")
''', "life-tests"),

        md(r"""
## Inspect a two-dimensional trajectory

Time can no longer be displayed as a second plotting axis because both axes
already represent space. Use snapshots or an animation, but retain direct
control of time so that individual updates can still be inspected.
""", "life-history-intro"),

        code(r'''
life_rng = np.random.default_rng(SEED)
life_initial = (life_rng.random((60, 60)) < 0.20).astype(np.uint8)
life_history = simulate_game_of_life(life_initial, steps=120)

snapshot_times = [0, 1, 10, 40, 80, 120]
fig, axes = plt.subplots(2, 3, figsize=(9, 6))
for ax, time in zip(axes.flat, snapshot_times):
    ax.imshow(life_history[time], cmap="binary", vmin=0, vmax=1, interpolation="nearest")
    ax.set_title(f"t = {time}")
    ax.set_xticks([])
    ax.set_yticks([])
fig.tight_layout()
plt.show()
''', "life-snapshots"),

        code(r'''
def life_player(history: np.ndarray, element_id: str = "life-player") -> HTML:
    """Return a dependency-free player for a Game-of-Life history."""
    history = np.asarray(history, dtype=np.uint8)
    if history.ndim != 3:
        raise ValueError("history must have shape (time, rows, columns)")
    data = json.dumps(history.tolist())
    return HTML(f"""
    <div id="{element_id}" style="font-family:Arial,sans-serif;color:#1B2A4C;max-width:720px">
      <canvas width="600" height="600" style="width:min(100%,560px);border:1px solid #C7CEDC;image-rendering:pixelated"></canvas>
      <div style="display:flex;gap:12px;align-items:center;margin-top:8px">
        <button type="button">Play</button>
        <input type="range" min="0" max="{len(history)-1}" value="0" style="flex:1;accent-color:#1B2A4C">
        <span></span>
      </div>
    </div>
    <script>
    (() => {{
      const root=document.getElementById('{element_id}'), states={data};
      const canvas=root.querySelector('canvas'), ctx=canvas.getContext('2d');
      const slider=root.querySelector('input'), button=root.querySelector('button'), label=root.querySelector('span');
      let timer=null;
      function draw(k) {{
        const state=states[k], rows=state.length, cols=state[0].length;
        const w=canvas.width/cols, h=canvas.height/rows;
        ctx.fillStyle='#ffffff'; ctx.fillRect(0,0,canvas.width,canvas.height);
        ctx.fillStyle='#1B2A4C';
        state.forEach((row,i)=>row.forEach((value,j)=>{{if(value)ctx.fillRect(j*w,i*h,w+.5,h+.5);}}));
        label.textContent=`t = ${{k}}`;
      }}
      function stop() {{clearInterval(timer);timer=null;button.textContent='Play';}}
      button.onclick=()=>{{if(timer){{stop();return;}}button.textContent='Pause';timer=setInterval(()=>{{let k=+slider.value;if(k>=states.length-1){{stop();return;}}slider.value=k+1;draw(k+1);}},140);}};
      slider.oninput=()=>draw(+slider.value); draw(0);
    }})();
    </script>
    """)


display(life_player(life_history))
''', "life-player"),

        md(r"""
## Investigate the two-dimensional model

1. Replace the random state with a block, blinker, glider, or another documented pattern. Does the observed period or displacement match the test?
2. Replace periodic boundaries with fixed-dead boundaries. Which objects distinguish the two choices, and how long must they run before the difference is visible?
3. Compare several random initial densities using the same grid size and runtime. Record live-cell density and activity through time rather than judging only the final picture.
4. Find a small seed with a long transient. Define the event that marks the end of the transient before comparing seeds.
5. Add one morphology-aware observable, such as connected-component count, cluster-size distribution, perimeter, or a box-counting estimate. State what spatial feature it retains that density discards.

> **Modelling choice:** A larger neighbourhood, an asynchronous clock, or a different boundary does not merely tune Conway's model; it defines a different cellular automaton.
""", "life-investigation"),

        md(r"""
# Choose an extension

## A · Change the update schedule

Implement asynchronous updates. Compare with the synchronous baseline using the same rule and initial state.

## B · Change the boundary

Implement fixed-zero or reflecting boundaries. Construct a test that distinguishes them from periodic boundaries.

## C · Challenge an observable

Add block entropy, compressibility, mutual information, or a spatial transition count. Find two histories your measure separates.

## D · Test robustness

Repeat selected rules over an ensemble of initial states and lattice sizes. Which conclusions survive?
""", "extensions"),

        code(r'''
# Your extension goes here. Keep the baseline functions unchanged where possible.

''', "student-extension"),

        md(r"""
# Exit ticket

In four sentences:

1. Decode one neighbourhood transition from a rule number.
2. Name one boundary or update-schedule choice.
3. Describe one system-level observable.
4. Explain one reason a visual or numerical classification may not generalise.
""", "exit-ticket"),
    ]

    nbf.write(nb, TARGET)
    print(f"Wrote {TARGET} ({len(nb.cells)} cells)")


if __name__ == "__main__":
    main()
