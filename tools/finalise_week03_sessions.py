#!/usr/bin/env python3
"""Apply the agreed two-session teaching spine to the Week 3 lecture notebook."""

from pathlib import Path

import nbformat


ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "notebooks/week03/L_Reaction_diffusion.ipynb"


def main() -> None:
    nb = nbformat.read(PATH, as_version=4)
    by_id = {cell.get("id"): cell for cell in nb.cells}

    def set_cell(cell_id: str, source: str, tags=None, slide_type=None) -> None:
        cell = by_id[cell_id]
        cell.source = source.strip() + "\n"
        if tags is not None:
            cell.metadata["tags"] = tags
        if slide_type is not None:
            cell.metadata.setdefault("slideshow", {})["slide_type"] = slide_type

    # The canonical model is Gray–Scott. Random walks are a supporting model
    # used to motivate the change from particles to concentration fields.
    set_cell(
        "d0dd3fdf-7bad-4b0c-b3bb-594128690712",
        r"""
# Reaction–diffusion systems
## MATH3024 · Week 3

<div class="canonical-model-marker"><span>Canonical model</span><strong>Gray–Scott reaction–diffusion</strong></div>

<p class="slide-subtitle">Supporting model: random-walk diffusion</p>
""",
        [],
        "slide",
    )

    # Compress the opening examples into two purposeful comparison tables.
    set_cell(
        "week03-same-mechanism-different-pattern",
        r"""
# Related mechanisms, different patterns

<div class="analysis-perspectives three coat-cards">
  <div><img src="images/cheetah_coat_card.jpg" alt="Cheetah coat"><strong>Cheetah</strong><p>Small spots</p></div>
  <div><img src="images/leopard_coat_card.jpg" alt="Leopard coat"><strong>Leopard</strong><p>Rosettes</p></div>
  <div><img src="images/jaguar_coat_card.jpg" alt="Jaguar coat"><strong>Jaguar</strong><p>Rosettes with central spots</p></div>
</div>

<div class="discussion-marker"><img src="images/discussion_marker.svg" alt="Discussion prompt"><span>Could related local interactions generate different system-level patterns?</span></div>
""",
        ["slides"],
        "slide",
    )
    set_cell(
        "week03-sand-zebra-first",
        r"""
# Similar patterns, different mechanisms

| Form | Example systems | Candidate mechanism |
|---|---|---|
| **Stripes** | sand dunes; zebra coat | transport and deposition; reaction and diffusion |
| **Cells** | garlic tissue; Voronoi growth | biological packing; nearest-seed construction |
| **Folds** | brain cortex; swelling gel | differential growth; elastic instability |
| **Waves** | slime mould; oscillating chemistry | cell signalling; chemical reaction–diffusion |

<div class="discussion-marker"><img src="images/discussion_marker.svg" alt="Discussion prompt"><span>Visual resemblance is evidence to investigate, not evidence of a shared mechanism.</span></div>
""",
        ["slides"],
        "slide",
    )
    for cell_id in (
        "7347319d-2e0d-49d0-a1c3-ac02ffcd446d",
        "week03-garlic-voronoi",
        "37090ea1-8469-43c1-82a4-15f95adc8616",
        "7530f174-b927-4f48-88af-1a06f5b4cfce",
    ):
        by_id[cell_id].metadata["tags"] = ["reader-only"]

    # Turing's life remains Reader enrichment; the live deck keeps only the
    # scientific question and the assessable mechanism.
    by_id["week03-alan-mathison-turing"].metadata["tags"] = ["reader-only"]
    set_cell(
        "a0a1efe7-e26e-4f6d-a529-3db70b3fe94f",
        r"""
# Turing’s question

<div class="two-panel equal-panels">
  <div class="image-panel"><img src="images/Turing_and_imitation_game.png" alt="Alan Turing and a representation of the imitation game"></div>
  <div class="text-panel"><h3>How does form emerge?</h3><p>An embryo can begin close to uniform, yet organised spatial differences appear.</p><p>Could local chemical reactions and ordinary diffusion create that structure without a pre-drawn template?</p></div>
</div>

<p class="figure-reference">A. M. Turing, “The Chemical Basis of Morphogenesis” (1952).</p>
""",
        ["slides"],
        "slide",
    )
    set_cell(
        "week03-turing-paper-scope",
        r"""
# Turing’s reaction–diffusion framework

Let $a(\mathbf x,t)$ and $b(\mathbf x,t)$ be morphogen concentrations:

$$
\frac{\partial a}{\partial t}=F(a,b)+D_a\nabla^2a,
\qquad
\frac{\partial b}{\partial t}=G(a,b)+D_b\nabla^2b.
$$

- **Reaction:** $F$ and $G$ change concentrations locally.
- **Diffusion:** the Laplacian couples neighbouring locations.
- **Perturbation:** a small departure from uniformity tests whether structure grows or disappears.

<div class="choice-marker"><img src="images/choice_marker.svg" alt="Modelling choice"><span>Turing proposed a general mechanism, not one unique pair of reaction functions.</span></div>
""",
        ["slides"],
        "slide",
    )
    set_cell(
        "week03-turing-six-modes",
        r"""
# The essential condition for a Turing instability

<div class="qa-grid">
  <div><strong>Without diffusion</strong><p>The spatially uniform equilibrium is stable. A small local disturbance decays.</p></div>
  <div><strong>With unequal diffusion</strong><p>The same equilibrium becomes unstable to a spatial disturbance. Some modes grow.</p></div>
</div>

$$
\text{stable local chemistry}+\text{differential diffusion}
\longrightarrow \text{spatial pattern}
$$

<div class="ladder-marker"><img src="images/ladder_marker.svg" alt="Ladder of abstraction"><span><strong>Up the ladder:</strong> ask whether a small perturbation grows, rather than follow every molecule.</span></div>
""",
        ["slides"],
        "slide",
    )
    # The six-case eigenvalue classification remains available only as detail.
    set_cell(
        "week03-turing-six-reader",
        r"""
## Turing’s linear analysis

Turing classified several possible responses of a near-uniform state by analysing the growth rates of small perturbations. The full classification distinguishes real and complex eigenvalues and spatial and non-spatial modes. For this unit, the important case is narrower: the local reaction equilibrium is stable without diffusion but unstable to at least one spatial mode when unequal diffusion is introduced.

This qualification matters. A reaction–diffusion simulation may produce waves, oscillations or transient structures without satisfying the classical Turing-instability condition.
""",
        ["reader-only"],
        "skip",
    )
    set_cell(
        "week03-turing-dappled",
        r"""
# Turing calculated a pattern by hand

<div class="two-panel equal-panels">
  <div class="image-panel"><img src="images/Turing_1952_dappled.png" alt="Turing's manually calculated dappled concentration pattern"></div>
  <div class="text-panel"><p>Turing reported that this dappled pattern was produced “in a few hours by a manual computation”.</p><p>The calculation demonstrated possibility, not a literal reconstruction of one animal coat.</p></div>
</div>

<p class="figure-reference">Turing (1952), Fig. 2.</p>
""",
        ["slides"],
        "slide",
    )
    set_cell(
        "week03-gray-scott-history",
        r"""
# From Turing to Gray–Scott

Turing gave a **framework**: local reaction plus unequal diffusion can destabilise a uniform state.

Gray–Scott gives us one explicit, computable model:

$$U+2V\longrightarrow3V,$$

with diffusion, a continuous feed of $U$, and removal of $V$.

We use it because a short rule produces spots, stripes, waves and replication-like structures across its parameter space. It is an example of the broader reaction–diffusion framework. Only parameter regimes satisfying the stability condition should be called classical Turing patterns.

<p class="figure-reference">Peter Gray and Stephen K. Scott developed the open autocatalytic reactor model; Pearson (1993) mapped its computational pattern catalogue.</p>
""",
        ["slides"],
        "slide",
    )

    # Use one consistent notation: U and V name chemical species; lowercase
    # u and v are their concentration fields.
    set_cell(
        "8858f425-48a5-492b-9a5a-2d277dacc632",
        r"""
## 1. Reaction: local positive feedback

The chemical species satisfy

$$U+2V\longrightarrow3V.$$

Let $u(\mathbf x,t)$ and $v(\mathbf x,t)$ be their concentrations. The local reaction rate is $uv^2$:

$$
\frac{\partial u}{\partial t}=-uv^2,
\qquad
\frac{\partial v}{\partial t}=+uv^2.
$$

Existing $V$ helps create more $V$, so a small local excess can be amplified.
""",
        ["slides"],
        "subslide",
    )
    set_cell(
        "562f3685-c727-4a03-ae6e-7e8ed6aaa9c6",
        r"""
## 2. Diffusion: spatial coupling

Reaction changes concentrations at one location. Diffusion connects locations:

$$
\frac{\partial u}{\partial t}=D_u\nabla^2u,
\qquad
\frac{\partial v}{\partial t}=D_v\nabla^2v.
$$

The Laplacian compares a location with its surroundings. Peaks spread out and troughs fill in.

<div class="choice-marker"><img src="images/choice_marker.svg" alt="Modelling choice"><span>The relative diffusion rates affect whether a small spatial disturbance is suppressed or amplified by the coupled system.</span></div>
""",
        ["slides"],
        "subslide",
    )
    set_cell(
        "d1f8631e",
        r"""
## 3. Feed and removal: keep the system driven

Gray–Scott is an open reactor:

$$
\text{feed of }U:\quad f(1-u),
\qquad
\text{removal of }V:\quad -(f+k)v.
$$

- $f$ replenishes $U$ towards the reservoir concentration $u=1$.
- The same flow dilutes $V$ at rate $f$.
- $k$ supplies additional removal of $V$.

Without feed and removal, the autocatalytic reaction would consume its available material and stop.
""",
        ["slides"],
        "subslide",
    )
    set_cell(
        "36fa3ed0",
        r"""
## The complete Gray–Scott model

<div class="two-panel equal-panels">
  <div class="image-panel"><img src="images/gray_scott_model_map.svg" alt="Reaction, diffusion, feed and removal in the Gray–Scott model"></div>
  <div class="text-panel">
  $$\frac{\partial u}{\partial t}=D_u\nabla^2u-uv^2+f(1-u),$$
  $$\frac{\partial v}{\partial t}=D_v\nabla^2v+uv^2-(f+k)v.$$
  <p><strong>Local:</strong> reaction, feed and removal.</p>
  <p><strong>Spatial:</strong> unequal diffusion.</p>
  </div>
</div>
""",
        ["slides"],
        "subslide",
    )
    set_cell(
        "week03-parameter-space",
        r"""
## The parameter space

The model contains four principal parameters:

$$D_u,\qquad D_v,\qquad f,\qquad k.$$

Exploring $m$ values of each would require $m^4$ combinations. This rapid growth is one form of the **curse of dimensionality**.

In practice we often fix $D_u$ and $D_v$ using physical knowledge, then sweep the experimentally controllable feed and removal rates $(f,k)$.

<div class="ladder-marker"><img src="images/ladder_marker.svg" alt="Ladder of abstraction"><span><strong>Up the ladder:</strong> compare many parameter choices to reveal a map of qualitative behaviours.</span></div>
""",
        ["slides"],
        "subslide",
    )
    set_cell(
        "week03-turing-six-evolution",
        r"""
## Return to Turing’s question

The Gray–Scott equations can generate organised structure from an almost uniform initial field.

That result alone does not prove a classical Turing instability. We must still ask:

1. Is the uniform reaction equilibrium stable without diffusion?
2. Does adding unequal diffusion make a spatial mode unstable?
3. Is the observed pattern robust to the numerical representation?

These distinctions separate a visually interesting simulation from a mechanistic explanation.
""",
        ["slides"],
        "subslide",
    )

    # Session 2 makes the representation problem explicit but restrained.
    set_cell(
        "d67005af-86fe-4102-b7b8-0cf9f629d586",
        r"""
# Session 2 · Which representation should we compute?

Reaction–diffusion gives us the modelling framework. Diffusion exposes a more general modelling problem:

<div class="discussion-marker"><img src="images/discussion_marker.svg" alt="Discussion prompt"><span>Should we represent moving particles, a continuous concentration field, or values on a numerical grid?</span></div>

We will move between all three. Each representation answers different questions and hides different details.
""",
        ["slides"],
        "slide",
    )
    set_cell(
        "4f8c9362",
        r"""
# The particle story is not the simulation

Individual molecules really do move and react, but a particle-level chemical simulation would be far more detailed and expensive than our question requires.

Gray–Scott therefore uses **concentration fields**:

$$
\text{many particles}
\longrightarrow
u(\mathbf x,t),\;v(\mathbf x,t).
$$

<div class="ladder-marker"><img src="images/ladder_marker.svg" alt="Ladder of abstraction"><span><strong>Up the ladder:</strong> aggregate many microscopic trajectories into macroscopic concentration fields.</span></div>
""",
        ["slides"],
        "slide",
    )
    by_id["d711b8ba"].metadata["tags"] = ["reader-only"]
    set_cell(
        "2ba9c92e-5488-45b4-a697-7aa99f2bc487",
        r"""
## One phenomenon, two descriptions

| Microscopic description | Macroscopic description |
|---|---|
| Track stochastic particle paths | Track concentration $u(\mathbf x,t)$ |
| Retain fluctuations and individual histories | Average over many particles |
| Expensive at chemical population sizes | Efficient for collective spreading |
| Natural observable: displacement | Natural observable: concentration gradient |

Both can describe diffusion. The appropriate choice depends on the question and scale.
""",
        ["slides"],
        "subslide",
    )
    set_cell(
        "1c111a8d-516f-4637-95c0-080efdec3d90",
        r"""
## Continuous description: a diffusion field

<div class="two-panel equal-panels">
  <div class="text-panel">
  $$\frac{\partial u}{\partial t}=D\nabla^2u.$$
  <p>The field $u(\mathbf x,t)$ records concentration at location $\mathbf x$ and time $t$.</p>
  <p>The diffusion coefficient $D$ controls the ensemble spreading rate.</p>
  </div>
  <div class="image-panel"><img src="images/Ficks_diffusion_micro_macro.gif" alt="Microscopic particle motion and macroscopic concentration spreading"></div>
</div>

<div class="ladder-marker"><img src="images/ladder_marker.svg" alt="Ladder of abstraction"><span><strong>Up the ladder:</strong> replace individual paths by a smooth field whose evolution captures their collective effect.</span></div>
""",
        ["slides"],
        "subslide",
    )
    set_cell(
        "57d73b10-bd0c-4326-b40d-50a7e9eb7c03",
        r"""
## From particle motion to Fick’s laws

A microscopic random walk and a macroscopic concentration field describe the same spreading process at different levels.

Fick’s first law connects concentration differences to flux:

$$
\mathbf J=-D\nabla u.
$$

The gradient points towards increasing concentration, so the minus sign sends net flux down the concentration gradient. Conservation of material then gives

$$
\frac{\partial u}{\partial t}=-\nabla\cdot\mathbf J
=D\nabla^2u.
$$

The diffusion equation is therefore a conservation statement: local concentration changes because material flows between neighbouring regions.
""",
        ["reader-only"],
        "skip",
    )
    set_cell(
        "4fad79e4-e78d-468c-be71-d70d8c4c711e",
        r"""
## Transport, smoothing and local change

$$
\frac{\partial u}{\partial t}
+\nabla\cdot(\mathbf w u)
=D\nabla^2u+R(u).
$$

| Term | Role |
|---|---|
| $\nabla\cdot(\mathbf w u)$ | advection transports material with a flow $\mathbf w$ |
| $D\nabla^2u$ | diffusion smooths local concentration differences |
| $R(u)$ | reaction creates or removes material locally |

Gray–Scott omits advection and couples two reacting, diffusing concentration fields.
""",
        ["slides"],
        "subslide",
    )
    set_cell(
        "954ca579-6444-4529-9190-05fb00912d11",
        r"""
# From continuous equations to a discrete simulation

The concentration fields are continuous, but a computer stores finitely many numbers.

$$
u(\mathbf x,t),v(\mathbf x,t)
\longrightarrow
u^n_{i,j},v^n_{i,j}.
$$

- $(i,j)$ identifies a grid cell.
- $n$ identifies the discrete time level.
- Each value is a concentration, not an individual particle.

<div class="ladder-marker"><img src="images/ladder_marker.svg" alt="Ladder of abstraction"><span><strong>Down the ladder:</strong> choose a computable representation and make each local numerical update explicit.</span></div>
""",
        ["slides"],
        "slide",
    )
    set_cell(
        "d3786649-2fd4-4766-8d86-df7cd2839294",
        r"""
## Discretise time

For the $u$ field, explicit Euler gives

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
""",
        ["slides"],
        "subslide",
    )
    set_cell(
        "week03-choosing-representation",
        r"""
# Choosing a useful representation

| If we need to understand… | Work at the level of… |
|---|---|
| one stochastic trajectory or fluctuation | particles and random walks |
| collective spreading | concentration fields and diffusion equations |
| one numerical update or bug | grid cells, neighbours and stencils |
| robust system-level behaviour | observables, refinement tests and parameter sweeps |

The “best” representation is the least detailed one that preserves what matters for the question.
""",
        ["slides"],
        "slide",
    )
    set_cell(
        "week03-final-discrete-continuous",
        r"""
# The modelling problem underneath the model

$$
\text{particles}
\xrightarrow{\text{aggregate}}
\text{continuous fields}
\xrightarrow{\text{discretise}}
\text{grid values}.
$$

We moved up the ladder to expose collective diffusion, then down the ladder to compute it.

This pattern recurs across Complex Systems: choose a representation, test what it preserves, and change level when the current view cannot answer the question.

<div class="reader-emphasis"><strong>Next:</strong> Week 4 keeps the grid and local neighbourhood, then replaces continuous concentrations with discrete cellular states and rules.</div>
""",
        ["slides"],
        "slide",
    )
    set_cell(
        "week03-choosing-representation-reader",
        r"""
## Choosing the level of description

The appropriate representation depends on the question. Particle paths retain stochastic fluctuations and individual histories. Concentration fields reveal collective transport. Grid values make the continuous equations computable. System-level observables and parameter sweeps reveal robust behaviour across runs or modelling choices.

This continues the Week 1 modelling process. We still identify a state, initialise it, specify dynamics, pause one update, choose observables and vary parameters. Week 2 also supplies a warning: a visually intricate pattern is not itself an explanation, and any morphological measurement must be tied to a stated scale and representation.
""",
        ["reader-only"],
        "skip",
    )

    # Resolve legacy tag conflicts and heading jumps.
    by_id["d711b8ba"].metadata["tags"] = ["reader-only"]
    if "week03-diffusion-numbers-t012" in by_id:
        by_id["week03-diffusion-numbers-t012"].metadata["tags"] = ["slides-only"]
    for cell in nb.cells:
        tags = list(dict.fromkeys(cell.metadata.get("tags", [])))
        if "reader-only" in tags and "slides-only" in tags:
            tags.remove("slides-only")
        cell.metadata["tags"] = tags

    nb.metadata["math3024_teaching_spine"] = {
        "session_1": "pattern question → Turing mechanism → Gray–Scott canonical model → parameter space",
        "session_2": "random walks → concentration field → numerical grid → tested representation",
        "modelling_core": "diffusion as a change of representation",
    }
    nbformat.write(nb, PATH)
    print(f"Updated {PATH} ({len(nb.cells)} cells)")


if __name__ == "__main__":
    main()
