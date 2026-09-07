#!/usr/bin/env python3
"""Rebuild the Week 5 lecture and Vicsek workshop in the current MATH3024 format."""

from pathlib import Path
import re

import nbformat as nbf


ROOT = Path(__file__).resolve().parents[1]
LECTURE = ROOT / "notebooks/week05/L_ABM.ipynb"
WORKSHOP = ROOT / "notebooks/week05/WS_ABM.ipynb"


def md(source: str, cell_id: str, *, tags=(), slide_type=""):
    cell = nbf.v4.new_markdown_cell(source.strip() + "\n")
    cell["id"] = cell_id
    cell.metadata["tags"] = list(tags)
    cell.metadata["slideshow"] = {"slide_type": slide_type}
    return cell


def code(source: str, cell_id: str, *, tags=(), slide_type=""):
    cell = nbf.v4.new_code_cell(source.strip() + "\n")
    cell["id"] = cell_id
    cell.metadata["tags"] = list(tags)
    cell.metadata["slideshow"] = {"slide_type": slide_type}
    return cell


def portable(source: str) -> str:
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
    return source


def lecture_notebook():
    nb = nbf.v4.new_notebook()
    nb.metadata = {
        "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
        "language_info": {"name": "python", "version": "3"},
        "math3024_slide_format": "blue-period-v3",
    }
    s = ("slides",)
    r = ("reader-only",)
    nb.cells = [
        md(r"""
# Agent-based modelling
## MATH3024 · Week 5

<div class="canonical-model-marker"><span>Canonical model</span><strong>Vicsek flocking model</strong></div>
""", "title", tags=s, slide_type="slide"),

        md(r"""
# We have already used agents

Schelling's segregation model represented people individually. Each agent observed a local neighbourhood and moved according to a local rule.

<div class="discussion-marker"><img src="images/discussion_marker.svg" alt="Discussion prompt"><span>What can an agent-based description retain that a population average or continuous field removes?</span></div>
""", "agents-before", tags=s, slide_type="slide"),

        md(r"""
Agent-based modelling is useful when individuals remain distinguishable and their locations, attributes, decisions, or interaction partners matter. It is not automatically the best description. The modelling question determines whether individual variation should be retained or averaged away.

This week uses collective motion to make the full workflow explicit: define agents and their environment, inspect one update, simulate, choose a system-level observable, sweep a parameter, and repeat across random runs.
""", "reader-opening", tags=r),

        md(r"""
# Collective behaviour

<div class="two-panel equal-panels">
<div class="image-panel"><img src="images/Vicsek_types_of_behaviour.png" alt="Disordered, locally ordered, and coherently moving Vicsek particles" style="max-height:250px"></div>
<div class="text-panel">
<p><strong>Microscopic description:</strong> positions, headings, neighbours, and local updates.</p>
<p><strong>Macroscopic description:</strong> disorder, bands, vortices, or coherent motion.</p>
<p>Large-scale coordination can arise from individuals responding only to local information.</p>
</div>
</div>
""", "collective-behaviour", tags=s, slide_type="slide"),

        md(r"""
## A classic example: flocking

<iframe width="960" height="500" src="https://www.youtube.com/embed/V4f_1_r80RY" title="Flocking birds" frameborder="0" allowfullscreen></iframe>

*Many birds coordinate without a leader or a global view of the flock.*
""", "flocking-video", tags=s, slide_type="slide"),

        md(r"""
## A model deferred from Week 2

<div class="two-panel equal-panels">
<div class="text-panel">
<p><strong>Agents:</strong> mobile particles.</p>
<p><strong>Motion:</strong> random local steps.</p>
<p><strong>Interaction:</strong> irreversible attachment on contact.</p>
</div>
<div class="text-panel">
<p><strong>Diffusion-limited aggregation:</strong> mobile particles take random steps and stick to an aggregate.</p>
<p>It is also an agent-based model. We defer its implementation because the Vicsek model makes interaction, motion, and collective order more explicit.</p>
</div>
</div>
""", "dla-return", tags=s, slide_type="slide"),

        md(r"""
# Three routes to a flocking model

| Perspective | Canonical model | Main emphasis |
|---|---|---|
| Computer graphics | Reynolds' boids (1987) | separation, alignment, cohesion |
| Statistical physics | Vicsek et al. (1995) | alignment, noise, phase transition |
| Behavioural biology | Couzin et al. (2002) | zones of repulsion, alignment, attraction |

Different abstractions can reproduce similar collective motion while answering different questions.
""", "three-routes", tags=s, slide_type="slide"),

        md(r"""
# What goes into an agent-based model?

| Ingredient | Question |
|---|---|
| World | Where can agents exist? |
| Agent state | What information is retained for each individual? |
| Initialisation | How is the first configuration generated? |
| Interaction network | Who can affect whom? |
| Dynamics | How is every state updated? |
| Clock | What counts as one step, and are updates synchronous? |
| Observables | What system-level behaviour will be recorded? |

<div class="choice-marker"><img src="images/choice_marker.svg" alt="Modelling choice"><span>Every row is a modelling choice.</span></div>
""", "abm-ingredients", tags=s, slide_type="slide"),

        md(r"""
# Build the Vicsek model

Vicsek and colleagues asked what happens when self-propelled particles repeatedly align with nearby particles while their headings are perturbed by noise.

The model deliberately removes aerodynamics, vision, body shape, memory, leadership, and attraction. It isolates local alignment.

*T. Vicsek et al. (1995), “Novel Type of Phase Transition in a System of Self-Driven Particles”, Physical Review Letters 75, 1226–1229.*
""", "vicsek-intro", tags=s, slide_type="slide"),

        md(r"""
## Initialise the world

| Ingredient | Choice |
|---|---|
| World | square of side length $L$ with periodic boundaries |
| Agents | $N$ point particles |
| Position | $\mathbf{x}_i=(x_i,y_i)$ |
| Heading | $\theta_i\in[0,2\pi)$ |
| Speed | constant $v$ |
| Initial state | independent random positions and headings |

<div class="discussion-marker"><img src="images/discussion_marker.svg" alt="Discussion prompt"><span>Which quantities evolve, and which remain fixed?</span></div>
""", "vicsek-initialise", tags=s, slide_type="slide"),

        md(r"""
## Define the interaction network

Agent $j$ is a neighbour of agent $i$ when its periodic distance is at most $R$:

$$\mathcal N_i(t)=\\{j:d_{\\mathrm{torus}}(\\mathbf x_i,\\mathbf x_j)\\le R\\}.$$

The interaction network changes as the agents move.

<div class="choice-marker"><img src="images/choice_marker.svg" alt="Modelling choice"><span>Metric distance is one choice. Real flocks are often better described by a fixed number of nearest neighbours.</span></div>
""", "vicsek-neighbours", tags=s, slide_type="slide"),

        md(r"""
## Apply one synchronous update

The new heading is the direction of the neighbours' mean velocity plus angular noise:

$$
\\theta_i(t+\\Delta t)
=\\operatorname{Arg}\\!\\left(\\sum_{j\\in\\mathcal N_i(t)}e^{\\mathrm{i}\\theta_j(t)}\\right)+\\xi_i(t),
\\qquad
\\xi_i\\sim U[-\\eta/2,\\eta/2].
$$

The original position update uses the old heading:

$$
\\mathbf x_i(t+\\Delta t)
=\\mathbf x_i(t)+v\\Delta t
(\\cos\\theta_i(t),\\sin\\theta_i(t)),
$$

Both new states are calculated from the same state at time $t$, then positions are wrapped periodically into the square.
""", "vicsek-update", tags=s, slide_type="slide"),

        md(r"""
Writing the position update carefully matters because moving with the old or new heading defines slightly different numerical models. We retain the original old-heading convention and update every agent synchronously.

Angular noise is not simply an inconvenience. It is a control parameter that competes with alignment.
""", "reader-update-detail", tags=r),

        md(r"""
# Pause the process

<div class="discussion-marker"><img src="images/discussion_marker.svg" alt="Discussion prompt"><span>For one focal agent, identify its periodic neighbours, calculate their mean heading, add noise, and then move it.</span></div>

<div class="ladder-marker"><img src="images/ladder_marker.svg" alt="Ladder of abstraction"><span><strong>Down the ladder:</strong> inspect one local update before interpreting the collective motion.</span></div>
""", "pause-process", tags=s, slide_type="slide"),

        md(r"""
# Qualitative analysis

<div class="two-panel equal-panels">
<div class="image-panel"><img src="images/Vicsek_types_of_behaviour.png" alt="Vicsek configurations at different density and noise values"></div>
<div class="text-panel">
<p>Simulation reveals coherent flocks, fragmented groups, and disordered motion.</p>
<p>These images help us identify candidate behaviours, but visual judgement alone is difficult to compare across many runs.</p>
</div>
</div>

*Figure adapted from Vicsek et al. (1995).*
""", "qualitative", tags=s, slide_type="slide"),

        md(r"""
# Quantitative analysis

The polarisation order parameter is

$$
\\Phi(t)=\\frac{1}{Nv}\\left|\\sum_{i=1}^{N}\\mathbf v_i(t)\\right|
=\\frac{1}{N}\\left|\\sum_{i=1}^{N}e^{\\mathrm{i}\\theta_i(t)}\\right|.
$$

- $\Phi\\approx0$: headings cancel.
- $\Phi\\approx1$: agents move in nearly the same direction.

<div class="discussion-marker"><img src="images/discussion_marker.svg" alt="Discussion prompt"><span>Can a visibly organised state still have low polarisation?</span></div>
""", "polarisation", tags=s, slide_type="slide"),

        md(r"""
Polarisation is one observable, not a complete definition of collective order. Two counter-rotating groups can each be highly organised while their mean velocity cancels. Couzin therefore used both polarisation and rotational order to distinguish different collective states.
""", "reader-observable", tags=r),

        md(r"""
# First sweep the parameter

<img src="images/Vicsek_parameter_sweeps.jpeg" alt="Vicsek order parameter as noise or density changes">

<div class="ladder-marker"><img src="images/ladder_marker.svg" alt="Ladder of abstraction"><span><strong>Up the ladder over noise:</strong> compare simulations to reveal the transition between coherent and disordered motion.</span></div>
""", "parameter-sweep", tags=s, slide_type="slide"),

        md(r"""
# Then repeat each condition

One stochastic run is one possible history. An ensemble repeats a fixed parameter setting using independent initial states and noise sequences.

| One run | Ensemble |
|---|---|
| exposes a mechanism and trajectory | estimates typical behaviour and variation |
| may be atypical | shows whether a pattern recurs |

The parameter sweep asks how behaviour changes across $\eta$. The ensemble asks how reliably we can make that comparison.
""", "ensemble", tags=s, slide_type="slide"),

        md(r"""
# History can matter

<div class="two-panel equal-panels">
<div class="image-panel"><img src="images/Couzin_hysteresis.png" alt="Hysteresis in a collective-motion model"></div>
<div class="text-panel">
<p>If a parameter is changed without reinitialising, the next run begins from the previous final state.</p>
<p>The observed state may then depend on the direction in which the parameter was changed. This is <strong>hysteresis</strong>.</p>
</div>
</div>

*Figure adapted from Couzin et al. (2002).*
""", "hysteresis", tags=s, slide_type="slide"),

        md(r"""
# A simple model is a question, not a bird

The Vicsek model shows that alignment plus noise can generate a transition to collective motion. It does not establish that real birds use metric-distance alignment.

<img src="images/Cavagna_robust_to_attack.png" alt="Empirical topological interaction network in a starling flock">

Measurements of starling flocks instead suggest interactions with a roughly fixed number of neighbours. Revising the network changed the biological interpretation while retaining the agent-based framework.
""", "improving", tags=s, slide_type="slide"),

        md(r"""
# The modelling workflow

Specify agents and world → inspect one update → simulate → choose an observable → sweep a parameter → repeat as an ensemble → compare with evidence → revise.

<div class="ladder-marker"><img src="images/ladder_marker.svg" alt="Ladder of abstraction"><span>Move down to check mechanisms and implementation. Move up to identify reproducible collective patterns.</span></div>
""", "workflow", tags=s, slide_type="slide"),

        md(r"""
# Connections

- Week 1: local preferences, parameter sweeps, and ensemble runs.
- Week 2: DLA returns as a mobile-particle ABM with irreversible attachment.
- Week 3: continuous fields average over individuals; ABMs retain them.
- Week 4: cellular automata are a constrained class of agent-based models in which sites are the agents.

The appropriate representation depends on what must remain visible in order to answer the question.
""", "connections", tags=r),
    ]
    return nb


