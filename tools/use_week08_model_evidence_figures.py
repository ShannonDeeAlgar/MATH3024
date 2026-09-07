#!/usr/bin/env python3
"""Update Week 8 prose for figures measured from site percolation."""

import json
from pathlib import Path


PATH = Path("notebooks/week08/L_Critical_phenomena.ipynb")


def lines(text):
    return text.strip().splitlines(keepends=True)


notebook = json.loads(PATH.read_text())
by_id = {cell.get("id"): cell for cell in notebook["cells"]}

by_id["w8-critical-point-distinction"]["source"] = lines(r"""
Figure 8.1a plots the normalized pair-connectedness $C(r)/C(1)$. Slower decay means that sites remain connected across longer distances.

Each snapshot is one independently occupied $128\times128$ lattice. Pale sites belong to smaller clusters; blue marks the largest connected cluster. This is distinct from the red flow in the explorable. Each curve averages 500 lattices. Near $p_c$, large clusters form and $C(r)$ decays more slowly.

<img src="images/critical_correlations.svg" alt="Simulated site-percolation clusters and measured pair-connectedness below and near the percolation threshold" style="display:block;width:88%;max-height:350px;margin:0 auto">
""")

by_id["w8-finite-size-slide"]["source"] = lines(r"""
### Finite-size effects

<div class="two-panel wide-left compact-panels">
<div class="image-panel"><img src="images/percolation_finite_size.svg" alt="Monte Carlo estimates of site-percolation spanning probability for three lattice sizes, with sampling uncertainty" style="max-height:420px"></div>
<div class="text-panel">
<p>Each point is measured from 450 independent site-percolation lattices; bands show approximate 95% binomial intervals.</p>
<p>The apparent transition becomes sharper as $L$ increases.</p>
<p>The crossing remains near $p_c\approx0.593$.</p>
<p>Finite-size scaling asks how the rounding and displacement change with $L$.</p>
</div>
</div>
""")

tail = by_id["dd5fbfb8-5f02-4683-9efa-cf0350649461"]
tail["source"] = lines(r"""
The curves below come from site-percolation simulations on $128\times128$ lattices. Each curve combines the cluster sizes from 600 independent lattices. The vertical axis is the complementary cumulative probability $\Pr(S\geq s)$: the fraction of measured clusters at least as large as $s$.

Near the percolation threshold, cluster sizes extend across a much wider range and the central portion decays slowly on log–log axes. Below the threshold, the tail bends down and reaches its finite cutoff much sooner. The critical sample is therefore the heavier-tailed of the two.

<img src="images/Tails_comparison.png" alt="Empirical cluster-size tails below and near the site-percolation threshold on linear and logarithmic axes" width="82%">

Finite lattices impose an upper cutoff. A straight-looking region remains preliminary evidence: a power-law claim requires a stated fitted range, uncertainty, repeated lattice sizes and comparison with plausible alternatives.
""")

PATH.write_text(json.dumps(notebook, indent=1, ensure_ascii=False) + "\n")
