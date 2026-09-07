"""Apply the final Week 3 Reader, slide, and workshop sequence."""

from pathlib import Path

import nbformat


ROOT = Path(__file__).resolve().parents[1]
LECTURE = ROOT / "notebooks/week03/L_Reaction_diffusion.ipynb"
WORKSHOP = ROOT / "notebooks/week03/WS_Reaction_diffusion.ipynb"


def set_source(nb, cell_id, source):
    for cell in nb.cells:
        if cell.get("id") == cell_id:
            cell.source = source.strip()
            return cell
    raise KeyError(cell_id)


def move_after(nb, cell_id, anchor_id):
    cell = next(c for c in nb.cells if c.get("id") == cell_id)
    nb.cells.remove(cell)
    anchor = next(i for i, c in enumerate(nb.cells) if c.get("id") == anchor_id)
    nb.cells.insert(anchor + 1, cell)


nb = nbformat.read(LECTURE, as_version=4)

set_source(
    nb,
    "d0dd3fdf-7bad-4b0c-b3bb-594128690712",
    r'''
# Reaction–diffusion systems
## MATH3024 · Week 3

<div class="canonical-model-marker"><span>Canonical model</span><strong>Gray–Scott reaction–diffusion<br><small>Supporting model: random-walk diffusion</small></strong></div>
''',
)

set_source(
    nb,
    "f129ebdb-49b2-451f-94bf-561270f0ee23",
    r'''
<div class="slide-columns" style="grid-template-columns:minmax(0,1.35fr) minmax(0,.65fr);">
  <img class="column-image" src="images/ChatGPT_Cheetah.png" alt="AI-generated striped cheetah" style="max-height:390px;">
  <div><p><strong>An AI-generated answer</strong></p><p>The requested appearance is plausible. The image does not explain the developmental mechanism.</p><p class="figure-reference">Image generated with ChatGPT.</p></div>
</div>
''',
)

set_source(
    nb,
    "week03-same-mechanism-different-pattern",
    r'''
# Related mechanisms, different patterns

<div class="analysis-perspectives three coat-cards">
  <div><div class="coat-image-frame"><img src="images/cheetah_coat_card.jpg" alt="Cheetah coat"></div><strong>Cheetah</strong><p>Small spots</p></div>
  <div><div class="coat-image-frame"><img src="images/leopard_coat_card_cropped.jpg" alt="Leopard coat"></div><strong>Leopard</strong><p>Rosettes</p></div>
  <div><div class="coat-image-frame"><img src="images/jaguar_coat_card.jpg" alt="Jaguar coat"></div><strong>Jaguar</strong><p>Rosettes with central spots</p></div>
</div>

<div class="discussion-marker"><img src="images/discussion_marker.svg" alt="Discussion prompt"><span>Could related local interactions generate different system-level patterns?</span></div>
''',
)

# The Reader now embeds microscope footage directly, so remove the obsolete
# Wikimedia animation credit left by an earlier draft.
for cell in nb.cells:
    if cell.cell_type == "markdown" and "Yasrena" in cell.source:
        cell.source = "\n".join(
            line for line in cell.source.splitlines()
            if "Yasrena" not in line and "Brownian Motion.gif" not in line
        )

set_source(
    nb,
    "week03-sand-zebra-first",
    r'''
# Similar patterns, different mechanisms

<div class="two-panel equal-panels">
  <div class="image-panel"><img src="images/sand_ridges_only.png" alt="Parallel ridges in wind-blown sand" style="width:100%;height:300px;object-fit:cover;"><p><strong>Sand ridges</strong><br>Transport, erosion and deposition.</p></div>
  <div class="image-panel"><img src="images/Zebras.png" alt="Zebra coat stripes" style="width:100%;height:300px;object-fit:cover;"><p><strong>Zebra stripes</strong><br>Developmental interactions between cells and signals.</p></div>
</div>

<div class="discussion-marker"><img src="images/discussion_marker.svg" alt="Discussion prompt"><span>What observations would distinguish a shared form from a shared mechanism?</span></div>
''',
)

set_source(
    nb,
    "a0a1efe7-e26e-4f6d-a529-3db70b3fe94f",
    r'''
# Turing’s question

<div class="two-panel equal-panels">
  <div class="image-panel"><img src="images/Turing_and_imitation_game.png" alt="Alan Turing and a representation of the imitation game" style="width:100%;height:430px;object-fit:contain;"></div>
  <div class="text-panel"><h3>How does form emerge?</h3><p>An embryo can begin close to uniform, yet organised spatial differences appear.</p><p>Could local processes create that structure without a pre-drawn template?</p><p class="figure-reference">A. M. Turing, “The Chemical Basis of Morphogenesis” (1952).</p></div>
</div>
''',
)

