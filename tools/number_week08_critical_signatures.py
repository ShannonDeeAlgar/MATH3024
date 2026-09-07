#!/usr/bin/env python3
"""Number and connect the three recurring signatures analysed in Week 8."""

import json
from pathlib import Path


PATH = Path("notebooks/week08/L_Critical_phenomena.ipynb")


def lines(text):
    return text.strip().splitlines(keepends=True)


def markdown(cell_id, text):
    return {
        "cell_type": "markdown",
        "id": cell_id,
        "metadata": {"slideshow": {"slide_type": "subslide"}, "tags": ["slides"]},
        "source": lines(text),
    }


notebook = json.loads(PATH.read_text())
cells = notebook["cells"]
cells[:] = [cell for cell in cells if cell.get("id") != "w8-three-critical-signatures"]

insert_at = next(i for i, cell in enumerate(cells) if cell.get("id") == "w8-correlation-scales-slide")
cells.insert(
    insert_at,
    markdown(
        "w8-three-critical-signatures",
        r"""
## Three signatures associated with critical phenomena

Critical-point phenomena provide one mechanism that can generate recurring features of complex systems:

1. **Fractal geometry:** spatial structure repeats statistically across a range of scales.
2. **Pink ($1/f$) noise:** fluctuations occur across a broad range of timescales, with spectral power approximately proportional to $1/f$.
3. **Power laws:** event sizes or other observables have no single characteristic scale over a fitted range.

Each feature is a measurement to test. A connection to criticality requires several consistent signatures together with evidence for the mechanism producing them.
""",
    ),
)

analysis = next(cell for cell in cells if cell.get("id") == "965627a4-2957-4331-a9a9-91bb3653fa05")
analysis["source"] = lines(
    r"""
## Three views of the same dynamics

1. **Space — fractal geometry:** which sites participated, what final heights remain, and how does occupied structure change with scale?
2. **Time — pink ($1/f$) noise:** when did topplings occur, how long did relaxation last, and how is variation distributed across frequencies?
3. **Events — power laws:** how are avalanche sizes, areas and durations distributed?

These measurements test whether the three proposed signatures occur in the same simulation. Their agreement strengthens a criticality claim; the organising mechanism must also be established.
"""
)

evidence = next(cell for cell in cells if cell.get("id") == "e44031eb-96d0-40d2-a9b5-5849ce5a16db")
old = "".join(evidence["source"])
old = old.replace(
    "Fractal spatial structure, heavy-tailed event statistics and $1/f$-like spectra are possible signatures of scale-free behaviour. Their presence depends on the model and measurement protocol. Establishing self-organised criticality requires evidence for both the scaling and the organising mechanism.",
    "The numbered analyses test (1) fractal spatial structure, (2) $1/f$-like temporal spectra and (3) power-law event statistics. Their presence depends on the model and measurement protocol. Establishing self-organised criticality requires consistent scaling evidence and the organising mechanism.",
)
evidence["source"] = lines(old)

PATH.write_text(json.dumps(notebook, indent=1, ensure_ascii=False) + "\n")
