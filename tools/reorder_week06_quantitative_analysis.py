"""Reorder Week 6 quantitative analysis and align its long-time summaries."""

from __future__ import annotations

import json
import re
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from figure_style import (
    BLUE,
    YELLOW,
    INK,
    LIGHT_BLUE,
    ORANGE,
    apply_course_figure_style,
    finish_axes,
)


ROOT = Path(__file__).resolve().parents[1]
LECTURE = ROOT / "notebooks/week06/L_Synchronisation.ipynb"
WORKSHOP = ROOT / "notebooks/week06/WS_Synchronisation.ipynb"
IMAGES = ROOT / "notebooks/week06/images"


def lines(text: str) -> list[str]:
    return [line + "\n" for line in text.rstrip().splitlines()]


def load(path: Path) -> dict:
    return json.loads(path.read_text())


def save(path: Path, notebook: dict) -> None:
    path.write_text(json.dumps(notebook, indent=1, ensure_ascii=False) + "\n")


def find(cells: list[dict], cell_id: str) -> dict:
    return next(cell for cell in cells if cell.get("id") == cell_id)


def move_after(cells: list[dict], cell_id: str, after_id: str) -> None:
    cell = find(cells, cell_id)
    cells.remove(cell)
    cells.insert(cells.index(find(cells, after_id)) + 1, cell)


def sustained_time(values: np.ndarray, dt: float, threshold: float, hold: float) -> float:
    """First time the raw coherence remains above threshold for the full hold interval."""
    width = max(1, int(round(hold / dt)))
    valid = np.convolve((values >= threshold).astype(int), np.ones(width, dtype=int), mode="valid")
    hits = np.flatnonzero(valid == width)
    return float(hits[0] * dt) if hits.size else np.nan


def make_run_summary_figure() -> None:
    rng = np.random.default_rng(3024)
    n, runs, coupling, sigma = 100, 16, 2.05, 0.72
    dt, duration = 0.03, 34.0
    threshold, hold = 0.80, 1.5
    times = np.arange(0.0, duration + dt, dt)
    histories = []
    for _ in range(runs):
        omega = rng.normal(3.0, sigma, n)
        theta = rng.uniform(0.0, 2 * np.pi, n)
        history = np.empty(times.size)
        for k in range(times.size):
            z = np.mean(np.exp(1j * theta))
            history[k] = abs(z)
            theta += dt * (omega + coupling * np.imag(z * np.exp(-1j * theta)))
        histories.append(history)
    histories = np.asarray(histories)
    late = times >= 26.0
    r_inf = histories[:, late].mean(axis=1)
    t_sync = np.array([sustained_time(row, dt, threshold, hold) for row in histories])

    apply_course_figure_style()
    fig, axes = plt.subplots(1, 3, figsize=(13.4, 4.45), constrained_layout=True,
                             gridspec_kw={"width_ratios": [1.8, 0.9, 0.9]})
    ax = axes[0]
    for row, crossing in zip(histories, t_sync):
        ax.plot(times, row, color=LIGHT_BLUE, alpha=0.42, lw=1.0)
        if np.isfinite(crossing):
            idx = int(round(crossing / dt))
            ax.scatter(crossing, row[idx], s=18, color=YELLOW, edgecolor=INK,
                       linewidth=0.45, zorder=4)
    ax.axhline(threshold, color=YELLOW, ls="--", lw=2,
               label=rf"threshold $r={threshold:.2f}$")
    ax.axvspan(26.0, duration, color=ORANGE, alpha=0.10,
               label=r"window for $r_\infty$")
    ax.set(xlabel="Simulation time", ylabel=r"Coherence, $r(t)$", ylim=(0, 1.03),
           title="Repeated runs retain different transients")
    ax.legend(frameon=False, loc="lower center", ncol=2, fontsize=10,
              bbox_to_anchor=(0.5, 0.01))
    finish_axes(ax)

    order = np.argsort(r_inf)
    axes[1].scatter(np.arange(1, runs + 1), r_inf[order], s=43, color=BLUE,
                    edgecolor=INK, linewidth=0.6)
    axes[1].set(xlabel="Run", ylabel=r"Late-time coherence, $r_\infty$",
                ylim=(0, 1.03), title="Amount of synchrony")
    finish_axes(axes[1])

    finite = np.isfinite(t_sync)
    order = np.argsort(t_sync[finite])
    axes[2].scatter(np.arange(1, finite.sum() + 1), t_sync[finite][order], s=43,
                    color=ORANGE, edgecolor=INK, linewidth=0.6)
    axes[2].set(xlabel="Synchronised run", ylabel=r"Time to synchrony, $t_{\rm sync}$",
                title="Speed of synchrony")
    finish_axes(axes[2])
    fig.savefig(IMAGES / "kuramoto_run_summaries.svg", transparent=True)
    plt.close(fig)