set_source(
    nb,
    "week03-turing-paper-scope",
    r'''
## A general reaction–diffusion model

Let $u(\mathbf{x},t)$ and $v(\mathbf{x},t)$ be two morphogen concentrations:

$$
\frac{\partial u}{\partial t}=R_u(u,v)+D_u\nabla^2u,
\qquad
\frac{\partial v}{\partial t}=R_v(u,v)+D_v\nabla^2v.
$$

<div class="analysis-perspectives">
  <div><strong>Reaction</strong><p>$R_u$ and $R_v$ describe local production, removal and feedback.</p></div>
  <div><strong>Diffusion</strong><p>The Laplacians communicate concentration differences through nearby tissue.</p></div>
</div>

<div class="choice-marker"><img src="images/choice_marker.svg" alt="Modelling choice"><span>Turing proposed a framework, not one unique pair of reaction functions. Gray–Scott will later specify them.</span></div>
''',
)

set_source(
    nb,
    "week03-turing-six-modes",
    r'''
## The essential condition for a Turing instability

$$
\text{stable local chemistry}+\text{differential diffusion}
\longrightarrow \text{spatial pattern}
$$

<div class="two-panel equal-panels compact-panels">
  <div class="text-panel"><p><strong>Without diffusion:</strong> the uniform reaction equilibrium is stable, so a small disturbance decays.</p></div>
  <div class="text-panel"><p><strong>With differential diffusion:</strong> $D_u\ne D_v$, and at least one repeating spatial disturbance grows.</p></div>
</div>

<p class="small-note"><strong>Spatial mode:</strong> a pattern of variation with a particular wavelength, such as repeating bands. Different diffusion rates are essential in the classical two-species mechanism, but are not sufficient by themselves.</p>

<div class="ladder-marker"><img src="images/ladder_marker.svg" alt="Ladder of abstraction"><span><strong>Up the ladder:</strong> ask which spatial disturbances grow instead of following every molecule.</span></div>
''',
)

# Bridge Turing's biological question to the model ingredients before showing
# the equations. This is slide-only; the Reader develops the same argument in
# the surrounding prose.
bridge_id = "week03-why-reaction-diffusion"
bridge_source = r'''
## Turing’s proposed solution

<div class="analysis-perspectives three">
  <div><strong>Reaction</strong><p>Production, removal and feedback change chemical signals locally.</p></div>
  <div><strong>Diffusion</strong><p>Signals spread through tissue and couple nearby locations.</p></div>
  <div><strong>Perturbations</strong><p>Small fluctuations are unavoidable. They may decay or grow.</p></div>
</div>

<div class="discussion-marker"><img src="images/discussion_marker.svg" alt="Discussion prompt"><span>Diffusion usually smooths differences. Could coupling two chemicals make a difference grow instead?</span></div>
'''.strip()
bridge = next((c for c in nb.cells if c.get("id") == bridge_id), None)
if bridge is None:
    bridge = nbformat.v4.new_markdown_cell(bridge_source)
    bridge["id"] = bridge_id
    bridge.metadata["tags"] = ["slides"]
    bridge.metadata["slideshow"] = {"slide_type": "slide"}
    anchor = next(i for i, c in enumerate(nb.cells) if c.get("id") == "a0a1efe7-e26e-4f6d-a529-3db70b3fe94f")
    nb.cells.insert(anchor + 1, bridge)
else:
    bridge.source = bridge_source
    move_after(nb, bridge_id, "a0a1efe7-e26e-4f6d-a529-3db70b3fe94f")

# Establish the qualitative mechanism before introducing its general equations.
move_after(nb, "week03-turing-six-modes", bridge_id)
move_after(nb, "week03-turing-paper-scope", "week03-turing-six-modes")

# The representation choice is the modelling reveal for the week.  Establish
# the microscopic story first, then explain why the canonical model uses
# concentrations, before writing any reaction--diffusion PDE.
set_source(
    nb,
    "d67005af-86fe-4102-b7b8-0cf9f629d586",
    r'''
# Diffusion as a change of representation

<div class="discussion-marker"><img src="images/discussion_marker.svg" alt="Discussion prompt"><span>If molecules move and react individually, what would an exact simulation have to store and update?</span></div>

<p>The literal particle story sounds like the solution: follow every molecule, collision and reaction.</p>

<div class="ladder-marker"><img src="images/ladder_marker.svg" alt="Ladder of abstraction"><span><strong>Stay low:</strong> begin with the entities and events that physically produce the process.</span></div>
''',
)

