#!/usr/bin/env python3
"""Rebuild the Week 6 Kuramoto lecture and workshop in the current format."""

from pathlib import Path
import re

import nbformat as nbf


ROOT = Path(__file__).resolve().parents[1]
LECTURE = ROOT / "notebooks/week06/L_Synchronisation.ipynb"
WORKSHOP = ROOT / "notebooks/week06/WS_Synchronisation.ipynb"


def md(source: str, cell_id: str, *, tags=(), slide_type=""):
    cell = nbf.v4.new_markdown_cell(source.strip() + "\n")
    cell["id"] = cell_id
    cell.metadata["tags"] = list(tags)
    cell.metadata["slideshow"] = {"slide_type": slide_type}
    return cell


def code(source: str, cell_id: str):
    cell = nbf.v4.new_code_cell(source.strip() + "\n")
    cell["id"] = cell_id
    return cell


def portable(source: str) -> str:
    for class_name, label in (
        ("ladder-marker", "The ladder of abstraction"),
        ("discussion-marker", "Discuss"),
        ("choice-marker", "Modelling choice"),
    ):
        source = re.sub(
            rf'<div class="{class_name}"><img[^>]*><span>(.*?)</span></div>',
            rf'> **{label}:** \1',
            source,
            flags=re.DOTALL,
        )
    return source.replace("<strong>", "**").replace("</strong>", "**")