lecture = load(LECTURE)
cells = lecture["cells"]

# Separate the Reader section banner from the definition of collective coherence.
# This allows the individual-frequency analysis to precede the collective summary.
quantitative = find(cells, "reader-quantitative-analysis")
quantitative_text = "".join(quantitative["source"])
coherence_heading = "### Measure collective coherence"
if coherence_heading in quantitative_text:
    coherence_text = coherence_heading + quantitative_text.split(coherence_heading, 1)[1]
    quantitative["source"] = lines("## Quantitative analysis")
    coherence = {
        "cell_type": "markdown",
        "id": "w6-reader-coherence",
        "metadata": {"tags": ["reader-only"]},
        "source": lines(coherence_text),
    }
    old = next((cell for cell in cells if cell.get("id") == "w6-reader-coherence"), None)
    if old is not None:
        cells.remove(old)
    cells.insert(cells.index(quantitative) + 1, coherence)

# Slides: individual rates, collective coherence, one-run summaries, sweeps, ensembles.
move_after(cells, "w6-frequency-heterogeneity-slide", "w6-quantitative-analysis")
move_after(cells, "w6-order", "w6-frequency-heterogeneity-slide")
move_after(cells, "w6-long-time-summary-motivation-slide", "w6-order")
move_after(cells, "w6-long-time-summary-choices-slide", "w6-long-time-summary-motivation-slide")
move_after(cells, "w6-sweep", "w6-long-time-summary-choices-slide")
move_after(cells, "w6-finite-large-n-slide", "w6-sweep")
move_after(cells, "w6-heterogeneity-width-sweep-slide", "w6-finite-large-n-slide")
move_after(cells, "w6-ensemble-reporting-slide", "w6-heterogeneity-width-sweep-slide")

# Reader: retain the detailed phase/coherence view, then follow the same hierarchy.
move_after(cells, "w6-realised-frequency-analysis-reader", "reader-quantitative-analysis")
move_after(cells, "w6-reader-coherence", "w6-realised-frequency-analysis-reader")
move_after(cells, "order-parameter", "w6-reader-coherence")
move_after(cells, "w6-long-time-summary-reader", "order-parameter")
move_after(cells, "parameter-sweep", "w6-long-time-summary-reader")
move_after(cells, "w6-onset-analysis-reader", "parameter-sweep")
move_after(cells, "w6-heterogeneity-width-sweep-reader", "w6-onset-analysis-reader")
move_after(cells, "w6-ensemble-reporting-reader", "w6-heterogeneity-width-sweep-reader")

