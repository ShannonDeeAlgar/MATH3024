#!/usr/bin/env python3
"""Add the unit's modelling-practice marker to each lecture title cell."""

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PRACTICES = {
    1: "Reproducibility and fair stochastic comparisons",
    2: "Measurement, resolution and representation",
    3: "Numerical verification before interpretation",
    4: "Computational complexity and finite budgets",
    5: "Stochastic implementation and noise",
    6: "Heterogeneity in finite populations",
    7: "Evaluation across runs and metrics",
    8: "Finite-size effects and scaling evidence",
    9: "Information retained and discarded by summaries",
    10: "Path dependence and implementation choices",
}


for week, practice in PRACTICES.items():
    notebook = next((ROOT / "notebooks" / f"week{week:02d}").glob("L_*.ipynb"))
    data = json.loads(notebook.read_text())
    source = "".join(data["cells"][0]["source"])
    marker = (
        '<div class="modelling-practice-marker"><span>Modelling practice</span>'
        f'<strong>{practice}</strong></div>'
    )
    if '<div class="modelling-practice-marker">' in source:
        before = source.split('<div class="modelling-practice-marker">', 1)[0].rstrip()
        source = before + "\n\n" + marker
    else:
        source = source.rstrip() + "\n\n" + marker
    data["cells"][0]["source"] = source.splitlines(keepends=True)
    notebook.write_text(json.dumps(data, ensure_ascii=False, indent=1) + "\n")
    print(notebook.relative_to(ROOT))
