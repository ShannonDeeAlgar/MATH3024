import json
from copy import deepcopy
from pathlib import Path


path = Path("notebooks/week05/L_ABM.ipynb")
notebook = json.loads(path.read_text())
cells = notebook["cells"]

for index, cell in enumerate(cells):
    text = "".join(cell.get("source", []))
    if text.lstrip().startswith("## Where is the noise added?"):
        angular = deepcopy(cell)
        vectorial = deepcopy(cell)
        vectorial["id"] = "week05-vectorial-noise"

        angular_text = r"""## Where is the noise added? · angular noise

$$
\theta_i'=\bar\theta_i+\xi_i,
\qquad \xi_i\sim U[-\eta/2,\eta/2].
$$

The agent first estimates the local mean heading $\bar\theta_i$, then makes a turning error $\xi_i$. The parameter $\eta$ controls the width of the error distribution.

**Interpretation:** uncertainty enters while the agent executes a chosen direction.
"""
        vectorial_text = r"""## Where is the noise added? · vectorial noise

$$
\theta_i'=\operatorname{Arg}\!\left(\mathbf m_i+\eta n_i e^{\mathrm i\chi_i}\right).
$$

| Symbol | Meaning |
|---|---|
| $\mathbf m_i=\sum_{j\in\mathcal N_i}e^{\mathrm i\theta_j}$ | local alignment signal |
| $n_i$ | number of neighbours |
| $\eta$ | relative noise strength |
| $\chi_i\sim U[0,2\pi)$ | random direction |

**Interpretation:** uncertainty perturbs the sensed alignment signal before a direction is chosen. Both conventions are valid, but they represent different mechanisms.
"""
        angular["source"] = angular_text.splitlines(keepends=True)
        vectorial["source"] = vectorial_text.splitlines(keepends=True)
        cells[index:index + 1] = [angular, vectorial]
        break
else:
    raise RuntimeError("Noise comparison cell not found")

path.write_text(json.dumps(notebook, indent=1, ensure_ascii=False) + "\n")
