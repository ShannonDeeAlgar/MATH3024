"""Separate the Week 6 model banner from the first model-detail slide."""

import json
from pathlib import Path


path = Path(__file__).resolve().parents[1] / "notebooks/week06/L_Synchronisation.ipynb"
notebook = json.loads(path.read_text())
cells = notebook["cells"]

if not any(cell.get("id") == "w6-model-banner" for cell in cells):
    index = next(i for i, cell in enumerate(cells) if cell.get("id") == "w6-one")
    cell = cells[index]
    text = "".join(cell["source"])
    prefix = "# Model details\n\n"
    if not text.startswith(prefix):
        raise RuntimeError("Week 6 first model slide does not contain the expected combined banner")
    cell["source"] = text.removeprefix(prefix).splitlines(keepends=True)
    cell["metadata"]["slideshow"]["slide_type"] = "subslide"
    cells.insert(
        index,
        {
            "cell_type": "markdown",
            "id": "w6-model-banner",
            "metadata": {
                "slideshow": {"slide_type": "slide"},
                "tags": ["slides-only"],
            },
            "source": ["# Model details\n"],
        },
    )

path.write_text(json.dumps(notebook, indent=1, ensure_ascii=False) + "\n")
