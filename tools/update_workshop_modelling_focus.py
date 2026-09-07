"""Keep the transferable modelling objective explicit across workshops."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

FOCI = {
    "week01/WS_Introduction_to_complex_systems.ipynb": (
        "Schelling segregation",
        "From stochastic examples to reproducible evidence",
        "A stochastic result cannot be interpreted unless it can be reproduced and compared fairly.",
        "One agent and one run are inspected first; parameter sweeps and ensembles then support system-level claims.",
    ),
    "week02/WS_Fractals.ipynb": (
        "Sierpiński triangle",
        "Measurement is part of the model",
        "An empirical measurement can change when its resolution, alignment, or fitting range changes.",
        "A known exact dimension becomes a benchmark for testing resolution, alignment, depth, and fitting-range choices.",
    ),
    "week03/WS_Reaction_diffusion.ipynb": (
        "Gray–Scott reaction–diffusion",
        "Verify a numerical representation before interpreting it",
        "A simulation is evidence only after we know that its numerical representation behaves as intended.",
        "Known operator tests and grid refinement are used before morphology or parameter effects are interpreted.",
    ),
    "week04/WS_Cellular_automata.ipynb": (
        "Elementary cellular automata and Conway's Game of Life",
        "Every summary is a lossy description",
        "A summary makes a system easier to compare, but necessarily discards some structure.",
        "Space–time diagrams are compared with density, activity, entropy, and other classifications to identify what each retains.",
    ),
    "week05/WS_ABM.ipynb": (
        "Vicsek flocking",
        "Stochastic implementation choices can change conclusions",
        "Small coding choices can alter a phase transition, while reliable comparisons consume finite computation time.",
        "Angular and vectorial noise are implemented and compared using matched sweeps and ensembles.",
    ),
    "week06/WS_Synchronisation.ipynb": (
        "Kuramoto coupled oscillators",
        "Individual heterogeneity shapes collective thresholds",
        "An apparent collective threshold can depend on who is in the population and how large that population is.",
        "Frequency distributions and finite oscillator populations are varied while coherence and the apparent onset of synchronisation are measured.",
    ),
    "week07/WS_Intelligent_systems.ipynb": (
        "Particle swarm optimisation",
        "A stochastic optimiser must be evaluated, not showcased",
        "One successful run may be luck, and the best value found is not the only measure of an optimiser.",
        "Exploration and exploitation are inspected in trajectories, then success is compared across repeated runs and more than one metric.",
    ),
    "week08/WS_Critical_phenomena.ipynb": (
        "Abelian sandpile",
        "A straight-looking log–log plot is not yet a scaling law",
        "Finite-size effects or a selectively chosen range can imitate scaling.",
        "Avalanche measurements are challenged against fitting range, finite-size cutoffs, and changes in system size.",
    ),
    "week10/WS_Game_theory.ipynb": (
        "Evolutionary iterated Prisoner's Dilemma",
        "Evolutionary outcomes are path- and implementation-dependent",
        "An outcome may reflect the route taken and the update rule, not only the payoff matrix.",
        "Initial composition, selection, mutation, and population replacement are treated as model choices and tested comparatively.",
    ),
}


def focus_cell(canonical: str, focus: str, why: str, practice: str) -> dict:
    return {
        "cell_type": "markdown",
        "id": "transferable-modelling-focus",
        "metadata": {},
        "source": [
            "## Two objectives, one investigation\n",
            "\n",
            f"**Canonical model:** {canonical}.\n",
            "\n",
            f"**Modelling focus:** {focus}.\n",
            "\n",
            f"**Why it matters:** {why}\n",
            "\n",
            f"**How it appears here:** {practice}\n",
            "\n",
            "It is developed through the canonical model rather than as a separate exercise.\n",
        ],
    }


for relative, content in FOCI.items():
    path = ROOT / "notebooks" / relative
    notebook = json.loads(path.read_text())
    notebook["cells"] = [
        cell for cell in notebook["cells"] if cell.get("id") != "transferable-modelling-focus"
    ]
    notebook["cells"].insert(1, focus_cell(*content))
    path.write_text(json.dumps(notebook, indent=1, ensure_ascii=False) + "\n")
    print(path.relative_to(ROOT))
