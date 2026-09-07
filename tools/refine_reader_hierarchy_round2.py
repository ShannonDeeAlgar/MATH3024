"""Final small-heading consolidation for the second Reader hierarchy pass."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def rewrite(path: Path, replacements: dict[str, str]) -> None:
    notebook = json.loads(path.read_text())
    for cell in notebook["cells"]:
        if cell.get("cell_type") != "markdown":
            continue
        tags = set(cell.get("metadata", {}).get("tags", []))
        if {"slides-only", "presenter-notes", "archive-only", "remove-cell"} & tags:
            continue
        lines = "".join(cell.get("source", [])).splitlines(keepends=True)
        for index, line in enumerate(lines):
            ending = "\n" if line.endswith("\n") else ""
            content = line[:-1] if ending else line
            if content in replacements:
                lines[index] = replacements[content] + ending
        cell["source"] = lines
    path.write_text(json.dumps(notebook, ensure_ascii=False, indent=1) + "\n")


rewrite(
    ROOT / "notebooks/week02/L_Fractals.ipynb",
    {
        # Model examples and qualifications sit beneath the main constructions.
        "## Fractal properties": "### Fractal properties",
        "## Evidence for fractal structure": "### Evidence for fractal structure",
        "## An early mathematical “monster”": "### An early mathematical “monster”",
        "## Three descriptions of an exact fractal": "### Three descriptions of an exact fractal",
        "## 2. Convergence of an IFS": "### 2. Convergence of an IFS",
        "## Controlled geometry vs stochastic iteration": "### Controlled geometry vs stochastic iteration",
        "## 3. L-systems: symbols first, geometry second": "### 3. L-systems: symbols first, geometry second",
        "## Three descriptions, three emphases": "### Three descriptions, three emphases",
        "## Infinite complexity is a limiting claim": "### Infinite complexity is a limiting claim",
        # Analysis keeps a few recognisable methods; derivations and cautions nest below them.
        "## Infinite detail changes what “size” means": "### Infinite detail changes what “size” means",
        "## Dimension as information": "### Dimension as information",
        "## Dimension as a scaling count": "### Dimension as a scaling count",
        "## Similarity dimension from self-similarity": "### Similarity dimension from self-similarity",
        "## Designing a fractal with a chosen dimension": "### Designing a fractal with a chosen dimension",
        "## Exact dimension is not always available": "### Exact dimension is not always available",
        "## Dimension is not one universal object": "### Dimension is not one universal object",
        "## Hausdorff dimension: an intrinsic definition": "### Hausdorff dimension: an intrinsic definition",
        "## Box counting as a dimension estimate": "### Box counting as a dimension estimate",
        "## A straight line is not enough": "### A straight line is not enough",
        "## Reproduce the Britain diagnostic": "### Reproduce the Britain diagnostic",
        "## Better depends on the question": "### Better depends on the question",
        "## Different coastlines": "### Different coastlines",
        "## What Euclidean geometry keeps, and what it misses": "### What Euclidean geometry keeps, and what it misses",
        "## A scaling law is not always self-similarity": "### A scaling law is not always self-similarity",
        "## Power laws and scale-free behaviour": "### Power laws and scale-free behaviour",
        "## Why the label matters": "### Why the label matters",
        "## Power-law data can be discrete or continuous": "### Power-law data can be discrete or continuous",
        "## Scale-free patterns in real complex systems": "### Scale-free patterns in real complex systems",
        "## Real systems are scale-free only over a range": "### Real systems are scale-free only over a range",
        # Scope has two main ideas: why it matters and where it connects.
        "## Very different (complex) systems": "### Very different (complex) systems",
        "## Complex system signatures in fractals": "### Complex system signatures in fractals",
        "## From pattern back to mechanism": "### From pattern back to mechanism",
        "## Connections to earlier units": "### Connections to earlier units",
        "## A reminder for your project": "### A reminder for your project",
    },
)

# Repair notebooks produced by the first, substring-based version of this
# transform.  Exact line matching below also makes subsequent runs harmless.
rewrite(
    ROOT / "notebooks/week02/L_Fractals.ipynb",
    {
        "#### Fractal properties": "### Fractal properties",
        "#### Evidence for fractal structure": "### Evidence for fractal structure",
        "#### An early mathematical “monster”": "### An early mathematical “monster”",
        "#### Three descriptions of an exact fractal": "### Three descriptions of an exact fractal",
        "#### 2. Convergence of an IFS": "### 2. Convergence of an IFS",
        "#### Controlled geometry vs stochastic iteration": "### Controlled geometry vs stochastic iteration",
        "#### 3. L-systems: symbols first, geometry second": "### 3. L-systems: symbols first, geometry second",
        "#### Three descriptions, three emphases": "### Three descriptions, three emphases",
        "#### Infinite complexity is a limiting claim": "### Infinite complexity is a limiting claim",
        "#### Dimension as information": "### Dimension as information",
        "#### Dimension as a scaling count": "### Dimension as a scaling count",
        "#### Similarity dimension from self-similarity": "### Similarity dimension from self-similarity",
        "#### Designing a fractal with a chosen dimension": "### Designing a fractal with a chosen dimension",
        "#### Exact dimension is not always available": "### Exact dimension is not always available",
        "#### Dimension is not one universal object": "### Dimension is not one universal object",
        "#### Hausdorff dimension: an intrinsic definition": "### Hausdorff dimension: an intrinsic definition",
        "#### Box counting as a dimension estimate": "### Box counting as a dimension estimate",
        "#### A straight line is not enough": "### A straight line is not enough",
        "#### Reproduce the Britain diagnostic": "### Reproduce the Britain diagnostic",
        "#### Better depends on the question": "### Better depends on the question",
        "#### Different coastlines": "### Different coastlines",
        "#### What Euclidean geometry keeps, and what it misses": "### What Euclidean geometry keeps, and what it misses",
        "#### A scaling law is not always self-similarity": "### A scaling law is not always self-similarity",
        "#### Power laws and scale-free behaviour": "### Power laws and scale-free behaviour",
        "#### Why the label matters": "### Why the label matters",
        "#### Power-law data can be discrete or continuous": "### Power-law data can be discrete or continuous",
        "#### Scale-free patterns in real complex systems": "### Scale-free patterns in real complex systems",
        "#### Real systems are scale-free only over a range": "### Real systems are scale-free only over a range",
        "#### Very different (complex) systems": "### Very different (complex) systems",
        "#### Complex system signatures in fractals": "### Complex system signatures in fractals",
        "#### From pattern back to mechanism": "### From pattern back to mechanism",
        "#### Connections to earlier units": "### Connections to earlier units",
        "#### A reminder for your project": "### A reminder for your project",
        "### Dimension": "## Dimension",
    },
)

# Merge the opening Analysis statement into the Dimension section rather than
# leaving a minor heading directly beneath the Analysis banner.
path = ROOT / "notebooks/week02/L_Fractals.ipynb"
notebook = json.loads(path.read_text())
seen_dimension = False
for cell in notebook["cells"]:
    if cell.get("cell_type") != "markdown":
        continue
    source = "".join(cell.get("source", []))
    if "### Infinite detail changes what “size” means" in source:
        source = source.replace("### Infinite detail changes what “size” means", "## Dimension", 1)
        seen_dimension = True
    elif seen_dimension and "## Dimension\n" in source:
        source = source.replace("## Dimension\n", "", 1)
        seen_dimension = False
    cell["source"] = source.splitlines(keepends=True)
path.write_text(json.dumps(notebook, ensure_ascii=False, indent=1) + "\n")

rewrite(
    ROOT / "notebooks/week04/L_Cellular_automata.ipynb",
    {
        "## State ": "### State ",
        "### Explore a two-dimensional cellular automaton": "## Explore a two-dimensional cellular automaton",
    },
)

print("Refined Week 2 and Week 4 Reader hierarchy")
