#!/usr/bin/env python3
"""Restore the conceptual and evidential middle of the Week 8 slide deck."""

from pathlib import Path

import nbformat


ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "notebooks/week08/L_Critical_phenomena.ipynb"


def clean(text: str) -> str:
    return text.strip() + "\n"


def slide(cell_id: str, text: str, slide_type: str = "subslide"):
    cell = nbformat.v4.new_markdown_cell(clean(text), id=cell_id)
    cell.metadata["tags"] = ["slides-only"]
    cell.metadata["slideshow"] = {"slide_type": slide_type}
    return cell


nb = nbformat.read(PATH, as_version=4)
by_id = {c.get("id"): c for c in nb.cells}


def add_tag(cell, tag: str) -> None:
    tags = list(cell.metadata.get("tags", []))
    if tag not in tags:
        tags.append(tag)
    cell.metadata["tags"] = tags


def archive(*ids: str) -> None:
    for cell_id in ids:
        if cell_id in by_id:
            add_tag(by_id[cell_id], "archive-only")


def upsert_after(anchor_id: str, cell) -> None:
    old = by_id.get(cell.id)
    if old is not None:
        nb.cells.remove(old)
    anchor = next(c for c in nb.cells if c.get("id") == anchor_id)
    nb.cells.insert(nb.cells.index(anchor) + 1, cell)
    by_id[cell.id] = cell


def move_after(cell_id: str, anchor_id: str) -> None:
    cell = next(c for c in nb.cells if c.get("id") == cell_id)
    nb.cells.remove(cell)
    anchor = next(c for c in nb.cells if c.get("id") == anchor_id)
    nb.cells.insert(nb.cells.index(anchor) + 1, cell)


# Connect Week 8 to transitions students have already encountered.
bridge = slide("w8-earlier-transitions-slide", r'''
## Critical transitions we have already seen

| Model | Control parameter | Collective response |
|---|---|---|
| Vicsek | noise or density | polarisation |
| Kuramoto | coupling relative to heterogeneity | phase coherence |
| Percolation | occupation probability | spanning connectivity |

**Week 8 asks:** What additional behaviour appears near a continuous transition, and how can a system remain near such a regime without external tuning?
''')
upsert_after("standardised-title-context", bridge)

# Keep the model specification with the explorable rather than repeating it on
# two introductory slides.
by_id["a5491561-24dd-4854-b885-7488872d7c7b"].source = clean(r'''
# Explorable

## Percolation
<div class="two-panel equal-panels compact-panels">
<div class="image-panel"><img src="images/Baristas_secret_screenshots.png" alt="Three percolation initialisations" style="max-height:410px"></div>
<div class="text-panel"><p>Each site is occupied independently with probability <i>p</i>. Occupied neighbouring sites form clusters.</p><p><strong>Choose:</strong> <i>p</i>.</p><p><strong>Observe:</strong> connected clusters and the first path spanning the system.</p><p><strong>Near <i>p</i><sub>c</sub>:</strong> connectivity changes sharply and clusters occur across many scales.</p><p>The experimenter selects <i>p</i>, making this an externally tuned critical point.</p><p><a href="https://www.complexity-explorables.org/explorables/baristas-secret/">The Barista's Secret explorable</a></p></div>
</div>
''')
by_id["a5491561-24dd-4854-b885-7488872d7c7b"].metadata["slideshow"] = {"slide_type": "slide"}
move_after("a5491561-24dd-4854-b885-7488872d7c7b", "w8-earlier-transitions-slide")

# Replace the dense critical-point paragraph with two visual, operational
# slides and one finite-size qualification.
by_id["w8-critical-point-distinction"].source = clean(r'''
## Behaviour near a continuous critical point

Near a continuous transition, local fluctuations become related across larger distances and persist for longer. **Correlation length** $\xi$ and **correlation time** $\tau$ quantify these effects; finite system size and observation time limit what we can measure.

<img src="images/critical_correlations.svg" alt="Schematic correlation functions showing rapid spatial decay away from a critical point and slow decay across a finite system near it" style="display:block;width:92%;max-height:430px;margin:0 auto">
''')

scales = slide("w8-correlation-scales-slide", r'''
## Correlation scales

| | Away from criticality | Near a continuous critical point |
|---|---|---|
| space | correlations decay over a finite length $\xi$ | $\xi$ grows towards the system size |
| time | fluctuations relax over a finite time $\tau$ | $\tau$ grows towards the observation time |
| consequence | one characteristic scale dominates | fluctuations occur across the available scales |

In an infinite idealisation, $\xi$ and $\tau$ may diverge. In every simulation or experiment, system size and observation time impose limits.
''')
upsert_after("w8-critical-point-distinction", scales)