set_source(
    nb,
    "4f8c9362",
    r'''
# The particle story is not the simulation

An exact particle simulation would have to update an enormous number of random trajectories, detect molecular encounters and decide which encounters react. That is far more detail and computation than our pattern question requires.

We therefore change the state representation:

$$
\text{many particle positions}
\quad\longrightarrow\quad
u(\mathbf x,t),\;v(\mathbf x,t),
$$

where each field records a local concentration averaged over many particles.

<div class="ladder-marker"><img src="images/ladder_marker.svg" alt="Ladder of abstraction"><span><strong>Up the ladder over particles:</strong> discard individual histories and retain collective concentration at each location.</span></div>
''',
)

set_source(
    nb,
    "762e37bb-dee7-495f-9fc4-9b7b764656c9",
    r'''
## From particles to concentrations

The microscopic story is still the physical interpretation, but it is no longer the simulated state. A field such as $u(\mathbf x,t)$ records the local concentration of chemical $U$, averaged over many particles near position $\mathbf x$.

This is **coarse-graining**. It is the same scientific move used when a gas is described by density, temperature and pressure rather than by every molecular trajectory. We lose individual histories and gain a tractable description of collective transport.
''',
)

# Put the representation reveal before the Turing condition and its PDE.
move_after(nb, "d67005af-86fe-4102-b7b8-0cf9f629d586", bridge_id)
move_after(nb, "4f8c9362", "d67005af-86fe-4102-b7b8-0cf9f629d586")
move_after(nb, "762e37bb-dee7-495f-9fc4-9b7b764656c9", "4f8c9362")
move_after(nb, "week03-turing-six-modes", "762e37bb-dee7-495f-9fc4-9b7b764656c9")
move_after(nb, "week03-turing-paper-scope", "week03-turing-six-modes")

set_source(
    nb,
    "week03-gray-scott-history",
    r'''
# From Turing to Gray–Scott

Turing supplied the framework: local reactions coupled by diffusion can generate spatial structure.

Gray–Scott supplies one explicit, compact model. It began as Peter Gray and Stephen K. Scott’s model of cubic autocatalysis in an open reactor. Pearson’s simulations later revealed its rich catalogue of spatial patterns.

$$U+2V\longrightarrow3V.$$

<p class="small-note">Gray–Scott belongs to the reaction–diffusion family. Some regimes are classical diffusion-driven Turing patterns; the model also supports transients and finite-amplitude behaviour outside that narrower case.</p>

<p class="figure-reference">Gray &amp; Scott (1983, 1984); Pearson (1993).</p>
''',
)

set_source(
    nb,
    "8858f425-48a5-492b-9a5a-2d277dacc632",
    r'''
## 1. Reaction: local positive feedback

$$U+2V\longrightarrow3V.$$

Let $u(\mathbf x,t)$ and $v(\mathbf x,t)$ be concentrations. Under the **mass-action assumption**, treating this as an elementary reaction gives a local rate proportional to $uv^2$. After nondimensionalisation the rate constant is absorbed, leaving

$$
\frac{\partial u}{\partial t}=-uv^2,
\qquad
\frac{\partial v}{\partial t}=+uv^2.
$$

<div class="choice-marker"><img src="images/choice_marker.svg" alt="Modelling choice"><span>The reaction mechanism and mass-action description are modelling choices. Given those choices, the powers of $u$ and $v$ follow from the stoichiometry; $uv^2$ is not selected merely because it makes patterns.</span></div>
''',
)

set_source(
    nb,
    "b7c839be-6ee3-4fef-9aae-72b880dbb4b9",
    r'''
### Random walk: a discrete model

<img src="images/random_walk_types_stats.svg" alt="Unbiased, biased and persistent random walks with their defining step statistics" style="display:block;width:96%;max-height:390px;object-fit:contain;margin:0 auto;">

$$
\mathbf{X}_n=\sum_{m=1}^{n}\boldsymbol{\xi}_m,
\qquad
\mathbb{E}[\boldsymbol{\xi}_m]=\mathbf{0}
\quad\text{for an unbiased walk}.
$$

For diffusion we begin with independent, unbiased increments of finite variance.
''',
)

set_source(
    nb,
    "11879310",
    r'''
### Brownian motion: the physical phenomenon

<div class="two-panel equal-panels">
<div class="image-panel"><iframe width="100%" height="315" src="https://www.youtube.com/embed/ZNzoTGv_XiQ" title="Microscope recordings of Brownian motion" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe></div>
<div class="text-panel">
<p>Brownian motion is the continuous-time stochastic limit of many small, independent random steps.</p>
<p>The film contains many short microscope recordings of real Brownian motion. It runs for about 12 minutes; sample the snippets rather than treating it as a required full-length viewing.</p>
<p>One path remains irregular. The predictable diffusion law appears in an ensemble or probability density.</p>
</div>
</div>

$$
\mathbf{B}(t+\Delta t)-\mathbf{B}(t)
\sim \mathcal{N}(\mathbf{0},2D\Delta t\,I_d),
$$

and in $d$ dimensions,

$$
\mathbb{E}\!\left[\lVert\mathbf{B}(t)-\mathbf{B}(0)\rVert^2\right]=2dDt.
$$
''',
)

