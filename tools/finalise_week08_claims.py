#!/usr/bin/env python3
import json
from pathlib import Path

path = Path(__file__).resolve().parents[1] / "notebooks/week08/L_Critical_phenomena.ipynb"
data = json.loads(path.read_text())
cells = data["cells"]

def source(c): return "".join(c.get("source", []))
def set_source(c, s): c["source"] = s.splitlines(keepends=True)

for cell in cells:
    s = source(cell)
    if s.startswith("Some power-law probability distributions are **heavy-tailed**"):
        s = """Of the three curves below, the **power law is heavy-tailed**; the exponential and Gaussian-like curves are light-tailed. Here, heavy-tailed means that the tail decays more slowly than an exponential, so comparatively more probability remains at very large values. It describes the asymptotic decay of the distribution rather than simply how wide the curve looks over one plotted range.

This matters for avalanche sizes, cluster sizes and other critical observables, but a straight segment on log–log axes is not enough to establish a power law. The fitted range, finite-size cutoff and plausible alternative distributions must be reported. The statistical question is developed through the percolation and sandpile examples below.

<img src="images/Tails_comparison.png" alt="Comparison of light and heavy distribution tails" width="58%">

For a fuller fitting workflow, see Clauset, Shalizi and Newman, [Power-Law Distributions in Empirical Data](https://doi.org/10.1137/070710111).
"""
    elif s.startswith("In the critical state these systems are poised"):
        s = """SOC is influential because it offers a mechanism for broad avalanche distributions without external fine-tuning: slow driving repeatedly moves the system towards marginal stability, while rapid local relaxation releases accumulated load.

The claim is model-dependent. We still need to establish a scaling range, finite-size cutoff and robustness to changes in the driving, redistribution and dissipation rules. Apparent power laws alone do not establish self-organised criticality.
"""
    elif s.startswith("Imagine building a sand pile by dropping grains"):
        s = """A physical sand pile suggests the modelling question. Adding grains steepens the pile; local slips reduce an excessive slope and may trigger further slips.

The Abelian sandpile keeps this threshold-and-cascade motif but is not a realistic granular model. Real sand can show characteristic avalanches, inertia and hysteresis rather than the ideal model's clean critical scaling. The comparison motivates the rule; it does not validate the model by resemblance alone.

<img src="images/Angle_of_repose.png" width="58%" alt="Angle of repose in a granular pile">
"""
    elif s.startswith("### Bak et al's Abelian sand pile model"):
        s = """### From BTW to the Abelian sandpile[^abelian-name]

Bak, Tang and Wiesenfeld introduced the threshold sandpile in 1987 as a minimal model of self-organised criticality. Dhar later developed the Abelian formulation used here.

It is a controlled cellular automaton of threshold redistribution.

[^abelian-name]: In algebra, *Abelian* means that the order of operations does not affect their combined result. Sandpile toppling operators commute: toppling site $i$ and then site $j$ has the same net effect as carrying out those topplings in the reverse order. For fixed grain additions and boundary conditions, every legal toppling order therefore reaches the same stable configuration and gives the same number of topplings at each site. The intermediate sequence can differ. See [Dhar (1990)](https://doi.org/10.1103/PhysRevLett.64.1613).
"""
    set_source(cell, s)

# Add a second, optional explorable immediately after the model rules.
anchor = next(i for i,c in enumerate(cells) if source(c).startswith("**Dynamics:** add one grain"))
if not any("virtual-laboratory/152-the-abelian-sandpile" in source(c) for c in cells):
    cells.insert(anchor + 1, {
        "cell_type": "markdown",
        "metadata": {"slideshow": {"slide_type": "slide"}},
        "id": "w8-abelian-sandpile-explorable",
        "source": [
            "### Explore the Abelian sandpile\n",
            "\n",
            "Use the [Abelian sandpile virtual laboratory](https://www.complexityexplorer.org/explore/virtual-laboratory/152-the-abelian-sandpile) to connect one local toppling rule with avalanches, recurrent configurations and system-wide relaxation.\n",
        ],
    })

data["cells"] = cells
path.write_text(json.dumps(data, ensure_ascii=False, indent=1) + "\n")
