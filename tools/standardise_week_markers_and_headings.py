"""Add canonical-model markers and repair known lecture heading jumps."""
from pathlib import Path
import re
import nbformat

ROOT = Path(__file__).resolve().parents[1]
CANONICAL = {
    "week01/L_Introduction_to_complex_systems.ipynb": "Planetary motion and Schelling segregation",
    "week02/L_Fractals.ipynb": "Sierpiński triangle and branching growth",
    "week03/L_Reaction_diffusion.ipynb": "Random walk diffusion and Gray–Scott reaction–diffusion",
    "week04/L_Cellular_automata.ipynb": "Elementary cellular automata and Conway's Game of Life",
    "week05/L_ABM.ipynb": "Vicsek flocking model",
    "week06/L_Synchronisation.ipynb": "Kuramoto model",
    "week07/L_Intelligent_systems.ipynb": "Perceptron, ant colony optimisation and particle swarm optimisation",
    "week08/L_Critical_phenomena.ipynb": "Ising, percolation and Abelian sandpile models",
    "week09/L_InformationTheory.ipynb": "Shannon's communication model and entropy",
    "week10/L_Game_theory.ipynb": "Prisoner's dilemma and iterated prisoner's dilemma",
}
FIXES = {
    "week01/L_Introduction_to_complex_systems.ipynb": {
        "### Simplify first": "## Simplify first", "### Purpose": "## Purpose",
        "### Quantitative analysis": "## Quantitative analysis",
        "### Vary an important parameter": "## Vary an important parameter"},
    "week02/L_Fractals.ipynb": {"### First interpretation: a coin": "## First interpretation: a coin"},
    "week03/L_Reaction_diffusion.ipynb": {
        "### What exactly is a pattern?": "## What exactly is a pattern?",
        "### Random walks": "## Random walk: a discrete model",
        "### Fick's Laws": "## Fick's laws", "### Transport equation": "## Transport equation",
        "### Evidence, mechanism and morphology": "## Evidence, mechanism and morphology"},
}
for relative, model in CANONICAL.items():
    path = ROOT / "notebooks" / relative
    nb = nbformat.read(path, as_version=4)
    source = nb.cells[0].source
    if '<div class="canonical-model-marker">' in source:
        source = source.split('<div class="canonical-model-marker">', 1)[0].rstrip()
    label = "Canonical models" if (" and " in model or "," in model) else "Canonical model"
    nb.cells[0].source = source + (
        f'\n\n<div class="canonical-model-marker"><span>{label}</span>'
        f'<strong>{model}</strong></div>'
    )
    for cell in nb.cells:
        if cell.cell_type == "markdown":
            for old, new in FIXES.get(relative, {}).items():
                cell.source = cell.source.replace(old, new)
    if relative.startswith("week03/"):
        for cell in nb.cells:
            if cell.id == "41bc5b10-40b8-4223-9cef-57fbdf5e8f77":
                cell.source = ("## Brownian motion: the phenomenon\n\nA microscopic particle suspended "
                               "in a fluid moves irregularly because surrounding molecules continually "
                               "strike it. Brownian motion is the physical phenomenon. A random walk is "
                               "one discrete model of it.")
            elif cell.id == "aa81f828-45bd-4d17-a25b-eab81f382f2d":
                cell.source = cell.source.replace("### Random walks", "## Random walk: a discrete model")
                if "number of steps" not in cell.source:
                    cell.source += ("\n\nHere \\(n\\) is the number of steps. The typical displacement grows "
                                    "like \\(\\sqrt{n}\\), even though path length grows like \\(n\\).")
    # Markdown hierarchy is semantic, not a font-size control. Prevent a
    # sub-subheading from appearing without its parent level.
    previous = None
    for cell in nb.cells:
        if cell.cell_type != "markdown" or "archive-only" in cell.metadata.get("tags", []):
            continue
        lines = cell.source.splitlines()
        for index, line in enumerate(lines):
            match = re.match(r"^(#{1,6})\s+(.+)$", line)
            if not match:
                continue
            level = len(match.group(1))
            if previous is not None and level > previous + 1:
                level = previous + 1
                lines[index] = "#" * level + " " + match.group(2)
            previous = level
        cell.source = "\n".join(lines)
    nbformat.write(nb, path)