set_source(
    nb,
    "36fa3ed0",
    r'''
## The continuous Gray–Scott model

$$
\frac{\partial u}{\partial t}=D_u\nabla^2u-uv^2+f(1-u),
\qquad
\frac{\partial v}{\partial t}=D_v\nabla^2v+uv^2-(f+k)v.
$$

<div class="two-panel equal-panels">
  <div class="image-panel"><img src="images/gray_scott_model_map.svg" alt="Reaction, diffusion, feed and removal in the Gray–Scott model"></div>
  <div class="text-panel">
  <p><strong>Local:</strong> autocatalytic reaction, feed and removal change concentrations at one location.</p>
  <p><strong>Spatial:</strong> diffusion couples neighbouring locations, usually at unequal rates.</p>
  <p>This is the model we intend to solve. The next task is to choose a finite representation that a computer can update.</p>
  </div>
</div>
''',
)

set_source(
    nb,
    "54e20377-5977-4ea6-a97b-7482a438a6c9",
    r'''
## First explore the parameter space

<div class="two-panel equal-panels">
<div class="image-panel"><img src="images/Hopfed_turingles.png" alt="Interactive Gray–Scott patterns" style="width:100%;"></div>
<div class="text-panel">
<p>Use the explorable first as a qualitative map. Hold the diffusion rates fixed, vary one of $(f,k)$ at a time, and record which morphologies change.</p>
<p><a href="https://www.complexity-explorables.org/explorables/hopfed-turingles/">Open the Complexity Explorable</a></p>
<p>We return to this parameter space after constructing the discrete update. Then the controls will have mathematical as well as visual meaning.</p>
</div>
</div>
''',
)

set_source(
    nb,
    "week03-neighbourhoods",
    r'''
### Which cells count as neighbours?

<img src="images/grid_neighbourhoods.svg" alt="Von Neumann and Moore neighbourhoods on square grids" style="display:block;width:70%;max-height:330px;object-fit:contain;margin:0 auto .35rem;">

<div class="two-panel equal-panels">
<div class="text-panel"><p><strong>Von Neumann</strong></p><p>Four edge-sharing cells. This is the standard five-point finite-difference Laplacian.</p></div>
<div class="text-panel"><p><strong>Moore</strong></p><p>Eight surrounding cells. It is useful when diagonal influence is part of the rule or deliberately weighted to improve rotational symmetry.</p></div>
</div>

<div class="choice-marker"><img src="images/choice_marker.svg" alt="Modelling choice" width="36" height="36"><span>Other neighbourhoods are possible. A diagonal cell is farther away than an edge-sharing cell, and material does not literally cross a shared corner. Equal diagonal and edge weights therefore describe a different process rather than an automatic improvement.</span></div>
''',
)

set_source(
    nb,
    "week03-neighbourhoods-reader",
    r'''
### Moore and von Neumann neighbourhoods

<img src="images/grid_neighbourhoods.svg" alt="Von Neumann and Moore neighbourhoods on square grids" style="display:block;width:64%;max-width:720px;margin:0 auto .6rem;">

A **von Neumann neighbourhood** contains the four cells sharing an edge with the focal cell. It is the natural choice for the standard five-point finite-difference Laplacian and for a rule that permits movement only across shared edges.

A **Moore neighbourhood** also contains the four diagonal cells. It is suitable when diagonal interaction is genuinely part of the rule. It should not be selected simply because it contains more information. A diagonal centre is farther away by a factor of $\sqrt{2}$, and material does not literally pass through a shared corner in the same way that it crosses an edge. Numerical diffusion schemes that include diagonals therefore need deliberate weights.

Other neighbourhoods and wider stencils are possible. The choice specifies which local information can affect an update, and it can change both the intended mechanism and grid-direction artefacts.
''',
)

set_source(
    nb,
    "b7ed04b2-de4a-400b-9f93-25974cb34399",
    r'''
### Why does this produce diffusion?

The discrete Laplacian compares the focal value with nearby values. A local peak gives a negative result and is reduced; a local valley gives a positive result and is increased. Repeating that local averaging smooths concentration differences while the chosen boundary rule determines whether total material is conserved.
''',
)