def workshop_notebook():
    nb = nbf.v4.new_notebook()
    nb.metadata = {
        "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
        "language_info": {"name": "python", "version": "3"},
        "math3024_workshop_format": "blue-period-v3",
    }
    cells = [
        md(r"""
# Week 5 workshop · From local alignment to collective motion

> **Route through the workshop:** Specify → test periodic geometry → update one step → simulate → measure polarisation → sweep noise → repeat runs.

## Workshop focus

The lecture and Reader introduce the Vicsek model. Here you will actively reconstruct and test it by:

- representing agent positions and headings explicitly;
- checking periodic distances and synchronous updates on small cases;
- controlling a simulation through time;
- comparing a single-run noise sweep with an ensemble.
""", "workshop-title"),

        md(r"""
# From the lecture to the workshop

The lecture used the Vicsek model to connect local alignment with system-level collective motion. This workshop stays deliberately close to that model so every plotted result can be traced back to a tested update rule.

**Canonical model used here:** Vicsek flocking model.

This notebook needs Python 3.10 or later, NumPy, Matplotlib, and IPython. It is self-contained and does not require the lecture repository or separate data files. Run the cells in order from a fresh kernel.
""", "workshop-bridge"),

        code(r'''
from dataclasses import dataclass
import json

import numpy as np
import matplotlib.pyplot as plt
from IPython.display import HTML, display

SEED = 3024
INK = "#1B2A4C"
BLUE = "#5879AA"
YELLOW = "#EDCC55"

print(f"NumPy {np.__version__} · seed {SEED}")
''', "setup"),

        md(r"""
# Specify the model

| Ingredient | Workshop choice |
|---|---|
| World | square of side length $L$ with periodic boundaries |
| Agent state | position $(x_i,y_i)$ and heading $\theta_i$ |
| Motion | constant speed $v$ |
| Interaction | all agents within metric radius $R$, including self |
| Heading update | direction of mean neighbour velocity plus angular noise |
| Position update | move using the old heading, as in the original model |
| Clock | synchronous discrete steps |
| Observable | polarisation $\Phi$ |

> **Modelling choice:** The interaction rule, noise convention, update order, and boundary conditions all define the model.
""", "specification"),

        code(r'''
@dataclass(frozen=True)
class VicsekParameters:
    n_agents: int = 80
    box_size: float = 10.0
    speed: float = 0.10
    radius: float = 1.0
    noise: float = 0.8
    dt: float = 1.0

    def __post_init__(self):
        if self.n_agents < 1:
            raise ValueError("n_agents must be positive")
        if min(self.box_size, self.radius, self.dt) <= 0 or self.speed < 0:
            raise ValueError("box_size, radius, and dt must be positive; speed cannot be negative")
        if self.noise < 0:
            raise ValueError("noise must be non-negative")


def initialise_vicsek(params: VicsekParameters, rng: np.random.Generator):
    positions = rng.uniform(0, params.box_size, size=(params.n_agents, 2))
    headings = rng.uniform(-np.pi, np.pi, size=params.n_agents)
    return positions, headings
''', "parameters-initialise"),

        md(r"""
# Test the periodic geometry

For a periodic square, agents close to opposite edges may be neighbours. The minimum-image displacement wraps each coordinate into $[-L/2,L/2)$.

> **Discuss:** Two agents have $x$ coordinates $0.2$ and $9.8$ in a box with $L=10$. What is their periodic separation in the $x$ direction?
""", "periodic-intro"),

        code(r'''
def periodic_displacements(positions: np.ndarray, box_size: float) -> np.ndarray:
    """Return pairwise minimum-image displacement vectors x_j - x_i."""
    positions = np.asarray(positions, dtype=float)
    if positions.ndim != 2 or positions.shape[1] != 2:
        raise ValueError("positions must have shape (n_agents, 2)")
    displacement = positions[None, :, :] - positions[:, None, :]
    return (displacement + box_size / 2) % box_size - box_size / 2


edge_case = np.array([[0.2, 5.0], [9.8, 5.0]])
edge_displacement = periodic_displacements(edge_case, 10.0)
assert np.isclose(abs(edge_displacement[0, 1, 0]), 0.4)
assert np.allclose(edge_displacement[0, 1], -edge_displacement[1, 0])
print("Periodic-distance tests passed.")
''', "periodic-function"),

        md(r"""
# Apply one synchronous update

For each agent:

1. find neighbours from the old positions;
2. average their unit velocity vectors;
3. add independent angular noise to obtain the next heading;
4. move using the old heading;
5. wrap the new position into the periodic box.

All agents must be updated from the same previous state.
""", "update-intro"),

        code(r'''
def vicsek_step(
    positions: np.ndarray,
    headings: np.ndarray,
    params: VicsekParameters,
    rng: np.random.Generator,
) -> tuple[np.ndarray, np.ndarray]:
    """Apply one synchronous Vicsek update."""
    positions = np.asarray(positions, dtype=float)
    headings = np.asarray(headings, dtype=float)
    if positions.shape != (params.n_agents, 2) or headings.shape != (params.n_agents,):
        raise ValueError("state shapes do not match params.n_agents")

    displacement = periodic_displacements(positions, params.box_size)
    distances_squared = np.sum(displacement**2, axis=2)
    neighbours = distances_squared <= params.radius**2

    mean_x = neighbours @ np.cos(headings)
    mean_y = neighbours @ np.sin(headings)
    mean_heading = np.arctan2(mean_y, mean_x)
    angular_noise = rng.uniform(-params.noise / 2, params.noise / 2, params.n_agents)
    new_headings = (mean_heading + angular_noise + np.pi) % (2 * np.pi) - np.pi

    velocity = params.speed * np.column_stack((np.cos(headings), np.sin(headings)))
    new_positions = (positions + params.dt * velocity) % params.box_size
    return new_positions, new_headings
''', "step-function"),

        md(r"""
## Check limiting cases

With zero speed, positions should not change. With identical headings and zero noise, headings should remain identical.
""", "step-tests-intro"),

        code(r'''
test_params = VicsekParameters(n_agents=4, box_size=4, speed=0, radius=5, noise=0)
test_positions = np.array([[0., 0.], [1., 0.], [0., 1.], [1., 1.]])
test_headings = np.full(4, 0.7)
new_positions, new_headings = vicsek_step(
    test_positions, test_headings, test_params, np.random.default_rng(SEED)
)
assert np.allclose(new_positions, test_positions)
assert np.allclose(new_headings, test_headings)
assert not np.shares_memory(new_positions, test_positions)
print("One-step tests passed.")
''', "step-tests"),

        md(r"""
# Simulate and record

The history includes the initial state at time zero. Keeping positions and headings separate makes it possible to inspect trajectories and calculate observables without rerunning the model.
""", "simulate-intro"),

        code(r'''
def simulate_vicsek(params: VicsekParameters, steps: int, seed: int):
    if not isinstance(steps, (int, np.integer)) or steps < 0:
        raise ValueError("steps must be a non-negative integer")
    rng = np.random.default_rng(seed)
    positions, headings = initialise_vicsek(params, rng)
    position_history = np.empty((steps + 1, params.n_agents, 2))
    heading_history = np.empty((steps + 1, params.n_agents))
    position_history[0], heading_history[0] = positions, headings
    for time in range(1, steps + 1):
        positions, headings = vicsek_step(positions, headings, params, rng)
        position_history[time], heading_history[time] = positions, headings
    return position_history, heading_history


baseline = VicsekParameters()
positions_history, headings_history = simulate_vicsek(baseline, steps=200, seed=SEED)
print("history shapes:", positions_history.shape, headings_history.shape)
''', "simulate-function"),

        md(r"""
## Pause the process

Use the time slider to inspect how local headings become coordinated.

> **The ladder of abstraction:** **Down the ladder:** inspect individual positions, headings, and neighbours before summarising the flock.
""", "player-intro"),

        code(r'''
def vicsek_player(position_history, heading_history, box_size, element_id="vicsek-player"):
    positions_json = json.dumps(np.round(position_history, 4).tolist())
    headings_json = json.dumps(np.round(heading_history, 4).tolist())
    return HTML(f"""
    <div id="{element_id}" style="font-family:Arial,sans-serif;color:#1B2A4C;max-width:900px">
      <canvas width="650" height="650" style="width:min(100%,520px);border:1px solid #C7CEDC"></canvas>
      <div style="display:flex;gap:10px;align-items:center;max-width:650px">
        <button type="button">Play</button>
        <input type="range" min="0" max="{len(position_history)-1}" value="0" style="flex:1;accent-color:#1B2A4C">
        <span></span>
      </div>
    </div>
    <script>
    (() => {{
      const root=document.getElementById('{element_id}');
      const pos={positions_json}, ang={headings_json}, L={box_size};
      const canvas=root.querySelector('canvas'), ctx=canvas.getContext('2d');
      const slider=root.querySelector('input'), button=root.querySelector('button'), label=root.querySelector('span');
      let timer=null;
      function draw(k) {{
        ctx.clearRect(0,0,canvas.width,canvas.height);
        ctx.fillStyle='#fff'; ctx.fillRect(0,0,canvas.width,canvas.height);
        const scale=canvas.width/L;
        pos[k].forEach((p,i)=>{{
          const x=p[0]*scale, y=(L-p[1])*scale, a=ang[k][i];
          ctx.strokeStyle='#1B2A4C'; ctx.lineWidth=2;
          ctx.beginPath(); ctx.moveTo(x,y); ctx.lineTo(x+10*Math.cos(a),y-10*Math.sin(a)); ctx.stroke();
        }});
        label.textContent=`t = ${{k}}`;
      }}
      function stop() {{clearInterval(timer);timer=null;button.textContent='Play';}}
      button.onclick=()=>{{if(timer){{stop();return;}}button.textContent='Pause';timer=setInterval(()=>{{let k=+slider.value;if(k>=pos.length-1){{stop();return;}}slider.value=k+1;draw(k+1);}},100);}};
      slider.oninput=()=>draw(+slider.value); draw(0);
    }})();
    </script>
    """)


display(vicsek_player(positions_history, headings_history, baseline.box_size))
''', "player"),

        md(r"""
# Measure collective alignment

$$
\Phi(t)=\frac{1}{N}\left|\sum_{i=1}^{N}e^{\mathrm{i}\theta_i(t)}\right|.
$$

> **Discuss:** What configurations give $\Phi=1$? Can a structured configuration give $\Phi\approx0$?
""", "polarisation-intro"),

        code(r'''
def polarisation(headings: np.ndarray) -> np.ndarray:
    """Return polarisation for one heading vector or a time-by-agent array."""
    headings = np.asarray(headings, dtype=float)
    if headings.ndim not in (1, 2):
        raise ValueError("headings must be one- or two-dimensional")
    return np.abs(np.mean(np.exp(1j * headings), axis=-1))


assert np.isclose(polarisation(np.zeros(5)), 1.0)
assert np.isclose(polarisation(np.array([0, np.pi / 2, np.pi, -np.pi / 2])), 0.0)

phi_history = polarisation(headings_history)
fig, ax = plt.subplots(figsize=(7, 3.5))
ax.plot(phi_history, color=INK, lw=2)
ax.set(xlabel="Simulation time step", ylabel="Polarisation", ylim=(-0.03, 1.03))
ax.grid(alpha=0.2)
fig.tight_layout()
plt.show()
''', "polarisation-code"),

        md(r"""
# First sweep the noise

Use the same initial seed at each noise value. This paired comparison reduces one source of variation and shows how this particular history responds to the parameter.

> **The ladder of abstraction:** **Up the ladder over noise:** compare simulations to look for a transition in collective behaviour.
""", "sweep-intro"),

        code(r'''
noise_values = np.linspace(0, 2 * np.pi, 7)
single_run_phi = []
for noise in noise_values:
    params = VicsekParameters(noise=float(noise))
    _, headings = simulate_vicsek(params, steps=180, seed=SEED)
    single_run_phi.append(polarisation(headings[-40:]).mean())

fig, ax = plt.subplots(figsize=(7, 3.5))
ax.plot(noise_values, single_run_phi, "o-", color=INK, lw=2)
ax.set(xlabel="Angular noise width, $\\eta$", ylabel="Final mean polarisation", ylim=(-0.03, 1.03))
ax.grid(alpha=0.2)
fig.tight_layout()
plt.show()
''', "single-sweep"),

        md(r"""
# Then repeat each condition

An ensemble repeats the model at fixed parameter values with independent initial states and noise sequences. We summarise both the typical outcome and run-to-run variation.
""", "ensemble-intro"),

        code(r'''
seeds = np.arange(8) + SEED
ensemble = np.empty((len(noise_values), len(seeds)))
for row, noise in enumerate(noise_values):
    params = VicsekParameters(noise=float(noise))
    for column, seed in enumerate(seeds):
        _, headings = simulate_vicsek(params, steps=180, seed=int(seed))
        ensemble[row, column] = polarisation(headings[-40:]).mean()

mean_phi = ensemble.mean(axis=1)
lower, upper = np.quantile(ensemble, [0.25, 0.75], axis=1)

fig, ax = plt.subplots(figsize=(7, 3.5))
ax.plot(noise_values, mean_phi, "o-", color=INK, lw=2, label="Mean of 8 runs")
ax.fill_between(noise_values, lower, upper, color=BLUE, alpha=0.25, label="Middle 50%")
ax.set(xlabel="Angular noise width, $\\eta$", ylabel="Final mean polarisation", ylim=(-0.03, 1.03))
ax.grid(alpha=0.2)
ax.legend(frameon=False)
fig.tight_layout()
plt.show()
''', "ensemble-code"),

        md(r"""
# Interpret the evidence

Discuss:

1. Which feature of the single-run sweep persists across the ensemble?
2. Where is run-to-run variation largest?
3. Does this finite simulation establish the location or order of a phase transition?
4. What alternative observable would detect rotation or multiple counter-moving groups?
""", "interpret"),

        md(r"""
# Choose an extension

## A · Change the interaction network

Replace the metric radius with the $k$ nearest neighbours.

## B · Change the update convention

Move using the old heading rather than the newly aligned heading.

## C · Challenge the observable

Construct an organised state with low polarisation and propose a second measure.

## D · Test robustness

Repeat the ensemble with a larger population, longer settling period, or different density.
""", "extensions"),

        code(r'''
# Implement one extension here.
''', "student-extension"),

        md(r"""
# Exit ticket

Record:

1. one local modelling choice that materially affected the collective result;
2. one test that increased your confidence in the implementation;
3. one conclusion supported by the ensemble;
4. one conclusion the experiment does not support.
""", "exit-ticket"),
    ]
    for cell in cells:
        if cell.cell_type == "markdown":
            cell.source = portable(cell.source)
            cell.metadata.pop("tags", None)
            cell.metadata.pop("slideshow", None)
    nb.cells = cells
    return nb


def main():
    nbf.write(lecture_notebook(), LECTURE)
    nbf.write(workshop_notebook(), WORKSHOP)
    print(f"Wrote {LECTURE}")
    print(f"Wrote {WORKSHOP}")


if __name__ == "__main__":
    main()
