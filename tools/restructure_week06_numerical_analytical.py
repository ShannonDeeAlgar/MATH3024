#!/usr/bin/env python3
"""Separate Week 6 numerical experiments from analytical mean-field analysis."""

from __future__ import annotations

import json
from pathlib import Path


PATH = Path("notebooks/week06/L_Synchronisation.ipynb")


def lines(text: str) -> list[str]:
    return text.splitlines(keepends=True)


def main() -> None:
    notebook = json.loads(PATH.read_text())
    cells = notebook["cells"]
    by_id = {cell.get("id"): cell for cell in cells}

    # Slides
    by_id["w6-66a5febb56"]["source"] = lines("# Numerical experiments\n")
    by_id["w6-order"]["source"] = lines(r"""## Measure collective coherence

$$
r(t)e^{\mathrm{i}\psi(t)}
=\frac{1}{N}\sum_{j=1}^{N}e^{\mathrm{i}\theta_j(t)}
$$

<div class="two-panel equal-panels compact-panels">
<div class="text-panel"><p><strong>$\psi$:</strong> mean phase.</p><p><strong>$r\approx0$:</strong> phases cancel around the circle.</p><p><strong>$r\approx1$:</strong> phases are tightly aligned.</p></div>
<div class="image-panel"><img src="images/kuramoto_order_parameter_geometry.svg" alt="Complex phase vectors and their average" style="max-height:330px"></div>
</div>
""")
    by_id["w6-sweep"]["source"] = lines(r"""## Numerical parameter sweep

<div class="two-panel wide-left compact-panels">
<div class="image-panel"><img src="images/kuramoto_numerical_sweep.svg" alt="Numerical Kuramoto parameter sweeps for three finite system sizes"></div>
<div class="text-panel">
<p>Each curve comes from direct simulation of the finite oscillator model.</p>
<p>Natural frequencies follow $\mathcal N(0,1)$. Points are ensemble means; bands show one standard deviation.</p>
<p>Increasing $N$ reduces finite-population fluctuations and clarifies the onset of collective coherence.</p>
</div>
</div>
""")
    by_id["w6-finite-large-n-slide"]["source"] = lines(r"""## What changes with $N$?

**Finite populations:** sampled frequencies and initial phases differ between runs. The onset is noisy and rounded.

**Larger populations:** the ensemble curve becomes more stable and the residual coherence below onset decreases.

A numerical conclusion therefore depends on system size, simulation time and the number of repeats.

<div class="discussion-marker"><img src="images/discussion_marker.svg" alt="Discussion prompt"><span>Which of these quantities would you hold fixed when comparing two coupling strengths?</span></div>
""")
    by_id["w6-mean-field-return"]["source"] = lines(r"""# Analytical mean-field analysis

## Return to mean field

The numerical sweep shows what finite populations do. We now ask whether the onset can be predicted without simulating every oscillator.

For all-to-all coupling, the complex order parameter stores exactly the collective quantities used by the interaction term:

$$
r e^{i\psi}=\frac{1}{N}\sum_{j=1}^{N}e^{i\theta_j}.
$$

Here the reduction is an exact rewriting of the finite model. The analytical threshold requires the additional large-population limit.
""")
    by_id["w6-mean-field-return"]["metadata"]["slideshow"]["slide_type"] = "slide"
    by_id["w6-ensemble"]["source"] = lines(r"""## Compare mean field with simulation

<div class="two-panel wide-left compact-panels">
<div class="image-panel"><img src="images/kuramoto_meanfield_comparison.svg" alt="Continuum Kuramoto mean-field curve compared with a finite numerical ensemble"></div>
<div class="text-panel">
<p>The grey curve is the direct numerical ensemble for $N=600$.</p>
<p>The orange curve solves the continuum self-consistency equation for the same standard-normal frequency distribution.</p>
<p>The dashed line marks $K_c=2/[\pi g(0)]$. Finite populations round the analytical onset.</p>
</div>
</div>
""")

    slide_ids = [
        "w6-66a5febb56", "w6-watch", "w6-order", "w6-sweep",
        "w6-finite-large-n-slide", "w6-mean-field-return", "w6-mean-field",
        "w6-heterogeneity-analysis-slide", "w6-ensemble",
    ]
    slide_cells = [by_id[cell_id] for cell_id in slide_ids]
    slide_positions = [cells.index(cell) for cell in slide_cells]
    insert_at = min(slide_positions)
    cells = [cell for cell in cells if cell not in slide_cells]
    cells[insert_at:insert_at] = slide_cells

    # Reader
    by_id = {cell.get("id"): cell for cell in cells}
    by_id["w6-e3d28ed62b"]["source"] = lines("# Analysis\n\n## Numerical experiments\n")
    by_id["order-parameter"]["source"] = lines(r"""### Measure collective coherence

The complex order parameter is

$$
r(t)e^{\mathrm{i}\psi(t)}
=\frac{1}{N}\sum_{j=1}^{N}e^{\mathrm{i}\theta_j(t)}.
$$

- $\psi$ is the mean phase;
- $r\in[0,1]$ measures concentration around that mean;
- $r\approx0$ means phases are spread around the circle;
- $r\approx1$ means phases are tightly clustered.

This is the same circular average used for polarisation in Week 5.
""")
    by_id["order-geometry"]["source"] = lines(r"""### Geometric interpretation

<div class="two-panel equal-panels">
<div class="image-panel"><img src="images/kuramoto_order_parameter_geometry.svg" alt="Phase vectors and their complex average"></div>
<div class="text-panel">
<p>Each phase contributes a unit vector.</p>
<p>Their vector average has direction $\psi$ and magnitude $r$.</p>
<p>Cancellation produces low coherence; alignment produces high coherence.</p>
</div>
</div>

*Order-parameter definition as in Strogatz (2000), Physica D 143, 1–20.*
""")
    by_id["parameter-sweep"]["source"] = lines(r"""### Sweep coupling and system size

<img src="images/kuramoto_numerical_sweep.svg" alt="Numerical Kuramoto parameter sweeps for three finite system sizes">

These curves come from direct numerical integration of the finite Kuramoto model, not from the mean-field calculation. Natural frequencies are sampled from $\mathcal N(0,1)$. For each coupling strength, the long-time coherence is averaged over independently sampled populations and initial phases. The bands show one standard deviation.

The figure uses 14 repeats for $N=60$, 10 for $N=180$, and 6 for $N=600$. Increasing $N$ reduces the residual coherence below onset and makes the transition easier to locate, but increasing $N$ also raises the computational cost.

<div class="ladder-marker"><img src="images/ladder_marker.svg" alt="Ladder of abstraction"><span><strong>Up the ladder over coupling and system size:</strong> replace many phase trajectories by long-time ensemble summaries.</span></div>
""")
    by_id["w6-onset-analysis-reader"]["source"] = lines(r"""### What changes with $N$?

For finite $N$, the sampled frequencies and initial phases differ between runs. Even below the onset of collective locking, random phase imbalance leaves $r$ small but non-zero, with fluctuations of typical scale $N^{-1/2}$. The observed transition is therefore rounded and its estimated location varies between samples.

A defensible numerical sweep should report the frequency distribution, system size, integration time, transient removed, and number of repeats. Comparing several $N$ values helps distinguish a robust population-level pattern from a finite-system feature.
""")
    by_id["mean-field"]["source"] = lines(r"""## Analytical mean-field analysis

### Return to mean field

The numerical sweep describes finite populations. Mean-field analysis asks whether the collective onset can be predicted without following every trajectory.

We used a mean-field description for the Game of Life in Week 4. There it was an approximation: replacing a neighbourhood by the global live-cell density discarded spatial correlations.

For the standard all-to-all Kuramoto model, the first reduction is exact. Every oscillator already couples to a sum over the entire population, and

$$
r e^{i\psi}=\frac{1}{N}\sum_{j=1}^{N}e^{i\theta_j}.
$$

Multiplying by $e^{-i\theta_i}$ and taking imaginary parts gives

$$
r\sin(\psi-\theta_i)
=\frac{1}{N}\sum_{j=1}^{N}\sin(\theta_j-\theta_i),
$$

so the finite model becomes

$$
\dot\theta_i=\omega_i+Kr\sin(\psi-\theta_i).
$$

The large-population calculation then replaces one sampled frequency list by a density $g(\omega)$. For a symmetric unimodal distribution,

$$
K_c=\frac{2}{\pi g(\bar\omega)},
$$

where $\bar\omega$ is the centre of the distribution. This continuum step produces the sharp analytical onset.
""")
    by_id["reader-mean-field-limits"]["source"] = lines("The reduction relies on all-to-all sinusoidal coupling. Sparse networks, unequal weights, time delays, noise, or higher-order interactions require different analysis and can produce different collective states.\n")
    by_id["ensemble"]["source"] = lines(r"""### Compare analytical and numerical results

<img src="images/kuramoto_meanfield_comparison.svg" alt="Continuum Kuramoto mean-field curve compared with a finite numerical ensemble">

The grey curve is the numerical ensemble for $N=600$. The orange curve is obtained by solving the continuum self-consistency equation for the same standard-normal frequency distribution. The dashed line marks

$$
K_c=\frac{2}{\pi g(0)}=\sqrt{\frac{8}{\pi}}.
$$

The mean-field result predicts the location and shape of the large-population onset. The finite simulations approach that result but retain sampling variation and a rounded transition. Placing both on the same axes makes clear which conclusions come from simulation and which come from analysis.
""")

    reader_ids = [
        "w6-e3d28ed62b", "kuramoto-video", "w6-3465fc0be5", "order-parameter",
        "order-geometry", "parameter-sweep", "w6-onset-analysis-reader", "mean-field",
        "reader-mean-field-limits", "ensemble",
    ]
    reader_cells = [by_id[cell_id] for cell_id in reader_ids]
    positions = [cells.index(cell) for cell in reader_cells]
    insert_at = min(positions)
    cells = [cell for cell in cells if cell not in reader_cells]
    cells[insert_at:insert_at] = reader_cells

    notebook["cells"] = cells
    PATH.write_text(json.dumps(notebook, indent=1, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