def lecture_notebook():
    nb = nbf.v4.new_notebook()
    nb.metadata = {
        "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
        "language_info": {"name": "python", "version": "3"},
        "math3024_slide_format": "blue-period-v3",
    }
    s, r = ("slides",), ("reader-only",)
    nb.cells = [
        md(r"""
# Synchronisation
## MATH3024 · Week 6

<div class="canonical-model-marker"><span>Canonical model</span><strong>Kuramoto coupled oscillators</strong></div>
""", "title", tags=s, slide_type="slide"),

        md(r"""
# Spontaneous synchronisation

Synchronisation is coordination in time produced through coupling.

<iframe width="880" height="410" src="https://www.youtube.com/embed/JWToUATLGzs" title="Coupled metronomes synchronising" frameborder="0" allowfullscreen></iframe>
""", "metronome-hook", tags=s, slide_type="slide"),

        md(r"""
Synchrony is not always desirable. Excessive neural synchronisation is associated with disorders including epilepsy and Parkinsonian tremor, while unwanted mechanical synchronisation contributed to lateral motion of London's Millennium Bridge.

Nor is every repeated coincidence synchronisation. Two uncoupled rhythms can produce beats or occasionally align. Coupling must change their dynamics and create a persistent temporal relationship.
""", "reader-motivation", tags=r),

        md(r"""
# Fireflies

<div class="two-panel equal-panels">
<div class="image-panel"><img src="images/Nicky_Case_fireflies.png" alt="Fireflies represented by individual internal clocks"></div>
<div class="text-panel">
<p>Each firefly has an internal rhythm.</p>
<p>A flash provides information that can shift another firefly's clock.</p>
<p>Collective flashing is a system-level pattern.</p>
<div class="discussion-marker"><img src="images/discussion_marker.svg" alt="Discussion prompt"><span>What information must pass between oscillators for their rhythms to change?</span></div>
</div>
</div>

*Explore: Nicky Case, “Fireflies”.*
""", "fireflies", tags=s, slide_type="slide"),

        md(r"""
## What goes into this model?

| Ingredient | Firefly interpretation |
|---|---|
| Individual state | position within a flashing cycle |
| Internal dynamics | its own natural flashing rate |
| Interaction network | which flashes it can perceive |
| Coupling | how a perceived flash shifts its cycle |
| Observable | collective coherence |

<div class="discussion-marker"><img src="images/discussion_marker.svg" alt="Discussion prompt"><span>How can we represent a repeating internal clock with one variable?</span></div>
""", "firefly-model", tags=s, slide_type="slide"),

        md(r"""
# A phase oscillator

A point on the unit circle represents position within a cycle:

$$
\dot{\theta}=\omega,
\qquad
\theta(t)=\theta_0+\omega t \pmod{2\pi}.
$$

- $\theta$: phase;
- $\omega$: natural angular frequency;
- $T=2\pi/|\omega|$: period.

Amplitude is deliberately omitted. The model retains only timing.
""", "single-oscillator", tags=s, slide_type="slide"),

        md(r"""
# Two uncoupled oscillators

<div class="two-panel equal-panels">
<div class="image-panel"><img src="images/Two_simple_oscillators.jpeg" alt="Two phase oscillators moving independently around a circle"></div>
<div class="text-panel">
<p>For $\dot\theta_1=\omega_1$ and $\dot\theta_2=\omega_2$, the phase difference $\phi=\theta_1-\theta_2$ evolves as</p>
<p>$$\dot\phi=\omega_1-\omega_2.$$</p>
<p>They drift unless their natural frequencies match.</p>
</div>
</div>
""", "uncoupled", tags=s, slide_type="slide"),

        md(r"""
Beats arise from adding two uncoupled oscillatory signals with nearby frequencies. The envelope varies slowly, but neither oscillator changes its frequency in response to the other. That is not spontaneous synchronisation.
""", "reader-beats", tags=r),

        md(r"""
# Add coupling

Suppose oscillator 2 drives oscillator 1:

$$
\dot{\theta}_1=\omega_1+K\sin(\theta_2-\theta_1),
\qquad
\dot{\theta}_2=\omega_2.
$$

The sine term is:

- zero when phases agree;
- positive when oscillator 1 lags;
- negative when oscillator 1 leads;
- strongest at a quarter cycle of separation.

$K$ controls coupling strength.
""", "two-coupled", tags=s, slide_type="slide"),

        md(r"""
# Reduce to phase difference

Let $\phi=\theta_1-\theta_2$ and $\Delta\omega=\omega_1-\omega_2$. Then

$$
\dot{\phi}=\Delta\omega-K\sin\phi.
$$

A phase-locked state requires $\dot\phi=0$, so

$$
\sin\phi^\ast=\frac{\Delta\omega}{K}.
$$

Locking is possible only when $|\Delta\omega|\le K$.

<div class="ladder-marker"><img src="images/ladder_marker.svg" alt="Ladder of abstraction"><span><strong>Up the ladder:</strong> two trajectories become one equation for their relative phase.</span></div>
""", "phase-difference", tags=s, slide_type="slide"),

        md(r"""
Phase locking means a constant phase difference and a common long-term frequency. It does not require equal phases. When $|\Delta\omega|>K$, the coupling is too weak to overcome the mismatch and the phase difference continues to drift.
""", "reader-locking", tags=r),

        md(r"""
# From two oscillators to a network

Why stop at two?

For $N$ all-to-all coupled phase oscillators, the Kuramoto model is

$$
\dot{\theta}_i
=\omega_i+\frac{K}{N}\sum_{j=1}^{N}\sin(\theta_j-\theta_i),
\qquad i=1,\ldots,N.
$$

The oscillators differ through their natural frequencies $\omega_i$, while coupling encourages phase alignment.
""", "kuramoto-equation", tags=s, slide_type="slide"),

        md(r"""
# Dynamics on a network

| Element | Kuramoto choice |
|---|---|
| Node state | phase $\theta_i$ |
| Internal dynamics | natural frequency $\omega_i$ |
| Network | complete graph |
| Interaction | sinusoidal phase attraction |
| Control parameter | coupling strength $K$ |
| Observable | phase coherence $r$ |

<div class="choice-marker"><img src="images/choice_marker.svg" alt="Modelling choice"><span>The complete graph and equal coupling weights are simplifying assumptions, not properties of synchronisation itself.</span></div>
""", "network-specification", tags=s, slide_type="slide"),

        md(r"""
Dynamics **on** a network means node states evolve while the network is fixed. Dynamics **of** a network means edges or nodes change. Adaptive networks combine both, for example when an epidemic changes behaviour and behaviour changes the contact network.
""", "reader-network-types", tags=r),

        md(r"""
# Watch phases organise

<video controls style="display:block;max-height:500px;max-width:100%;margin:auto">
  <source src="videos/Kuramoto_phase_locking.webm" type="video/webm">
</video>

*Points represent oscillator phases on the unit circle.*
""", "kuramoto-video", tags=("slides-only",), slide_type="slide"),

        md(r"""
## Watch phases organise

<img src="images/Coherence_evolution.png" alt="Snapshots showing oscillator phases becoming more coherent">

The moving version is included in the lecture slides. You can also [open the Kuramoto phase-locking animation](videos/Kuramoto_phase_locking.webm) directly. Follow the phase points around the unit circle and compare nil, partial, and strong phase locking.
""", "kuramoto-video-reader", tags=r),

        md(r"""
# Quantify phase coherence

The complex order parameter is

$$
r(t)e^{\mathrm{i}\psi(t)}
=\frac{1}{N}\sum_{j=1}^{N}e^{\mathrm{i}\theta_j(t)}.
$$

- $\psi$: mean phase;
- $r\in[0,1]$: concentration of phases around that mean;
- $r\approx0$: phases spread around the circle;
- $r\approx1$: phases tightly clustered.

This is the same circular average used for polarisation in Week 5.
""", "order-parameter", tags=s, slide_type="slide"),

        md(r"""
## Geometric interpretation

<div class="two-panel equal-panels">
<div class="image-panel"><img src="images/Geometric_interpretation_of_order_param.png" alt="Phase vectors and their complex average"></div>
<div class="text-panel">
<p>Each phase contributes a unit vector.</p>
<p>Their vector average has direction $\psi$ and magnitude $r$.</p>
<p>Cancellation produces low coherence; alignment produces high coherence.</p>
</div>
</div>

*Adapted from Strogatz (2000), Physica D 143, 1–20.*
""", "order-geometry", tags=s, slide_type="slide"),

        md(r"""
# Replace many interactions with a mean field

Using the order parameter,

$$
\frac{1}{N}\sum_{j=1}^{N}\sin(\theta_j-\theta_i)
=r\sin(\psi-\theta_i).
$$

Therefore the all-to-all system can be written exactly as

$$
\dot{\theta}_i=\omega_i+Kr\sin(\psi-\theta_i).
$$

Each oscillator responds to the collective field $(r,\psi)$.
""", "mean-field", tags=s, slide_type="slide"),

        md(r"""
This exact reduction relies on all-to-all sinusoidal coupling. Sparse networks, unequal weights, time delays, noise, or higher-order interactions require different analysis and can produce different collective states.
""", "reader-mean-field-limits", tags=r),

        md(r"""
# First sweep coupling strength

<img src="images/Param_sweep.png" alt="Kuramoto coherence as coupling strength increases">

<div class="ladder-marker"><img src="images/ladder_marker.svg" alt="Ladder of abstraction"><span><strong>Up the ladder over coupling:</strong> compare final coherence across $K$ to reveal the transition towards synchronisation.</span></div>

*Adapted from Strogatz (2000).*
""", "parameter-sweep", tags=s, slide_type="slide"),

        md(r"""
# Then repeat each condition

One numerical trajectory depends on the sampled natural frequencies and initial phases. An ensemble repeats each $K$ using independent samples.

| One run | Ensemble |
|---|---|
| shows one route towards or away from coherence | estimates typical coherence and variation |
| helps inspect phase locking | tests whether the transition is reproducible |

The sweep precedes the ensemble: first reveal a possible pattern, then test its robustness.
""", "ensemble", tags=s, slide_type="slide"),

        md(r"""
# What the model explains

The Kuramoto model shows how coupling can recruit heterogeneous oscillators into a coherent group.

It does not imply that every synchronising system uses sinusoidal, instantaneous, all-to-all coupling. Fireflies are pulse-coupled; neural and power-grid networks are sparse; delays and noise can matter.

A useful model isolates one mechanism, then makes its scope visible.
""", "scope", tags=s, slide_type="slide"),

        md(r"""
# Connections

- Week 4: the network specifies who interacts.
- Week 5: the circular order parameter is mathematically the same as flock polarisation.
- Later network models: topology, weights, delays, and adaptation can all modify synchronisation.

The ladder remains useful: move down to inspect phases and coupling; move up to coherence, transitions, and ensemble behaviour.
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
# Week 6 workshop · From phase drift to collective synchronisation

> **Route through the workshop:** Build one oscillator → compare uncoupled phases → add coupling → simulate a population → measure coherence → sweep $K$ → repeat runs.

## Workshop focus

The lecture and Reader introduce the Kuramoto model. Here you will actively reconstruct and test it by:

- representing oscillator phases and natural frequencies;
- checking uncoupled motion and the coupling term on known cases;
- controlling a population simulation through time;
- comparing a single coupling sweep with an ensemble.
""", "workshop-title"),

        md(r"""
# From the lecture to the workshop

The lecture moves from a pair of phase oscillators to the all-to-all Kuramoto model. The workshop follows the same route numerically, keeping phase trajectories and the collective order parameter visible together.

**Canonical model used here:** Kuramoto coupled oscillators.

This notebook needs Python 3.10 or later, NumPy, Matplotlib, and IPython. It is self-contained and does not require the lecture repository or separate files. Run the cells in order from a fresh kernel.
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
# Begin with uncoupled oscillators

For $\dot\theta_i=\omega_i$, forward Euler gives

$$
\theta_i^{n+1}=\theta_i^n+\Delta t\,\omega_i \pmod{2\pi}.
$$

Because the derivative is constant, this numerical update agrees with the exact solution at the sampled times.
""", "uncoupled-intro"),

        code(r'''
def wrap_phase(phases: np.ndarray) -> np.ndarray:
    """Wrap phases into [-pi, pi)."""
    return (np.asarray(phases, dtype=float) + np.pi) % (2 * np.pi) - np.pi


def uncoupled_step(phases: np.ndarray, frequencies: np.ndarray, dt: float) -> np.ndarray:
    phases = np.asarray(phases, dtype=float)
    frequencies = np.asarray(frequencies, dtype=float)
    if phases.shape != frequencies.shape:
        raise ValueError("phases and frequencies must have the same shape")
    if dt <= 0:
        raise ValueError("dt must be positive")
    return wrap_phase(phases + dt * frequencies)


phases = np.array([0.0, 0.0])
frequencies = np.array([1.0, 1.3])
assert np.allclose(uncoupled_step(phases, frequencies, 0.1), [0.1, 0.13])
print("Uncoupled update test passed.")
''', "uncoupled-code"),

        md(r"""
> **Discuss:** With frequencies $1.0$ and $1.3$, what happens to the phase difference? Why is their occasional agreement not synchronisation?
""", "uncoupled-discussion"),

        md(r"""
# Specify the Kuramoto model

| Ingredient | Workshop choice |
|---|---|
| Oscillator state | phase $\theta_i$ |
| Internal dynamics | fixed natural frequency $\omega_i$ |
| Network | equally weighted complete graph |
| Interaction | $\sin(\theta_j-\theta_i)$ |
| Control parameter | coupling strength $K$ |
| Numerical update | synchronous forward Euler |
| Observable | coherence $r$ |

> **Modelling choice:** The frequency distribution, coupling function, network, timestep, and initial phases are separate choices.
""", "specification"),

        code(r'''
@dataclass(frozen=True)
class KuramotoParameters:
    n_oscillators: int = 80
    coupling: float = 1.5
    dt: float = 0.05
    frequency_sd: float = 1.0

    def __post_init__(self):
        if self.n_oscillators < 1:
            raise ValueError("n_oscillators must be positive")
        if self.dt <= 0 or self.frequency_sd < 0 or self.coupling < 0:
            raise ValueError("dt must be positive; frequency_sd and coupling cannot be negative")


def initialise_kuramoto(params: KuramotoParameters, rng: np.random.Generator):
    phases = rng.uniform(-np.pi, np.pi, params.n_oscillators)
    frequencies = rng.normal(0.0, params.frequency_sd, params.n_oscillators)
    frequencies -= frequencies.mean()
    return phases, frequencies
''', "parameters"),

        md(r"""
# Inspect the coupling term

For all-to-all coupling,

$$
C_i=\frac{1}{N}\sum_j\sin(\theta_j-\theta_i).
$$

> **Discuss:** What should $C_i$ be when all phases are identical? What sign should it have for an oscillator lagging just behind a coherent group?

> **The ladder of abstraction:** **Down the ladder:** test the local response before embedding it in a population trajectory.
""", "coupling-intro"),

        code(r'''
def kuramoto_coupling(phases: np.ndarray) -> np.ndarray:
    """Return the all-to-all sinusoidal coupling experienced by each oscillator."""
    phases = np.asarray(phases, dtype=float)
    if phases.ndim != 1:
        raise ValueError("phases must be one-dimensional")
    order_parameter = np.mean(np.exp(1j * phases))
    return np.imag(order_parameter * np.exp(-1j * phases))


assert np.allclose(kuramoto_coupling(np.zeros(5)), 0.0)
opposite_pair = np.array([0.0, np.pi])
assert np.allclose(kuramoto_coupling(opposite_pair), 0.0, atol=1e-12)
print("Coupling tests passed.")
''', "coupling-code"),

        md(r"""
# Apply one synchronous update

$$
\theta_i^{n+1}
=\theta_i^n+\Delta t\left[
\omega_i+K C_i(\boldsymbol\theta^n)
\right]\pmod{2\pi}.
$$

All coupling terms must be calculated from the same previous phase vector.
""", "step-intro"),

        code(r'''
def kuramoto_step(
    phases: np.ndarray,
    frequencies: np.ndarray,
    params: KuramotoParameters,
) -> np.ndarray:
    phases = np.asarray(phases, dtype=float)
    frequencies = np.asarray(frequencies, dtype=float)
    if phases.shape != (params.n_oscillators,) or frequencies.shape != phases.shape:
        raise ValueError("state shapes do not match params.n_oscillators")
    derivative = frequencies + params.coupling * kuramoto_coupling(phases)
    return wrap_phase(phases + params.dt * derivative)


zero_coupling = KuramotoParameters(n_oscillators=3, coupling=0.0, dt=0.1)
test_phases = np.array([0.0, 0.2, -0.4])
test_frequencies = np.array([1.0, 0.0, -1.0])
assert np.allclose(
    kuramoto_step(test_phases, test_frequencies, zero_coupling),
    uncoupled_step(test_phases, test_frequencies, 0.1),
)
print("One-step limiting-case test passed.")
''', "step-code"),

        md(r"""
# Simulate and record

The natural frequencies remain fixed within one run. Only the phases evolve.
""", "simulate-intro"),

        code(r'''
def simulate_kuramoto(params: KuramotoParameters, steps: int, seed: int):
    if not isinstance(steps, (int, np.integer)) or steps < 0:
        raise ValueError("steps must be a non-negative integer")
    rng = np.random.default_rng(seed)
    phases, frequencies = initialise_kuramoto(params, rng)
    history = np.empty((steps + 1, params.n_oscillators))
    history[0] = phases
    for time in range(1, steps + 1):
        phases = kuramoto_step(phases, frequencies, params)
        history[time] = phases
    return history, frequencies


baseline = KuramotoParameters()
phase_history, natural_frequencies = simulate_kuramoto(baseline, steps=500, seed=SEED)
print("history shape:", phase_history.shape)
''', "simulate-code"),

        md(r"""
## Pause the process

The circle shows individual phases. The arrow shows the collective complex average.
""", "player-intro"),

        code(r'''
def kuramoto_player(history: np.ndarray, element_id="kuramoto-player"):
    data = json.dumps(np.round(history, 4).tolist())
    return HTML(f"""
    <div id="{element_id}" style="font-family:Arial,sans-serif;color:#1B2A4C;max-width:700px">
      <canvas width="600" height="600" style="width:min(100%,480px);border:1px solid #C7CEDC"></canvas>
      <div style="display:flex;gap:10px;align-items:center;max-width:600px">
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
        const cx=canvas.width/2, cy=canvas.height/2, R=220, phases=states[k];
        ctx.clearRect(0,0,canvas.width,canvas.height); ctx.fillStyle='#fff';ctx.fillRect(0,0,canvas.width,canvas.height);
        ctx.strokeStyle='#C7CEDC';ctx.lineWidth=2;ctx.beginPath();ctx.arc(cx,cy,R,0,2*Math.PI);ctx.stroke();
        let mx=0,my=0;
        phases.forEach(a=>{{mx+=Math.cos(a);my+=Math.sin(a);ctx.fillStyle='#5879AA';ctx.beginPath();ctx.arc(cx+R*Math.cos(a),cy-R*Math.sin(a),4,0,2*Math.PI);ctx.fill();}});
        mx/=phases.length;my/=phases.length;ctx.strokeStyle='#1B2A4C';ctx.lineWidth=5;ctx.beginPath();ctx.moveTo(cx,cy);ctx.lineTo(cx+R*mx,cy-R*my);ctx.stroke();
        label.textContent=`t = ${{k}}`;
      }}
      function stop() {{clearInterval(timer);timer=null;button.textContent='Play';}}
      button.onclick=()=>{{if(timer){{stop();return;}}button.textContent='Pause';timer=setInterval(()=>{{let k=+slider.value;if(k>=states.length-1){{stop();return;}}slider.value=k+1;draw(k+1);}},70);}};
      slider.oninput=()=>draw(+slider.value);draw(0);
    }})();
    </script>
    """)


display(kuramoto_player(phase_history))
''', "player"),

        md(r"""
# Measure phase coherence

$$
r(t)e^{\mathrm{i}\psi(t)}
=\frac{1}{N}\sum_j e^{\mathrm{i}\theta_j(t)}.
$$

> **Discuss:** Why is the arithmetic mean of the angles unsuitable near the $-\pi/\pi$ boundary?
""", "coherence-intro"),

        code(r'''
def coherence(phases: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Return coherence magnitude r and mean phase psi."""
    phases = np.asarray(phases, dtype=float)
    if phases.ndim not in (1, 2):
        raise ValueError("phases must be one- or two-dimensional")
    order = np.mean(np.exp(1j * phases), axis=-1)
    return np.abs(order), np.angle(order)


r_history, psi_history = coherence(phase_history)
fig, ax = plt.subplots(figsize=(7, 3.5))
ax.plot(np.arange(len(r_history)) * baseline.dt, r_history, color=INK, lw=2)
ax.set(xlabel="Simulation time", ylabel="Coherence, $r$", ylim=(-0.03, 1.03))
ax.grid(alpha=0.2)
fig.tight_layout()
plt.show()
''', "coherence-code"),

        md(r"""
# First sweep coupling strength

Use the same seed at every $K$. This paired sweep reveals how one sampled population responds as coupling increases.

> **The ladder of abstraction:** **Up the ladder over coupling:** compare final coherence across a family of simulations.
""", "sweep-intro"),

        code(r'''
coupling_values = np.linspace(0, 4, 9)
single_run_r = []
for coupling in coupling_values:
    params = KuramotoParameters(coupling=float(coupling))
    history, _ = simulate_kuramoto(params, steps=700, seed=SEED)
    r, _ = coherence(history[-150:])
    single_run_r.append(r.mean())

fig, ax = plt.subplots(figsize=(7, 3.5))
ax.plot(coupling_values, single_run_r, "o-", color=INK, lw=2)
ax.set(xlabel="Coupling strength, $K$", ylabel="Final mean coherence", ylim=(-0.03, 1.03))
ax.grid(alpha=0.2)
fig.tight_layout()
plt.show()
''', "single-sweep"),

        md(r"""
# Then repeat each condition

Each run independently samples initial phases and natural frequencies. The band records run-to-run variation, not uncertainty from measurement error.
""", "ensemble-intro"),

        code(r'''
seeds = np.arange(8) + SEED
ensemble = np.empty((len(coupling_values), len(seeds)))
for row, coupling in enumerate(coupling_values):
    params = KuramotoParameters(coupling=float(coupling))
    for column, seed in enumerate(seeds):
        history, _ = simulate_kuramoto(params, steps=700, seed=int(seed))
        r, _ = coherence(history[-150:])
        ensemble[row, column] = r.mean()

mean_r = ensemble.mean(axis=1)
lower, upper = np.quantile(ensemble, [0.25, 0.75], axis=1)

fig, ax = plt.subplots(figsize=(7, 3.5))
ax.plot(coupling_values, mean_r, "o-", color=INK, lw=2, label="Mean of 8 runs")
ax.fill_between(coupling_values, lower, upper, color=BLUE, alpha=0.25, label="Middle 50%")
ax.set(xlabel="Coupling strength, $K$", ylabel="Final mean coherence", ylim=(-0.03, 1.03))
ax.grid(alpha=0.2)
ax.legend(frameon=False)
fig.tight_layout()
plt.show()
''', "ensemble-code"),

        md(r"""
# Interpret the evidence

Discuss:

1. Over which coupling range does coherence change most strongly?
2. Where is run-to-run variation largest?
3. Does high $r$ mean every oscillator is phase locked?
4. How would a bimodal frequency distribution or sparse network alter the experiment?
""", "interpret"),

        md(r"""
# Choose an extension

## A · Change the frequency distribution

Use a narrower, broader, or bimodal distribution.

## B · Change the network

Replace all-to-all coupling with a ring or random graph.

## C · Challenge the observable

Construct two antipodal coherent clusters and examine $r$.

## D · Test the numerical representation

Repeat with a smaller timestep and compare trajectories and final coherence.
""", "extensions"),

        code(r'''
# Implement one extension here.
''', "student-extension"),

        md(r"""
# Exit ticket

Record:

1. the distinction between phase coincidence and synchronisation;
2. one test that checked the implementation;
3. one conclusion supported by the ensemble;
4. one limitation of the all-to-all Kuramoto model.
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