find(cells, "w6-realised-frequency-analysis-reader")["metadata"]["tags"] = ["reader-only"]
find(cells, "w6-long-time-summary-motivation-slide")["source"] = lines(r'''## Decide how to summarise the behaviour

<img src="images/kuramoto_run_summaries.svg" alt="Repeated Kuramoto coherence histories summarised by long-time coherence and time to sustained synchrony" style="display:block;width:96%;max-height:475px;margin:0 auto">

The yellow points use the same rule as the time-to-synchrony panel: the first time that $r\geq0.80$ continuously for 1.5 time units.''')
find(cells, "w6-long-time-summary-choices-slide")["source"] = lines(r'''## More than one defensible summary

| Summary | Question answered |
|---|---|
| $r_\infty$ | How coherent is the late-time state? |
| late-time variability | Does coherence remain steady? |
| $t_{\rm sync}$ | How quickly is sustained synchrony reached? |
| fraction synchronised by a deadline | How reliably does it occur? |

The threshold, persistence interval and late-time window must be stated. They are part of the analysis, not hidden plotting choices.''')
find(cells, "w6-mean-field-return")["source"] = lines(r'''# Analytical mean-field analysis

## What this adds

The numerical ensemble describes selected finite populations and observation times. The analytical calculation asks where coherence should begin in an idealised infinite, all-to-all population with a known frequency distribution.

It can expose a mechanism and predict a critical coupling. It does not retain finite-population fluctuations, transient times, irregular networks, noise or a particular initial condition.

The first rewriting is exact:

$$
r(t)e^{\mathrm{i}\psi(t)}=\dfrac{1}{N}\sum_{j=1}^{N}e^{\mathrm{i}\theta_j(t)}.
$$

The approximation comes when the finite sample is replaced by a continuum frequency distribution.

<div class="ladder-marker"><img src="images/ladder_marker.svg" alt="Ladder of abstraction"><span><strong>Up the ladder:</strong> replace a finite frequency sample by a population density.</span></div>''')
find(cells, "w6-long-time-summary-reader")["source"] = lines(r'''### Decide how to summarise the behaviour

<img src="images/kuramoto_run_summaries.svg" alt="Repeated Kuramoto coherence histories summarised by long-time coherence and time to sustained synchrony" style="display:block;width:94%;max-width:1150px;margin:1rem auto">

Repeated simulations do not pass through their transients at exactly the same time. Reading the final stored value of $r(t)$ would make the result depend on an arbitrary stopping time. Before comparing runs, state how the transient is excluded and what feature of the remaining history is retained.

- A **late-time window mean**, denoted $r_\infty$ here, estimates sustained coherence.
- **Late-time variability** distinguishes a steady locked state from persistent collective fluctuations.
- **Time to synchrony**, $t_{\rm sync}$, records how quickly a stated and sustained level of coherence is reached.
- The **fraction synchronised by a deadline** retains runs that never meet the criterion rather than silently discarding them.

In the figure, $t_{\rm sync}$ is the first time at which the raw coherence remains at or above $0.80$ for 1.5 consecutive time units. The yellow points mark those same events on the histories. The late-time summary $r_\infty$ is the mean over the shaded window. A different threshold or persistence interval is possible, but it must be applied consistently and reported.

The stationary Kuramoto calculation below concerns sustained long-time coherence, so $r_\infty$ is appropriate there. A study of speed or reliability also needs $t_{\rm sync}$ or a deadline-based summary.

<div class="ladder-marker"><img src="images/ladder_marker.svg" alt="Ladder of abstraction"><span><strong>Up the ladder:</strong> compress each history into a summary chosen for the question. <strong>Down the ladder:</strong> return to the histories to check what the threshold and transient rule have concealed.</span></div>''')

parameter_text = "".join(find(cells, "parameter-sweep")["source"])
parameter_text = re.sub(r"^#+ (?:Numerical parameter sweep|Parameter sweeps)(?:\n\n#+ Sweep coupling and population size)?",
                        "### Parameter sweeps\n\n#### Sweep coupling and population size",
                        parameter_text)
find(cells, "parameter-sweep")["source"] = lines(parameter_text)

onset_text = re.sub(r"^#+ What changes with \$N\$\?", "##### What changes with $N$?",
                    "".join(find(cells, "w6-onset-analysis-reader")["source"]))
find(cells, "w6-onset-analysis-reader")["source"] = lines(onset_text)

heterogeneity_text = re.sub(r"^#+ Sweep the heterogeneity", "#### Sweep the heterogeneity",
                            "".join(find(cells, "w6-heterogeneity-width-sweep-reader")["source"]))
find(cells, "w6-heterogeneity-width-sweep-reader")["source"] = lines(heterogeneity_text)

