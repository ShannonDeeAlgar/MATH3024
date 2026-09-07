#!/usr/bin/env python3
"""Keep Week 3's Reveal hierarchy aligned with its conceptual narrative."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK = ROOT / "notebooks/week03/L_Reaction_diffusion.ipynb"

# A horizontal slide starts a genuinely new conceptual section. A vertical
# subslide develops, exemplifies, or calculates within the current section.
SLIDE_TYPES = {
    # Opening question and its two complementary comparisons.
    "a2fe3243": "slide",
    "week03-same-mechanism-different-pattern": "subslide",
    "week03-sand-zebra-first": "subslide",

    # One Turing section: context -> question -> paper -> mechanism -> result.
    "week03-alan-mathison-turing": "slide",
    "a0a1efe7-e26e-4f6d-a529-3db70b3fe94f": "subslide",
    "week03-turing-model-excerpt": "subslide",
    "week03-turing-reference-list": "subslide",
    "week03-why-reaction-diffusion": "subslide",
    "week03-turing-six-modes": "subslide",
    "week03-turing-dappled": "subslide",

    # Diffusion is a new modelling idea; its analyses remain below it.
    "b7c839be-6ee3-4fef-9aae-72b880dbb4b9": "slide",
    "11879310": "subslide",
    "dc08556a": "subslide",
    "bf26cf2d": "subslide",
    "25b5d7f3": "subslide",
    "a241f850": "subslide",

    # Gray-Scott is the canonical model; controls and exploration develop it.
    "week03-gray-scott-history": "slide",
    "week03-lowercase-full-model": "subslide",
    "54e20377-5977-4ea6-a97b-7482a438a6c9": "subslide",

    # Coarse-graining is the second-session modelling move. Reaction-diffusion
    # and the concentration-level Gray-Scott model continue that move.
    "4f8c9362": "slide",
    "week03-coarse-grain-state": "subslide",
    "1c111a8d-516f-4637-95c0-080efdec3d90": "subslide",
    "week03-turing-paper-scope": "subslide",
    "8858f425-48a5-492b-9a5a-2d277dacc632": "subslide",
    "562f3685-c727-4a03-ae6e-7e8ed6aaa9c6": "subslide",
    "d1f8631e": "subslide",
    "36fa3ed0": "subslide",
    "week03-parameter-space": "subslide",

    # Numerical approximation is a new section; every implementation choice
    # stays in its vertical stack.
    "954ca579-6444-4529-9190-05fb00912d11": "slide",
    "09eb9036-81a5-4e05-8806-69d16664865b": "subslide",
    "534e95c9-97e8-4864-b3cc-66d3c2e9e0aa": "subslide",
    "week03-diffusion-t012": "subslide",
    "83145c3c-d8d8-4002-acdc-2bd46b355ee3": "subslide",
    "ecd5c9ba-5acd-42ce-9fba-d6a584a56494": "subslide",
    "62003953": "subslide",
    "f2e3c94d-6d0e-4d20-992a-8e23122ce6d0": "subslide",
    "week03-neighbourhoods": "subslide",
    "2d86506f-baf9-4f97-9a53-63015dd1e05f": "subslide",
    "d3786649-2fd4-4766-8d86-df7cd2839294": "subslide",
    "0ac1d921-5f1e-4b64-8c65-8454c1e70e8f": "subslide",

    # Return to the simulation is a new synthesis; the chemical test develops
    # it, while the final modelling lesson is its own concluding section.
    "week03-return-to-simulation": "slide",
    "week03-gray-scott-world": "subslide",
    "week03-final-discrete-continuous": "slide",
}


def main() -> None:
    notebook = json.loads(NOTEBOOK.read_text())
    found: set[str] = set()

    for cell in notebook["cells"]:
        cell_id = cell.get("id")
        if cell_id not in SLIDE_TYPES:
            continue
        cell.setdefault("metadata", {}).setdefault("slideshow", {})["slide_type"] = (
            SLIDE_TYPES[cell_id]
        )
        found.add(cell_id)

    missing = set(SLIDE_TYPES) - found
    if missing:
        raise SystemExit(f"Missing expected Week 3 cell IDs: {sorted(missing)}")

    NOTEBOOK.write_text(json.dumps(notebook, indent=1, ensure_ascii=False) + "\n")
    print(f"Updated {len(found)} Week 3 slide boundaries.")


if __name__ == "__main__":
    main()
