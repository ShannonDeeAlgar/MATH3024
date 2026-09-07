#!/usr/bin/env python3
"""Create consistently named WS_* copies of the legacy weekly workshops."""

from pathlib import Path

import nbformat


ROOT = Path(__file__).resolve().parents[1]
WORKSHOPS = {
    "notebooks/week03/2_Reaction_diffusion.ipynb": "notebooks/week03/WS_Reaction_diffusion.ipynb",
    "notebooks/week04/2_CellularAutomata.ipynb": "notebooks/week04/WS_Cellular_automata.ipynb",
    "notebooks/week05/2_ABM.ipynb": "notebooks/week05/WS_ABM.ipynb",
    "notebooks/week06/2_Synchronisation.ipynb": "notebooks/week06/WS_Synchronisation.ipynb",
    "notebooks/week07/2_IntelligentSystems.ipynb": "notebooks/week07/WS_Intelligent_systems.ipynb",
    "notebooks/week08/2_CriticalPhenomena.ipynb": "notebooks/week08/WS_Critical_phenomena.ipynb",
    "notebooks/week10/2_GameTheory.ipynb": "notebooks/week10/WS_Game_theory.ipynb",
}


def main() -> None:
    for source_name, target_name in WORKSHOPS.items():
        source, target = ROOT / source_name, ROOT / target_name
        if target.exists():
            print(f"Kept existing {target.relative_to(ROOT)}")
            continue
        notebook = nbformat.read(source, as_version=4)
        notebook.metadata["math3024_workshop_source"] = source_name
        nbformat.write(notebook, target)
        print(f"Created {target.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
