"""Refine Week 6 framing, notation, heterogeneity and spatial extensions."""

import json
from pathlib import Path

path = Path("notebooks/week06/L_Synchronisation.ipynb")
nb = json.loads(path.read_text())
cells = nb["cells"]


def cell(cid):
    return next(c for c in cells if c.get("id") == cid)


def set_source(cid, text):
    cell(cid)["source"] = text.splitlines(keepends=True)


def md(cid, text, tag=None, slide_type=None):
    meta = {}
    if tag:
        meta["tags"] = [tag]
    if slide_type:
        meta["slideshow"] = {"slide_type": slide_type}
    return {"cell_type": "markdown", "id": cid, "metadata": meta,
            "source": text.splitlines(keepends=True)}


def insert_after(anchor, new_cells):
    global cells
    ids = {c.get("id") for c in new_cells}
    cells[:] = [c for c in cells if c.get("id") not in ids]
    i = next(i for i, c in enumerate(cells) if c.get("id") == anchor) + 1
    cells[i:i] = new_cells


contrast_slide = md("w6-coordination-contrast-slide", '''## Not all synchrony is self-organised

<div class="two-panel compact-panels">
<div class="meaning-panel">
<h3>Choreographed coordination</h3>
<p>Dance and synchronised swimming use a shared score, rehearsal, cues and sometimes a leader.</p>
<p>The timing is organised largely from the top down.</p>
</div>
<div class="meaning-panel">
<h3>Spontaneous synchronisation</h3>
<p>Fireflies and coupled oscillators keep their own clocks while responding to one another.</p>
<p>Collective timing can emerge without a conductor.</p>
</div>
</div>
''', "slides-only", "subslide")
insert_after("w6-hook", [contrast_slide])

contrast_reader = md("w6-coordination-contrast-reader", '''### Not all synchrony is self-organised

Dance and synchronised swimming can be extremely precise, but their coordination is usually organised through choreography, rehearsal, shared music, visual cues and sometimes a leader. The timing is imposed largely from the top down.

The firefly problem is different. Each animal retains its own internal clock and responds to signals from others. No individual specifies the group rhythm. This week uses **synchronisation** for that second process: coupled systems adjust their timing until a collective temporal relationship emerges.
''')
insert_after("reader-motivation", [contrast_reader])

# Repair equation rendering and keep notation visually consistent.
set_source("w6-uncoupled", r'''## Two oscillators without coupling

<div class="two-panel wide-left compact-panels">
<div class="image-panel"><img src="images/two_phase_oscillators.svg" alt="Two independent phase oscillators on the unit circle" style="max-height:410px"></div>
<div class="text-panel">
<p>Without coupling,</p>

$$
\dot{\theta}_1=\omega_1, \qquad \dot{\theta}_2=\omega_2.
$$

<p>For $\phi=\theta_1-\theta_2$,</p>

$$
\dot{\phi}=\omega_1-\omega_2.
$$

<p>The separation drifts unless the natural frequencies match.</p>
</div>
</div>
''')
set_source("uncoupled", r'''## Two uncoupled oscillators

<div class="two-panel wide-left">
<div class="image-panel"><img src="images/two_phase_oscillators.svg" alt="Two independent phase oscillators on the unit circle"></div>
<div class="text-panel">
<p>Without coupling, each phase follows its own internal dynamics:</p>

$$
\dot{\theta}_1=\omega_1, \qquad \dot{\theta}_2=\omega_2.
$$

<p>For $\phi=\theta_1-\theta_2$,</p>

$$
\dot{\phi}=\omega_1-\omega_2.
$$

<p>Unless the natural frequencies match, the relative phase drifts.</p>
</div>
</div>
''')

# Make the order-parameter caption ordinary prose rather than emphasis.
for cid in ("w6-order", "order-geometry"):
    s = "".join(cell(cid)["source"])
    s = s.replace("<p><strong>Their vector average</strong>", "<p>Their vector average")
    s = s.replace("<p>Their vector average has direction $\\psi$ and magnitude $r$.</p>",
                  "<p>Their vector average has direction $\\psi$ and magnitude $r$.</p>")
    cell(cid)["source"] = s.splitlines(keepends=True)

# Replace the thin existing heterogeneity slide with a controlled sequence.
set_source("w6-heterogeneity-analysis-slide", '''## Heterogeneity · change one assumption at a time

1. Give every oscillator the same natural frequency and vary $K$.
2. Hold $K$ fixed and draw natural frequencies from $g(\omega)$.
3. Only then consider variation in both $\omega_i$ and responsiveness $K_i$.

This separates two questions: how quickly an oscillator responds, and how quickly it would run in isolation.
''')
hetero_freq_slide = md("w6-frequency-heterogeneity-slide", '''## Different clocks can lock to a common rate

<img src="images/kuramoto_frequency_heterogeneity.svg" alt="Kuramoto phases coloured by natural frequency beside the frequency distribution" style="display:block;max-height:510px;max-width:100%;margin:0 auto">

Coupling does not erase intrinsic differences. Locked oscillators share an observed rate even though their natural frequencies remain different.
''', "slides-only", "subslide")
hetero_k_slide = md("w6-coupling-heterogeneity-slide", '''## Heterogeneous responsiveness

<div class="two-panel wide-left compact-panels">
<div class="image-panel"><img src="images/kuramoto_coupling_heterogeneity.svg" alt="Oscillators with different coupling strengths approach the group phase at different rates" style="max-height:430px"></div>
<div class="text-panel"><p>Set all $\omega_i$ equal first.</p><p>A larger $K_i$ means oscillator $i$ responds more strongly to the group.</p><p>After that result is understood, vary both $\omega_i$ and $K_i$.</p></div>
</div>
''', "slides-only", "subslide")
insert_after("w6-heterogeneity-analysis-slide", [hetero_freq_slide, hetero_k_slide])

