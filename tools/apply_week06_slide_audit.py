#!/usr/bin/env python3
"""Apply the September Week 6 slide audit without changing Reader content."""

from pathlib import Path

import nbformat


ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "notebooks/week06/L_Synchronisation.ipynb"


def source(text: str) -> str:
    return text.strip() + "\n"


def add_tag(cell, tag: str) -> None:
    tags = list(cell.metadata.get("tags", []))
    if tag not in tags:
        tags.append(tag)
    cell.metadata["tags"] = tags


def remove_tag(cell, tag: str) -> None:
    cell.metadata["tags"] = [x for x in cell.metadata.get("tags", []) if x != tag]


def slide(cell_id: str, text: str, slide_type: str = "subslide"):
    cell = nbformat.v4.new_markdown_cell(source=source(text), id=cell_id)
    cell.metadata["tags"] = ["slides-only"]
    cell.metadata["slideshow"] = {"slide_type": slide_type}
    return cell


nb = nbformat.read(PATH, as_version=4)
by_id = {cell.get("id"): cell for cell in nb.cells}


def archive(*cell_ids: str) -> None:
    for cell_id in cell_ids:
        cell = by_id.get(cell_id)
        if cell is not None:
            add_tag(cell, "archive-only")


def show(cell_id: str) -> None:
    cell = by_id[cell_id]
    remove_tag(cell, "archive-only")
    remove_tag(cell, "reader-only")
    add_tag(cell, "slides-only")


def upsert_after(anchor_id: str, cell) -> None:
    existing = by_id.get(cell.id)
    if existing is not None:
        nb.cells.remove(existing)
    anchor = next(c for c in nb.cells if c.get("id") == anchor_id)
    nb.cells.insert(nb.cells.index(anchor) + 1, cell)
    by_id[cell.id] = cell


# State the idea explicitly before introducing the mathematical model.
definition = slide(
    "w6-definition-slide",
    r'''
## Synchronisation through interaction

**Synchronisation occurs when interaction causes systems with their own internal dynamics to develop a stable timing relationship.**

<table class="compact-table">
<thead><tr><th>Choreographed</th><th>Coincidental</th><th>Self-organised</th></tr></thead>
<tbody><tr>
<td>A shared plan prescribes the timing.</td>
<td>Similar rhythms occur without interaction.</td>
<td>Interaction adjusts the rhythms.</td>
</tr></tbody>
</table>

The stable relationship may be in phase, anti-phase or separated by another constant phase difference.
''',
)
upsert_after("w6-choreographed-swimmers", definition)

# Establish the sign and periodicity of the coupling before asking students to
# interpret the equation.  Preview the pairwise result here; retain its formal
# derivation in Analysis.
by_id["w6-coupling"].source = source(r'''
## Add coupling

Suppose oscillator 2 influences oscillator 1:

$$
\dot{\theta}_1=\omega_1+K\sin(\theta_2-\theta_1),
\qquad
\dot{\theta}_2=\omega_2.
$$

<div style="display:grid;grid-template-columns:0.9fr 1.1fr;gap:1.6rem;align-items:center">
<img src="images/two_phase_oscillators.svg?v=20260826c" alt="Two phase oscillators on a circle" style="width:100%;max-height:285px">
<div>
<p>If oscillator 1 is <strong>behind</strong>, the coupling increases its rate.</p>
<p>If oscillator 1 is <strong>ahead</strong>, the coupling decreases its rate.</p>
<p>The correction is zero at alignment and repeats after a full cycle.</p>
<p><i>K</i> controls how strongly the clocks can correct their mismatch.</p>
</div>
</div>

For a coupled pair, locking is possible when $|\Delta\omega|\leq K$. The population model asks how the same competition operates across a distribution of natural frequencies.
''')

