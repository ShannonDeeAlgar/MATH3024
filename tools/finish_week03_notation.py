import json
from pathlib import Path


path = Path("notebooks/week03/L_Reaction_diffusion.ipynb")
notebook = json.loads(path.read_text())


def set_source(index: int, text: str) -> None:
    notebook["cells"][index]["source"] = text.splitlines(keepends=True)


set_source(
    73,
    r"""## Return to reaction–diffusion
This is now a coupled system of equations:
$$\frac{\partial U}{\partial t}=R_U(U,V)+D_U\nabla^2U,\qquad
\frac{\partial V}{\partial t}=R_V(U,V)+D_V\nabla^2V.$$
Reaction changes concentrations locally. The Laplacian compares each point with its neighbourhood, moving material down gradients and smoothing isolated peaks.

<div class="choice-marker"><img src="images/choice_marker.svg" alt=""><span><strong>Notation:</strong> $C$ denoted a generic transported concentration. Uppercase $U$ and $V$ denote the two specific Gray–Scott concentration fields.</span></div>
""",
)

set_source(
    108,
    r"""## Discretise time

Let

$$
t_n=n\Delta t,
$$

where $n=0,1,2,\ldots$ is the time-step index and $\Delta t$ is the chosen finite step size. The notation $U^n_{i,j}$ means the numerical value of the $U$ field at grid cell $(i,j)$ and time $t_n$.

If the continuous equations are written as

$$
\frac{\partial U}{\partial t}=F_U(U,V),\qquad
\frac{\partial V}{\partial t}=F_V(U,V),
$$

then explicit Euler gives

$$
U^{n+1}=U^n+\Delta t\,F_U(U^n,V^n),\qquad
V^{n+1}=V^n+\Delta t\,F_V(U^n,V^n).
$$

Both right-hand sides must be evaluated from the same old state at time level $n$. We can now substitute the Gray–Scott reaction and discrete-diffusion terms.

<div class="choice-marker"><img src="images/choice_marker.svg" alt="Modelling choice"><span>Grid spacing, time step, stencil and boundary conditions can change the numerical result and must be tested.</span></div>
""",
)

# Keep the two most image-heavy slides within a 16:9 lecture viewport.
for index, old, new in (
    (17, 'height:360px', 'height:280px'),
    (31, 'max-height:430px', 'max-height:350px'),
):
    source = "".join(notebook["cells"][index]["source"])
    notebook["cells"][index]["source"] = source.replace(old, new).splitlines(keepends=True)

source = "".join(notebook["cells"][17]["source"])
source = source.replace('<p class="figure-reference">A. M. Turing, “The Chemical Basis of Morphogenesis” (1952).</p>', '')
notebook["cells"][17]["source"] = source.splitlines(keepends=True)

path.write_text(json.dumps(notebook, indent=1, ensure_ascii=False) + "\n")
