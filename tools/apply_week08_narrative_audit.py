import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "notebooks/week08/L_Critical_phenomena.ipynb"
nb = json.loads(PATH.read_text())
cells = nb["cells"]


def item(cell_id):
    return next(c for c in cells if c.get("id") == cell_id)


def text(cell_id):
    value = item(cell_id).get("source", "")
    return "".join(value) if isinstance(value, list) else value


def set_text(cell_id, value):
    item(cell_id)["source"] = value.strip() + "\n"


def blank(*cell_ids):
    for cell_id in cell_ids:
        set_text(cell_id, "")


def slide(cell_id, heading, body, slide_type="subslide"):
    return {
        "cell_type": "markdown",
        "id": cell_id,
        "metadata": {"slideshow": {"slide_type": slide_type}, "tags": ["slides", "slides-only"]},
        "source": f"## {heading}\n\n{body.strip()}\n",
    }


def insert_after(after_id, new_cell):
    if any(c.get("id") == new_cell["id"] for c in cells):
        return
    index = next(i for i, c in enumerate(cells) if c.get("id") == after_id)
    cells.insert(index + 1, new_cell)


def move_after(cell_id, after_id):
    moving = item(cell_id)
    cells.remove(moving)
    index = next(i for i, c in enumerate(cells) if c.get("id") == after_id)
    cells.insert(index + 1, moving)


set_text("a5491561-24dd-4854-b885-7488872d7c7b", r"""
# Explorable

## Site percolation

<div class="two-panel equal-panels compact-panels">
<div class="image-panel"><img src="images/Baristas_secret_screenshots.png" alt="Three site-percolation initialisations" style="max-height:410px"></div>
<div class="text-panel"><p><strong>State:</strong> each site is occupied independently with probability <i>p</i>.</p><p><strong>Structure:</strong> neighbouring occupied sites form connected clusters.</p><p><strong>Response:</strong> record whether a cluster spans the lattice and the fraction of sites in the largest cluster.</p><p><strong>Control parameter:</strong> the experimenter selects <i>p</i>.</p><p>For a finite lattice, spanning remains probabilistic. Increasing the lattice size sharpens the transition near <i>p</i><sub>c</sub>.</p><p><a href="https://www.complexity-explorables.org/explorables/baristas-secret/">The Barista's Secret explorable</a></p></div>
</div>
""")

set_text("6186397c", r"""
## The sandpile question

Percolation becomes critical only when $p$ is selected near $p_c$; its dynamics do not move it there. The sandpile instead asks whether slow driving, threshold redistribution and dissipation can maintain a statistically stationary regime with activity across many scales.

We test that claim using spatial, event and temporal measurements, together with comparisons across lattice sizes.
""")

set_text("29f6e3a1", r"""
## The proposed sandpile mechanism

1. Slow driving adds one grain after the previous event has finished.
2. A local threshold triggers redistribution.
3. Redistribution can activate neighbouring sites and form an avalanche.
4. Open boundaries dissipate grains.
5. Loading and loss produce a statistically stationary regime.

In a finite lattice, avalanche size is limited by the system. Criticality is assessed through scaling with event size and lattice size.
""")
blank("1688c8df", "bba65e0b-cdd4-4d39-bca2-c72a8fbce982")

for cell_id in (
    "1bc8a371-5d9f-4701-9530-6c588265ddb1",
    "069f3c75-9a6d-4b56-8d07-bea6f96f3a63",
    "4e00ef41-61b4-4cb0-8ae3-4f8c96782794",
    "da0e12f1-d368-4311-ba37-9a58d215d359",
    "5afe6b3c-eddf-4e0e-b53f-ca066fc623ea",
    "6a5d524b-f1ae-497a-99c5-0c3703b17894",
):
    tags = item(cell_id).setdefault("metadata", {}).setdefault("tags", [])
    if "archive-only" not in tags:
        tags.append("archive-only")

set_text("7faf3c7e-82c0-4a11-b8d3-f8705292d2fa", r"""
## Specify the model

| Component | Specification |
|---|---|
| state | integer height $z_{ij}$ |
| domain | finite square lattice with four nearest neighbours |
| threshold | $z_c=4$ |
| drive | add one grain after the previous avalanche finishes |
| redistribution | remove four grains and give one to each neighbour |
| boundary | grains leaving the lattice are lost |
| observation | record $S$, $A$, $T$, and zero-toppling additions |

Initialisation and burn-in determine when measurement begins. The toppling rule determines how an avalanche relaxes.
""")
blank("67ac4af2-2829-4299-861e-446bec736474", "2cbb2ddc-fc78-4f1c-85e0-9ce16c5c27c3")

insert_after("w8-qualitative-analysis-slide", {
    "cell_type": "markdown",
    "id": "w8-qualitative-analysis-reader",
    "metadata": {"tags": ["reader-only"]},
    "source": "## Qualitative analysis\n",
})

