#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def update_week01():
    path = ROOT / "notebooks/week01/L_Introduction_to_complex_systems.ipynb"
    nb = json.loads(path.read_text())
    for cell in nb["cells"]:
        source = "".join(cell.get("source", ""))
        if "## Canonical models at a glance · Schelling segregation and planetary motion" not in source:
            continue
        if "#### Pseudocode: planetary motion" not in source:
            source = source.rstrip() + """

#### Pseudocode: planetary motion

```text
SET the initial position and velocity
CHOOSE a time step and final time
FOR each time step:
    compute gravitational acceleration from the current position
    update velocity using that acceleration
    update position using the new velocity
    record time, position and velocity
END FOR
```

The time step is part of the numerical implementation, not a new physical parameter. Refining it checks whether the computed trajectory is stable to that approximation.
"""
        cell["source"] = source
        break
    path.write_text(json.dumps(nb, indent=1, ensure_ascii=False) + "\n")


def add_gutenberg_note():
    path = ROOT / "notebooks/week09/WS_Information_theory.ipynb"
    nb = json.loads(path.read_text())
    for cell in nb["cells"]:
        source = "".join(cell.get("source", ""))
        if source.startswith("# Estimate a distribution from text"):
            source = source.replace(
                "The files are public-domain texts from Project Gutenberg: *Alice's Adventures in Wonderland* (eBook 11) and *Pride and Prejudice* (eBook 1342).",
                "The bundled files are public-domain texts from Project Gutenberg: [*Alice's Adventures in Wonderland*, eBook 11](https://www.gutenberg.org/ebooks/11) and [*Pride and Prejudice*, eBook 1342](https://www.gutenberg.org/ebooks/1342).",
            )
            cell["source"] = source
            break
    path.write_text(json.dumps(nb, indent=1, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    update_week01()
    add_gutenberg_note()
