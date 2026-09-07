#!/usr/bin/env python3
import json
from pathlib import Path

PATH = Path("notebooks/week06/L_Synchronisation.ipynb")
nb = json.loads(PATH.read_text())
cells = nb["cells"]


def by_id(cell_id):
    return next(c for c in cells if c.get("id") == cell_id)


def set_source(cell_id, text):
    by_id(cell_id)["source"] = text.splitlines(keepends=True)


def move_after(cell_id, after_id):
    cell = by_id(cell_id)
    cells.remove(cell)
    cells.insert(cells.index(by_id(after_id)) + 1, cell)


set_source("w6-coordination-contrast-slide", r'''## Not all synchrony is self-organised

<div class="two-panel equal-panels compact-panels">
<div class="image-panel"><iframe width="560" height="315" src="https://www.youtube.com/embed/qsRmVtvbrAE" title="Choreographed synchronisation" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe></div>
<div class="text-panel"><img src="images/coordination_contrast.svg" alt="Choreographed coordination compared with spontaneous synchronisation" style="display:block;max-height:300px;max-width:100%;margin:0 auto"><p>Dance and synchronised swimming follow a rehearsed sequence and shared cues. Fireflies retain their own clocks and adjust through interaction.</p></div>
</div>
''')

set_source("w6-coordination-contrast-reader", r'''### Not all synchrony is self-organised

<div style="position:relative;padding-bottom:56.25%;height:0;overflow:hidden;margin:1rem 0;"><iframe src="https://www.youtube.com/embed/qsRmVtvbrAE" title="Choreographed synchronisation" style="position:absolute;top:0;left:0;width:100%;height:100%;border:0;" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe></div>

Dance and synchronised swimming can be precisely coordinated, but their timing follows choreography, rehearsal and shared cues. The systems studied here are different: each component retains its own dynamics and responds to the others. A common rhythm can then arise without a conductor.
''')

# This title now links back to the opening contrast.
s = "".join(by_id("w6-millennium-video-slide")["source"])
s = s.replace("## The wobbling Millennium Bridge", "## Not all synchrony is good")
by_id("w6-millennium-video-slide")["source"] = s.splitlines(keepends=True)

# Model transition: interpret the fireflies, then mark the model-details section,
# then pause to decide how a clock and a nudge should be represented.
move_after("w6-firefly-kuramoto", "w6-kuramoto-explorable")
move_after("w6-model-banner", "w6-firefly-kuramoto")
move_after("w6-specify", "w6-model-banner")
move_after("reader-firefly-kuramoto", "kuramoto-video-reader")
move_after("w6-e00ea3001e", "reader-firefly-kuramoto")
move_after("firefly-model", "w6-e00ea3001e")

# Raw HTML does not reliably pass dollar-delimited mathematics to MathJax.
for cell_id in ("w6-uncoupled", "w6-watch", "w6-order", "w6-sweep",
                "w6-coupling-heterogeneity-slide", "w6-ensemble",
                "uncoupled", "order-geometry"):
    c = by_id(cell_id)
    src = "".join(c["source"])
    replacements = {
        '$\\phi=\\theta_1-\\theta_2$': r'\(\phi=\theta_1-\theta_2\)',
        '$r$': r'\(r\)',
        '$\\psi$': r'\(\psi\)',
        '$\\mathcal N(0,1)$': r'\(\mathcal N(0,1)\)',
        '$N$': r'\(N\)',
        '$\\omega_i$': r'\(\omega_i\)',
        '$K_i$': r'\(K_i\)',
        '$N=600$': r'\(N=600\)',
    }
    for old, new in replacements.items():
        src = src.replace(old, new)
    c["source"] = src.splitlines(keepends=True)

# A sinusoidal waveform is a visualisation choice; Equation 1 only advances phase.
for cell_id in ("w6-one", "single-oscillator"):
    c = by_id(cell_id)
    src = "".join(c["source"])
    needle = "Kuramoto's sine is part of the coupling rule, not an assumed signal shape."
    replacement = ("Equation 1 specifies uniform phase advance; it does not make the observed signal sinusoidal. "
                   "An output $y=h(\\theta)$ may be sinusoidal, sawtooth-like or pulse-like. "
                   "Kuramoto's sine is part of the coupling rule, not an assumed signal shape.")
    if needle in src:
        src = src.replace("The phase does not specify the observed waveform. An output $y=h(\\theta)$ may be sinusoidal, sawtooth-like or pulse-like. " + needle, replacement)
        src = src.replace("The **waveform** is the observed output over one cycle. It can be written as $y=h(\\theta)$ and may be sinusoidal, sawtooth-like or pulse-like. The phase model stores $\\theta$, not the full function $h$ or changes in its amplitude. " + needle,
                          "The **waveform** is the observed output over one cycle. The phase model stores $\\theta$, not the full function $h$ or changes in its amplitude. " + replacement)
    c["source"] = src.splitlines(keepends=True)

