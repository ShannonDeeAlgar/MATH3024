"""Apply the final Week 3 narrative, hierarchy, and Reader-safe formatting pass."""

from pathlib import Path

import nbformat


ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK = ROOT / "notebooks/week03/L_Reaction_diffusion.ipynb"


def set_source(nb, cell_id, source):
    for cell in nb.cells:
        if cell.get("id") == cell_id:
            cell.source = source.strip() + "\n"
            return
    raise KeyError(cell_id)


nb = nbformat.read(NOTEBOOK, as_version=4)

set_source(
    nb,
    "week03-same-mechanism-different-pattern",
    r'''
# Related mechanisms, different patterns

<div class="analysis-perspectives three coat-cards">
  <div><img src="images/cheetah_coat_card.jpg" alt="Cheetah coat"><strong>Cheetah</strong><p>Small spots</p></div>
  <div><div style="overflow:hidden;"><img src="images/leopard_coat_card.jpg" alt="Leopard coat" style="width:112%;max-width:none;margin-left:-6%;"></div><strong>Leopard</strong><p>Rosettes</p></div>
  <div><img src="images/jaguar_coat_card.jpg" alt="Jaguar coat"><strong>Jaguar</strong><p>Rosettes with central spots</p></div>
</div>

<div class="discussion-marker"><img src="images/discussion_marker.svg" alt="Discussion prompt"><span>Could related local interactions generate different system-level patterns?</span></div>
''',
)

set_source(
    nb,
    "7347319d-2e0d-49d0-a1c3-ac02ffcd446d",
    r'''
## Convection cells

<div class="two-panel equal-panels">
<div class="image-panel">
<iframe width="100%" height="340" src="https://www.youtube.com/embed/nQUH9nGTZTY"
title="Rayleigh–Bénard convection experiment" frameborder="0"
referrerpolicy="strict-origin-when-cross-origin"
allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
allowfullscreen></iframe>
</div>
<div class="text-panel">
<p><strong>Rayleigh–Bénard convection</strong></p>
<p>Heating a fluid from below can organise circulation into persistent cells. The pattern is produced by buoyancy and flow, not biological growth.</p>
</div>
</div>

<p class="figure-reference"><a href="https://www.youtube.com/watch?v=nQUH9nGTZTY">Rayleigh–Bénard convection experiment</a>.</p>
''',
)

for cell_id, heading in [
    ("week03-garlic-voronoi", "## Cell-like partitions"),
    ("37090ea1-8469-43c1-82a4-15f95adc8616", "## Folded surfaces"),
    ("7530f174-b927-4f48-88af-1a06f5b4cfce", "## Travelling waves"),
]:
    for cell in nb.cells:
        if cell.get("id") == cell_id:
            lines = cell.source.splitlines()
            lines[0] = heading
            cell.source = "\n".join(lines) + "\n"

set_source(
    nb,
    "week03-turing-paper-scope",
    r'''
## Turing’s reaction–diffusion framework

Let $a(\mathbf{x},t)$ and $b(\mathbf{x},t)$ be morphogen concentrations:

$$
\frac{\partial a}{\partial t}=F(a,b)+D_a\nabla^2a,
\qquad
\frac{\partial b}{\partial t}=G(a,b)+D_b\nabla^2b.
$$

- **Reaction:** $F$ and $G$ change concentrations locally.
- **Diffusion:** the Laplacian couples neighbouring locations.

Suppose $(a^*,b^*)$ is a spatially uniform equilibrium, so $F(a^*,b^*)=G(a^*,b^*)=0$. Write a small disturbance as

$$
a=a^*+\delta a,\qquad b=b^*+\delta b.
$$

The perturbation is not an extra term in the model. It is a small change to the state. Linearising the equations asks whether each spatial mode of $(\delta a,\delta b)$ decays or grows.

<div class="choice-marker"><img src="images/choice_marker.svg" alt="Modelling choice"><span>Turing proposed a general mechanism, not one unique pair of reaction functions.</span></div>
''',
)

# The activation/inhibition explanation is incorporated into the essential condition.
for cell in nb.cells:
    if cell.get("id") == "d112f5d4":
        cell.metadata["tags"] = sorted(set(cell.metadata.get("tags", [])) | {"remove-cell"})