find(cells, "mean-field")["source"] = lines(r'''## Analytical mean-field analysis

### What the analytical result adds

The numerical analysis tells us what happened for chosen values of $N$, a finite observation time, sampled frequencies and a particular parameter grid. The analytical calculation asks a broader question: for an idealised infinite all-to-all population with a known frequency distribution, where should collective coherence begin and how should it depend on $K$?

This is useful when we want a mechanism, a critical coupling or a result that is not tied to one finite simulation. It is less useful when finite-population fluctuations, transient times, an irregular interaction network, noise or a particular initial condition are central. The calculation therefore provides a benchmark for the numerical ensemble rather than replacing it.

### Exact collective-field rewriting

The first reduction is exact for the finite all-to-all model:

$$
r(t)e^{\mathrm{i}\psi(t)}=\dfrac{1}{N}\sum_{j=1}^{N}e^{\mathrm{i}\theta_j(t)}.
$$

Multiplying by $e^{-\mathrm{i}\theta_i}$ and taking imaginary parts gives

$$
r(t)\sin(\psi(t)-\theta_i)
=\dfrac{1}{N}\sum_{j=1}^{N}\sin(\theta_j-\theta_i),
$$

and hence

$$
\dot\theta_i=\omega_i+Kr(t)\sin(\psi(t)-\theta_i).
$$

The continuum step is different: one sampled frequency list is replaced by a population density $g(\omega)$. A stationary calculation then replaces $r(t)$ by its long-time value $r_\infty$. For a symmetric unimodal distribution centred at $\bar\omega$, the onset occurs at

$$
K_c=\frac{2}{\pi g(\bar\omega)}.
$$

This result is quoted rather than required as a student derivation. Obtaining it needs the continuum self-consistency argument below. See [Strogatz (2000), “From Kuramoto to Crawford”](https://doi.org/10.1016/S0167-2789(00)00094-4).

```{dropdown} Optional derivation sketch
Work in the rotating frame so that $\bar\omega=0$. A frequency-locked oscillator satisfies

$$
\omega=Kr\sin\theta.
$$

Only oscillators with $|\omega|\le Kr$ can lock. For a symmetric $g(\omega)$, the drifting oscillators cancel in the stationary average and the locked population gives

$$
r=\int_{-Kr}^{Kr}\sqrt{1-\left(\frac{\omega}{Kr}\right)^2}\,g(\omega)\,\mathrm d\omega.
$$

Set $\omega=Kr\sin\theta$:

$$
1=K\int_{-\pi/2}^{\pi/2}\cos^2\theta\,g(Kr\sin\theta)\,\mathrm d\theta.
$$

At onset, $r\to0^+$, so $g(Kr\sin\theta)\to g(0)$. Since

$$
\int_{-\pi/2}^{\pi/2}\cos^2\theta\,\mathrm d\theta=\frac{\pi}{2},
$$

we obtain $K_c=2/[\pi g(0)]$.
```

<div class="ladder-marker"><img src="images/ladder_marker.svg" alt="Ladder of abstraction"><span><strong>Up the ladder:</strong> replace one finite frequency sample by the population density <i>g</i>(<i>ω</i>).</span></div>''')

# Use omega-infinity for each oscillator's realised long-time rate; reserve Omega for a common group rate.
for cell in cells:
    src = "".join(cell.get("source", []))
    src = src.replace(r"$\Omega_i$", r"$\omega_i^\infty$")
    src = src.replace(r"$\Omega_i=\omega_i$", r"$\omega_i^\infty=\omega_i$")
    src = src.replace("a moving average of $r(t)$ remains above $0.75$",
                      "the raw coherence $r(t)$ remains above $0.75$")
    cell["source"] = lines(src)

save(LECTURE, lecture)

workshop = load(WORKSHOP)
for cell in workshop["cells"]:
    src = "".join(cell.get("source", []))
    src = src.replace(r"$\Omega_i$", r"$\omega_i^\infty$")
    src = src.replace(r"$\Omega_i=\omega_i$", r"$\omega_i^\infty=\omega_i$")
    cell["source"] = lines(src)
save(WORKSHOP, workshop)

make_run_summary_figure()
