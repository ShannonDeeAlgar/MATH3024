#!/usr/bin/env python3
"""Give legacy workshops an active-learning purpose without rewriting their content."""

from pathlib import Path
import nbformat

ROOT = Path(__file__).resolve().parents[1]

FOCUS = {
    "week04/WS_Cellular_automata.ipynb": (
        "elementary cellular automata and Conway's Game of Life",
        [
            "turning local transition rules into executable updates",
            "checking individual updates before iterating a whole world",
            "comparing behaviours under controlled initial and boundary conditions",
            "challenging quantitative summaries against the visible dynamics",
        ],
    ),
    "week05/WS_ABM.ipynb": (
        "Vicsek flocking model",
        [
            "reconstructing the agent state and local update rule",
            "inspecting individual motion before calculating collective observables",
            "sweeping noise and density while holding other choices fixed",
            "using ensembles to separate robust behaviour from one random history",
        ],
    ),
    "week06/WS_Synchronisation.ipynb": (
        "Kuramoto synchronisation",
        [
            "building from one oscillator to a coupled population",
            "tracking phases alongside a collective order parameter",
            "varying coupling and frequency heterogeneity",
            "connecting individual dynamics with the onset of synchronisation",
        ],
    ),
    "week07/WS_Intelligent_systems.ipynb": (
        "particle swarm optimisation",
        [
            "implementing the particle update from its component influences",
            "inspecting exploration and exploitation in individual trajectories",
            "varying algorithmic choices while keeping the objective fixed",
            "judging success from more than one run and more than one metric",
        ],
    ),
    "week08/WS_Critical_phenomena.ipynb": (
        "Abelian sandpile",
        [
            "implementing local toppling and checking conservation carefully",
            "observing how local perturbations generate avalanches",
            "measuring distributions rather than relying on striking examples",
            "testing whether apparent scaling survives changes in system size and range",
        ],
    ),
    "week10/WS_Game_theory.ipynb": (
        "iterated Prisoner's Dilemma and evolutionary dynamics",
        [
            "turning strategies and payoffs into an executable interaction",
            "tracking individual encounters and population-level outcomes",
            "testing how reproduction and mutation alter the strategy distribution",
            "challenging conclusions against alternative initial conditions and rules",
        ],
    ),
}


def focus_cell(model: str, activities: list[str]):
    bullets = "\n".join(f"- {item};" for item in activities[:-1])
    bullets += f"\n- {activities[-1]}."
    source = f"""# Workshop focus

The lecture and Reader introduce the weekly ideas. This workshop is for actively exploring the **{model}** by:

{bullets}
"""
    cell = nbformat.v4.new_markdown_cell(source)
    cell["id"] = "workshop-focus"
    return cell


for relative, (model, activities) in FOCUS.items():
    path = ROOT / "notebooks" / relative
    notebook = nbformat.read(path, as_version=4)
    notebook.metadata.pop("author", None)
    notebook.metadata.pop("authors", None)
    notebook.cells = [
        cell for cell in notebook.cells
        if cell.get("id") != "workshop-focus"
    ]
    notebook.cells.insert(0, focus_cell(model, activities))
    nbformat.write(notebook, path)
    print(path)
