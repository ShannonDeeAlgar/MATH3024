"""Separate Week 6 model specification from later analysis and variants."""

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "notebooks/week06/L_Synchronisation.ipynb"


def src(text):
    return [line + "\n" for line in text.rstrip().splitlines()]


nb = json.loads(PATH.read_text())
cells = nb["cells"]
by_id = {cell.get("id"): cell for cell in cells}

# A chance crossing is part of the definition of synchronisation, not a
# qualification of the later network variant.
by_id["reader-locking"]["source"] = src(r"""
Phase locking means a constant phase difference and a common long-term frequency. It does not require equal phases. Occasional alignment is not enough: the interaction must alter the dynamics and maintain a relationship between the timings. When $|\Delta\omega|>K$, the coupling is too weak to overcome the mismatch and the phase difference continues to drift.
""")

# Specify the frequency population before beginning the analysis. This first
# figure deliberately contains no realised-rate annotations.
early_reader = by_id["w6-natural-frequency-before-analysis-reader"]
early_reader["source"] = src(r"""
## Natural-frequency distribution

The natural frequencies are part of the model specification. In the numerical examples we use

$$
\omega_i\sim\mathcal N(3,0.65^2).
$$

The centre sets the population's average rotation rate in the laboratory frame. Its width sets the heterogeneity that coupling must overcome.

<img src="images/kuramoto_natural_frequency_distribution.svg" alt="Histogram of natural frequencies assigned to the Kuramoto oscillators" style="display:block;width:56%;max-width:620px;margin:0.8rem auto">

It is often simpler to analyse the same population in a frame rotating at the population mean $\Omega_0=3$. Defining $\nu_i=\omega_i-\Omega_0$ gives a zero-centred distribution. This change of coordinates removes a rotation shared by the whole population; it does not change phase differences, coherence or the coupling at which locking begins.
""")

early_slide = by_id["w6-natural-frequency-before-analysis-slide"]
early_slide["source"] = src(r"""
## Natural-frequency distribution

<div class="two-panel compact-panels">
<div class="image-panel"><img src="images/kuramoto_natural_frequency_distribution.svg" alt="Histogram of assigned natural frequencies" style="max-height:405px"></div>
<div class="text-panel"><p>Each oscillator is assigned a natural frequency <i>ω</i><sub>i</sub> drawn from <i>g</i>(<i>ω</i>).</p><p>The centre sets the population's mean rotation rate.</p><p>The width sets the heterogeneity that coupling must overcome.</p></div>
</div>
""")

# Qualitative analysis is the section name; the animation is its content rather
# than another competing header.
by_id["w6-watch"]["source"] = src(r"""
# Qualitative analysis

<img src="images/kuramoto_phase_circle.gif" alt="Kuramoto oscillators moving around the phase circle and organising under coupling" style="display:block;max-height:350px;max-width:70%;width:auto;margin:0 auto">

This is a **phase-circle display**: angle around the circle is the oscillator phase $\theta_i$. It is a picture of the model's phase space, not a map of physical positions. At this level we retain every oscillator and watch how the phases reorganise.
""")
by_id["kuramoto-video"]["source"] = src(r"""
## Qualitative analysis

<img src="images/kuramoto_phase_circle.gif" alt="Kuramoto oscillators moving around the phase circle and organising under coupling" style="display:block;width:34%;max-width:330px;margin:0.7rem auto">

This is a **phase-circle display**. The angle around the circle records phase $\theta_i$; it is not a map of physical position. The moving display retains every oscillator, so clustering and frequency locking remain visible before we replace them with a collective summary.
""")

# Keep the standard model concise and point forward to the variants.
by_id["network-specification"]["source"] = src(r"""
### Standard all-to-all coupling

| Element | Kuramoto choice |
|---|---|
| Node state | phase $\theta_i$ |
| Internal dynamics | natural frequency $\omega_i$ |
| Network | complete graph |
| Interaction | sinusoidal phase attraction |
| Control parameter | coupling strength $K$ |
| Observable | phase coherence $r$ |

<div class="choice-marker"><img src="images/choice_marker.svg" alt="Modelling choice"><span>The complete graph and equal coupling weights simplify the system. Later we replace them with local, sparse and modular interaction networks.</span></div>
""")