finite = slide("w8-finite-size-slide", r'''
## Finite-size effects

<div class="two-panel wide-left compact-panels">
<div class="image-panel"><img src="images/percolation_finite_size.svg" alt="Illustrative percolation response curves sharpening as lattice size increases" style="max-height:420px"></div>
<div class="text-panel">
<p>$\xi$ cannot exceed the lattice size $L$.</p>
<p>The apparent transition is rounded and may shift.</p>
<p>Comparing sizes tests whether the scaling region expands.</p>
<p>When varying $N$ or $L$, density and other relevant quantities must remain controlled.</p>
</div>
</div>
''')
upsert_after("w8-correlation-scales-slide", finite)

# One overfull-start animation is enough once initialisation has been specified.
archive("1bc8a371-5d9f-4701-9530-6c588265ddb1")

# Restore the spatial measurements that the overview currently promises.
by_id["ff17bec4-36da-4b5c-9a64-3f11b2ffab2f"].source = clean(r'''
## Spatial analysis

The symmetric construction makes nested spatial organisation visible. We separate the four stable height classes, then test their apparent scaling using the Week 2 box-counting method.
''')

height_classes = slide("w8-height-classes-slide", r'''
## Height classes

<img src="images/sandpile_height_subsets.png" alt="Four height classes from one symmetric sandpile with finite-scale dimension estimates" style="display:block;width:100%;max-height:455px;margin:0 auto">

The slopes are finite-scale descriptions of this image. The four classes need not have equal estimates, and dimensions do not add like area fractions.
''')
upsert_after("ff17bec4-36da-4b5c-9a64-3f11b2ffab2f", height_classes)

box_counting = slide("w8-box-counting-slide", r'''
## Box-counting results

<img src="images/sandpile_box_counting.png" alt="Box-counting diagnostics for four sandpile height classes with fitted scale ranges and slopes" style="display:block;width:92%;max-height:455px;margin:0 auto">

The single shaded band marks the common fitted range: the same four box widths are used for every height class, making the slopes directly comparable. If the usable linear regions differed, each line would need its own stated fit range.
''')
upsert_after("w8-height-classes-slide", box_counting)

# Interpret the avalanche exponents where they first appear.
by_id["4ef815da-7df1-4d08-a36c-f5593e8edd2c"].source = clean(r'''
## Avalanche scaling exponents

Candidate scaling laws are

$$
p(S)\propto S^{-\tau_S},
\qquad
p(T)\propto T^{-\tau_T}.
$$

$\tau_S$ describes how quickly large avalanches become less common as size increases. A larger $\tau_S$ gives a more steeply falling tail. The same interpretation applies to $\tau_T$ for duration.

An exponent is meaningful only with its observable, fitted range, uncertainty, dimensionality, boundary conditions and model class. $\tau_S$ and $\tau_T$ need not match.
''')

# Let the figure carry the distribution slide; retain only the distinctions
# students need to interpret its axes and fits.
by_id["6ef6999f-aeb2-47d9-a94d-4f405a74be02"].source = clean(r'''
## Avalanche distributions

<img src="images/sandpile_avalanche_distributions.png" alt="Histograms and log-binned probability densities for avalanche size and duration" style="display:block;width:88%;max-height:405px;margin:0 auto">

<p style="font-size:0.72em">Each row shows the same non-zero events twice. Grey bands mark illustrative fitted ranges; a finite-size cutoff should move outward as lattice size increases.</p>
''')

# Complete the temporal analysis with this simulation's actual diagnostic.
by_id["036605fa-9869-40cc-8e9b-8d69aac0261b"].source = clean(r'''
## Temporal analysis

The grain-addition record is intermittent: many additions trigger no toppling, while some trigger bursts. A power spectrum tests how variation is distributed across frequencies.

The result depends on the recorded signal and the driving protocol. Here each avalanche finishes before the next grain is added.
''')

temporal_result = slide("w8-temporal-result-slide", r'''
## Activity spectrum

<div class="two-panel wide-left compact-panels">
<div class="image-panel"><img src="images/sandpile_activity_spectrum.png" alt="Intermittent sandpile activity time series and its nearly flat power spectrum" style="max-height:440px"></div>
<div class="text-panel">
<p>The time series is visibly intermittent.</p>
<p>The spectrum is nearly flat and gives no convincing $1/f$ evidence for this signal.</p>
<p>Continuously driven variants allow avalanches to overlap. They define a different signal and may have different spectral behaviour.</p>
</div>
</div>
''')
upsert_after("036605fa-9869-40cc-8e9b-8d69aac0261b", temporal_result)

# Keep the longer methodological conclusion in the Reader; the result slide
# now makes the slide narrative complete.
archive("40949b83-6a08-4aeb-814d-25c07e0aac0d")

nbformat.write(nb, PATH)
print(f"Updated {PATH.relative_to(ROOT)}")
