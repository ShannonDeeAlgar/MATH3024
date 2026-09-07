"""Insert the two-parameter Kuramoto sweep into the Week 6 Reader."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK = ROOT / "notebooks/week06/L_Synchronisation.ipynb"
CELL_ID = "w6-two-parameter-sweep-reader"

SOURCE = r'''#### Sweep coupling and heterogeneity together

<img src="images/kuramoto_coupling_heterogeneity_map.svg" alt="Heatmap of long-time Kuramoto coherence across coupling strength and natural-frequency spread" style="display:block;width:84%;max-width:960px;margin:1rem auto">

The one-dimensional sweep above fixes $K$ and varies the population. The heatmap now varies both $K$ and the natural-frequency standard deviation $\sigma_\omega$. Each coloured cell is the mean long-time coherence $r_\infty$ from six finite simulations with $N=120$ oscillators. The simulations use $\Delta t=0.04$, discard the first 16.8 time units and average coherence over the following 6.4 time units.

The broad trend is not surprising: more heterogeneous clocks require stronger coupling. The useful result is quantitative. It locates the boundary between mostly incoherent and coherent behaviour and suggests that the balance $K/\sigma_\omega$, rather than either parameter alone, controls the onset.

The dashed curve is the continuum prediction

$$
K_c=\sqrt{\frac{8}{\pi}}\,\sigma_\omega
$$

for a Gaussian frequency distribution. It is not fitted to the coloured cells. The finite simulations change gradually around this line because $N$, the integration time and the ensemble are finite. The analytical result introduced later predicts the onset in the idealised infinite-population model.
'''


def main() -> None:
    notebook = json.loads(NOTEBOOK.read_text())
    cells = notebook["cells"]
    cells[:] = [cell for cell in cells if cell.get("id") != CELL_ID]
    insertion = next(
        index + 1
        for index, cell in enumerate(cells)
        if cell.get("id") == "w6-heterogeneity-width-sweep-reader"
    )
    cells.insert(
        insertion,
        {
            "cell_type": "markdown",
            "id": CELL_ID,
            "metadata": {"slideshow": {"slide_type": "skip"}, "tags": ["reader-only"]},
            "source": [line + "\n" for line in SOURCE.splitlines()],
        },
    )
    NOTEBOOK.write_text(json.dumps(notebook, indent=1, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