# At first introduction, state the standard model and point forward. The
# physical meaning of different coupling mechanisms belongs with the later
# network variant rather than inside this assumptions slide.
by_id["w6-assumptions"]["source"] = src(r"""
## Kuramoto model · assumptions

| Element | Kuramoto choice |
|---|---|
| State | phase $\theta_i$ |
| Internal dynamics | natural frequency $\omega_i$ |
| Network | complete graph |
| Interaction | sinusoidal attraction |
| Control parameter | coupling $K$ |
| Observable | coherence $r$ |

<div class="choice-marker"><img src="images/choice_marker.svg" alt="Modelling choice"><span>The complete graph and equal coupling weights simplify the interaction. Later we replace them with local, sparse and modular networks.</span></div>
""")

by_id["w6-network-variant-slide"]["source"] = src(r"""
## Change the interaction network

Mechanical, electrical, chemical and informational coupling describe different physical systems. The network records who can influence whom.

$$
\dot{\theta}_i=\omega_i+\frac{K}{k_i}\sum_{j=1}^{N}A_{ij}\sin(\theta_j-\theta_i),
\qquad k_i=\sum_{j=1}^{N}A_{ij}.
$$

Here $A_{ij}=1$ when oscillator $j$ can influence oscillator $i$.

<div class="analysis-perspectives four">
<div><strong>Complete</strong><p>Every oscillator interacts with every other.</p></div>
<div><strong>Local</strong><p>Interaction is restricted by distance.</p></div>
<div><strong>Sparse</strong><p>Each oscillator has few neighbours.</p></div>
<div><strong>Modular</strong><p>Interaction is stronger within groups.</p></div>
</div>

Hold $g(\omega)$ and the coupling rule fixed while comparing networks.
""")

# Later analysis: now compare assigned frequencies with realised rates.
late_reader = {
    "cell_type": "markdown",
    "id": "w6-realised-frequency-analysis-reader",
    "metadata": {"slideshow": {"slide_type": "skip"}},
    "source": src(r"""
### Natural frequencies and realised rates

Coupling does not change an oscillator's assigned natural frequency. It changes the realised rate $\dot\theta_i$. Oscillators with low $\omega_i$ must speed up and those with high $\omega_i$ must slow down to join a frequency-locked group.

<img src="images/kuramoto_frequency_heterogeneity.gif" alt="Kuramoto phases coloured by natural frequency beside the frequency distribution and common realised rate" style="display:block;width:64%;max-width:720px;margin:1rem auto">

The animation reports $\Omega$, the population's realised mean angular velocity. For symmetric all-to-all coupling, the interaction terms cancel when averaged over all oscillators, so $\Omega$ equals the sample mean of the assigned $\omega_i$. A locked subgroup shares a common realised rate even though its members retain different natural frequencies.
"""),
}

late_slide = by_id["w6-frequency-heterogeneity-slide"]
late_slide["metadata"]["slideshow"]["slide_type"] = "subslide"

# Physical coupling mechanisms introduce the deliberate network variant.
network_reader = {
    "cell_type": "markdown",
    "id": "w6-network-variant-reader",
    "metadata": {"slideshow": {"slide_type": "skip"}},
    "source": src(r"""
### Change the interaction network

Mechanical, electrical, chemical and informational coupling describe different physical systems. Coupling may act one way or both ways, locally or globally, continuously or in pulses, immediately or after a delay. These features belong to the system being represented. The modeller decides how to encode them and which details can be omitted.

For a network rather than all-to-all coupling, let $A_{ij}$ record whether oscillator $j$ influences oscillator $i$, and let $w_{ij}$ give the strength of that influence. One normalised form is

$$
\dot{\theta}_i
=\omega_i
+\frac{K}{s_i}\sum_{j=1}^{N}A_{ij}w_{ij}\sin(\theta_j-\theta_i),
\qquad
s_i=\sum_{j=1}^{N}A_{ij}w_{ij}.
$$

The complete, equally weighted network recovers the standard Kuramoto interaction. Sparse, local or modular choices change who can coordinate with whom. Keep $g(\omega)$ and the coupling rule fixed when comparing these networks.
"""),
}

