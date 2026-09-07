#!/usr/bin/env python3
"""Polish the Week 3 discretisation sequence in slides and Reader."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK = ROOT / "notebooks/week03/L_Reaction_diffusion.ipynb"


def source(cell: dict) -> str:
    return "".join(cell.get("source", []))


def set_source(cell: dict, text: str) -> None:
    cell["source"] = [line for line in text.splitlines(keepends=True)]
    if text and not text.endswith("\n"):
        cell["source"].append("\n")


def by_id(cells: list[dict], cell_id: str) -> dict:
    return next(cell for cell in cells if cell.get("id") == cell_id)


def main() -> None:
    notebook = json.loads(NOTEBOOK.read_text())
    cells = notebook["cells"]

    complete = by_id(cells, "36fa3ed0")
    set_source(
        complete,
        source(complete).replace(
            "a **pair of coupled nonlinear reaction–diffusion partial differential equations**",
            "a pair of coupled nonlinear reaction–diffusion partial differential equations",
        ),
    )

    return_to_turing = by_id(cells, "week03-turing-six-evolution")
    return_to_turing.setdefault("metadata", {})["slideshow"] = {"slide_type": "skip"}
    return_to_turing["metadata"]["tags"] = ["reader-only"]

    index_grid = by_id(cells, "09eb9036-81a5-4e05-8806-69d16664865b")
    set_source(
        index_grid,
        r'''## Discretise space · index the grid

<div class="two-panel equal-panels">
<div class="image-panel"><img src="images/grid_indexing_Uij.svg" alt="A grid showing a focal value and neighbouring indices" style="display:block;width:100%;height:auto;max-height:330px;object-fit:contain;margin:0 auto;"></div>
<div class="text-panel">
<p>The continuous field is sampled at grid points.</p>
<p><i>U</i><sup><i>n</i></sup><sub><i>i,j</i></sub> is the value at row <i>i</i>, column <i>j</i>, and discrete time level <i>n</i>.</p>
<p>The Laplacian will be replaced by a comparison between this focal value and its neighbours.</p>
</div>
</div>''',
    )

    values = by_id(cells, "534e95c9-97e8-4864-b3cc-66d3c2e9e0aa")
    set_source(
        values,
        r'''### Inspect the stored values

<img src="images/diffusion_grid_numbers_t012.svg" alt="Numerical concentration values at discrete time levels zero, one and two" style="display:block;width:76%;max-height:400px;object-fit:contain;margin:0 auto;">

<div class="discussion-marker"><img src="images/discussion_marker.svg" alt="Discussion prompt"><span>The values are precise. Can you see the spatial pattern quickly?</span></div>

<div class="ladder-marker"><img src="images/ladder_marker.svg" alt="Ladder of abstraction"><span><strong>Down the ladder:</strong> inspect the value stored in each cell at time level <i>n</i>.</span></div>''',
    )

    two_fields = by_id(cells, "83145c3c-d8d8-4002-acdc-2bd46b355ee3")
    set_source(
        two_fields,
        r'''## Two concentrations occupy every grid location

<div class="two-panel equal-panels">
<div class="image-panel"><img src="images/two_concentration_fields.svg" alt="Aligned U and V concentration grids showing that each location stores two values" style="display:block;width:100%;height:auto;max-height:390px;object-fit:contain;margin:0 auto;"></div>
<div class="text-panel">
<p>At cell (<i>i</i>, <i>j</i>) and time level <i>n</i>, the state is (<i>U</i><sup><i>n</i></sup><sub><i>i,j</i></sub>, <i>V</i><sup><i>n</i></sup><sub><i>i,j</i></sub>).</p>
<p>The arrays share one grid, but a single colour map can show only one field. Separate sequential maps are the clearest starting point.</p>
<p>The label must state which concentration is displayed.</p>
</div>
</div>

<div class="choice-marker"><img src="images/choice_marker.svg" alt="Modelling choice"><span>Visualisation does not change the simulated state, but it changes which patterns are visible.</span></div>''',
    )

    # The colour representation motivates the question of which of the two stored
    # fields is being displayed. Keep the same order in slides and Reader source.
    cells.remove(two_fields)
    reveal_index = next(i for i, cell in enumerate(cells) if cell.get("id") == "week03-diffusion-t012")
    cells.insert(reveal_index + 1, two_fields)

    neighbourhoods = by_id(cells, "week03-neighbourhoods")
    set_source(
        neighbourhoods,
        r'''### Which cells count as neighbours?

<img src="images/grid_neighbourhoods.svg" alt="Von Neumann and Moore neighbourhoods on square grids" style="display:block;width:58%;max-width:690px;height:auto;max-height:265px;object-fit:contain;margin:0 auto .35rem;">

<div class="two-panel equal-panels">
<div class="text-panel"><p><strong>Von Neumann:</strong> Four edge-sharing cells. This gives the standard five-point finite-difference Laplacian.</p></div>
<div class="text-panel"><p><strong>Moore:</strong> Eight surrounding cells. Use it when diagonal influence is part of the rule or is weighted to improve rotational symmetry.</p></div>
</div>

<div class="choice-marker"><img src="images/choice_marker.svg" alt="Modelling choice" width="36" height="36"><span>A diagonal cell is farther away than an edge-sharing cell. Equal weights therefore describe a different process, not an automatic improvement.</span></div>''',
    )

    simulation = by_id(cells, "week03-return-to-simulation")
    set_source(
        simulation,
        r'''## Return to the Gray–Scott simulation

<div class="two-panel equal-panels">
<div class="image-panel"><img src="images/gray_scott_two_fields.png" alt="The U and V concentration fields from one Gray–Scott simulation" style="display:block;width:100%;max-height:430px;object-fit:contain;margin:0 auto;"></div>
<div class="text-panel">
<p>This is one run of the complete discrete Gray–Scott model. The left panel displays <i>U</i>; the right displays <i>V</i>.</p>
<p>Both arrays belong to the same state. Where autocatalytic <i>V</i> is concentrated, <i>U</i> has generally been depleted.</p>
<div class="discussion-marker"><img src="images/discussion_marker.svg" alt="Discussion prompt"><span>How could we quantify these patterns and label parameter space by model output, rather than by eye or by the explorable’s red region?</span></div>
</div>
</div>

<div class="ladder-marker"><img src="images/ladder_marker.svg" alt="Ladder of abstraction"><span><strong>Up the ladder:</strong> compare fields, runs and parameter choices to identify robust morphology.</span></div>''',
    )

    experiment = by_id(cells, "week03-gray-scott-world")
    set_source(
        experiment,
        r'''# Test the mechanism in a chemical system

<div class="two-panel equal-panels">
<div class="image-panel"><img src="images/cima_experimental_turing_patterns.webp" alt="Experimental setup and stationary patterns in a CIMA gel reactor" style="display:block;width:100%;height:auto;max-height:330px;object-fit:contain;margin:0 auto;"></div>
<div class="text-panel">
<p><strong>CIMA gel reactor:</strong> Reactants diffuse through an unstirred gel supplied by reservoirs. Starch binding changes their effective transport rates.</p>
<p>An initially uniform reactor can develop stationary hexagons or labyrinths. Controlled reaction, differential transport and sustained driving provide a mechanistic test.</p>
</div>
</div>

<p class="figure-reference">The morphology is measured as evidence; the controlled transport and reaction conditions test the proposed mechanism.</p>''',
    )

    closing = by_id(cells, "week03-final-discrete-continuous")
    set_source(
        closing,
        r'''# The modelling problem underneath the model

One system, represented at three levels:

$$
\text{particles}
\xrightarrow{\text{aggregate}}
\text{continuous fields}
\xrightarrow{\text{discretise}}
\text{grid values}.
$$

**Up the ladder:** reveal ensemble diffusion and system-level morphology.  
**Down the ladder:** inspect the local update and compute an approximation.

Next week keeps the grid and neighbourhood, then replaces continuous concentrations with discrete cellular states and rules.''',
    )

    NOTEBOOK.write_text(json.dumps(notebook, ensure_ascii=False, indent=1) + "\n")


if __name__ == "__main__":
    main()