set_source(
    nb,
    "week03-turing-six-modes",
    r'''
## The essential condition for a Turing instability

<div class="qa-grid">
  <div><strong>Without diffusion</strong><p>The spatially uniform equilibrium is stable. A small local disturbance decays.</p></div>
  <div><strong>With unequal diffusion</strong><p>The same equilibrium becomes unstable to at least one spatial disturbance. That mode grows.</p></div>
</div>

$$
\text{stable local chemistry}+\text{differential diffusion}
\longrightarrow \text{spatial pattern}
$$

Local activation with a faster, longer-range inhibitory influence is a useful intuition for many Turing systems. Reaction provides feedback; unequal diffusion gives the influences different spatial ranges. These phrases describe how the mechanism behaves, not two additional terms in the equations.

<div class="ladder-marker"><img src="images/ladder_marker.svg" alt="Ladder of abstraction"><span><strong>Up the ladder:</strong> ask which perturbation modes grow instead of following every molecule.</span></div>
''',
)

for cell_id, heading in [
    ("week03-turing-six-reader", "### Linear stability analysis"),
    ("week03-turing-dappled", "### Turing calculated a pattern by hand"),
]:
    for cell in nb.cells:
        if cell.get("id") == cell_id:
            lines = cell.source.splitlines()
            lines[0] = heading
            cell.source = "\n".join(lines) + "\n"

set_source(
    nb,
    "week03-gray-scott-history",
    r'''
# From Turing to Gray–Scott

Turing supplied the general framework. Gray–Scott gives us one explicit model that is cheap to simulate and rich enough to explore.

Peter Gray and Stephen K. Scott originally studied cubic autocatalysis in an open, continuously stirred reactor. The reaction product helps produce more of itself:

$$
U+2V\longrightarrow 3V.
$$

John Pearson later simulated the spatially extended model and mapped a striking catalogue of spots, waves, splitting structures and irregular dynamics. This combination of a short rule, inexpensive computation and a rich parameter space made Gray–Scott a canonical reaction–diffusion model.

It belongs to Turing’s broader reaction–diffusion framework. Only regimes created by a diffusion-driven instability of a stable uniform equilibrium are classical **Turing patterns**; Gray–Scott also supports transients and finite-amplitude behaviour outside that narrower case.

<p class="figure-reference">Gray and Scott (1983, 1984) studied cubic autocatalysis in open stirred reactors; Pearson (1993) established the familiar computational pattern catalogue.</p>
''',
)

set_source(
    nb,
    "b7c839be-6ee3-4fef-9aae-72b880dbb4b9",
    r'''
### Random walk: a discrete model

<div class="two-panel equal-panels">
<div class="image-panel"><img src="images/random_walk_types_stats.svg" alt="Unbiased, biased and persistent random walks with the statistics used to compare them" style="display:block;width:100%;max-height:430px;object-fit:contain;"></div>
<div class="text-panel">
<p>A random walk is built by adding successive random steps.</p>
<p><strong>Unbiased:</strong> no preferred direction.</p>
<p><strong>Biased:</strong> a non-zero mean step creates drift.</p>
<p><strong>Persistent:</strong> successive directions are correlated.</p>
</div>
</div>

$$
\mathbf{X}_n=\sum_{m=1}^{n}\boldsymbol{\xi}_m,
\qquad
\mathbb{E}[\boldsymbol{\xi}_m]=\mathbf{0}
\quad\text{for an unbiased walk}.
$$

For diffusion we begin with independent, unbiased increments of finite variance. We then examine displacement, squared displacement and their ensemble averages.
''',
)

set_source(
    nb,
    "11879310",
    r'''
### Brownian motion: the physical phenomenon

<div class="two-panel equal-panels">
<div class="image-panel"><img src="images/brownian_motion_nanoparticles.gif" alt="Brownian motion of polymer nanoparticles" style="display:block;width:82%;max-height:330px;object-fit:contain;margin:0 auto;"></div>
<div class="text-panel">
<p>Brownian motion is the continuous-time stochastic limit of many small, independent random steps.</p>
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

<p class="figure-reference">Brownian motion of 350 nm polymer nanoparticles: Yasrena, Wikimedia Commons, CC BY-SA 4.0.</p>
''',
)

