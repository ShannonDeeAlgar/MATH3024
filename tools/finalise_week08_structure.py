"""Finish the Week 8 Reader and workshop narrative after the first reorder."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def body(cell: dict) -> str:
    return "".join(cell.get("source", []))


def put(cell: dict, value: str) -> None:
    cell["source"] = value.splitlines(keepends=True)


def one(cells: list[dict], prefix: str) -> dict:
    found = [c for c in cells if body(c).lstrip().startswith(prefix)]
    if len(found) != 1:
        raise RuntimeError(f"Expected one {prefix!r}, found {len(found)}")
    return found[0]


def markdown(value: str) -> dict:
    return {
        "cell_type": "markdown",
        "id": "week08-pseudocode",
        "metadata": {},
        "source": value.splitlines(keepends=True),
    }


def fix_reader() -> None:
    path = ROOT / "notebooks/week08/L_Critical_phenomena.ipynb"
    nb = json.loads(path.read_text())
    cells = nb["cells"]

    explorable = one(cells, "# Explorable")
    tuned = one(cells, "## Tuned criticality · percolation")
    critical = one(cells, "## What changes at a critical point?")
    corr_length = one(cells, "#### Correlation length")
    corr_time = one(cells, "#### Correlation time")
    corr_forms = one(cells, "### Exponential and power-law correlations")
    ising = one(cells, "## Supporting comparison · the Ising model")
    diverging = one(cells, "### Diverging Correlations")
    scale = one(cells, "### Scale language used here")
    exponents = one(cells, "### Power law scaling and critical exponents")
    model = one(cells, "# Model details")

    # Percolation prose sits between its heading and the critical-point prompt.
    tuned_i = cells.index(tuned)
    critical_i = cells.index(critical)
    percolation_block = cells[tuned_i:critical_i]

    # Abstract correlation language should follow, not precede, the visible
    # percolation transition. Pull all of that material into one coherent block.
    abstract_start = cells.index(corr_length)
    abstract_block = cells[abstract_start:tuned_i]
    replace_start = abstract_start
    replace_end = cells.index(model)
    ordered = percolation_block + [critical] + abstract_block
    cells[replace_start:replace_end] = ordered

    put(corr_length, body(corr_length).replace("#### Correlation length", "### Correlation length", 1))
    put(corr_time, body(corr_time).replace("#### Correlation time", "### Correlation time", 1))
    put(ising, body(ising).replace("## Supporting comparison", "### Supporting comparison", 1))
    put(diverging, body(diverging).replace("### Diverging Correlations", "#### Diverging correlations", 1))
    put(scale, body(scale).replace("### Scale language", "#### Scale language", 1))
    put(exponents, body(exponents).replace("### Power law scaling", "#### Power-law scaling", 1))

    nb["cells"] = cells
    path.write_text(json.dumps(nb, ensure_ascii=False, indent=1) + "\n")


def fix_workshop() -> None:
    path = ROOT / "notebooks/week08/WS_Critical_phenomena.ipynb"
    nb = json.loads(path.read_text())
    cells = nb["cells"]

    title = one(cells, "# Week 8 workshop")
    put(title, "# Week 8 workshop · Abelian sandpile\n")

    implement = one(cells, "# Implement and test")
    if not any(body(c).lstrip().startswith("# Pseudocode") for c in cells):
        pseudo = markdown(
            "# Pseudocode\n\n"
            "This version is written as a nested procedure because one grain addition may trigger many local updates. It makes the boundary, initialisation and recorded outputs explicit.\n\n"
            "```text\n"
            "choose lattice size L, threshold z_c = 4, open boundaries,\n"
            "number of additions, burn-in length and random seed\n"
            "initialise every lattice height z[i,j] = 0\n\n"
            "repeat for each grain addition\n"
            "    choose one lattice site uniformly at random\n"
            "    add one grain there\n"
            "    set avalanche size and duration to zero\n\n"
            "    while at least one site has z[i,j] >= z_c\n"
            "        identify the sites that topple in this parallel relaxation step\n"
            "        for each toppling site\n"
            "            subtract four grains from that site\n"
            "            give one grain to each edge-sharing neighbour\n"
            "            discard grains sent beyond an open boundary\n"
            "            add one to the avalanche size\n"
            "        add one to the avalanche duration\n\n"
            "    after burn-in, record avalanche size and duration\n"
            "check that every recorded final configuration is stable\n"
            "```\n\n"
            "The record step is part of the model specification when the aim is to analyse avalanches. It could be omitted for a demonstration that only displays the lattice.\n"
        )
        cells.insert(cells.index(implement), pseudo)

    # Testing inherited code is the practical expression of the week's modelling
    # focus, so state the checks before students run the long investigation.
    put(
        implement,
        "# Implement and test\n\n"
        "Before collecting avalanche statistics, test the inherited lattice machinery against the new model: one central toppling conserves grains away from a boundary; a boundary toppling loses the expected grains; relaxation ends with every height below four; and changing the order used to process unstable sites leaves the same stable result. These checks are the evidence that the reused code is valid here.\n",
    )

    nb["cells"] = cells
    path.write_text(json.dumps(nb, ensure_ascii=False, indent=1) + "\n")


if __name__ == "__main__":
    fix_reader()
    fix_workshop()
