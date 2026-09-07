from pathlib import Path

import nbformat


root = Path(__file__).resolve().parents[1]
path = root / "notebooks/week03/L_Reaction_diffusion.ipynb"
nb = nbformat.read(path, as_version=4)

for cell in nb.cells:
    if cell.cell_type != "markdown":
        continue
    stripped = cell.source.lstrip()
    if stripped.startswith("## What can happen near the uniform state?"):
        cell.source = cell.source.replace("## What can happen near the uniform state?", "# What can happen near the uniform state?", 1)
    elif stripped.startswith("## Turing computed a pattern by hand"):
        cell.source = cell.source.replace("## Turing computed a pattern by hand", "# Turing computed a pattern by hand", 1)
    elif stripped.startswith("## Explore the parameter space"):
        cell.source = cell.source.replace("## Explore the parameter space", "# The parameter space grows quickly", 1)
    elif stripped.startswith("# Explore the Gray–Scott parameter space"):
        cell.source = cell.source.replace("# Explore the Gray–Scott parameter space", "## Explore the Gray–Scott parameter space", 1)
        cell.metadata["slideshow"] = {"slide_type": "subslide"}
    elif stripped.startswith("## Return to Turing’s question"):
        cell.metadata["slideshow"] = {"slide_type": "subslide"}
    elif stripped.startswith("### Brownian motion: the physical phenomenon"):
        cell.metadata["slideshow"] = {"slide_type": "subslide"}
    elif stripped.startswith("## Gray–Scott regulation terms"):
        cell.source = cell.source.replace("## Gray–Scott regulation terms", "## Return to the complete Gray–Scott model", 1)
    elif stripped.startswith("## Assemble the Gray–Scott update"):
        cell.source = cell.source.replace("## Assemble the Gray–Scott update", "## Discretise time: the Gray–Scott update", 1)

nbformat.write(nb, path)
print(f"Updated {path}")