set_source(
    nb,
    "08162448",
    r'''
### One path: distance from the origin

<img src="images/brownian_distance_sqrt.svg" alt="Two Brownian trajectories and their distances from the origin compared with square-root reference curves" style="display:block;width:86%;max-height:430px;object-fit:contain;margin:0 auto;">

Running longer does not make an individual path follow the square-root curve. $\sqrt{2dDt}$ is a typical ensemble distance scale, not a deterministic trajectory.

<div class="ladder-marker"><img src="images/ladder_marker.svg" alt=""><span><strong>Stay low:</strong> inspect the irregular path. Then move up to an ensemble statistic to recover the diffusion law.</span></div>
''',
)

set_source(
    nb,
    "36fa3ed0",
    r'''
## The complete Gray–Scott model

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
  </div>
</div>
''',
)

set_source(
    nb,
    "d67005af-86fe-4102-b7b8-0cf9f629d586",
    r'''
# Diffusion as a change of representation

Reaction–diffusion is this week’s modelling framework. Inside it sits a more general modelling decision:

<div class="discussion-marker"><img src="images/discussion_marker.svg" alt="Discussion prompt"><span>Should we represent moving particles, a continuous concentration field, or values on a numerical grid?</span></div>

We will move between all three. Each representation answers different questions and hides different details.
''',
)

set_source(
    nb,
    "1c111a8d-516f-4637-95c0-080efdec3d90",
    r'''
## Continuous description: a diffusion field

$$
\frac{\partial u}{\partial t}=D\nabla^2u.
$$

<div class="two-panel equal-panels">
  <div class="text-panel">
  <p>The field <em>u</em> records concentration at each location and time.</p>
  <p>The diffusion coefficient <em>D</em> controls the ensemble spreading rate.</p>
  </div>
  <div class="image-panel"><img src="images/Ficks_diffusion_micro_macro.gif" alt="Microscopic particle motion and macroscopic concentration spreading"></div>
</div>

<div class="ladder-marker"><img src="images/ladder_marker.svg" alt="Ladder of abstraction"><span><strong>Up the ladder:</strong> replace individual paths by a smooth field whose evolution captures their collective effect.</span></div>
''',
)

set_source(
    nb,
    "8d24112f-90ca-4f2e-b3d6-26a6612e7d5f",
    r'''
## From a random walk to the diffusion equation

Consider a particle on a one-dimensional grid. At each time step $\Delta t$, it moves left or right by $\Delta x$ with equal probability. If $P(x,t)$ is the probability of finding it at $x$ at time $t$, then

$$
P(x,t+\Delta t)=\frac12P(x-\Delta x,t)+\frac12P(x+\Delta x,t).
$$

Taylor-expand both sides. Symmetry cancels the first-order spatial terms, leaving

$$
\Delta t\,\frac{\partial P}{\partial t}
=\frac12\Delta x^2\frac{\partial^2P}{\partial x^2}+\text{higher-order terms}.
$$

Let

$$
D=\frac{\Delta x^2}{2\Delta t},
$$

and take the continuum limit while holding $D$ fixed. The result is

$$
\frac{\partial P}{\partial t}=D\frac{\partial^2P}{\partial x^2}.
$$

The continuum field retains the collective spreading law and discards each particle’s particular sequence of steps.
''',
)

set_source(
    nb,
    "09eb9036-81a5-4e05-8806-69d16664865b",
    r'''
### Approximate the gradient

<div class="two-panel equal-panels">
<div class="text-panel">
<p>In continuous space, the gradient points in the direction of steepest increase. Its components are limits of changes over arbitrarily small distances.</p>
<p>After discretising, the field is known only at grid points. We therefore replace the derivative by a finite difference between nearby values.</p>
</div>
<div class="image-panel"><img src="images/grid_indexing_Uij.svg" alt="A five by five grid labelled with U sub i comma j" style="width:100%;max-height:430px;object-fit:contain;"></div>
</div>

$$
\left.\frac{\partial U}{\partial x}\right|_{i,j}
\approx\frac{U_{i+1,j}-U_{i-1,j}}{2\Delta x},
\qquad
\left.\frac{\partial U}{\partial y}\right|_{i,j}
\approx\frac{U_{i,j+1}-U_{i,j-1}}{2\Delta y}.
$$

<div class="choice-marker"><img src="images/choice_marker.svg" alt=""><span>Central differences use information equally far to either side. They become more accurate as the grid spacing decreases.</span></div>
''',
)