insert_after("w8-qualitative-analysis-reader", slide("w8-symmetric-pile-slide", "A deliberately symmetric pile", """
<img src="images/sandpile_fractal_stills.png" alt="Stable Abelian sandpiles produced by adding grains at one central site" style="display:block;width:94%;max-height:440px;margin:0 auto">

Central loading is a separate experiment chosen to expose nested geometry. The avalanche ensemble below instead uses random slow driving. Results must be interpreted with the protocol that produced them.
"""))

move_after("w8-symmetric-pile-slide", "w8-qualitative-analysis-reader")
move_after("week08-sandpile-fractal-stills", "w8-symmetric-pile-slide")
move_after("3cdcf36d-eddc-4976-973b-e53a589762af", "week08-sandpile-fractal-stills")
item("3cdcf36d-eddc-4976-973b-e53a589762af")["metadata"]["tags"] = ["slides"]
move_after("965627a4-2957-4331-a9a9-91bb3653fa05", "3cdcf36d-eddc-4976-973b-e53a589762af")
move_after("ff17bec4-36da-4b5c-9a64-3f11b2ffab2f", "965627a4-2957-4331-a9a9-91bb3653fa05")
move_after("w8-height-classes-slide", "ff17bec4-36da-4b5c-9a64-3f11b2ffab2f")
move_after("w8-box-counting-slide", "w8-height-classes-slide")
move_after("w8-avalanche-definitions-slide", "w8-box-counting-slide")

set_text("965627a4-2957-4331-a9a9-91bb3653fa05", """
## Three views of critical behaviour

1. **Space — fractal geometry:** analyse a deliberately symmetric stable configuration using box counting.
2. **Events — power laws:** analyse avalanche size, area and duration under random slow driving.
3. **Time — pink ($1/f$) noise:** analyse the grain-addition activity record produced by separated driving and relaxation.

These protocols test different proposed signatures. Report each result with the experiment that produced it.
""")

insert_after("6ef6999f-aeb2-47d9-a94d-4f405a74be02", slide("w8-finite-avalanche-slide", "Avalanche cutoffs and lattice size", """
<img src="images/sandpile_finite_size_ccdf.png" alt="Avalanche-size complementary cumulative distributions for three lattice sizes" style="display:block;width:88%;max-height:430px;margin:0 auto">

The upper cutoff moves outward as the lattice grows. This supports a finite-size interpretation of the cutoff. A stable power-law exponent would require formal fits, uncertainty and comparison with alternative heavy-tailed distributions.
"""))

insert_after("w8-finite-avalanche-slide", {
    "cell_type": "markdown",
    "id": "w8-finite-avalanche-reader",
    "metadata": {"tags": ["reader-only"]},
    "source": r"""### Avalanche cutoffs and lattice size

![Avalanche-size complementary cumulative distributions for three lattice sizes](images/sandpile_finite_size_ccdf.png)

The upper cutoff moves towards larger avalanches as the lattice grows. The finite lattice therefore limits the largest observable events. This comparison supplies the finite-size test required to interpret the cutoff. Establishing a power law would also require formal fits with uncertainty and comparison against alternative heavy-tailed distributions.
""",
})

insert_after("w8-temporal-result-slide", slide("w8-evidence-summary-slide", "What the three analyses show", """
| Proposed signature | Result in this course experiment | Interpretation |
|---|---|---|
| spatial scaling | finite-scale linear regions in a centrally loaded configuration | geometric structure under a special protocol |
| event scaling | broad tails with a cutoff that moves with lattice size | evidence for finite-size event scaling; distributional form remains to be tested |
| $1/f$ activity | nearly flat spectrum | unsupported for this signal and driving protocol |

The organising mechanism is present in the model. The measurements provide mixed support for the proposed signatures.
"""))

set_text("08a562f9-0694-4038-a05a-61e480341aef", """
## What this week establishes

Near-critical regimes can provide sensitivity, wide dynamic range and long-range coordination in systems where those functions matter.

In the Abelian sandpile, slow driving, threshold redistribution and boundary dissipation maintain a statistically stationary regime with avalanches across a system-size-limited range.

Our spatial, event and temporal measurements provide mixed evidence. Applying the same mechanism to earthquakes, neural systems or markets requires system-specific tests.
""")

set_text("9f6df625", r"""
For a finite lattice, repeat the experiment at each occupation probability $p$ and estimate the probability that an occupied cluster spans the system. The transition is rounded: spanning can occur below the infinite-lattice threshold and fail above it in individual realisations. As the lattice grows, the spanning curve sharpens near the site-percolation threshold $p_c$.

The largest-cluster fraction provides a second response measure. Below the transition, occupied clusters are usually local. Near $p_c$, clusters span a broad range of sizes. Above it, a system-spanning cluster occupies a substantial part of the lattice.
""")
set_text("cd594555-6784-4911-8c48-a6a58a43c0b1", r"""
Numerical experiments estimate the finite-size transition by repeating many independently generated lattices over a range of $p$ and several lattice sizes $L$. Finite-size scaling then asks how the transition sharpens and shifts as $L$ increases. Analytical and mean-field approaches provide other estimates, but the emphasis here is numerical evidence.
""")
set_text("27be62e0", """
Percolation is useful whenever global connectivity depends on many local connections. Examples include porous transport, network robustness and simplified descriptions of epidemic reach or fire spread. Each application has its own states, dynamics and threshold.
""")