set_source(
    nb,
    "1c111a8d-516f-4637-95c0-080efdec3d90",
    r'''
## Continuous description: a diffusion field

<div class="two-panel equal-panels">
  <div class="text-panel">
  <p>The field $u(\mathbf x,t)$ records concentration at every location and time. The diffusion coefficient $D$ controls the ensemble spreading rate.</p>
  <p>In one dimension, a positive second derivative means the value sits below its surroundings; diffusion raises it. A negative second derivative marks a local peak; diffusion lowers it.</p>
  <p>The Laplacian $\nabla^2u$ generalises this curvature comparison to several directions. It is positive in a local valley, negative at a local peak and zero on a locally linear field.</p>
  </div>
  <div class="image-panel"><img src="images/Ficks_diffusion_micro_macro.gif" alt="Microscopic particle motion and macroscopic concentration spreading" style="display:block;width:100%;max-height:440px;object-fit:contain;"></div>
</div>

$$
\frac{\partial u}{\partial t}=D\nabla^2u.
$$

<div class="ladder-marker"><img src="images/ladder_marker.svg" alt="Ladder of abstraction"><span><strong>Up the ladder:</strong> replace individual paths by a field equation that preserves their collective spreading.</span></div>
''',
)

set_source(
    nb,
    "4fad79e4-e78d-468c-be71-d70d8c4c711e",
    r'''
## Reader extension: transport as well as diffusion

Reaction–diffusion assumes that there is no imposed bulk flow. If a fluid velocity $\mathbf w$ also carries material, a broader transport equation is

$$
\frac{\partial u}{\partial t}
+\nabla\!\cdot(\mathbf w u)
=D\nabla^2u+R(u).
$$

Here $\nabla\!\cdot(\mathbf w u)$ is **advection**, which transports concentration with the flow; $D\nabla^2u$ is **diffusion**, which smooths local differences; and $R(u)$ creates or removes material locally.

This extension is included for students who have met transport PDEs. It is not required for the Gray–Scott model used this week.
''',
)
transport_cell = next(c for c in nb.cells if c.get("id") == "4fad79e4-e78d-468c-be71-d70d8c4c711e")
transport_cell.metadata["tags"] = ["reader-only"]
transport_cell.metadata["slideshow"] = {"slide_type": "skip"}

set_source(
    nb,
    "534e95c9-97e8-4864-b3cc-66d3c2e9e0aa",
    r'''
## Discretise space

To simulate a continuous field, sample it at grid cells and replace spatial derivatives with neighbour comparisons.

<img src="images/diffusion_grid_numbers_t012.svg" alt="Numerical concentration values at discrete time levels zero, one and two" style="display:block;width:82%;max-height:440px;object-fit:contain;margin:0 auto;">

<div class="discussion-marker"><img src="images/discussion_marker.svg" alt="Discussion prompt"><span>The values are precise. Can you see the spatial pattern quickly?</span></div>

<div class="ladder-marker"><img src="images/ladder_marker.svg" alt="Ladder of abstraction"><span><strong>Down the ladder:</strong> inspect the value stored in each cell at discrete time level $n$.</span></div>
''',
)

# The exact-value grid is now part of “Discretise space”; remove its duplicate.
nb.cells = [c for c in nb.cells if c.get("id") != "week03-diffusion-numbers-t012"]

# Remove the superseded transport-equation expansion.  The concise reader-only
# extension above keeps the useful connection without interrupting the
# reaction-diffusion narrative or introducing a second notation system.
legacy_transport_ids = {
    "37657297-cfc2-4009-b14b-ba11959e6d92",
    "349945e6-9630-4b03-9928-ecbc2e849df9",
    "c623110e-be57-41f5-a3f7-f2357ccb453f",
}
nb.cells = [c for c in nb.cells if c.get("id") not in legacy_transport_ids]

set_source(
    nb,
    "ecd5c9ba-5acd-42ce-9fba-d6a584a56494",
    r'''
### Can everyone recover the same information?

<div class="two-panel equal-panels">
<div class="image-panel">
<img src="images/Colourblind.png" alt="A pseudo-Ishihara colour-vision image" style="display:block;width:72%;max-height:390px;object-fit:contain;margin:0 auto;">
</div>
<div class="text-panel">
<p>I did my PhD, and continue to work, with someone who is red–green colour blind. He cannot see the number inside this circle.</p>
<p>Red–green colour-vision deficiency affects about 8% of men and 0.5% of women in populations where it has been most extensively measured. Prevalence varies between populations.</p>
<p>I may mark your project on a colour screen and see a full rainbow. Aim for a higher standard: the ordering and conclusion should also survive colour-vision differences and black-and-white printing.</p>
</div>
</div>

<p class="figure-reference">Prevalence summary: Webvision, NCBI Bookshelf, “Prevalence of congenital color deficiencies.”</p>
''',
)

