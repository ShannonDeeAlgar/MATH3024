from pathlib import Path

import nbformat


ROOT = Path(__file__).resolve().parents[1]
LECTURE = ROOT / "notebooks/week03/L_Reaction_diffusion.ipynb"
WORKSHOP = ROOT / "notebooks/week03/WS_Reaction_diffusion.ipynb"


def find_cell(nb, cell_id):
    for cell in nb.cells:
        if cell.get("id") == cell_id:
            return cell
    raise KeyError(cell_id)


def first_heading(source):
    return next((line.strip() for line in source.splitlines() if line.strip().startswith("#")), "")


def replace_heading(cell, old, new):
    if old in cell.source:
        cell.source = cell.source.replace(old, new, 1)


def update_lecture():
    nb = nbformat.read(LECTURE, as_version=4)

    intro = find_cell(nb, "week03-alan-mathison-turing")
    intro.source = '''# Alan Turing

<div class="two-panel equal-panels compact-panels">
  <div class="image-panel"><img src="images/Turing_and_imitation_game.png" alt="Alan Turing and a representation of the imitation game" style="width:100%;height:260px;object-fit:contain;"></div>
  <div class="text-panel"><p>Turing helped establish theoretical computer science, worked in wartime cryptanalysis, designed early stored-program computers, and asked how machines might exhibit intelligence.</p><p>His work on morphogenesis asked a different question: can a simple physical mechanism generate biological form?</p></div>
</div>'''

    life = find_cell(nb, "week03-turing-life-reader")
    replace_heading(life, "## Alan Turing: a wider scientific life", "## A wider scientific life")

    question = find_cell(nb, "a0a1efe7-e26e-4f6d-a529-3db70b3fe94f")
    question.source = '''## Turing’s question

### How does form emerge?

An embryo can begin close to uniform, yet organised spatial differences appear.

Could local processes create that structure without a pre-drawn template?'''

    replace_heading(find_cell(nb, "week03-turing-model-excerpt"),
                    "## A model is a deliberate simplification",
                    "### A model is a deliberate simplification")
    replace_heading(find_cell(nb, "week03-turing-reference-list"),
                    "## A remarkably short reference list",
                    "### A remarkably short reference list")
    replace_heading(find_cell(nb, "week03-turing-reception-reader"),
                    "## From an unusual proposal to a modern framework",
                    "### From an unusual proposal to a modern framework")

    mechanism = find_cell(nb, "week03-why-reaction-diffusion")
    replace_heading(mechanism, "## Turing’s proposed solution",
                    "## Turing’s mechanism: reaction and diffusion")
    replace_heading(find_cell(nb, "week03-turing-six-modes"),
                    "## The essential condition for a Turing instability",
                    "### The essential condition for a Turing instability")
    replace_heading(find_cell(nb, "week03-turing-paper-reader"),
                    "## What else is in the 1952 paper?",
                    "### What else is in the 1952 paper?")

    walk = find_cell(nb, "b7c839be-6ee3-4fef-9aae-72b880dbb4b9")
    if "overlap" not in walk.source.lower():
        walk.source += '''

<p class="small-note">Every panel contains 45 unit steps on the same axes. Numbered checkpoints show elapsed steps; revisiting a location can hide several segments.</p>'''

    walk_reader = find_cell(nb, "week03-random-walk-detail-reader")
    if "retracing" not in walk_reader.source.lower():
        walk_reader.source += '''

All three examples use 45 unit-length steps. The apparent amount of line is not a step count: an unbiased walk often retraces an edge or revisits a site, so several steps can lie on top of one another. The numbered checkpoints in the figure make the common time budget visible.'''

    compressed = find_cell(nb, "a241f850")
    bridge_id = "week03-random-motion-laplacian-bridge"
    bridge_source = r'''### From random motion to the Laplacian

At particle level, unbiased steps spread positions without producing a preferred direction.

At ensemble level, probability or concentration flows away from crowded locations. For a smooth field $C(\mathbf{x},t)$, the Laplacian $\nabla^2C$ measures that local imbalance: it is negative at a peak and positive in a valley.

$$
\frac{\partial C}{\partial t}=D\nabla^2C.
$$

<div class="ladder-marker"><img src="images/ladder_marker.svg" alt="Ladder of abstraction"><span><strong>Up the ladder:</strong> replace many random paths by the field equation that preserves their collective spreading.</span></div>'''
    existing = next((c for c in nb.cells if c.get("id") == bridge_id), None)
    if existing is None:
        bridge = nbformat.v4.new_markdown_cell(bridge_source)
        bridge["id"] = bridge_id
        bridge.metadata["tags"] = ["slides"]
        bridge.metadata["slideshow"] = {"slide_type": "subslide"}
        nb.cells.insert(nb.cells.index(compressed) + 1, bridge)
    else:
        existing.source = bridge_source

    driven = find_cell(nb, "week03-particle-open-reactor")
    driven.source = driven.source.replace(
        "Without a continuing supply, the autocatalytic reaction consumes its available <i>u</i> and stops.",
        "Gray–Scott is an open, driven reactor. Feed prevents <i>u</i> from being exhausted; removal and decay prevent products from accumulating indefinitely. Without these terms, the transient reaction runs down instead of sustaining a non-equilibrium pattern-forming regime.",
        1,
    )

    for cell in nb.cells:
        if first_heading(cell.source).startswith("# "):
            cell.metadata.setdefault("slideshow", {})["slide_type"] = "slide"

    nbformat.write(nb, LECTURE)


def update_workshop():
    nb = nbformat.read(WORKSHOP, as_version=4)
    guide = find_cell(nb, "week03-workshop-guide")
    note = '''

> **Notation in this workshop.** The slides and Reader use lowercase $u$ and $v$ for individual particle species, then uppercase $U$ and $V$ for concentration fields. In Python it is conventional to name concentration arrays `u` and `v`. In this workshop those lowercase code variables store **concentrations**, not individual particles.
'''
    if "Notation in this workshop" not in guide.source:
        guide.source = guide.source.rstrip() + note
    nbformat.write(nb, WORKSHOP)


if __name__ == "__main__":
    update_lecture()
    update_workshop()
