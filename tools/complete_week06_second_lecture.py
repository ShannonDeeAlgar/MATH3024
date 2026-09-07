"""Complete the worked-analysis narrative for the second Week 6 lecture."""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "notebooks/week06/L_Synchronisation.ipynb"
IMAGES = ROOT / "notebooks/week06/images"


def make_ensemble_history_figure() -> None:
    """Show why one long-time number requires a defensible transient choice."""
    rng = np.random.default_rng(3024)
    n_oscillators = 90
    n_runs = 18
    coupling = 1.72
    dt = 0.035
    times = np.arange(0.0, 36.0 + dt, dt)
    histories = []

    for _ in range(n_runs):
        omega = rng.normal(3.0, 0.72, n_oscillators)
        theta = rng.uniform(0.0, 2 * np.pi, n_oscillators)
        r_history = np.empty(times.size)
        for k in range(times.size):
            z = np.mean(np.exp(1j * theta))
            r_history[k] = np.abs(z)
            psi = np.angle(z)
            theta += dt * (omega + coupling * r_history[k] * np.sin(psi - theta))
        histories.append(r_history)

    histories = np.asarray(histories)
    transient_end = 24.0
    tail = times >= transient_end
    tail_means = histories[:, tail].mean(axis=1)

    fig, axes = plt.subplots(
        1, 2, figsize=(12.2, 4.5), gridspec_kw={"width_ratios": [1.75, 1]}
    )
    for history in histories:
        axes[0].plot(times, history, color="#4C95C6", alpha=0.24, lw=1.15)
    axes[0].plot(times, histories.mean(axis=0), color="#172D55", lw=2.7,
                 label="ensemble mean")
    axes[0].axvspan(transient_end, times[-1], color="#F6C445", alpha=0.2,
                    label="chosen summary window")
    axes[0].set(xlabel="Simulation time", ylabel=r"Coherence, $r(t)$",
                ylim=(0, 1.02), title="The histories do not settle at the same time")
    axes[0].legend(frameon=False, loc="lower right", fontsize=10)

    order = np.argsort(tail_means)
    axes[1].scatter(np.arange(1, n_runs + 1), tail_means[order], s=42,
                    color="#4C95C6", edgecolor="#172D55", linewidth=0.6)
    axes[1].axhline(tail_means.mean(), color="#E15D35", lw=2.2,
                    label="mean across runs")
    axes[1].set(xlabel="Run, ordered by summary", ylabel=r"Window mean of $r(t)$",
                ylim=(0, 1.02), title="One number per run")
    axes[1].legend(frameon=False, loc="lower right", fontsize=10)

    for ax in axes:
        ax.spines[["top", "right"]].set_visible(False)
        ax.grid(axis="y", color="#D8E1EF", lw=0.8)
        ax.tick_params(labelsize=10)
    fig.tight_layout()
    fig.savefig(IMAGES / "kuramoto_ensemble_long_time_choices.svg",
                bbox_inches="tight", transparent=True)
    plt.close(fig)


def markdown(cell_id: str, source: str, tags: list[str]) -> dict:
    return {
        "cell_type": "markdown",
        "id": cell_id,
        "metadata": {"tags": tags},
        "source": [line + "\n" for line in source.strip().splitlines()],
    }


nb = json.loads(PATH.read_text())
cells = nb["cells"]

make_ensemble_history_figure()

motivation = markdown(
    "w6-long-time-summary-motivation-slide",
    r"""
## One curve is not the result

<img src="images/kuramoto_ensemble_long_time_choices.svg" alt="Coherence histories from repeated Kuramoto simulations and one long-time summary for each run" style="display:block;width:92%;max-height:470px;margin:0 auto">

The transient duration varies between runs. A long-time summary therefore requires a stated window or convergence rule.

<div class="ladder-marker"><img src="images/ladder_marker.svg" alt="Ladder of abstraction"><span><strong>Up the ladder:</strong> replace each evolving history by a comparable summary, while retaining variation across runs.</span></div>
""",
    ["slides-only"],
)

summary_choices = markdown(
    "w6-long-time-summary-choices-slide",
    r"""
## What should one run become?

| Summary | Question answered |
|---|---|
| window mean of $r(t)$ | How coherent is the settled or late-time state? |
| late-time variability | Does coherence remain steady or fluctuate? |
| time to synchronisation | How quickly is a stated threshold reached and maintained? |
| fraction synchronised by a deadline | How reliably does synchronisation occur? |

$r_\infty$ is useful for the stationary onset calculation. It is not the only defensible summary.
""",
    ["slides-only"],
)

# Make the numerical-to-analytical transition explicit on the slides. This
# uses a result already generated from the same finite Kuramoto simulation.
transition = markdown(
    "w6-dynamic-to-stationary-slide",
    r"""
## From evolving phases to a stationary prediction

<div class="two-panel wide-left compact-panels">
<div class="image-panel"><img src="images/kuramoto_phase_trajectories_coherence.svg" alt="Individual Kuramoto phase histories above the evolving coherence r of the same population" style="max-height:430px"></div>
<div class="text-panel">
<p><i>r</i>(<i>t</i>) remains time dependent in the finite simulation.</p>
<p>For the onset calculation, ask whether its long-time value <i>r</i><sub>∞</sub> can remain greater than zero.</p>
<p>Then replace the sampled frequencies by their population density <i>g</i>(<i>ω</i>).</p>
</div>
</div>

<div class="ladder-marker"><img src="images/ladder_marker.svg" alt="Ladder of abstraction"><span><strong>Up the ladder:</strong> replace evolving individual histories by a long-time collective state.</span></div>
""",
    ["slides-only"],
)

