#!/usr/bin/env python3
"""Clarify what the avalanche log-log slopes measure in Week 8."""

import json
from pathlib import Path


PATH = Path("notebooks/week08/L_Critical_phenomena.ipynb")


def lines(text):
    return text.splitlines(keepends=True)


notebook = json.loads(PATH.read_text())
by_id = {cell.get("id"): cell for cell in notebook["cells"]}

by_id["4ef815da-7df1-4d08-a36c-f5593e8edd2c"]["source"] = lines(r"""## Avalanche scaling exponents

Candidate scaling laws are

$$
p(S)\propto S^{-\tau_S},
\qquad
p(T)\propto T^{-\tau_T}.
$$

Taking logarithms gives $\log p(S)=\log C-\tau_S\log S$. The slope of a log-density versus log-size plot is therefore $-\tau_S$; the corresponding statement holds for duration. For example, $\tau_S\approx1.06$ means that, within the fitted range, multiplying $S$ by 10 reduces the estimated probability density by about $10^{1.06}\approx11.5$.

The exponent summarises how rapidly large events become rarer. It supports comparisons across system sizes, parameter choices and models when the observable and fitting method are held fixed. Its interpretation depends on the fitted range, uncertainty, dimensionality, boundary conditions and model class. $\tau_S$ and $\tau_T$ can differ because size and duration measure different aspects of an avalanche.
""")

by_id["6ef6999f-aeb2-47d9-a94d-4f405a74be02"]["source"] = lines(r"""## Avalanche distributions

<img src="images/sandpile_avalanche_distributions.png" alt="Histograms and log-binned probability densities for avalanche size and duration" style="display:block;width:88%;max-height:405px;margin:0 auto">

<p style="font-size:0.70em">Each row shows the same non-zero events twice. The right-hand slope estimates the exponent because slope $=-\tau$. Here the shaded middle bins were selected by a fixed illustrative rule, so these values describe this simulation and fitting choice. A scaling claim requires fit uncertainty and repeated lattice sizes, with the upper cutoff moving outward while a common fitted region remains stable.</p>
""")

PATH.write_text(json.dumps(notebook, indent=1, ensure_ascii=False) + "\n")
