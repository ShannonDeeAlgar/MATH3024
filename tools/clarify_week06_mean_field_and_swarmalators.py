"""Clarify the Week 6 collective-field argument and isolate the final explorable."""

import json
from pathlib import Path


path = Path(__file__).resolve().parents[1] / "notebooks/week06/L_Synchronisation.ipynb"
notebook = json.loads(path.read_text())
cells = notebook["cells"]
by_id = {cell.get("id"): cell for cell in cells}


def set_source(cell_id, text):
    by_id[cell_id]["source"] = text.splitlines(keepends=True)


set_source("w6-mean-field-return", r'''# Analytical large-population analysis

## Exact collective-field rewriting

The numerical sweep shows what finite populations do. We now ask whether the onset can be predicted without simulating every oscillator.

For all-to-all coupling, the order parameter stores exactly the collective quantities already present in the interaction term:

$$
r e^{i\psi}=\frac{1}{N}\sum_{j=1}^{N}e^{i\theta_j}.
$$

No approximation has been made at this stage. The additional approximation comes when a large population is represented by a continuous frequency distribution.

<div class="ladder-marker"><img src="images/ladder_marker.svg" alt="Ladder of abstraction"><span><strong>Up the ladder:</strong> replace one finite sample of frequencies by a population distribution.</span></div>
''')

set_source("w6-mean-field", r'''## Rewrite the all-to-all interaction exactly

Multiply the order parameter by $e^{-i\theta_i}$ and take its imaginary part:

$$
r\sin(\psi-\theta_i)
=\frac{1}{N}\sum_{j=1}^{N}\sin(\theta_j-\theta_i).
$$

The finite model can therefore be written as

$$
\dot\theta_i=\omega_i+Kr\sin(\psi-\theta_i).
$$

This is an identity for all-to-all coupling. It expresses the same finite system through its collective field $r e^{i\psi}$.
''')

set_source("w6-ensemble", r'''## Compare the analytical limit with simulation

<div class="two-panel wide-left compact-panels">
<div class="image-panel"><img src="images/kuramoto_meanfield_comparison.svg" alt="Large-population Kuramoto prediction compared with a finite numerical ensemble"></div>
<div class="text-panel">
<p>The grey curve is a direct numerical ensemble with <i>N</i> = 600.</p>
<p>The orange curve is the continuum, large-population prediction for the same standard-normal frequency distribution.</p>
<p>Here <i>g</i>(0) is the height of the frequency-density curve at its centre. The dashed line marks <i>K</i><sub>c</sub> = 2/[π<i>g</i>(0)].</p>
</div>
</div>
''')

set_source("mean-field", r'''## Analytical large-population analysis

### Exact rewriting first

The numerical sweep describes finite populations. We now ask whether the collective onset can be predicted without following every trajectory.

For all-to-all Kuramoto coupling, define

$$
r e^{\mathrm{i}\psi}=\frac{1}{N}\sum_{j=1}^{N}e^{\mathrm{i}\theta_j}.
$$

Multiplying by $e^{-\mathrm{i}\theta_i}$ and taking imaginary parts gives

$$
r\sin(\psi-\theta_i)
=\frac{1}{N}\sum_{j=1}^{N}\sin(\theta_j-\theta_i),
$$

so the finite model can be rewritten exactly as

$$
\dot\theta_i=\omega_i+Kr\sin(\psi-\theta_i).
$$

This is not a mean-field approximation: every oscillator already interacts with the whole population through this average.

The large-population analysis makes a further move. It replaces one sampled list of natural frequencies by a continuous density $g(\omega)$. For a symmetric unimodal distribution centred at $\bar\omega$, the predicted onset is

$$
K_c=\frac{2}{\pi g(\bar\omega)}.
$$

Here $g(\bar\omega)$ is the height of the natural-frequency density at its centre. A taller peak means that more oscillators have similar frequencies and less coupling is required for collective locking. In a frame rotating with $\bar\omega$, the centre is zero and the formula contains $g(0)$.

The threshold is quoted rather than derived in this unit. Its derivation uses a continuum self-consistency argument; see [Strogatz (2000), “From Kuramoto to Crawford”](https://doi.org/10.1016/S0167-2789(00)00094-4).

```{dropdown} Optional derivation sketch
Work in the rotating frame so that $\bar\omega=0$. A frequency-locked oscillator satisfies

$$
\omega=Kr\sin\theta.
$$

Only oscillators with $|\omega|\le Kr$ can lock. For a symmetric $g(\omega)$, the drifting oscillators cancel in the stationary average and the locked population gives

$$
r=\int_{-Kr}^{Kr}\sqrt{1-\left(\frac{\omega}{Kr}\right)^2}\,g(\omega)\,\mathrm d\omega.
$$

Setting $\omega=Kr\sin\theta$ gives

$$
1=K\int_{-\pi/2}^{\pi/2}\cos^2\theta\,g(Kr\sin\theta)\,\mathrm d\theta.
$$

At onset, $r\to0^+$, so $g(Kr\sin\theta)\to g(0)$. Since

$$
\int_{-\pi/2}^{\pi/2}\cos^2\theta\,\mathrm d\theta=\frac{\pi}{2},
$$

we obtain $K_c=2/[\pi g(0)]$.
```

### Where a mean-field approximation would enter

Suppose oscillator $i$ interacts only with neighbours in a network with adjacency matrix $A$. Its exact local field is

$$
z_i=\frac{1}{k_i}\sum_j A_{ij}e^{i\theta_j},
$$

where $k_i=\sum_j A_{ij}$ is its number of neighbours. Replacing every different local field $z_i$ by the same global field $r e^{i\psi}$ would be a genuine mean-field approximation. It may be useful for a dense, well-mixed network, but it removes spatial or community structure.

This is the Week 4 distinction in a new setting: the collective average is exact when the model itself is all-to-all, and approximate when it replaces heterogeneous local neighbourhoods.

<div class="ladder-marker"><img src="images/ladder_marker.svg" alt="Ladder of abstraction"><span><strong>Up the ladder:</strong> first replace one finite frequency sample by $g(\omega)$; for a locally coupled model, a further approximation would replace different local fields by one global field.</span></div>
''')

set_source("reader-mean-field-limits", "The large-population result assumes all-to-all sinusoidal coupling. Sparse networks, unequal weights, time delays, noise and higher-order interactions require different analysis and can produce different collective states.\n")

set_source("w6-swarmalators-slide", '''## Oscillators that sync and swarm

<iframe src="https://www.complexity-explorables.org/explorables/swarmalators/" title="Swårmalätørs explorable" style="display:block;width:100%;height:535px;border:1px solid #C7CEDC;margin:0 auto;" allowfullscreen></iframe>\n''')

# The explorable is the final lecture slide. Reader-only cells must not spill into it.
swarm_index = next(i for i, cell in enumerate(cells) if cell.get("id") == "w6-swarmalators-slide")
for cell in cells[swarm_index + 1:]:
    cell.setdefault("metadata", {}).setdefault("slideshow", {})["slide_type"] = "skip"

path.write_text(json.dumps(notebook, indent=1, ensure_ascii=False) + "\n")