set_text("6465c807-1a3e-4842-ab2b-6b160a12cf18", r"""
### Correlation length, $\xi$

The **correlation length** measures the distance over which local fluctuations remain statistically related. Away from a continuous critical point, spatial correlations commonly decay approximately as

$$C(r)\sim e^{-r/\xi}.$$

As the control parameter approaches its critical value, $\xi$ grows and distant regions fluctuate together over a larger range. In the infinite-system idealisation, $\xi$ can diverge at criticality and the decay may become a power law. In a finite simulation, $\xi$ is limited by the lattice size.
""")
set_text("e813432b-01c8-4358-84c8-71764ac6e06d", r"""
### Correlation time, $\tau$

The **correlation time** measures how long the effect of a fluctuation persists. Away from a continuous critical point, temporal correlations commonly decay approximately as

$$C(t)\sim e^{-t/\tau}.$$

Near the transition, $\tau$ grows and relaxation becomes slower. This is **critical slowing down**. Divergence occurs only in an infinite-system, infinite-observation-time idealisation; simulations and experiments impose finite limits.
""")

set_text("w8-why-critical-reader", text("w8-why-critical-reader") + """

Functional arguments ask why evolution or design might favour a near-critical regime. The sandpile addresses a separate question: which dynamics can maintain critical-like activity? The sandpile has no objective. It supplies a mechanism for maintaining activity near a critical regime.
""")

set_text("3328e586-a153-4582-be6e-42dab0938460", """
Bak, Tang and Wiesenfeld introduced the model in *Self-Organized Criticality: An Explanation of 1/f Noise*. Pink noise was one of the phenomena they aimed to explain. The activity signal analysed here gives us a direct test of that proposed signature under our stated driving protocol.
""")
set_text("729d84cf-01d7-4cce-b4aa-ff50d6c87ab5", """
## Variations

For a fixed sequence of grain additions, Abelian relaxation reaches the same stable configuration regardless of legal toppling order. Randomness enters our experiment through the selected addition sites.

The [Bak–Sneppen model of evolution](https://doi.org/10.1103/PhysRevLett.71.4083) uses a different construction. It repeatedly replaces the least-fit species and changes its ecological neighbours, allowing one replacement to trigger a cascade. The model proposes SOC as a mechanism for punctuated evolutionary activity; empirical application requires separate evidence.
""")

set_text("cb05e58d-a142-4678-b52a-359ecf3f018a", """
## Forest-fire example

This example makes coarse-graining concrete. A site contains a tree with probability $q$, and fire spreads between neighbouring occupied sites. The question is whether a connected tree cluster allows fire to cross a block. The calculation is an approximate route to a connectivity threshold. It uses a different mechanism from the sandpile.

[Critically inflammatory](https://www.complexity-explorables.org/explorables/critically-inflammatory/) adds regrowth and lightning to create a driven dynamical model.
""")
set_text("10b1bd93-b83e-4d3b-b2d3-18032b8f3314", r"""
Define $P_s$ as the probability that fire crosses a block at scale $s$. For one site, $P_1=q$. Enumerating the connected configurations of a $2\times2$ block gives an approximate scale transformation

$$P_{s+1}=P_s^4+4P_s^3(1-P_s)+4P_s^2(1-P_s)^2.$$

Iterating this map sends initial values below its unstable interior fixed point towards zero and values above it towards system-spanning connection. The estimate is useful because it links a local occupancy probability to large-scale connectivity; it remains an approximation because a block variable discards internal geometry and correlations.
""")
blank("6d9eb663-a3e9-4661-86d3-0ca14962879f", "d647c09e-b920-416c-ad02-8bc0839dbc98", "a20b19e4-3a96-46e6-a1ff-43ff5fd095b4", "2ef3ce6c-6636-43e4-9e5d-668f7757f5ed", "3fd2ba4c-ccee-43bd-a316-0275a97854da", "e366b59a-df9a-46b3-9f21-04f774943173")

set_text("219e7e0b-ddca-4791-9637-a95bc0e0515b", """
## What this topic establishes

Near-critical regimes can support sensitivity, dynamic range and long-range coordination when those properties serve a system's function. The Abelian sandpile supplies one mechanism for maintaining a statistically stationary regime with events over many finite scales: slow driving, threshold redistribution and boundary dissipation.

The course measurements give mixed evidence for the three proposed signatures. Spatial structure depends on a special central-loading protocol, the avalanche cutoff moves with lattice size, and the separated activity signal has an approximately flat spectrum. SOC remains one candidate explanation for broad real-world event distributions and requires system-specific evidence.
""")

PATH.write_text(json.dumps(nb, ensure_ascii=False, indent=1) + "\n")
print(PATH)
