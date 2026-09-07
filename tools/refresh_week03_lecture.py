#!/usr/bin/env python3
"""Bring the Week 3 lecture/Reader source into the current MATH3024 house style."""

from pathlib import Path
import re

import nbformat


ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "notebooks/week03/L_Reaction_diffusion.ipynb"

LADDER = (
    '<div class="ladder-marker"><img src="images/ladder_marker.svg" '
    'alt="Ladder of abstraction" width="30" height="40"><span>{}</span></div>'
)
DISCUSSION = (
    '<div class="discussion-marker"><img src="images/discussion_marker.svg" '
    'alt="Discussion prompt" width="36" height="36"><span>{}</span></div>'
)
CHOICE = (
    '<div class="choice-marker"><img src="images/choice_marker.svg" '
    'alt="Modelling choice" width="36" height="36"><span>{}</span></div>'
)


def source(cell):
    return cell.source if isinstance(cell.source, str) else "".join(cell.source)


def append_once(cell, marker, text):
    if marker not in cell.source:
        cell.source = cell.source.rstrip() + "\n\n" + text + "\n"


def set_source(cells, cell_id, text):
    cells[cell_id].source = text.strip() + "\n"


def main():
    nb = nbformat.read(PATH, as_version=4)
    nb.metadata["math3024_slide_format"] = "blue-period-v3"
    cells = {cell.id: cell for cell in nb.cells}

    # Minimal title and an explicit two-session route.
    set_source(cells, "d0dd3fdf-7bad-4b0c-b3bb-594128690712", """
# Reaction-diffusion systems
## MATH3024 · Week 3
""")
    if not any(cell.get("id") == "week03-route" for cell in nb.cells):
        route = nbformat.v4.new_markdown_cell(r"""
# This week

<div class="analysis-perspectives">
  <div><strong>1 · How can a pattern organise itself?</strong><p>Begin with animal coats and other spatial patterns. Build Turing's activator-inhibitor explanation from reaction, diffusion, and regulation.</p></div>
  <div><strong>2 · How can we model it?</strong><p>Move from particle random walks to concentration fields, discretise diffusion, and assemble the Gray-Scott update rule.</p></div>
</div>

<div class="ladder-marker"><img src="images/ladder_marker.svg" alt="Ladder of abstraction" width="30" height="40"><span><strong>Across the week:</strong> microscopic motion → concentration fields → local numerical updates → system-level spatial patterns.</span></div>
""")
        route["id"] = "week03-route"
        route.metadata["tags"] = ["slides"]
        route.metadata["slideshow"] = {"slide_type": "slide"}
        nb.cells.insert(1, route)
        cells[route.id] = route

    set_source(cells, "a2fe3243", r"""
# How did the cheetah get its spots?

<div class="discussion-marker"><img src="images/discussion_marker.svg" alt="Discussion prompt" width="36" height="36"><span>Why spots rather than stripes, one uniform colour, or a unique pattern for every animal?</span></div>
""")

    set_source(cells, "9253675a-2529-494e-b524-48a841f31a6d", """
# Pattern formation

Patterns are organised differences in space or time. The question is not only what a pattern looks like, but which local process can generate it.
""")

    set_source(cells, "a5a1b98b-07e0-4417-be77-e1090bcfd254", r"""
## How do patterns form?

Pattern formation and pattern recognition are different questions. This week concerns formation: how local physical or biological processes create organised large-scale structure.

<div class="discussion-marker"><img src="images/discussion_marker.svg" alt="Discussion prompt" width="36" height="36"><span>For any pattern we observe, what evidence would distinguish a generating mechanism from a visual description?</span></div>
""")

    set_source(cells, "562f3685-c727-4a03-ae6e-7e8ed6aaa9c6", r"""
# A mechanism for spontaneous pattern

Reaction-diffusion systems can generate spots, stripes, and spirals without a pre-drawn template.

Turing's key proposal was that diffusion can destabilise an otherwise uniform chemical state. Local interactions and unequal diffusion rates amplify small perturbations into organised spatial structure.

<div class="ladder-marker"><img src="images/ladder_marker.svg" alt="Ladder of abstraction" width="30" height="40"><span><strong>Down:</strong> reaction and movement of morphogens. <strong>Up:</strong> a tissue-scale pattern produced by those local processes.</span></div>
""")

    set_source(cells, "d112f5d4", r"""
# Build the Turing mechanism

Turing proposed that complex spatial structures could arise from interacting chemical substances, called **morphogens**, diffusing through tissue.

<div class="analysis-perspectives">
  <div><strong>Activator</strong><p>Promotes local change and reinforces its own production.</p></div>
  <div><strong>Inhibitor</strong><p>Suppresses that change and spreads more rapidly.</p></div>
</div>

Neither chemical contains a map of the final pattern.
""")

    set_source(cells, "e5f79f48-d91b-473c-a24a-2d442239d788", r"""
The pattern is produced by the **interaction** between activator and inhibitor, together with their different diffusion rates.

<div class="choice-marker fragment"><img src="images/choice_marker.svg" alt="Modelling choice" width="36" height="36"><span>We must specify the reaction terms, diffusion coefficients, regulation rates, initial concentrations, perturbation, domain, and boundaries.</span></div>
""")

    set_source(cells, "8858f425-48a5-492b-9a5a-2d277dacc632", r"""
# Ingredient 1 · Reaction

Let $A$ and $B$ denote the activator and inhibitor. In the Gray-Scott example,

$$A+2B\rightarrow 3B.$$

One unit of $A$ and two of $B$ produce three units of $B$. The local reaction rate therefore depends nonlinearly on the concentrations.

Reaction can change concentrations only where the chemicals meet. Movement through space is supplied by diffusion.
""")

    set_source(cells, "c5c3ba5e", r"""
# Ingredient 2 · Diffusion

Brownian motion is the irregular motion of a microscopic particle suspended in a fluid. Robert Brown documented the phenomenon in 1827; Einstein's 1905 model connected microscopic random motion to macroscopic diffusion.

<div class="ladder-marker"><img src="images/ladder_marker.svg" alt="Ladder of abstraction" width="30" height="40"><span><strong>Down:</strong> one random particle trajectory. <strong>Up:</strong> predictable spreading of a population.</span></div>
""")

    set_source(cells, "d1f8631e", r"""
# Ingredient 3 · Regulation

The Gray-Scott model also includes:

- **feed rate, $f$:** supplies $A$;
- **kill rate, $k$:** removes $B$ by conversion to an inert product.

These are local reaction terms rather than diffusion.

<div class="choice-marker"><img src="images/choice_marker.svg" alt="Modelling choice" width="36" height="36"><span>$f$ and $k$ are parameters. Varying them changes which system-level pattern, if any, is selected.</span></div>
""")

    set_source(cells, "78500506-7c93-46a4-a0f6-c639fa9285d4", r"""
# What happens when the ingredients interact?

<div class="discussion-marker"><img src="images/discussion_marker.svg" alt="Discussion prompt" width="36" height="36"><span>Before simulating, predict what reaction, unequal diffusion, feed, and kill could do to an initially almost-uniform field.</span></div>

A parameter sweep is an upward move on the ladder: compare many simulations to reveal how the qualitative pattern changes across modelling choices.
""")

    set_source(cells, "4f8c9362", r"""
# The first model was deliberately incomplete

The chemical story builds intuition, but the system contains enormous numbers of particles. Tracking every collision is neither necessary nor usually useful.

The next modelling decision is therefore about representation: individual particles or concentration fields?
""")

    set_source(cells, "d67005af-86fe-4102-b7b8-0cf9f629d586", r"""
# Is the world discrete or continuous?

<div class="discussion-marker"><img src="images/discussion_marker.svg" alt="Discussion prompt" width="36" height="36"><span>When is a discrete description useful? When is a continuous approximation more informative?</span></div>

This is not a claim that nature must be only one or the other. It is a question about which representation answers the question at hand.
""")

    set_source(cells, "2ba9c92e-5488-45b4-a697-7aa99f2bc487", r"""
# One phenomenon, two descriptions

<div class="analysis-perspectives">
  <div><strong>Microscopic</strong><p>A particle follows a stochastic path composed of many small random changes.</p></div>
  <div><strong>Macroscopic</strong><p>A concentration field evolves deterministically according to a diffusion equation.</p></div>
</div>

The descriptions live at different levels of abstraction. The macroscopic law emerges from the collective statistics of microscopic motion.
""")

    set_source(cells, "b7c839be-6ee3-4fef-9aae-72b880dbb4b9", r"""
# Discrete description · Random walk

Model one particle as a sequence of random spatial steps.

- state: particle position;
- time: discrete steps;
- update: a random displacement;
- observable: displacement or squared displacement.

<div class="ladder-marker"><img src="images/ladder_marker.svg" alt="Ladder of abstraction" width="30" height="40"><span><strong>Stay low:</strong> inspect individual trajectories and the stochastic update rule.</span></div>
""")

    set_source(cells, "1c111a8d-516f-4637-95c0-080efdec3d90", r"""
# Continuous description · Diffusion field

Aggregate many particles into a concentration field $u(\mathbf{x},t)$.

- state: concentration at each point;
- time and space: continuous;
- update: the diffusion PDE;
- observable: field shape, gradients, and spreading rate.

<div class="ladder-marker"><img src="images/ladder_marker.svg" alt="Ladder of abstraction" width="30" height="40"><span><strong>Up the ladder over particles:</strong> replace individual trajectories with a smoothly evolving density.</span></div>
""")

    set_source(cells, "954ca579-6444-4529-9190-05fb00912d11", r"""
# From equations to a simulation

The reaction-diffusion PDEs are nonlinear and generally do not have a useful analytic solution.

To simulate them, we make another controlled change of representation:

$$\text{continuous field and time}\quad\longrightarrow\quad\text{grid values and finite time steps}.$$

<div class="choice-marker"><img src="images/choice_marker.svg" alt="Modelling choice" width="36" height="36"><span>Grid spacing, time step, stencil, domain, and boundary conditions become part of the numerical model.</span></div>
""")

    set_source(cells, "534e95c9-97e8-4864-b3cc-66d3c2e9e0aa", r"""
# Discretise the field

Represent space by grid cells, time by steps, and each concentration by one number per cell.

The local numerical update approximates the continuous diffusion operator.

<div class="ladder-marker"><img src="images/ladder_marker.svg" alt="Ladder of abstraction" width="30" height="40"><span><strong>Down the ladder:</strong> turn a continuous PDE into a local update that can be inspected and tested one cell at a time.</span></div>
""")

    set_source(cells, "09eb9036-81a5-4e05-8806-69d16664865b", r"""
# Approximate the gradient

Central differences estimate how the field changes in each coordinate direction:

$$
\frac{\partial U}{\partial x}\bigg|_{i,j}
\approx \frac{U_{i+1,j}-U_{i-1,j}}{2\Delta x},
\qquad
\frac{\partial U}{\partial y}\bigg|_{i,j}
\approx \frac{U_{i,j+1}-U_{i,j-1}}{2\Delta y}.
$$

<div class="choice-marker"><img src="images/choice_marker.svg" alt="Modelling choice" width="36" height="36"><span>Central differences are symmetric and second-order accurate, but they are still a numerical approximation.</span></div>
""")

    set_source(cells, "f2e3c94d-6d0e-4d20-992a-8e23122ce6d0", r"""
# Approximate the Laplacian

For equal grid spacing $\Delta x=\Delta y=h$,

$$
\nabla^2U_{i,j}\approx
\frac{U_{i+1,j}+U_{i-1,j}+U_{i,j+1}+U_{i,j-1}-4U_{i,j}}{h^2}.
$$

This measures how the centre differs from its four axial neighbours.

<div class="discussion-marker"><img src="images/discussion_marker.svg" alt="Discussion prompt" width="36" height="36"><span>What should this expression return for a perfectly uniform field? What sign should it have at an isolated peak?</span></div>
""")

    set_source(cells, "d3786649-2fd4-4766-8d86-df7cd2839294", r"""
# Assemble the Gray-Scott update

$$
\frac{\partial U}{\partial t}=D_U\nabla^2U+f(1-U)-UV^2,
$$

$$
\frac{\partial V}{\partial t}=D_V\nabla^2V-(k+f)V+UV^2.
$$

With an explicit time step $\Delta t$:

$$
U^{n+1}=U^n+\Delta t\left[D_U\Delta_hU^n+f(1-U^n)-U^n(V^n)^2\right],
$$

$$
V^{n+1}=V^n+\Delta t\left[D_V\Delta_hV^n-(k+f)V^n+U^n(V^n)^2\right].
$$

<div class="ladder-marker"><img src="images/ladder_marker.svg" alt="Ladder of abstraction" width="30" height="40"><span><strong>Local to global:</strong> repeat one local update across the grid and through time; then interpret the emergent field-level pattern.</span></div>
""")

    set_source(cells, "a45a0945-5b93-4ba3-9345-168dd54d526c", r"""
# Simulate, inspect, then generalise

The goal is not to predict the precise location of every zebra stripe. It is to determine which mechanisms and parameter regimes generate stripes, spots, waves, or uniform states.

<div class="analysis-perspectives">
  <div><strong>Down the ladder</strong><p>Check the stencil, one update, conservation or bounds, and numerical stability.</p></div>
  <div><strong>Up the ladder</strong><p>Compare patterns, observables, parameter sweeps, and repeated runs.</p></div>
</div>

The workshop builds and tests this simulation.
""")

    set_source(cells, "d5cb018d-702d-462f-b281-49a412e736f5", r"""
# So, is the world discrete or continuous?

Both descriptions can be useful:

<div class="analysis-perspectives">
  <div><strong>Discrete stochastic model</strong><p>Explains how microscopic random motion is represented.</p></div>
  <div><strong>Continuous deterministic model</strong><p>Explains how a concentration distribution evolves collectively.</p></div>
</div>

Numerical simulation makes a continuous model discrete again. That is an approximation chosen for computation, not a reversal of the physical argument.
""")

    # Reader signposts. These cells already carry reader-only tags.
    reader_headers = {
        "9253675a-2529-494e-b524-48a841f31a6d": "# Pattern formation",
        "b72f5b93": "# Turing's mechanism",
        "b7c839be-6ee3-4fef-9aae-72b880dbb4b9": "# From particles to fields",
        "534e95c9-97e8-4864-b3cc-66d3c2e9e0aa": "# From fields to a numerical model",
    }
    # Shared slide cells already provide these headings in the Reader; avoid
    # inserting duplicate cells while keeping the hierarchy explicit.

    # Standardise legacy prompts and prose throughout without touching code.
    old_prompt = re.compile(
        r'<div style="border-left:\s*4px solid #1e70bf;[^"]*">\s*'
        r'<strong>Pause and consider:</strong><br>\s*(.*?)\s*</div>',
        re.I | re.S,
    )
    for cell in nb.cells:
        if cell.cell_type != "markdown":
            continue
        text = cell.source
        text = old_prompt.sub(lambda m: DISCUSSION.format(m.group(1).strip()), text)
        text = text.replace("##### ", "## ")
        text = text.replace("### feed:", "## Feed").replace("### kill:", "## Kill")
        text = text.replace("## Putting it all together:", "# Putting it all together")
        text = text.replace(" — ", ". ")
        if "reader-voice-quote" not in text:
            text = text.replace("—", ", ")
        text = text.replace("complex-systems", "complex systems")
        text = text.replace("Complex-systems", "Complex systems")
        text = text.replace(
            "font-family: 'Comic Neue', 'Segoe Script', cursive; ",
            "",
        )
        # Keep figures within a readable page/slide width.
        if "![" in text and "<img" not in text and text.count("![") == 1:
            text = re.sub(
                r'!\[([^\]]+)\]\((images/[^)]+)\)',
                r'<img src="\2" alt="\1" style="display:block;max-width:100%;max-height:520px;object-fit:contain;margin:.5rem auto">',
                text,
            )
        text = re.sub(
            r'<img\s+src="(images/([^"/]+))"(?![^>]*\balt=)',
            lambda m: (
                f'<img src="{m.group(1)}" '
                f'alt="{Path(m.group(2)).stem.replace("_", " ")}"'
            ),
            text,
            flags=re.I,
        )
        cell.source = text

    # Code shown as a visual result should not expose implementation in slides.
    for cell in nb.cells:
        tags = list(cell.metadata.get("tags", []))
        slide_type = cell.metadata.get("slideshow", {}).get("slide_type")
        if cell.cell_type == "code" and slide_type in {"slide", "subslide", "fragment"}:
            if "hide-input" not in tags:
                tags.append("hide-input")
            cell.metadata["tags"] = tags

    nbformat.write(nb, PATH)
    print(f"Refreshed {PATH} ({len(nb.cells)} cells)")


if __name__ == "__main__":
    main()
