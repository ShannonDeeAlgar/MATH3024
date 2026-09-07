#!/usr/bin/env python3
"""Add the brief Week 2 DLA return to the Week 5 ABM lecture."""

from pathlib import Path

import nbformat


ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "notebooks/week05/L_ABM.ipynb"
CELL_ID = "week05-dla-return"


def main() -> None:
    notebook = nbformat.read(TARGET, as_version=4)
    notebook.cells = [cell for cell in notebook.cells if cell.get("id") != CELL_ID]

    cell = nbformat.v4.new_markdown_cell(
        r"""
# A model we deferred · Diffusion-limited aggregation

<div class="slide-columns">
  <img class="column-image" src="../week02/images/particularly_stuck_image1.png" alt="A branching diffusion-limited aggregate">
  <div>
    <p><strong>Agents:</strong> mobile particles.</p>
    <p><strong>Motion:</strong> random local steps.</p>
    <p><strong>Interaction:</strong> a particle sticks when it contacts the aggregate.</p>
    <p><strong>Emergence:</strong> exposed tips grow while interior regions become screened.</p>
  </div>
</div>

Week 2 introduced this morphology but deferred the model. With Brownian motion and agent-based modelling now available, DLA becomes a natural synthesis: simple mobile agents modify the environment encountered by every agent that follows.

<div class="ladder-marker"><img src="images/ladder_marker.svg" alt="Ladder of abstraction"><span><strong>Down:</strong> one random step and one attachment. <strong>Up:</strong> branching morphology, screening, and fractal scaling.</span></div>

We will develop the implementation and analysis later. For now, identify the agents, state, interaction rule, and emergent outcome.
""".strip()
        + "\n"
    )
    cell["id"] = CELL_ID
    cell.metadata["tags"] = ["slides"]
    cell.metadata["slideshow"] = {"slide_type": "slide"}

    insertion = min(8, len(notebook.cells))
    notebook.cells.insert(insertion, cell)
    nbformat.write(notebook, TARGET)
    print(f"Updated {TARGET}")


if __name__ == "__main__":
    main()
