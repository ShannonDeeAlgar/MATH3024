#!/usr/bin/env python3
"""Polish the Week 3 Laplacian intuition and Reader hierarchy."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK = ROOT / "notebooks/week03/L_Reaction_diffusion.ipynb"


def lines(text: str) -> list[str]:
    return [line + "\n" for line in text.strip().splitlines()]


nb = json.loads(NOTEBOOK.read_text())
by_id = {cell.get("id"): cell for cell in nb["cells"]}

by_id["week03-turing-six-modes"]["source"] = lines(r"""
### Diffusion-driven instability

Diffusion destabilises a spatially uniform state that was stable to uniform perturbations.

<div class="definition-panel"><strong>Turing pattern:</strong> the stationary spatial pattern left when the growing variation saturates.</div>

<div class="discussion-prompt"><span class="discussion-icon" aria-hidden="true"></span><div><strong>Diffusion normally smooths differences. How could it instead help a pattern grow?</strong></div></div>
""")

by_id["57d73b10-bd0c-4326-b40d-50a7e9eb7c03"]["source"] = lines(r"""
## From particle motion to Fick’s laws

A microscopic random walk does not survive unchanged at the concentration level. Its collective effect becomes a **flux law**.

Fick’s first law says that material flows down a concentration gradient:

$$
\mathbf J=-D\nabla C.
$$

The gradient $\nabla C$ points in the direction in which concentration increases most rapidly. The minus sign therefore sends material towards lower concentration.

Conservation of material gives

$$
\frac{\partial C}{\partial t}=-\nabla\!\cdot\mathbf J
=D\nabla^2 C.
$$

The divergence $\nabla\!\cdot\mathbf J$ measures the net outward flux from a very small region. Since $\mathbf J$ is proportional to a gradient, the Laplacian $\nabla^2 C=\nabla\!\cdot(\nabla C)$ asks whether the surrounding slopes point, overall, into or out of that region. It is positive in a local valley, negative at a local peak and zero for a locally linear field. Diffusion therefore fills valleys and lowers peaks.

This is the bridge from many irregular particle trajectories to a smooth concentration field.
""")

coarse = "".join(by_id["2ba9c92e-5488-45b4-a697-7aa99f2bc487"]["source"])
coarse = coarse.replace("### What changes when we coarse-grain?\n", "", 1)
coarse = coarse.replace("## What changes when we coarse-grain?\n", "", 1)
by_id["2ba9c92e-5488-45b4-a697-7aa99f2bc487"]["source"] = lines(
    "## What changes when we coarse-grain?\n\n" + coarse
)
by_id["f2e3c94d-6d0e-4d20-992a-8e23122ce6d0"]["source"][0] = "## Approximate the Laplacian\n"

by_id["83145c3c-d8d8-4002-acdc-2bd46b355ee3"]["source"][0] = "### Two concentrations occupy every grid location\n"
by_id["ecd5c9ba-5acd-42ce-9fba-d6a584a56494"]["source"][0] = "#### Can everyone recover the same information?\n"
by_id["62003953"]["source"][0] = "#### Design colour deliberately\n"

NOTEBOOK.write_text(json.dumps(nb, indent=1, ensure_ascii=False) + "\n")
print(f"Updated {NOTEBOOK}")
