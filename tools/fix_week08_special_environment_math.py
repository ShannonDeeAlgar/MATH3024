#!/usr/bin/env python3
import json
from pathlib import Path

path = Path(__file__).resolve().parents[1] / "notebooks/week08/L_Critical_phenomena.ipynb"
data = json.loads(path.read_text())

for cell in data["cells"]:
    value = "".join(cell.get("source", []))
    if "In percolation, critical behaviour only appears" in value and "discussion-marker" in value:
        value = """<div class="discussion-marker"><img src="images/discussion_marker.svg" alt="Discussion prompt"><span>Percolation becomes critical only when the occupation probability <i>p</i> is tuned to <i>p</i><sub>c</sub>. The sandpile also contains a toppling threshold <i>z</i><sub>c</sub>. Why are these thresholds playing different roles?</span></div>
"""
    value = value.replace(
        "The system's response shows a sharp transition at a certain porosity.",
        "The system's response shows a sharp transition at a certain occupation probability.",
    )
    value = value.replace(
        "<p>Binarising the pile at $z=\\{0,1,2,3\\}$ reveals spatial structure at several thresholds.</p>",
        "<p>Binarising the pile at grain levels 0, 1, 2 and 3 reveals different spatial subsets.</p>",
    )
    value = value.replace(
        "<p>The power spectrum of the number of toppled cells gives $\\beta=1.58$ over the fitted range.</p>",
        "<p>The power spectrum of the number of toppled cells gives β = 1.58 over the fitted range.</p>",
    )
    if value.startswith('<div style="border-left: 4px solid #b22222'):
        value = """<div class="discussion-marker"><img src="images/discussion_marker.svg" alt="Check the estimate"><span>Downey reports box-counting estimates for the four sandpile levels. Which values are impossible for subsets of a two-dimensional image, and what may have gone wrong?</span></div>

```{dropdown} Values reported in the source
The four reported estimates are

$$
(1.871,\;3.502,\;1.781,\;2.084).
$$

Values above 2 cannot be box-counting dimensions of subsets of the plane. Reproduce the calculation before interpreting the estimates.
```
"""
    value = value.replace(
        "<p>$$P_{2}=P_{1}^{4}+4P_{1}^{3}(1-P_{1})+4P_{1}^{2}(1-P_{1})^{2}.$$</p>",
        "<p>P₂ = P₁⁴ + 4P₁³(1 − P₁) + 4P₁²(1 − P₁)².</p>",
    )
    value = value.replace(
        "<p>The approximation predicts a threshold near $P_1=q=0.382$.</p>",
        "<p>The approximation predicts a threshold near P₁ = q = 0.382.</p>",
    )
    cell["source"] = value.splitlines(keepends=True)

path.write_text(json.dumps(data, ensure_ascii=False, indent=1) + "\n")
