import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "notebooks/week03/L_Reaction_diffusion.ipynb"
nb = json.loads(PATH.read_text())


def markdown(cell_id, source):
    return {
        "cell_type": "markdown",
        "id": cell_id,
        "metadata": {"tags": ["reader-only"], "slideshow": {"slide_type": "skip"}},
        "source": [line + "\n" for line in source.strip().splitlines()],
    }


new_cells = {
    "week03-reader-two-fields": markdown(
        "week03-reader-two-fields",
        r"""
### Two concentrations occupy every grid location

At the aggregate level, one grid cell does not contain either (U) or (V). It carries both concentrations. At time step (n), the state at location ((i,j)) is the pair

\[
\left(u^n_{i,j},v^n_{i,j}\right).
\]

![Two aligned grids showing the U and V concentrations stored at every spatial location](images/two_concentration_fields.svg)

We cannot show both scalar fields with one ordinary colour map. A clear default is therefore to show two aligned panels, one for (U) and one for (V), with a separate labelled colour scale for each. A derived image, such as (v-u) or a thresholded pattern, is another modelling and visualisation choice. It should be labelled as a derived quantity rather than presented as the state itself.
""",
    ),
    "week03-reader-return-simulation": markdown(
        "week03-reader-return-simulation",
        r"""
### Return to the complete simulated system

![The U and V concentration fields from one complete Gray–Scott simulation](images/gray_scott_two_fields.png)

This is one simulation of the complete discretised Gray–Scott equations, not diffusion by itself. Both panels show the same run and the same grid. Low (u) aligns with high (v) because the autocatalytic reaction consumes (U) while producing (V). Showing only the (V) panel can reveal the morphology, but it hides half of the model state.
""",
    ),
}

cells = [c for c in nb["cells"] if c.get("id") not in new_cells]

transition_index = next(i for i, c in enumerate(cells) if c.get("id") == "762e37bb-dee7-495f-9fc4-9b7b764656c9")
cells.insert(transition_index + 1, new_cells["week03-reader-two-fields"])

return_index = next(i for i, c in enumerate(cells) if c.get("id") == "week03-return-to-simulation")
cells.insert(return_index + 1, new_cells["week03-reader-return-simulation"])

nb["cells"] = cells
PATH.write_text(json.dumps(nb, indent=1, ensure_ascii=False) + "\n")