set_source(
    nb,
    "62003953",
    r'''
### Design colour deliberately

<div class="two-panel equal-panels">
<div class="image-panel"><img src="images/colormap_good_bad.svg" alt="Accessible sequential colormaps compared with rainbow and red-green scales" style="display:block;width:100%;max-height:410px;object-fit:contain;"></div>
<div class="text-panel">
<p>Colour is part of the representation, not decoration.</p>
<p><strong>Prefer:</strong> perceptually ordered sequential maps such as <code>viridis</code>, <code>cividis</code> and <code>plasma</code> for concentration.</p>
<p><strong>Avoid:</strong> rainbow scales and red–green contrasts when ordered values must be read accurately.</p>
<p>Check the figure in greyscale. Also use labels, line styles or markers when colour distinguishes categories.</p>
</div>
</div>

<p class="figure-reference"><a href="https://matplotlib.org/stable/users/explain/colors/colormaps.html">Matplotlib: Choosing Colormaps</a> · <a href="https://www.nature.com/articles/d41586-021-02696-z">Nature guide</a> · <a href="https://www.ascb.org/science-news/how-to-make-scientific-figures-accessible-to-readers-with-color-blindness/">ASCB guide</a></p>
''',
)

set_source(
    nb,
    "09eb9036-81a5-4e05-8806-69d16664865b",
    r'''
### Index the grid before approximating derivatives

<div class="two-panel equal-panels">
<div class="image-panel"><img src="images/grid_indexing_Uij.svg" alt="A grid showing a focal value and neighbouring indices" style="width:100%;max-height:420px;object-fit:contain;"></div>
<div class="text-panel">
<p>The continuous field is now known only at grid points. $U^n_{i,j}$ means the approximation at row $i$, column $j$, and discrete time level $n$.</p>
<p>A gradient describes direction and rate of steepest increase. Gray–Scott does not need the gradient directly, so we do not build a separate gradient operator here.</p>
<p>We do need the Laplacian. Its finite-difference approximation will compare this focal value with its neighbours.</p>
</div>
</div>
''',
)

set_source(
    nb,
    "0ac1d921-5f1e-4b64-8c65-8454c1e70e8f",
    r'''
## Assemble the complete discrete model

After choosing a grid, spatial stencil and time step, the continuous model becomes

$$
u^{n+1}_{i,j}=u^n_{i,j}
+\Delta t\left[
D_u(\nabla_h^2u^n)_{i,j}
-u^n_{i,j}(v^n_{i,j})^2
+f(1-u^n_{i,j})
\right],
$$

$$
v^{n+1}_{i,j}=v^n_{i,j}
+\Delta t\left[
D_v(\nabla_h^2v^n)_{i,j}
+u^n_{i,j}(v^n_{i,j})^2
-(f+k)v^n_{i,j}
\right].
$$

Both right-hand sides use time level $n$. Only after both have been calculated do we replace the old arrays with the new arrays.

<div class="ladder-marker"><img src="images/ladder_marker.svg" alt="Ladder of abstraction"><span><strong>Down the ladder:</strong> the PDE has become a local numerical update that can be inspected, tested and debugged.</span></div>
''',
)

# The time discretisation must precede the assembled fully discrete update.
move_after(nb, "0ac1d921-5f1e-4b64-8c65-8454c1e70e8f", "d3786649-2fd4-4766-8d86-df7cd2839294")

# Return to an implementation only after the fully discrete update is known.
simulation_id = "week03-return-to-simulation"
simulation_source = r'''
## Return to the simulated system

<div class="two-panel equal-panels">
<div class="image-panel"><img src="images/gray_scott_classic.svg" alt="A Gray–Scott concentration field simulated from the complete discrete update" style="display:block;width:88%;max-height:490px;object-fit:contain;margin:0 auto;"></div>
<div class="text-panel">
<p>This run uses $D_u=0.16$, $D_v=0.08$, $f=0.035$ and $k=0.065$ from a local perturbation.</p>
<p>Pause here before sweeping parameters. Check one update, confirm the boundary and refinement choices, then compare morphologies across $(f,k)$.</p>
<p>The explorable gives a fast qualitative map. Our own implementation lets us test whether a pattern survives changes in grid spacing, time step, initial condition and observable.</p>
</div>
</div>

<div class="ladder-marker"><img src="images/ladder_marker.svg" alt="Ladder of abstraction"><span><strong>Up the ladder:</strong> once the local update is trusted, compare many runs to reveal robust regions of parameter space.</span></div>
'''.strip()
existing_sim = next((c for c in nb.cells if c.get("id") == simulation_id), None)
if existing_sim is None:
    existing_sim = nbformat.v4.new_markdown_cell(simulation_source)
    existing_sim["id"] = simulation_id
    existing_sim.metadata["tags"] = ["slides"]
    existing_sim.metadata["slideshow"] = {"slide_type": "slide"}
    anchor = next(i for i, c in enumerate(nb.cells) if c.get("id") == "0ac1d921-5f1e-4b64-8c65-8454c1e70e8f")
    nb.cells.insert(anchor + 1, existing_sim)
