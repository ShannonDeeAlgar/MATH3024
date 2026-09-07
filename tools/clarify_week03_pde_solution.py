#!/usr/bin/env python3
"""Clarify what solving Gray–Scott means and why numerical work is needed."""

import json
from pathlib import Path


NOTEBOOK = Path("notebooks/week03/L_Reaction_diffusion.ipynb")
CELL_ID = "954ca579-6444-4529-9190-05fb00912d11"

nb = json.loads(NOTEBOOK.read_text())
cell = next(cell for cell in nb["cells"] if cell.get("id") == CELL_ID)

text = r'''# From continuous equations to a discrete simulation

A solution is a pair of evolving fields,

$$
\bigl(U(\mathbf x,t),V(\mathbf x,t)\bigr),
$$

giving both concentrations at every location and time. Local reaction changes the fields; diffusion couples nearby locations. Their nonlinear feedback can amplify small spatial variations into spots, stripes, waves or irregular behaviour.

<div class="compact-summary">
<p><strong>Analytic solutions:</strong> Special cases can be solved exactly or analysed through equilibria, linearised modes and some travelling waves. These results expose mechanisms and parameter dependence without numerical artefacts.</p>
<p><strong>Numerical solutions:</strong> For a nonlinear two-dimensional system with particular initial and boundary conditions, a useful closed form is generally unavailable. A grid and finite time steps let us approximate the evolving fields.</p>
</div>

<div class="ladder-marker"><img src="images/ladder_marker.svg" alt="Ladder of abstraction"><span><strong>Down the ladder:</strong> replace the continuous fields by finitely many stored concentrations and make each numerical update explicit.</span></div>

<div class="reader-only-detail">
<p>The PDEs do not determine one universal picture by themselves. A particular solution also requires a domain, parameter values, boundary conditions and initial fields. The mathematical object being solved for is still the complete pair of functions <i>U</i>(<b>x</b>, <i>t</i>) and <i>V</i>(<b>x</b>, <i>t</i>), not merely a final image.</p>

<p>Analytic work remains preferable when it is available. It can establish whether an equilibrium exists, which spatial wavelengths grow, how a wave travels, or how a result depends on parameters. Such conclusions can apply to a whole family of initial conditions and do not contain grid or time-step error. The difficulty is that nonlinear coupling, two spatial dimensions, finite boundaries and irregular initial data usually prevent a closed-form expression for the full pattern.</p>

<p>Numerical discretisation is therefore required for the patterns explored here. It does not add the complexity by hand. It approximates the local reaction and diffusion rules repeatedly across space and time, allowing their collective consequences to become visible. Because it is an approximation, we must later check time-step stability and whether refining the grid changes the result.</p>
</div>
'''

cell["source"] = text.splitlines(keepends=True)
NOTEBOOK.write_text(json.dumps(nb, ensure_ascii=False, indent=1) + "\n")
print(NOTEBOOK.resolve())
