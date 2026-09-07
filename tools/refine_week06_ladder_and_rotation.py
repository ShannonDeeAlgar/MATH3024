"""Clarify the two levels of numerical compression in Week 6."""

import json
from pathlib import Path


BOOK = Path(__file__).resolve().parents[1]
PATH = BOOK / "notebooks/week06/L_Synchronisation.ipynb"
data = json.loads(PATH.read_text())
cells = data["cells"]
by_id = {cell.get("id"): cell for cell in cells}


def set_source(cell_id: str, source: str) -> None:
    by_id[cell_id]["source"] = source.strip().splitlines(keepends=True)


set_source("w6-watch", r'''
## From individual phases to collective coherence

<img src="images/kuramoto_phase_trajectories_coherence.svg" alt="Individual Kuramoto phase trajectories, their mean phase and the resulting collective coherence" style="display:block;max-height:500px;max-width:96%;margin:0 auto">

The faint curves retain the individual phase histories. Their circular average gives the mean phase $\psi(t)$ and the coherence $r(t)$.

<div class="ladder-marker"><img src="images/ladder_marker.svg" alt="Ladder of abstraction"><span><strong>Up the ladder:</strong> replace many phase trajectories by the collective variables $\psi(t)$ and $r(t)$.</span></div>
''')

set_source("w6-order", r'''
## Measure collective coherence

$$
r e^{\mathrm{i}\psi}=rac{1}{N}\sum_{j=1}^{N}e^{\mathrm{i}\theta_j}
$$

$\psi$ is the population's mean phase. The magnitude $r$ records how tightly phases cluster around it: $r\approx0$ for cancellation around the circle and $r\approx1$ for strong phase alignment.

This is the phase-oscillator counterpart of the polarisation order parameter used for Vicsek agents. Both are magnitudes of an average of unit direction vectors.
''')

set_source("w6-sweep", r'''
## Numerical parameter sweep

<div class="two-panel wide-left compact-panels">
<div class="image-panel"><img src="images/kuramoto_numerical_sweep.svg" alt="Numerical Kuramoto parameter sweeps for three finite system sizes"></div>
<div class="text-panel">
<p>Each curve comes from direct simulation of the finite oscillator model.</p>
<p>Natural frequencies follow 𝒩(0, 1). Points are ensemble means; bands show one standard deviation.</p>
<p>Increasing <i>N</i> reduces finite-population fluctuations and clarifies the onset of collective coherence.</p>
</div>
</div>

<div class="ladder-marker"><img src="images/ladder_marker.svg" alt="Ladder of abstraction"><span><strong>Up the ladder twice:</strong> first replace each run by its long-time coherence $r_\infty$; then compare those summaries across $K$, $N$ and repeated populations.</span></div>
''')

set_source("kuramoto-video", r'''
## From individual phases to collective coherence

<img src="images/kuramoto_phase_trajectories_coherence.svg" alt="Individual Kuramoto phase trajectories, their mean phase and the resulting collective coherence" style="display:block;max-width:100%;margin:auto">

The faint curves retain individual phase histories. Their circular average gives the mean phase $\psi(t)$ and coherence $r(t)$. This is the first upward move in the analysis: many trajectories become two collective time series.
''')

set_source("order-parameter", r'''
### Measure collective coherence

The complex order parameter is

$$
r(t)e^{\mathrm{i}\psi(t)}
=\frac{1}{N}\sum_{j=1}^{N}e^{\mathrm{i}\theta_j(t)}.
$$

- $\psi$ is the population's mean phase;
- $r\in[0,1]$ measures concentration around that mean;
- $r\approx0$ means phases are spread around the circle;
- $r\approx1$ means phases are tightly clustered.

This is the same circular average used for polarisation in Week 5.

<div class="ladder-marker"><img src="images/ladder_marker.svg" alt="Ladder of abstraction"><span><strong>Up the ladder:</strong> replace the full phase configuration by the collective variables $\psi(t)$ and $r(t)$.</span></div>
''')

set_source("parameter-sweep", r'''
### Sweep coupling and system size

<img src="images/kuramoto_numerical_sweep.svg" alt="Numerical Kuramoto parameter sweeps for three finite system sizes">

These curves come from direct numerical integration of the finite Kuramoto model, not from the mean-field calculation. Natural frequencies are sampled from $\mathcal N(0,1)$. For each coupling strength, each run is first reduced to its long-time coherence $r_\infty$. Those values are then summarised across independently sampled populations and initial phases. The bands show one standard deviation.

The figure uses 14 repeats for $N=60$, 10 for $N=180$, and 6 for $N=600$. Increasing $N$ reduces the residual coherence below onset and makes the transition easier to locate, but also raises the computational cost.

<div class="ladder-marker"><img src="images/ladder_marker.svg" alt="Ladder of abstraction"><span><strong>Up the ladder twice:</strong> phase trajectories become $r_\infty$ for one run; repeated runs then become an ensemble curve across $K$ and $N$.</span></div>
''')

# The old vector diagram repeats information now shown directly against trajectories.
cells[:] = [cell for cell in cells if cell.get("id") != "order-geometry"]

reader = "".join(by_id["w6-controlled-heterogeneity-reader"]["source"])
reader = reader.replace(
    "The baseline gives every oscillator the same natural frequency. In a frame rotating at that common frequency, the intrinsic drift disappears.",
    "The baseline gives every oscillator the same natural frequency. The group still rotates at that common rate in the laboratory frame. We often subtract that shared rate and work in a co-rotating frame, where the intrinsic drift appears to disappear."
)
reader = reader.replace(
    "**Natural-frequency heterogeneity:** draw $\\omega_i$ from $g(\\omega)$ while keeping a common $K$.",
    "**Natural-frequency heterogeneity:** draw $\\omega_i$ from a distribution centred on a non-zero population rate while keeping a common $K$. The centred-at-zero form used in analysis is the equivalent co-rotating frame."
)
by_id["w6-controlled-heterogeneity-reader"]["source"] = reader.splitlines(keepends=True)

slide = "".join(by_id["w6-frequency-heterogeneity-slide"]["source"])
slide = slide.replace(
    "Coupling changes realised phase velocities, not the assigned natural frequencies.",
    "The distribution is centred at a non-zero rate, so the locked group keeps rotating. Coupling changes realised phase velocities, not the assigned natural frequencies."
)
by_id["w6-frequency-heterogeneity-slide"]["source"] = slide.splitlines(keepends=True)

PATH.write_text(json.dumps(data, indent=1, ensure_ascii=False) + "\n")