# Replace the early terminology catalogue with one compact comparison.  The
# collective states are useful as extensions, not before the coupled pair has
# been understood.
by_id["sync-types-slide"].source = source(r'''
## Compare timing relationships

<table class="compact-table">
<thead><tr><th>Behaviour</th><th>Phase difference</th><th>Long-time frequencies</th></tr></thead>
<tbody>
<tr><td><strong>In phase</strong></td><td>$0$</td><td>equal</td></tr>
<tr><td><strong>Anti-phase</strong></td><td>$\pi$</td><td>equal</td></tr>
<tr><td><strong>Phase locked</strong></td><td>constant</td><td>equal</td></tr>
<tr><td><strong>Drifting</strong></td><td>changes continuously</td><td>unequal</td></tr>
<tr><td><strong>Beats without interaction</strong></td><td>changes continuously</td><td>unequal</td></tr>
</tbody>
</table>

<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:0.8rem;margin-top:0.5rem">
<img src="images/synchronisation_types/in_phase.svg?v=20260826" alt="In-phase oscillators" style="width:100%;max-height:145px">
<img src="images/synchronisation_types/anti_phase.svg?v=20260826" alt="Anti-phase oscillators" style="width:100%;max-height:145px">
<img src="images/synchronisation_types/phase_locked.svg?v=20260826" alt="Phase-locked oscillators" style="width:100%;max-height:145px">
</div>
''')
archive("sync-types-collective-slide")

# Keep the exact finite-population identity and one slide connecting the
# analytical onset to numerical evidence.  The continuum derivation remains
# available in the Reader.
by_id["w6-mean-field-return"].source = source(r'''
# Analytical benchmark

The order parameter defines the collective field:

$$
r(t)e^{\mathrm{i}\psi(t)}=\dfrac{1}{N}\sum_{j=1}^{N}e^{\mathrm{i}\theta_j(t)}.
$$

Rewriting the all-to-all interaction through $r$ and $\psi$ is exact. Replacing the finite population by a continuous frequency density $g(\omega)$ gives a large-population prediction for the onset of coherence.

The analytical result provides a benchmark for the numerical ensemble and shows how the onset depends on heterogeneity.
''')
show("w6-ensemble")
by_id["w6-ensemble"].source = source(r'''
## Predicted onset and finite simulations

<div class="two-panel wide-left compact-panels">
<div class="image-panel"><img src="images/kuramoto_meanfield_comparison.svg" alt="Large-population Kuramoto prediction compared with a finite numerical ensemble"></div>
<div class="text-panel">
<p>For a symmetric frequency density centred at zero,</p>
<p style="font-size:1.25em;text-align:center">$K_c=2/[\pi g(0)]$.</p>
<p>The orange curve is the continuum prediction. The grey curve is a direct numerical ensemble with $N=600$.</p>
<p>Finite populations round and fluctuate around the idealised onset.</p>
</div>
</div>
''')
archive("w6-dynamic-to-stationary-slide", "w6-onset-result-slide")

# The lecture ends with one network change, one spatial example and a compact
# menu of other project directions.  Their detailed treatments remain in the
# Reader.
by_id["w6-model-variants-slide"].source = source(r'''
# Selected extensions

| Change | Question it opens |
|---|---|
| interaction network | Who can influence whom? |
| independent noise | How robust is collective timing? |
| coupling strengths | What if responsiveness varies? |
| oscillator order | What changes when velocity has its own dynamics? |
| physical position | What if motion and phase affect each other? |

Each extension changes one modelling assumption and creates a possible project direction.
''')
archive(
    "w6-independent-noise-slide",
    "w6-coupling-heterogeneity-slide",
    "w6-second-order-kuramoto-slide",
    "w6-spatial-fireflies-slide",
    "w6-spin-wheels-slide",
    "w6-drone-shows-slide",
)
by_id["w6-swarmalators-slide"].source = source(r'''
## Spatial extension · swarmalators

<iframe src="https://www.complexity-explorables.org/explorables/swarmalators/" title="Swårmalätørs explorable" style="display:block;width:100%;height:470px;border:1px solid #C7CEDC;margin:0 auto;" allowfullscreen></iframe>

Each individual now has a phase and a physical position. Phase affects motion while changing neighbours alter phase coupling.
''')

synthesis = slide(
    "w6-synthesis-slide",
    r'''
# Synchronisation · synthesis

- Each oscillator has **intrinsic dynamics** even in isolation.
- A distribution of natural frequencies creates **heterogeneity**.
- Coupling competes with that heterogeneity.
- Individual oscillators may lock to the group or continue to drift.
- The order parameter $r(t)$ compresses the population's phase organisation.
- Repeated simulations reveal the collective transition and its finite-size variation.
- The large-population calculation predicts how the onset depends on $g(\omega)$.

**Canonical question:** When can interaction overcome differences between individual clocks and produce a stable collective rhythm?
''',
    slide_type="slide",
)
upsert_after("w6-swarmalators-slide", synthesis)

nbformat.write(nb, PATH)
print(f"Updated {PATH.relative_to(ROOT)}")