# In the exact finite-N rewriting the collective variables evolve in time. The
# stationary self-consistency calculation later uses r_infinity explicitly.
mean = ''.join(by_id["mean-field"]["source"])
mean = mean.replace(r"r e^{\mathrm{i}\psi}=", r"r(t)e^{\mathrm{i}\psi(t)}=")
mean = mean.replace(r"r\sin(\psi-\theta_i)", r"r(t)\sin(\psi(t)-\theta_i)")
mean = mean.replace(r"\dot\theta_i=\omega_i+Kr\sin(\psi-\theta_i)", r"\dot\theta_i=\omega_i+Kr(t)\sin(\psi(t)-\theta_i)")
mean = mean.replace("the first reduction is exact:", "the first reduction is exact and remains time dependent:")
mean = mean.replace("The large-population calculation then replaces", "A stationary calculation later replaces $r(t)$ by its long-time value $r_\\infty$ and replaces")
by_id["mean-field"]["source"] = src(mean)

# The exact collective field is dynamic in the finite model. Reserve
# r_infinity for the stationary/long-time calculation that follows.
by_id["w6-mean-field-return"]["source"] = src(r"""
# Analytical mean-field analysis

## Exact collective-field rewriting

The numerical sweep shows what finite populations do. We now ask whether the onset can be predicted without simulating every oscillator.

For all-to-all coupling, the order parameter stores the collective quantities already present in the interaction term:

$$
r(t)e^{i\psi(t)}=\dfrac{1}{N}\sum_{j=1}^{N}e^{i\theta_j(t)}.
$$

No approximation has been made at this stage. The approximation comes later, when a large population is represented by a continuous frequency distribution.

<div class="ladder-marker"><img src="images/ladder_marker.svg" alt="Ladder of abstraction"><span><strong>Up the ladder:</strong> replace a finite sample by a continuum frequency distribution.</span></div>
""")

by_id["w6-mean-field"]["source"] = src(r"""
## Rewrite the all-to-all interaction exactly

Multiply the order parameter by $e^{-i\theta_i(t)}$ and take its imaginary part:

$$
r(t)\sin\!\bigl(\psi(t)-\theta_i(t)\bigr)
=\dfrac{1}{N}\sum_{j=1}^{N}\sin\!\bigl(\theta_j(t)-\theta_i(t)\bigr).
$$

The finite model can therefore be written as

$$
\dot\theta_i(t)=\omega_i+Kr(t)\sin\!\bigl(\psi(t)-\theta_i(t)\bigr).
$$

This is an identity for all-to-all coupling. Both $r(t)$ and $\psi(t)$ continue to evolve. The stationary analysis later asks about their long-time behaviour.
""")

# Reorder slide and reader cells without otherwise disturbing content.
def move_after(cell, target_id):
    cells.remove(cell)
    idx = next(i for i, c in enumerate(cells) if c.get("id") == target_id)
    cells.insert(idx + 1, cell)

move_after(early_slide, "w6-assumptions")
move_after(early_reader, "kuramoto-equation")
move_after(late_slide, "w6-finite-large-n-slide")

# Add fresh reader cells if the script is re-run safely.
cells[:] = [c for c in cells if c.get("id") not in {late_reader["id"], network_reader["id"]}]
idx = next(i for i, c in enumerate(cells) if c.get("id") == "w6-onset-analysis-reader")
cells[idx + 1:idx + 1] = [late_reader, network_reader]

PATH.write_text(json.dumps(nb, indent=1, ensure_ascii=False) + "\n")