else:
    existing_sim.source = simulation_source
    move_after(nb, simulation_id, "0ac1d921-5f1e-4b64-8c65-8454c1e70e8f")

# Keep this modelling choice as Reader context, but not as a separate slide.
set_source(
    nb,
    "week03-choosing-representation-reader",
    r'''
## Choosing the level of description

Particle paths retain stochastic fluctuations and individual histories. Concentration fields reveal collective transport. Grid values make the continuous equations computable. System-level observables and parameter sweeps reveal robust behaviour across runs or modelling choices.

This continues the Week 1 modelling process. We still identify a state, initialise it, specify dynamics, pause one update, choose observables and vary parameters. Week 2 also supplies a warning: a visually intricate pattern is not itself an explanation, and any morphological measurement must be tied to a stated scale and representation.
''',
)
move_after(nb, "week03-choosing-representation-reader", "week03-sand-zebra-first")

# Remove the duplicated answer reveal, Reader practice and its duplicate outputs.
remove_ids = {
    "ea36afa9-fb04-466d-8be2-b06e97766cf8",
    "fceb8a4d-ace1-43ca-be0a-33d1efdeecde",
    "2ed906af-cf26-424b-9c08-752ab6f99e41",
    "185a81bb-3356-4da3-97b0-b2e8b7857530",
    "c8c241e4-a4b4-4dd4-b4f0-06b8f0349c95",
    "week03-choosing-representation",
    "week03-gray-scott-citations",
}
nb.cells = [c for c in nb.cells if c.get("id") not in remove_ids]

set_source(
    nb,
    "week03-gray-scott-world",
    r'''
# Test the mechanism in a chemical system

<div class="two-panel equal-panels">
<div class="image-panel"><img src="images/cima_experimental_turing_patterns.webp" alt="Experimental setup and stationary patterns in a CIMA gel reactor" style="display:block;width:100%;max-height:410px;object-fit:contain;"></div>
<div class="text-panel">
<p><strong>CIMA gel reactor</strong></p>
<p>Reactants diffuse through an unstirred gel supplied by reservoirs. Starch binds iodide and changes the effective transport rates.</p>
<p>Within part of the operating range, an initially uniform reactor develops stationary hexagons or labyrinths. The experiment tests whether reaction, differential transport and sustained driving can break spatial symmetry under controlled conditions.</p>
</div>
</div>

<p class="figure-reference">The morphology is evidence to measure; the experimental controls and transport mechanism are what make the mechanistic test possible.</p>
''',
)

# Keep the detailed historical bridge and kinetic qualification in the Reader,
# while the slides carry their compact versions.
reader_history_id = "week03-gray-scott-history-reader"
reader_history_source = r'''
# From Turing to Gray–Scott

Turing supplied a general framework rather than a single chemical scheme: nonlinear local reactions coupled by diffusion can generate spatial structure.

Peter Gray and Stephen K. Scott originally studied **cubic autocatalysis** in an open, continuously stirred reactor. Their problem concerned the dynamics and multiple steady states of a continuously fed chemical system, not animal coats. The reaction product helps produce more of itself:

$$U+2V\longrightarrow3V.$$

John Pearson later simulated the spatially extended equations and mapped a striking catalogue of spots, waves, splitting structures and irregular dynamics. A short explicit rule, inexpensive numerical implementation and rich parameter space made Gray–Scott a useful canonical reaction–diffusion model.

Gray–Scott belongs to Turing's broader reaction–diffusion framework, but not every Gray–Scott pattern is a classical **Turing pattern**. That narrower label requires a uniform equilibrium that is stable without diffusion and destabilised by differential diffusion. Gray–Scott also supports transients and finite-amplitude behaviour outside that case.

*Gray and Scott (1983, 1984) studied cubic autocatalysis in open stirred reactors; Pearson (1993) established the familiar computational pattern catalogue.*
'''.strip()
reader_history = next((c for c in nb.cells if c.get("id") == reader_history_id), None)
if reader_history is None:
    reader_history = nbformat.v4.new_markdown_cell(reader_history_source)
    reader_history["id"] = reader_history_id
    reader_history.metadata["tags"] = ["reader-only"]
    reader_history.metadata["slideshow"] = {"slide_type": "skip"}
    anchor = next(i for i, c in enumerate(nb.cells) if c.get("id") == "week03-gray-scott-history")
    nb.cells.insert(anchor + 1, reader_history)
