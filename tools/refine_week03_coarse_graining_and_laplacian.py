#!/usr/bin/env python3
"""Refine Week 3's coarse-graining transition and discrete-Laplacian notation."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK = ROOT / "notebooks/week03/L_Reaction_diffusion.ipynb"


def set_source(cell: dict, source: str) -> None:
    cell["source"] = [line + "\n" for line in source.rstrip().splitlines()]


def markdown_cell(cell_id: str, source: str, slide_type: str = "subslide") -> dict:
    return {
        "cell_type": "markdown",
        "id": cell_id,
        "metadata": {"slideshow": {"slide_type": slide_type}, "tags": ["slides"]},
        "source": [line + "\n" for line in source.rstrip().splitlines()],
    }


def main() -> None:
    notebook = json.loads(NOTEBOOK.read_text())
    by_id = {cell.get("id"): cell for cell in notebook["cells"]}

    # Caption-like notes duplicate information already carried by the figures,
    # axes, labels or surrounding Reader prose.
    for cell_id, sentence in {
        "b7c839be-6ee3-4fef-9aae-72b880dbb4b9": '<p class="small-note">Each path contains 45 unit-length steps and uses the same axes. The rule for choosing the next direction is the only difference.</p>\n',
        "bf26cf2d": '<p class="small-note"><i>D</i> = 0.25. The mean-square displacement (MSD) averages squared displacement across the walkers.</p>\n',
        "25b5d7f3": '<p class="small-note"><i>D</i> = 0.25 remains in the sweep, so the previous ensemble can be compared with the wider pattern.</p>\n',
        "a241f850": '<p class="small-note">Each point is the mean fitted MSD slope; each error bar shows one standard deviation across independent batches. The highlighted point is <i>D</i> = 0.25.</p>\n',
        "week03-lowercase-full-model": '<p class="small-note">Feed and removal keep the reactor away from equilibrium. Without them, reactant is exhausted and the transient reaction runs down.</p>\n',
    }.items():
        source = "".join(by_id[cell_id]["source"])
        source = source.replace(sentence, "")
        set_source(by_id[cell_id], source)

    # Separate the reveal that particle-level simulation is infeasible from the
    # upward abstraction to concentration fields.
    set_source(by_id["4f8c9362"], r'''# From particle motion to continuous equations

<p>The Complexity Explorable is not directly simulating every particle interaction.</p>

<div class="discussion-marker"><img src="images/discussion_marker.svg" alt="Discussion prompt"><span>Could it update every molecule, collision and three-particle encounter?</span></div>

An exact particle simulation would require an enormous number of random trajectories and collision tests. Statistical physics handles systems such as gases by replacing inaccessible microscopic histories with collective quantities that can be predicted and measured.''')

    coarse_id = "week03-coarse-grain-state"
    if coarse_id not in by_id:
        position = next(i for i, cell in enumerate(notebook["cells"]) if cell.get("id") == "4f8c9362") + 1
        notebook["cells"].insert(position, markdown_cell(coarse_id, r'''## Coarse-grain the state

We therefore **coarse-grain** the state:

$$
\text{many particle positions}
\quad\longrightarrow\quad
U(\mathbf x,t),\;V(\mathbf x,t),
$$

where the fields record local concentrations. We lose individual histories and gain a tractable description of collective transport and reaction.

<div class="ladder-marker"><img src="images/ladder_marker.svg" alt="Ladder of abstraction"><span><strong>Up the ladder over particles:</strong> retain how much of each chemical is present at each location.</span></div>'''))

    set_source(by_id["week03-turing-paper-scope"], r'''## A reaction–diffusion system: Gray–Scott

Let $U(\mathbf{x},t)$ and $V(\mathbf{x},t)$ be two concentration fields:

$$
\frac{\partial U}{\partial t}=R_U(U,V)+D_U\nabla^2U,
\qquad
\frac{\partial V}{\partial t}=R_V(U,V)+D_V\nabla^2V.
$$

<div class="analysis-perspectives">
  <div><strong>Reaction</strong><p><i>R</i><sub><i>U</i></sub> and <i>R</i><sub><i>V</i></sub> describe local production, removal and feedback.</p></div>
  <div><strong>Diffusion</strong><p>The Laplacians communicate concentration differences through nearby locations.</p></div>
</div>

<div class="choice-marker"><img src="images/choice_marker.svg" alt="Modelling choice"><span>The Gray–Scott model specifies one particular pair of reaction functions inside this wider reaction–diffusion framework.</span></div>''')

    source = "".join(by_id["8858f425-48a5-492b-9a5a-2d277dacc632"]["source"])
    source = source.replace("## Assemble Gray–Scott at the concentration level\n\n", "")
    set_source(by_id["8858f425-48a5-492b-9a5a-2d277dacc632"], source)

    set_source(by_id["954ca579-6444-4529-9190-05fb00912d11"], r'''# From continuous equations to a discrete simulation

A solution is a pair of evolving concentration fields:

$$
\bigl(U(\mathbf x,t),V(\mathbf x,t)\bigr).
$$

<p><strong>Analytic solutions:</strong> exact results are available in special cases and can expose equilibria, growing modes and parameter dependence.</p>
<p><strong>Numerical solutions:</strong> a nonlinear two-dimensional pattern usually requires a grid and finite time steps.</p>

<div class="ladder-marker"><img src="images/ladder_marker.svg" alt="Ladder of abstraction"><span><strong>Down the ladder:</strong> replace continuous fields by finitely many stored concentrations and explicit updates.</span></div>

<div class="reader-only-detail">
<p>The PDEs do not determine one universal picture by themselves. A particular solution also requires a domain, parameter values, boundary conditions and initial fields. The mathematical object being solved for is still the complete pair of functions <i>U</i>(<b>x</b>, <i>t</i>) and <i>V</i>(<b>x</b>, <i>t</i>), not merely a final image.</p>
<p>Analytic work remains preferable when it is available. It can establish whether an equilibrium exists, which spatial wavelengths grow, how a wave travels, or how a result depends on parameters. Such conclusions can apply to a whole family of initial conditions and do not contain grid or time-step error. Nonlinear coupling, two spatial dimensions, finite boundaries and irregular initial data usually prevent a closed-form expression for the full pattern.</p>
<p>Numerical discretisation is therefore required for the patterns explored here. It approximates the local reaction and diffusion rules repeatedly across space and time. Because it is an approximation, we must later check time-step stability and whether refining the grid changes the result.</p>
</div>''')

    # Keep the personal context and detailed accessibility guidance in the
    # Reader, while the projected slides retain the visual question and example.
    set_source(by_id["ecd5c9ba-5acd-42ce-9fba-d6a584a56494"], r'''#### Can everyone recover the same information?

<img src="images/Colourblind.png" alt="A pseudo-Ishihara colour-vision image" style="display:block;width:42%;max-height:400px;object-fit:contain;margin:0 auto;">

<div class="reader-only-detail">
<p>I did my PhD, and continue to work, with someone who is red–green colour blind. He cannot see the number inside this circle.</p>
<p>Red–green colour-vision deficiency affects about 8% of men and 0.5% of women in populations where it has been most extensively measured. Prevalence varies between populations.</p>
<p>I may mark your project on a colour screen and see a full rainbow. Aim for a higher standard: the ordering and conclusion should also survive colour-vision differences and black-and-white printing.</p>
<p class="figure-reference">Prevalence summary: Webvision, NCBI Bookshelf, “Prevalence of congenital color deficiencies.”</p>
</div>''')

    set_source(by_id["62003953"], r'''#### Design colour deliberately

<img src="images/colormap_good_bad.svg" alt="Accessible sequential colormaps compared with rainbow and red-green scales" style="display:block;width:82%;max-height:430px;object-fit:contain;margin:0 auto;">

<div class="reader-only-detail">
<p>Colour is part of the representation, not decoration.</p>
<p><strong>Prefer:</strong> perceptually ordered sequential maps such as <code>viridis</code>, <code>cividis</code> and <code>plasma</code> for concentration.</p>
<p><strong>Avoid:</strong> rainbow scales and red–green contrasts when ordered values must be read accurately.</p>
<p>Check the figure in greyscale. Also use labels, line styles or markers when colour distinguishes categories.</p>
<p class="figure-reference"><a href="https://matplotlib.org/stable/users/explain/colors/colormaps.html">Matplotlib: Choosing Colormaps</a> · <a href="https://www.nature.com/articles/d41586-021-02696-z">Nature guide</a> · <a href="https://www.ascb.org/science-news/how-to-make-scientific-figures-accessible-to-readers-with-color-blindness/">ASCB guide</a></p>
</div>''')

    set_source(by_id["f2e3c94d-6d0e-4d20-992a-8e23122ce6d0"], r'''## Approximate the Laplacian

In continuous space,
$$
\nabla^2U=\nabla\!\cdot(\nabla U)
=\frac{\partial^2U}{\partial x^2}+\frac{\partial^2U}{\partial y^2}.
$$

On a square grid with spacing $h=\Delta x=\Delta y$, use
$$
(\nabla_h^2U)_{i,j}
=\frac{U_{i+1,j}+U_{i-1,j}+U_{i,j+1}+U_{i,j-1}-4U_{i,j}}{h^2}.
$$

Here $\nabla^2$ is the continuous Laplacian; $\nabla_h^2$ is its grid approximation; $h$ is the distance between neighbouring grid points; and $(i,j)$ identifies the focal cell.

<div class="reader-only-detail">
<p>This is a second-derivative approximation, not a first derivative. In one dimension the centred second difference is</p>
$$
(\nabla_h^2U)_i=\frac{U_{i+1}-2U_i+U_{i-1}}{h^2}.
$$
<p>The two-dimensional stencil adds one such curvature comparison in the horizontal direction and one in the vertical direction. The four neighbour values are compared with four copies of the focal value. A constant or locally linear field gives zero; a focal peak gives a negative value; and a focal valley gives a positive value. Multiplication by a positive diffusion coefficient therefore lowers peaks and fills valleys.</p>
<p>The subscript <i>h</i> is a reminder that this is a discrete operator whose value depends on the mesh spacing. As the grid is refined and <i>h</i> decreases, a consistent approximation should approach the continuous Laplacian.</p>
</div>''')

    NOTEBOOK.write_text(json.dumps(notebook, indent=1, ensure_ascii=False) + "\n")
    print("Refined Week 3 coarse-graining, slide captions and Laplacian notation.")


if __name__ == "__main__":
    main()
