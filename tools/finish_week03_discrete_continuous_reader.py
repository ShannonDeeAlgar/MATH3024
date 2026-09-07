from pathlib import Path

import nbformat


root = Path(__file__).resolve().parents[1]
path = root / "notebooks/week03/L_Reaction_diffusion.ipynb"
nb = nbformat.read(path, as_version=4)

# Restore the colour-vision figure in the Reader as well as the slide deck.
for cell in nb.cells:
    if cell.cell_type == "markdown" and cell.source.lstrip().startswith(
        "I did my PhD (and continue to work) with someone who is red-green colour blind."
    ):
        cell.source = '''## Colour must not carry the message alone

<img src="images/Colourblind.png" alt="A pseudo-Ishihara colour-vision image in which the number 74 is formed from green dots among orange dots" style="display:block;width:48%;max-width:520px;margin:0 auto;">

I did my PhD, and continue to work, with someone who is red-green colour blind. He cannot recover the number in this image in the same way that I can. A figure that is clear to its author may therefore conceal information from part of its audience.

For concentration fields, use a perceptually ordered map such as `viridis`, `cividis` or `plasma`. Do not rely on a red-green distinction, and check that the ordering remains legible in greyscale. See [Matplotlib's guide to choosing colormaps](https://matplotlib.org/stable/users/explain/colors/colormaps.html), [Nature's accessibility guidance](https://www.nature.com/articles/d41586-021-02696-z), and the [ASCB guide](https://www.ascb.org/science-news/how-to-make-scientific-figures-accessible-to-readers-with-color-blindness/).
'''
        break

# Add the neighbourhood definitions to the Reader immediately before the stencil discussion.
if not any(c.id == "week03-neighbourhoods-reader" for c in nb.cells):
    target = next(
        i for i, c in enumerate(nb.cells)
        if c.cell_type == "markdown" and c.source.startswith("### Convolve with the five-point stencil")
    )
    cell = nbformat.v4.new_markdown_cell('''### Moore and von Neumann neighbourhoods

A **von Neumann neighbourhood** contains the four cells that share an edge with the focal cell: north, south, east and west. The usual five-point Laplacian stencil combines those four neighbours with the centre cell.

A **Moore neighbourhood** contains all eight surrounding cells, including the diagonals. It may be used in a nine-point stencil, but the diagonal and edge-sharing cells should not automatically receive equal weights. The weights determine which continuous operator is being approximated and how strongly the grid directions appear in the result.

Choosing a neighbourhood determines which local information can affect one update. It is therefore both a numerical choice and part of the model specification.
''')
    cell.id = "week03-neighbourhoods-reader"
    cell.metadata["slideshow"] = {"slide_type": ""}
    cell.metadata["tags"] = ["reader-only"]
    nb.cells.insert(target, cell)

# Make the criteria behind the representation choice explicit before the final return.
if not any(c.id == "week03-choosing-representation" for c in nb.cells):
    target = next(i for i, c in enumerate(nb.cells) if c.id == "week03-final-discrete-continuous")
    cell = nbformat.v4.new_markdown_cell('''# Choosing a useful representation

| Consideration | Ask |
|---|---|
| **Question** | Do we need individual trajectories, fluctuations, or only a system-level pattern? |
| **Scale** | Are microscopic differences important, or will many interactions average into a field? |
| **Computation** | What state can we update at the required domain size and duration? |
| **Approximation** | Which behaviour must survive coarse-graining and discretisation? |

<div class="choice-marker"><img src="images/choice_marker.svg" alt="Modelling choice" width="36" height="36"><span>A finer model is not automatically a better model. It is better only if the extra detail matters to the question and can be validated.</span></div>
''')
    cell.id = "week03-choosing-representation"
    cell.metadata["slideshow"] = {"slide_type": "slide"}
    cell.metadata["tags"] = ["slides"]
    nb.cells.insert(target, cell)

if not any(c.id == "week03-choosing-representation-reader" for c in nb.cells):
    target = next(i for i, c in enumerate(nb.cells) if c.id == "week03-final-discrete-continuous-reader")
    cell = nbformat.v4.new_markdown_cell('''### Choosing the level of description

The appropriate representation depends on four related considerations:

- **Question:** whether we need individual trajectories and fluctuations or a system-level pattern.
- **Scale:** whether microscopic differences remain important or average into a field.
- **Computation:** which state can be updated at the required domain size and duration.
- **Approximation:** which behaviour must survive coarse-graining and discretisation, and which numerical artefacts must be checked.

A finer model is not automatically a better model. Additional detail is useful only when it matters to the question and can be constrained or validated.
''')
    cell.id = "week03-choosing-representation-reader"
    cell.metadata["slideshow"] = {"slide_type": ""}
    cell.metadata["tags"] = ["reader-only"]
    nb.cells.insert(target, cell)

nbformat.write(nb, path)
print(f"Updated {path}")