onset = markdown(
    "w6-onset-result-slide",
    r"""
## Heterogeneity sets the onset

In the frame rotating with the centre of the frequency distribution:

$$
|\omega|\le Kr_\infty
$$

identifies the oscillators that can lock to the collective rhythm. At onset, the self-consistency calculation gives

$$
K_c=\frac{2}{\pi g(0)}.
$$

The height of the frequency distribution at its centre therefore controls how much coupling is required. This result is quoted here; the derivation is reader-only extension material.
""",
    ["slides-only"],
)

payoff_slide = markdown(
    "w6-population-payoff-slide",
    r"""
## What did the population create?

No common rhythm was assigned to the oscillators.

- Natural frequencies remain heterogeneous.
- Coupling recruits a central band into one realised frequency.
- More extreme oscillators continue to drift.
- The resulting collective rhythm feeds back into every individual update through $r$ and $\psi$.

The model therefore links a distribution of individual clocks to a measurable population-level transition.
""",
    ["slides-only"],
)

ids = [c.get("id") for c in cells]
for new in (motivation, summary_choices, transition, onset, payoff_slide):
    if new["id"] in ids:
        cells[ids.index(new["id"])] = new
    elif new["id"] == motivation["id"]:
        cells.insert(ids.index("w6-mean-field"), new)
        ids.insert(ids.index("w6-mean-field"), new["id"])
    elif new["id"] == summary_choices["id"]:
        cells.insert(ids.index("w6-mean-field"), new)
        ids.insert(ids.index("w6-mean-field"), new["id"])
    elif new["id"] == transition["id"]:
        cells.insert(ids.index("w6-mean-field") + 1, new)
        ids.insert(ids.index("w6-mean-field") + 1, new["id"])
    elif new["id"] == onset["id"]:
        cells.insert(ids.index("w6-ensemble"), new)
        ids.insert(ids.index("w6-ensemble"), new["id"])
    else:
        cells.insert(ids.index("w6-model-variants-slide"), new)
        ids.insert(ids.index("w6-model-variants-slide"), new["id"])

# Reader synthesis: place the interpretive payoff after the numerical and
# analytical accounts have both been seen.
payoff_reader = markdown(
    "w6-population-payoff-reader",
    r"""
### What did the population create?

The oscillators were not assigned a common frequency. Their natural frequencies remain heterogeneous throughout the simulation. Coupling instead changes their realised rates. A central band becomes frequency locked and rotates at a shared rate, while oscillators in the tails continue to drift through the locked group.

This is the central result of the week. Heterogeneity is not merely noise around an otherwise identical population: its distribution helps determine which oscillators can be recruited and the coupling strength at which collective coherence appears. The population-level variables $r(t)$ and $\psi(t)$ then feed back into every individual update.

<div class="ladder-marker"><img src="images/ladder_marker.svg" alt="Ladder of abstraction"><span><strong>Down the ladder:</strong> inspect the locked and drifting oscillators that produce the ensemble curve. <strong>Up the ladder:</strong> use the frequency distribution and self-consistency relation to predict the collective onset.</span></div>
""",
    ["reader-only"],
)

summary_reader = markdown(
    "w6-long-time-summary-reader",
    r"""
### Decide what one run becomes

<img src="images/kuramoto_ensemble_long_time_choices.svg" alt="Coherence histories from repeated Kuramoto simulations and one long-time summary for each run" style="display:block;width:86%;max-width:1100px;margin:1rem auto">

Repeated simulations do not pass through their transients at exactly the same time. Reading the final stored value of $r(t)$ would make the result depend on an arbitrary stopping time. Before comparing runs, state how the transient is excluded and what feature of the remaining history is being retained.

- A **late-time window mean** estimates sustained coherence. This is the numerical counterpart of $r_\infty$ when the history has settled.
- **Late-time variability** distinguishes a steady locked state from persistent collective fluctuations.
- **Time to synchronisation** records the first time that $r(t)$ crosses a chosen threshold and remains above it for a stated duration.
- The **fraction synchronised by a deadline** includes runs that never satisfy that criterion, rather than silently discarding them.

The choice depends on the question. The stationary Kuramoto calculation below concerns sustained long-time coherence, so $r_\infty$ is the appropriate quantity there. A study of speed or reliability would need one of the other summaries as well.

<div class="ladder-marker"><img src="images/ladder_marker.svg" alt="Ladder of abstraction"><span><strong>Up the ladder:</strong> compress each history into a summary chosen for the question. <strong>Down the ladder:</strong> return to the trajectories to check that the transient rule and threshold have not concealed qualitatively different behaviour.</span></div>
""",
    ["reader-only"],
)

ids = [c.get("id") for c in cells]
if summary_reader["id"] in ids:
    cells[ids.index(summary_reader["id"])] = summary_reader
else:
    cells.insert(ids.index("mean-field"), summary_reader)

ids = [c.get("id") for c in cells]
if payoff_reader["id"] in ids:
    cells[ids.index(payoff_reader["id"])] = payoff_reader
else:
    cells.insert(ids.index("w6-model-variants-reader"), payoff_reader)

PATH.write_text(json.dumps(nb, indent=1, ensure_ascii=False) + "\n")
