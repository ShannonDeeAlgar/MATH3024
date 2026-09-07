#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def text(cell):
    return "".join(cell.get("source", []))

def replace(cell, value):
    cell["source"] = value.splitlines(keepends=True)

path = ROOT / "notebooks/week08/L_Critical_phenomena.ipynb"
data = json.loads(path.read_text())
cells = data["cells"]

replace(cells[0], text(cells[0]).replace(
    "Ising, percolation and Abelian sandpile models",
    "Site percolation and the Abelian sandpile",
))

# Collapse the inaccurate transition preamble to the distinction needed here.
start = next(i for i, c in enumerate(cells) if text(c).startswith("## Critical phenomena"))
end = next(i for i, c in enumerate(cells[start + 1:], start + 1) if text(c).startswith("### Diverging correlations"))
cells[start:end] = [{
    "cell_type": "markdown",
    "metadata": {"slideshow": {"slide_type": "slide"}},
    "source": [
        "## Critical points\n",
        "\n",
        "A continuous phase transition has a critical point at which correlations extend across increasingly large distances and times. No single correlation scale dominates, and observable quantities often follow scaling laws.\n",
        "\n",
        "A discontinuous transition instead has a jump in the order parameter and usually retains finite correlation scales. First-order lines can terminate at critical endpoints, so *phase transition* and *critical point* are not interchangeable terms.\n",
    ],
    "id": "w8-critical-point-distinction",
}]

for cell in cells:
    value = text(cell)
    value = value.replace("##### Exponentials and Power laws: a very quick review", "### Exponential and power-law correlations")
    value = value.replace("Power laws are **heavy-tailed**.", "Some power-law probability distributions are **heavy-tailed**.")
    value = value.replace("**Extreme events are common**:", "**Extreme events are less strongly suppressed:**")
    value = value.replace("If you wait long enough, a “big one” will eventually arrive.", "Large observations can therefore be much more frequent than under a light-tailed model.")
    value = value.replace(
        "Ising, percolation and Vicsek models display criticality: they require an external control parameter (temperature, density, noise or density respectively).",
        "The Ising, percolation and Vicsek models provide examples of tuned transitions: temperature, occupation probability, noise or density acts as an external control parameter.",
    )
    replace(cell, value)

data["cells"] = cells
path.write_text(json.dumps(data, ensure_ascii=False, indent=1) + "\n")

workshop = ROOT / "notebooks/week08/WS_Critical_phenomena.ipynb"
if workshop.exists():
    data = json.loads(workshop.read_text())
    for cell in data["cells"]:
        value = text(cell)
        value = value.replace("$K_c$", "$z_c$").replace("K_c=4", "z_c=4").replace("#K_c", "# z_c")
        value = value.replace("values $z>z_c$", "values $0\\le z<z_c$")
        replace(cell, value)
    workshop.write_text(json.dumps(data, ensure_ascii=False, indent=1) + "\n")