hetero_reader = md("w6-controlled-heterogeneity-reader", '''### Controlled heterogeneity experiments

The simplest baseline gives every oscillator the same natural frequency. In a frame rotating at that common frequency, the intrinsic drift disappears. With attractive all-to-all coupling, phase differences then arise from initial conditions and the interaction draws the phases together. This is the `variability = 0` case in the Kuramotocycle.

Next vary one ingredient at a time.

**Natural-frequency heterogeneity:** draw $\omega_i$ from $g(\omega)$ while keeping a common $K$. Oscillators with low natural frequencies must speed up and those with high natural frequencies must slow down to join a frequency-locked group. Their intrinsic frequencies do not change; the interaction changes their realised phase velocities.

<img src="images/kuramoto_frequency_heterogeneity.svg" alt="Kuramoto phases coloured by natural frequency beside the frequency distribution" style="display:block;max-width:100%;margin:1rem auto">

**Coupling heterogeneity:** set the natural frequencies equal and assign each oscillator its own $K_i$,

$$
\dot{\theta}_i
=\omega+\frac{K_i}{N}\sum_{j=1}^{N}\sin(\theta_j-\theta_i).
$$

Now $K_i$ measures responsiveness: large values pull an oscillator towards the group more quickly, while small values make it less influenced by the others.

<img src="images/kuramoto_coupling_heterogeneity.svg" alt="Different coupling strengths produce different rates of relaxation towards the group phase" style="display:block;max-width:82%;margin:1rem auto">

Only after these two effects have been separated is it sensible to draw both $\omega_i$ and $K_i$ from distributions. Stacking heterogeneities immediately may produce a realistic population, but makes it harder to identify which assumption produced a change in the collective behaviour.
''')
insert_after("w6-onset-analysis-reader", [hetero_reader])

# Replace the abrupt spatial ending with a fixed-space then moving-space progression.
set_source("w6-spatial-fireflies-slide", '''## Put the oscillators back into space

The Kuramoto phase circle is not a physical map.

<div class="three-step">
<div><strong>Kuramoto</strong><span>phase only; all-to-all coupling</span></div>
<div><strong>Spin Wheels</strong><span>fixed positions; local spatial coupling</span></div>
<div><strong>Swarmalators</strong><span>positions and phases both evolve</span></div>
</div>
''')
spin_slide = md("w6-spin-wheels-slide", '''## Fixed positions · Spin Wheels

<iframe src="https://www.complexity-explorables.org/explorables/spin-wheels/" title="Spin Wheels explorable" style="display:block;width:100%;height:535px;border:1px solid #C7CEDC;margin:0 auto;"></iframe>
''', "slides-only", "subslide")
swarm_slide = md("w6-swarmalators-slide", '''## Moving oscillators · swarmalators

<iframe src="https://www.complexity-explorables.org/explorables/swarmalators/" title="Swårmalätørs explorable" style="display:block;width:100%;height:535px;border:1px solid #C7CEDC;margin:0 auto;"></iframe>

<p class="figure-credit"><a href="https://www.nature.com/articles/s41467-017-01190-3">O'Keeffe, Hong and Strogatz (2017), “Oscillators that sync and swarm”</a>.</p>
''', "slides-only", "subslide")
insert_after("w6-spatial-fireflies-slide", [spin_slide, swarm_slide])

set_source("w6-spatial-fireflies-reader", r'''## Return to the fireflies: restore physical space

In a standard Kuramoto plot, position around the circle records phase. It is not a map of where an oscillator sits in the world.

There are two useful intermediate extensions.

### Fixed positions: Spin Wheels

[**Spin Wheels**](https://www.complexity-explorables.org/explorables/spin-wheels/) places phase oscillators on a fixed lattice and couples nearby sites. Physical arrangement now determines the interaction network, but the oscillators do not move. This is a useful step between all-to-all Kuramoto coupling and a population of mobile fireflies.

### Moving positions: swarmalators

If each individual also has a position $\mathbf{x}_i$, the model requires equations for both phase and motion. When phase affects movement and changing positions affect phase coupling, the agents are often called **swarmalators**.

[**Explore Swårmalätørs**](https://www.complexity-explorables.org/explorables/swarmalators/), based on O'Keeffe, Hong and Strogatz's [**“Oscillators that sync and swarm”**](https://www.nature.com/articles/s41467-017-01190-3).

<div class="two-panel compact-panels">
<div class="image-panel"><iframe src="https://www.youtube.com/embed/atLhROLzsFo" title="Swarmalator realisation one" style="width:100%;height:300px;border:0" allowfullscreen></iframe></div>
<div class="image-panel"><iframe src="https://www.youtube.com/embed/Db6aiSa4soU" title="Swarmalator realisation two" style="width:100%;height:300px;border:0" allowfullscreen></iframe></div>
</div>

The progression is deliberate: phase-only Kuramoto, fixed spatial coupling in Spin Wheels, then mobile oscillators whose positions and phases co-evolve. Each step adds one new modelling commitment.
''')

path.write_text(json.dumps(nb, indent=1, ensure_ascii=False) + "\n")