set_source("w6-onset-analysis-reader", r'''### What changes with $N$?

For finite $N$, the sampled frequencies and initial phases differ between runs. Even below the onset of collective locking, random phase imbalance leaves $r$ small but non-zero. The $N$ unit vectors cancel imperfectly like a random walk: their resultant is typically of order $\sqrt{N}$, and dividing by $N$ leaves fluctuations of typical scale $N^{-1/2}$. This is a scaling estimate, not an exact value for every run.

The observed transition is therefore rounded and its estimated location varies between samples. A defensible numerical sweep should report the frequency distribution, system size, integration time, transient removed, and number of repeats. Comparing several $N$ values helps distinguish a robust population-level pattern from a finite-system feature.
''')

set_source("w6-coupling-heterogeneity-slide", r'''## Heterogeneous responsiveness

<div class="two-panel wide-left compact-panels">
<div class="image-panel"><img src="images/kuramoto_coupling_heterogeneity.svg" alt="Numerical simulation of oscillator groups with different coupling strengths" style="max-height:430px"></div>
<div class="text-panel"><p>First give all oscillators the same \(\omega_i\), then assign different \(K_i\).</p><p>The plotted offset is the mean wrapped angular distance from the instantaneous group phase \(\psi(t)\).</p><p>Larger \(K_i\) groups respond more strongly and approach \(\psi(t)\) faster.</p></div>
</div>
''')

set_source("w6-order", r'''## Measure collective coherence

$$
r e^{\mathrm{i}\psi}=\frac{1}{N}\sum_{j=1}^{N}e^{\mathrm{i}\theta_j}
$$

<div class="two-panel wide-left compact-panels">
<div class="image-panel"><img src="images/kuramoto_order_parameter_geometry.svg" alt="Phase vectors and their complex average" style="max-height:410px"></div>
<div class="text-panel"><p>\(\psi\): mean phase.</p><p>\(r\approx0\): phases cancel around the circle.</p><p>\(r\approx1\): phases are tightly aligned.</p><div class="ladder-marker"><img src="images/ladder_marker.svg" alt="Ladder of abstraction"><span><strong>Up the ladder:</strong> compress the phase configuration to one coherence measure.</span></div></div>
</div>
''')

c = by_id("w6-controlled-heterogeneity-reader")
src = "".join(c["source"])
src = src.replace(
    '<img src="images/kuramoto_coupling_heterogeneity.svg" alt="Different coupling strengths produce different rates of relaxation towards the group phase" style="display:block;max-width:82%;margin:1rem auto">',
    '<img src="images/kuramoto_coupling_heterogeneity.svg" alt="Numerical simulation of oscillator groups with different coupling strengths" style="display:block;max-width:82%;margin:1rem auto">\n\nThis is a direct numerical simulation. At each time, the group phase $\\psi(t)$ is calculated from the complex mean. The plotted quantity is the mean wrapped angular distance $|\\operatorname{wrap}(\\theta_i-\\psi)|$ within each $K_i$ group. It therefore measures how far that group remains from the population direction, rather than distance from a fixed external target.'
)
c["source"] = src.splitlines(keepends=True)

c = by_id("ensemble")
src = "".join(c["source"])
needle = "The dashed line marks\n\n$$\nK_c=\\frac{2}{\\pi g(0)}=\\sqrt{\\frac{8}{\\pi}}.\n$$"
replacement = "The dashed line uses the general onset result derived above. For the standard-normal distribution, $g(0)=1/\\sqrt{2\\pi}$, so\n\n$$\nK_c=\\frac{2}{\\pi g(0)}=\\sqrt{\\frac{8}{\\pi}}.\n$$\n\nThis is the earlier formula evaluated for the distribution used in the simulation, not a second independent expression for $K_c$."
src = src.replace(needle, replacement)
c["source"] = src.splitlines(keepends=True)

PATH.write_text(json.dumps(nb, ensure_ascii=False, indent=1) + "\n")
