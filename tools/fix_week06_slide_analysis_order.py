"""Separate the Week 6 analysis banner from its first content slide."""

import json
from pathlib import Path


path = Path(__file__).resolve().parents[1] / "notebooks/week06/L_Synchronisation.ipynb"
nb = json.loads(path.read_text())
cells = nb["cells"]

for i, cell in enumerate(cells):
    source = "".join(cell.get("source", []))
    if source.startswith("# Analysis\n\n## Quantitative analysis · collective coherence\n"):
        cell["source"] = source.replace("# Analysis\n\n", "", 1).splitlines(keepends=True)
        cell["metadata"]["slideshow"]["slide_type"] = "subslide"
        cells.insert(
            i,
            {
                "cell_type": "markdown",
                "metadata": {
                    "slideshow": {"slide_type": "slide"},
                    "tags": ["slides-only"],
                },
                "source": ["# Analysis\n"],
            },
        )
        break
else:
    raise RuntimeError("Could not find the combined slide analysis banner")

path.write_text(json.dumps(nb, indent=1, ensure_ascii=False) + "\n")
