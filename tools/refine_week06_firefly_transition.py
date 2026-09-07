import json
from pathlib import Path


path = Path("notebooks/week06/L_Synchronisation.ipynb")
nb = json.loads(path.read_text())


def get(cell_id):
    return next(c for c in nb["cells"] if c.get("id") == cell_id)


def set_source(cell_id, text):
    get(cell_id)["source"] = text.splitlines(keepends=True)


def markdown_cell(cell_id, text, tag, slide_type):
    return {
        "cell_type": "markdown",
        "id": cell_id,
        "metadata": {
            "slideshow": {"slide_type": slide_type},
            "tags": [tag],
        },
        "source": text.splitlines(keepends=True),
    }


set_source("w6-specify", '''## Specify the model

The fireflies have internal clocks, and a neighbour's flash can shift one of those clocks. How should that become a model?

- **State:** what records position within the flash cycle?
- **Dynamics:** how does an isolated clock advance?
- **Interaction:** is a “nudge” a fixed jump, a temporary speed change, or something that depends on both clock readings?
- **Network:** which flashes can a firefly perceive?

<div class="discussion-marker"><img src="images/discussion_marker.svg" alt="Discussion prompt"><span>There are many possible implementations. Which is the simplest one that remains consistent with what we observed?</span></div>
''')

set_source("w6-1657fb237d", '''# Explorable

The Kuramotocycle shows one proposed mathematical implementation. Explore what it does before unpacking the assumptions behind it.
''')

set_source("w6-one", r'''## One phase oscillator

If a cycle repeats reliably and only timing matters, one angle is enough to record position within it.

A <strong>phase oscillator</strong> retains that angle and its rate of advance:

$$
\dot{\theta}=\omega,
\qquad
\theta(t)=\theta_0+\omega t \pmod{2\pi}
$$

- $\theta$: position within the cycle, or **phase**;
- $\omega$: the natural rate of phase advance;
- $T=2\pi/|\omega|$: the time taken to complete one cycle.

The phase does not specify the observed waveform. An output $y=h(\theta)$ may be sinusoidal, sawtooth-like or pulse-like. Kuramoto's sine is part of the coupling rule, not an assumed signal shape.
''')

set_source("w6-uncoupled", r'''## Two oscillators without coupling

<div class="two-panel wide-left compact-panels">
<div class="image-panel"><img src="images/two_phase_oscillators.svg" alt="Two independent phase oscillators on the unit circle" style="max-height:410px"></div>
<div class="text-panel">
<p>Let $\phi=\theta_1-\theta_2$.</p>
<p>$$\dot\phi=\omega_1-\omega_2$$</p>
<p>The separation drifts unless the natural frequencies match.</p>
</div>
</div>
''')

set_source("firefly-model", '''## Specify the model

The fireflies have internal clocks, and a neighbour's flash can shift one of those clocks. Turning that statement into mathematics requires several decisions:

- **State:** what records position within the flash cycle?
- **Dynamics:** how does an isolated clock advance?
- **Interaction:** is a “nudge” a fixed jump, a temporary speed change, or a change that depends on both clock readings?
- **Network:** which flashes can a firefly perceive?

<div class="discussion-marker"><img src="images/discussion_marker.svg" alt="Discussion prompt"><span>Which implementation is simplest while remaining consistent with the observed behaviour?</span></div>
''')

set_source("single-oscillator", r'''## A phase oscillator

Many systems repeatedly pass through approximately the same sequence of states: a flashing cycle, a heartbeat or a chemical oscillation. If the cycle repeats reliably and only timing matters, an angle can represent position within it.

An **oscillator** may have both amplitude and phase. A **phase oscillator** keeps only position within the cycle and discards variations in amplitude and the detailed shape of the observed signal:

$$
\dot{\theta}=\omega,
\qquad
\theta(t)=\theta_0+\omega t \pmod{2\pi}
$$

- $\theta$: position within the cycle, or **phase**;
- $\omega$: natural angular frequency;
- $T=2\pi/|\omega|$: period.

The **waveform** is the observed output over one cycle. It can be written as $y=h(\theta)$ and may be sinusoidal, sawtooth-like or pulse-like. The phase model stores $\theta$, not the full function $h$ or changes in its amplitude. Kuramoto's sine appears in the coupling between phases; it does not require the observed signal itself to be sinusoidal.

The reduction is reasonable when disturbances return to the same stable cycle and only timing is of interest.
''')

