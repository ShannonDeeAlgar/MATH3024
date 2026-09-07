#!/usr/bin/env python3
"""Add one concise modelling-practice checkpoint to each workshop."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1] / "notebooks"

CHECKPOINTS = {
    "week01": "Explain why matched seeds help compare parameter values, why independent seeds are still needed for an ensemble, and which claim would be unsafe to make from one run.",
    "week02": "Name the resolution, alignment, or fitting-range choice that most affected your estimate, and state the evidence you would report with the final dimension.",
    "week03": "State which refinement or operator test separated a numerical artefact from a feature of the reaction–diffusion model.",
    "week04": "Given a fixed update budget, justify how you divided computation among world size, duration, rules, and repeated initial states.",
    "week05": "State where noise entered each implementation and identify one conclusion that changed—or became less certain—when the noise convention changed.",
    "week06": "Explain how the natural-frequency distribution and finite population size changed the apparent onset of synchronisation.",
    "week07": "Use repeated runs and more than one metric to distinguish a robust optimisation result from a fortunate trajectory.",
    "week08": "Challenge one scaling claim by changing the fitted range or system size, then state whether the evidence became stronger or weaker.",
    "week09": "State what your chosen representation allowed entropy to retain and what information it necessarily discarded.",
    "week10": "Change one initial-condition or update-rule choice and explain what the resulting difference reveals about path dependence.",
}


def markdown(text: str) -> dict:
    return {
        "cell_type": "markdown",
        "metadata": {},
        "source": [line + "\n" for line in text.splitlines()],
    }


for week, prompt in CHECKPOINTS.items():
    paths = sorted((ROOT / week).glob("WS_*.ipynb"))
    if len(paths) != 1:
        raise RuntimeError(f"Expected one workshop in {week}, found {paths}")
    path = paths[0]
    nb = json.loads(path.read_text())
    cells = nb["cells"]

    # Idempotent replacement if the checkpoint has already been inserted.
    cells[:] = [
        cell for cell in cells
        if not (
            cell.get("cell_type") == "markdown"
            and "# Modelling practice checkpoint" in "".join(cell.get("source", []))
        )
    ]

    checkpoint = markdown(
        "# Modelling practice checkpoint\n\n"
        + prompt
    )
    exit_index = next(
        (
            i for i, cell in enumerate(cells)
            if cell.get("cell_type") == "markdown"
            and "# Exit ticket" in "".join(cell.get("source", []))
        ),
        len(cells),
    )
    cells.insert(exit_index, checkpoint)
    path.write_text(json.dumps(nb, indent=1, ensure_ascii=False) + "\n")
    print(path.relative_to(ROOT.parent))