else:
    reader_history.source = reader_history_source
    move_after(nb, reader_history_id, "week03-gray-scott-history")

reader_rate_id = "week03-mass-action-reader"
reader_rate_source = r'''
## Why does the rate contain $uv^2$?

For an **elementary** reaction governed by mass-action kinetics, the reaction rate is proportional to the product of the reactant concentrations raised to their stoichiometric powers. Treating

$$U+2V\longrightarrow3V$$

as elementary therefore gives $r=Kuv^2$. The Gray–Scott equations are normally nondimensionalised so that the constant $K$ is absorbed into the units, leaving $uv^2$.

This is conditional on two modelling decisions: the proposed reaction mechanism and the mass-action approximation. Once those decisions are made, however, $uv^2$ is not an arbitrary term chosen to make an attractive pattern.
'''.strip()
reader_rate = next((c for c in nb.cells if c.get("id") == reader_rate_id), None)
if reader_rate is None:
    reader_rate = nbformat.v4.new_markdown_cell(reader_rate_source)
    reader_rate["id"] = reader_rate_id
    reader_rate.metadata["tags"] = ["reader-only"]
    reader_rate.metadata["slideshow"] = {"slide_type": "skip"}
    anchor = next(i for i, c in enumerate(nb.cells) if c.get("id") == "8858f425-48a5-492b-9a5a-2d277dacc632")
    nb.cells.insert(anchor + 1, reader_rate)
else:
    reader_rate.source = reader_rate_source
    move_after(nb, reader_rate_id, "8858f425-48a5-492b-9a5a-2d277dacc632")

# This list supports the Reader discussion but is too detailed for the deck.
measure_cell = next(c for c in nb.cells if c.get("id") == "week03-brownian-ensemble")
measure_cell.metadata["tags"] = ["reader-only"]
measure_cell.metadata["slideshow"] = {"slide_type": "skip"}

# The figure-building pass recreates this cell, so restore its stable id before
# applying the final wording.
ensemble_slide = next(
    (c for c in nb.cells if c.get("id") == "bf26cf2d"),
    next(c for c in nb.cells if c.cell_type == "markdown" and c.source.startswith("### From one path to an ensemble")),
)
ensemble_slide["id"] = "bf26cf2d"
set_source(
    nb,
    "bf26cf2d",
    r'''
### From one path to an ensemble

<img src="images/brownian_ensemble_msd.svg" alt="Squared displacement for individual Brownian paths, their ensemble mean and the theoretical diffusion law" style="display:block;width:82%;max-height:440px;object-fit:contain;margin:0 auto;">

<p class="small-note">The wide spread is expected. In two dimensions, the squared displacement of one Brownian walker at a fixed time has a standard deviation equal to its mean. Averaging many walkers reveals the stable law.</p>

<div class="ladder-marker"><img src="images/ladder_marker.svg" alt=""><span><strong>Up the ladder over walkers and random histories:</strong> individual paths vary widely, while their mean-square displacement approaches <em>4Dt</em>.</span></div>
''',
)

nbformat.write(nb, LECTURE)


ws = nbformat.read(WORKSHOP, as_version=4)
interpret = next(c for c in ws.cells if c.get("id") == "interpret-comparison")
extension = next((c for c in ws.cells if c.get("id") == "extensions"), None)
interpret.source = r'''
# Further investigation

There is no universally best feed or kill rate. A preferred parameter pair exists only after specifying a pattern, biological question, or quantitative objective.

First interpret the comparison already produced:

1. Which visual differences are captured by variance?
2. Which are invisible to it?
3. Did the refinement check support interpreting these differences?
4. Which aspects are chemistry, and which depend on the numerical representation?

Then choose one extension. Record a prediction and preserve the tested baseline.

- **Challenge a boundary choice:** implement no-flux boundaries and test the boundary operator before simulating.
- **Challenge an observable:** implement an observable that distinguishes spots from stripes and test it on constructed fields first.
- **Challenge the initial condition:** vary perturbation geometry or noise amplitude while holding model parameters fixed.
'''.strip()
if extension is not None:
    ws.cells.remove(extension)
nbformat.write(ws, WORKSHOP)

print(f"Updated {LECTURE}")
print(f"Updated {WORKSHOP}")