set_source("uncoupled", r'''## Two uncoupled oscillators

<div class="two-panel wide-left">
<div class="image-panel"><img src="images/two_phase_oscillators.svg" alt="Two independent phase oscillators on the unit circle"></div>
<div class="text-panel">
<p>Without coupling, each phase follows its own internal dynamics:</p>
<p>$$\dot\theta_1=\omega_1,\qquad \dot\theta_2=\omega_2$$</p>
<p>For $\phi=\theta_1-\theta_2$,</p>
<p>$$\dot\phi=\omega_1-\omega_2$$</p>
<p>Unless the natural frequencies match, the relative phase drifts.</p>
</div>
</div>
''')

# Use crisp, locally generated vector diagrams in both delivery formats.
for cell in nb["cells"]:
    if cell["cell_type"] != "markdown":
        continue
    text = "".join(cell["source"])
    text = text.replace("images/Geometric_interpretation_of_order_param.png", "images/kuramoto_order_parameter_geometry.svg")
    text = text.replace("*Adapted from Strogatz (2000), Physica D 143, 1–20.*", "*Order-parameter definition as in Strogatz (2000), Physica D 143, 1–20.*")
    cell["source"] = text.splitlines(keepends=True)

# Add the explicit firefly-to-Kuramoto reduction at the start of Model details.
ids = {c.get("id") for c in nb["cells"]}
if "w6-firefly-kuramoto" not in ids:
    nb["cells"].append(markdown_cell("w6-firefly-kuramoto", '''## From fireflies to Kuramoto

| Keep | Replace or omit |
|---|---|
| an internal clock | a flash pulse becomes smooth phase coupling |
| an intrinsic flashing rate | spatial visibility becomes equal all-to-all interaction |
| neighbours can alter timing | brightness, movement and physiology are omitted |

Kuramoto is not a literal model of flashing fireflies. It isolates one question: can coupling overcome differences in the clocks' intrinsic rates?
''', "slides-only", "subslide"))

if "reader-firefly-kuramoto" not in ids:
    nb["cells"].append(markdown_cell("reader-firefly-kuramoto", '''## From fireflies to Kuramoto

The Kuramoto model is not a literal model of flashing fireflies. It keeps three features:

- each individual has an internal clock represented by a phase;
- clocks may have different intrinsic rates;
- interaction can change the rate at which a clock advances.

It then makes strong simplifications. Discrete flash pulses are replaced by continuous sinusoidal phase coupling. Spatial visibility is replaced by equal all-to-all interaction. Brightness, pulse shape, movement, occlusion and physiology are omitted.

The resulting model isolates a narrower question: can coupling overcome heterogeneity in the clocks' intrinsic rates? Pulse-coupled and spatial firefly models can be introduced later when those omitted features matter.
''', "reader-only", "skip"))

# Reorder the opening without changing any later material.
slide_order = [
    "w6-fireflies-video",
    "w6-fireflies",
    "w6-1657fb237d",
    "w6-kuramoto-explorable",
    "w6-specify",
    "w6-model-banner",
    "w6-firefly-kuramoto",
    "w6-one",
]
slide_cells = {cid: get(cid) for cid in slide_order}
first = min(nb["cells"].index(c) for c in slide_cells.values())
nb["cells"] = [c for c in nb["cells"] if c.get("id") not in slide_order]
for offset, cid in enumerate(slide_order):
    nb["cells"].insert(first + offset, slide_cells[cid])

reader_order = [
    "fireflies",
    "w6-8bb38f86c6",
    "kuramoto-video-reader",
    "firefly-model",
    "w6-e00ea3001e",
    "reader-firefly-kuramoto",
    "single-oscillator",
]
reader_cells = {cid: get(cid) for cid in reader_order}
first = min(nb["cells"].index(c) for c in reader_cells.values())
nb["cells"] = [c for c in nb["cells"] if c.get("id") not in reader_order]
for offset, cid in enumerate(reader_order):
    nb["cells"].insert(first + offset, reader_cells[cid])

path.write_text(json.dumps(nb, indent=1, ensure_ascii=False) + "\n")
