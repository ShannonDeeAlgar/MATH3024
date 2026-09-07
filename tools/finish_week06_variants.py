"""Finish the Week 6 heterogeneity, variants and retrospective structure."""

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "notebooks/week06/L_Synchronisation.ipynb"


def source(cell):
    return "".join(cell.get("source", []))


def set_source(cell, text):
    cell["source"] = [line + "\n" for line in text.rstrip().splitlines()]


def markdown(cell_id, text, tags=()):
    return {
        "cell_type": "markdown",
        "id": cell_id,
        "metadata": {"tags": list(tags)},
        "source": [line + "\n" for line in text.rstrip().splitlines()],
    }


data = json.loads(PATH.read_text())
cells = data["cells"]
by_id = {cell.get("id"): cell for cell in cells}

# Keep the clean distribution in the model specification. The main animation
# now carries the same colours through the individual phase histories.
set_source(by_id["w6-watch"], r'''# Qualitative analysis

<img src="images/kuramoto_phase_organisation.gif" alt="Kuramoto oscillators coloured by natural frequency moving around phase space, with individual phase histories, mean phase and coherence" style="display:block;max-height:500px;max-width:100%;margin:0 auto">

Blue marks the slower natural clocks and red the faster ones. Coupling bends both sets of trajectories towards a common realised rate; the orange vector and traces summarise the population without hiding the individuals.''')

set_source(by_id["kuramoto-video"], r'''## Qualitative analysis

<img src="images/kuramoto_phase_organisation.gif" alt="Kuramoto oscillators coloured by natural frequency moving around phase space, with individual phase histories, mean phase and coherence" style="display:block;width:82%;max-width:980px;margin:1rem auto">

The circle is **phase space**, not physical space. Each colour is fixed by the oscillator's natural frequency. The paths show the compromise produced by coupling: slower natural clocks accelerate and faster natural clocks slow down as a frequency-locked group forms.

The orange vector is the instantaneous population average. Its angle is the mean phase $\psi(t)$ and its length is the coherence $r(t)$.''')

# The separate animation repeated the same evidence. Keep the frequency-rate
# comparison as quantitative analysis, but remove the duplicate GIF.
set_source(by_id["w6-frequency-heterogeneity-slide"], r'''## Natural and realised frequencies

<img src="images/kuramoto_realised_frequency.svg" alt="Natural frequency against long-time realised frequency for a Kuramoto population" style="display:block;max-height:500px;max-width:100%;margin:0 auto">

Locked oscillators share a common realised rate. Drifting oscillators retain a different long-time average rate.''')

set_source(by_id["w6-realised-frequency-analysis-reader"], r'''### Natural and realised frequencies

<img src="images/kuramoto_realised_frequency.svg" alt="Natural frequency against long-time realised frequency for a Kuramoto population" style="display:block;width:72%;max-width:800px;margin:1rem auto">

The horizontal band contains **frequency-locked** oscillators: their natural frequencies differ, but coupling gives them the same long-time realised rate. Points away from that band are **drifting** oscillators. Their phases continue to slip relative to the locked group.''')

# Remove cells that will be reinserted as one coherent variants section.
variant_ids = {
    "w6-network-variant-slide", "w6-heterogeneity-analysis-slide",
    "w6-coupling-heterogeneity-slide", "w6-network-variant-reader",
    "w6-controlled-heterogeneity-reader", "w6-second-order-kuramoto-reader",
    "w6-model-variants-slide", "w6-model-variants-reader",
    "w6-second-order-kuramoto-slide",
}
variants = {cell.get("id"): cell for cell in cells if cell.get("id") in variant_ids}
cells[:] = [cell for cell in cells if cell.get("id") not in variant_ids]