set_source(
    nb,
    "2d86506f-baf9-4f97-9a53-63015dd1e05f",
    r'''
### Convolve with the five-point stencil

$$
L=\begin{bmatrix}0&1&0\\1&-4&1\\0&1&0\end{bmatrix}.
$$

<div class="two-panel equal-panels">
<div class="image-panel"><img src="images/laplacian_convolution_example.svg" alt="A numerical example of convolving a grid with the five-point Laplacian stencil" style="width:100%;"></div>
<div class="text-panel">
<p>Place the stencil over one cell, multiply overlapping entries, and add. Then slide it to the next cell.</p>
<p>A constant patch gives zero. A high centre gives a negative result; a low centre gives a positive result.</p>
<p>The same local comparison is applied everywhere, producing a field of approximate Laplacian values.</p>
</div>
</div>
''',
)

set_source(
    nb,
    "fceb8a4d-ace1-43ca-be0a-33d1efdeecde",
    r'''
### Practice: implement the discrete Laplacian

Use

$$
\nabla^2u_{i,j}\approx
u_{i+1,j}+u_{i-1,j}+u_{i,j+1}+u_{i,j-1}-4u_{i,j}
$$

to evolve the system with diffusion coefficient $D_u=0.25$.

1. Compute one update by hand on a small grid.
2. Implement it with nested loops.
3. Repeat using convolution with the five-point stencil.
4. Check that the two implementations agree.
5. Compare this method with the earlier rule-based update.
''',
)

set_source(
    nb,
    "d3786649-2fd4-4766-8d86-df7cd2839294",
    r'''
## Discretise time

Let

$$
t_n=n\Delta t,
$$

where $n=0,1,2,\ldots$ is the time-step index and $\Delta t$ is the chosen finite step size. The notation $u^n_{i,j}$ means the numerical value of the $u$ field at grid cell $(i,j)$ and time $t_n$.

Explicit Euler updates the $u$ field by

$$
u^{n+1}_{i,j}=u^n_{i,j}
+\Delta t\left[
D_u(\nabla_h^2u^n)_{i,j}
-u^n_{i,j}(v^n_{i,j})^2
+f(1-u^n_{i,j})
\right].
$$

The $v$ field is updated from the same time level $n$:

$$
v^{n+1}_{i,j}=v^n_{i,j}
+\Delta t\left[
D_v(\nabla_h^2v^n)_{i,j}
+u^n_{i,j}(v^n_{i,j})^2
-(f+k)v^n_{i,j}
\right].
$$

<div class="choice-marker"><img src="images/choice_marker.svg" alt="Modelling choice"><span>Grid spacing, time step, stencil and boundary conditions can change the numerical result and must be tested.</span></div>
''',
)

for cell in nb.cells:
    if cell.get("id") == "6f94e1bd":
        additions = [
            '- Gray, P. and Scott, S. K. (1983), “Autocatalytic reactions in the isothermal, continuous stirred tank reactor: Isolas and other forms of multistability”, *Chemical Engineering Science* 38, 29–43.',
            '- Gray, P. and Scott, S. K. (1984), [“Autocatalytic reactions in the isothermal, continuous stirred tank reactor”](https://doi.org/10.1016/0009-2509(84)87017-7), *Chemical Engineering Science* 39, 1087–1097.',
            '- Pearson, J. E. (1993), [“Complex Patterns in a Simple System”](https://doi.org/10.1126/science.261.5118.189), *Science* 261, 189–192.',
            '- Yasrena (2021), [“Brownian Motion.gif”](https://commons.wikimedia.org/wiki/File:Brownian_Motion.gif), Wikimedia Commons, CC BY-SA 4.0.',
        ]
        for addition in additions:
            if addition not in cell.source:
                cell.source = cell.source.rstrip() + "\n" + addition + "\n"
        break

nbformat.write(nb, NOTEBOOK)
print(f"Updated {NOTEBOOK}")
