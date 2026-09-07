#!/usr/bin/env python3
"""Remove duplicate Week 3 transitions and clarify the Session 2 hierarchy."""

import json
from pathlib import Path


PATH = Path("notebooks/week03/L_Reaction_diffusion.ipynb")


def set_source(cell, text):
    cell["source"] = [line + "\n" for line in text.rstrip().splitlines()]


nb = json.loads(PATH.read_text())
cells = nb["cells"]
by_id = {cell.get("id"): cell for cell in cells}

# These cells repeated material now stated more clearly in the section opener
# and in the first-session account of Turing's stability argument.
remove_ids = {
    "762e37bb-dee7-495f-9fc4-9b7b764656c9",  # duplicate particle-to-field prose
    "week03-turing-six-reader",              # duplicate linear-stability summary
}
cells[:] = [cell for cell in cells if cell.get("id") not in remove_ids]
by_id = {cell.get("id"): cell for cell in cells}

set_source(by_id["4f8c9362"], r"""
# From particle motion to continuous equations

<p><strong>The particle story is not the simulation.</strong></p>

<div class="discussion-marker"><img src="images/discussion_marker.svg" alt="Discussion prompt"><span>Could the explorable be updating every molecule, collision and three-particle encounter?</span></div>

An exact particle simulation would update an enormous number of random trajectories, detect molecular encounters and decide which encounters react. That is far more microscopic detail and computation than our pattern question requires.

We therefore **coarse-grain** the state:

$$
\text{many particle positions}
\quad\longrightarrow\quad
U(\mathbf x,t),\;V(\mathbf x,t),
$$

where the two fields record concentrations averaged over many particles near each location. We lose individual histories and gain a tractable description of collective transport and reaction.

<div class="ladder-marker"><img src="images/ladder_marker.svg" alt="Ladder of abstraction"><span><strong>Up the ladder over particles:</strong> discard individual histories and retain the amount of each chemical at each location.</span></div>
""")

# The comparison is useful in the Reader, but not as another lecture transition.
cell = by_id["2ba9c92e-5488-45b4-a697-7aa99f2bc487"]
cell["metadata"]["slideshow"] = {"slide_type": "skip"}
cell["metadata"]["tags"] = ["reader-only"]
set_source(cell, r"""
### What changes when we coarse-grain?

| Microscopic description | Macroscopic description |
|---|---|
| Track stochastic particle paths | Track concentration fields $U(\mathbf x,t)$ and $V(\mathbf x,t)$ |
| Retain fluctuations and individual histories | Average over many particles |
| Resolve molecular encounters | Represent their average local reaction rate |
| Natural observable: displacement | Natural observable: concentration gradient |

Both descriptions concern the same physical system. The appropriate state depends on the question and the scale at which we need an answer.
""")

set_source(by_id["1c111a8d-516f-4637-95c0-080efdec3d90"],
           ''.join(by_id["1c111a8d-516f-4637-95c0-080efdec3d90"]["source"]).replace(
               "## Continuous description: a diffusion field",
               "## Diffusion as a concentration field", 1))

set_source(by_id["57d73b10-bd0c-4326-b40d-50a7e9eb7c03"],
           ''.join(by_id["57d73b10-bd0c-4326-b40d-50a7e9eb7c03"]["source"]).replace(
               "## From particle motion to Fick’s laws",
               "### From particle motion to Fick’s laws", 1))

set_source(by_id["4fad79e4-e78d-468c-be71-d70d8c4c711e"],
           ''.join(by_id["4fad79e4-e78d-468c-be71-d70d8c4c711e"]["source"]).replace(
               "## Reader extension: transport as well as diffusion",
               "### Reader extension: transport as well as diffusion", 1))

set_source(by_id["week03-turing-paper-scope"],
           ''.join(by_id["week03-turing-paper-scope"]["source"]).replace(
               "## A general reaction–diffusion model",
               "## From diffusion to reaction–diffusion", 1))

# Gray–Scott is one coherent construction, not five peer sections.
cell = by_id["8858f425-48a5-492b-9a5a-2d277dacc632"]
set_source(cell, ''.join(cell["source"]).replace(
    "## 1. Reaction at the concentration level",
    "## Assemble Gray–Scott at the concentration level\n\n### 1. Reaction", 1))

for cell_id, old, new in [
    ("562f3685-c727-4a03-ae6e-7e8ed6aaa9c6", "## 2. Diffusion at the concentration level", "### 2. Diffusion"),
    ("d1f8631e", "## 3. Feed and removal at the concentration level", "### 3. Feed and removal"),
    ("week03-feed-kill-reader", "### Intuition for feed and kill", "#### Intuition for feed and kill"),
    ("36fa3ed0", "## The continuous Gray–Scott model", "### The complete continuous model"),
    ("week03-parameter-space", "## The parameter space", "### Explore the parameter space"),
]:
    set_source(by_id[cell_id], ''.join(by_id[cell_id]["source"]).replace(old, new, 1))

# Returning to the scientific question is a new interpretive stage.
set_source(by_id["week03-turing-six-evolution"],
           ''.join(by_id["week03-turing-six-evolution"]["source"]).replace(
               "## Return to Turing’s question",
               "## Return to Turing’s question", 1))

PATH.write_text(json.dumps(nb, ensure_ascii=False, indent=1) + "\n")
print("Cleaned Week 3 Session 2 hierarchy and removed duplicate transitions.")