# Reuse the existing substantive variant cells with clearer headings.
set_source(variants["w6-coupling-heterogeneity-slide"], source(variants["w6-coupling-heterogeneity-slide"]).replace("## Heterogeneous responsiveness", "## Heterogeneous coupling strength"))
set_source(variants["w6-network-variant-slide"], source(variants["w6-network-variant-slide"]).replace("## Change the interaction network", "## Local and network coupling"))
set_source(variants["w6-controlled-heterogeneity-reader"], source(variants["w6-controlled-heterogeneity-reader"]).replace("### Controlled heterogeneity experiments", "### Heterogeneous coupling strength"))
set_source(variants["w6-network-variant-reader"], source(variants["w6-network-variant-reader"]).replace("### Change the interaction network", "### Local and network coupling"))
set_source(variants["w6-second-order-kuramoto-reader"], source(variants["w6-second-order-kuramoto-reader"]).replace("### Further model variant · add inertia", "### Second-order Kuramoto model"))

slide_banner = markdown("w6-model-variants-slide", "# Model variants\n\nChange one assumption at a time.", ("slides-only",))
second_order_slide = markdown("w6-second-order-kuramoto-slide", r'''## Second-order Kuramoto model

The canonical model specifies phase velocity directly:

$$
\dot\theta_i=\omega_i+\text{coupling}.
$$

Adding inertia gives angular velocity its own dynamics:

$$
m_i\ddot\theta_i+d_i\dot\theta_i
=\omega_i+\frac{K}{N}\sum_j\sin(\theta_j-\theta_i).
$$

This is a reader extension. It changes the equation order; it does not, by itself, define the order of the collective transition.''', ("slides-only",))
reader_banner = markdown("w6-model-variants-reader", r'''## Model variants

The numerical and analytical results above describe the canonical first-order, equally coupled, all-to-all Kuramoto model. Each variant below changes one part of that specification. Keeping the other parts fixed makes the consequence of the change interpretable.''', ("reader-only",))

# Insert slide variants directly after the slide analytical comparison, before
# the later spatial extensions.
slide_ensemble_i = next(i for i, cell in enumerate(cells) if cell.get("id") == "w6-ensemble")
slide_insert = [
    slide_banner,
    variants["w6-coupling-heterogeneity-slide"],
    variants["w6-network-variant-slide"],
    second_order_slide,
]
cells[slide_ensemble_i + 1:slide_ensemble_i + 1] = slide_insert

# Reader variants follow the Reader analytical comparison.
ensemble_i = next(i for i, cell in enumerate(cells) if cell.get("id") == "ensemble")
reader_insert = [
    reader_banner,
    variants["w6-controlled-heterogeneity-reader"],
    variants["w6-network-variant-reader"],
    variants["w6-second-order-kuramoto-reader"],
]
cells[ensemble_i + 1:ensemble_i + 1] = reader_insert

# Remove the generic forward-looking bullet and replace the retrospective with
# modelling lessons that connect directly to this unit.
for cell in cells:
    text = source(cell).replace("- Later network models: topology, weights, delays, and adaptation can all modify synchronisation.\n", "")
    if text != source(cell):
        set_source(cell, text)

set_source(by_id["kuramoto-retrospective-2026"], r'''## Kuramoto looks back

The Kuramoto model reuses ideas already developed in this unit.

- **Week 3:** move between individual motion and a continuous description. Here we replace a detailed oscillator by one phase variable.
- **Week 5:** compress many headings into a circular order parameter. The same complex-number construction now measures phase coherence.
- **Week 6:** keep heterogeneity explicit through $\omega_i$, then move up the ladder from individual phases to $r(t)$, long-time coherence and parameter sweeps.

The wider modelling lesson is that a useful canonical model is not a small copy of the real system. It retains the mechanism needed for the question and removes the rest. Amplitude, waveform, physical position, network structure and inertia can then be restored one at a time when the question requires them.

This is also historically apt. Kuramoto's phase model emerged from work on reaction–diffusion oscillators: a more detailed system was reduced until the common structure became visible. A recent reconstruction of that development is given by [Nakao and Kawamura (2026)](https://arxiv.org/abs/2602.20505).''')

# Guard against older helper scripts reintroducing the stale heading in the
# notebook itself.
for cell in cells:
    text = source(cell).replace("## Choreographed synchronisation", "## Not all synchrony is complex")
    if text != source(cell):
        set_source(cell, text)

PATH.write_text(json.dumps(data, indent=1, ensure_ascii=False) + "\n")
