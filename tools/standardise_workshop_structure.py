#!/usr/bin/env python3
"""Give Weeks 1–10 a shared workshop spine without rewriting their content."""

from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
NOTEBOOKS = ROOT / "notebooks"


STAGE_TITLES = {
    "context": "Context",
    "specify": "Specify the model",
    "implement": "Implement and test",
    "simulate": "Simulate and inspect",
    "analyse": "Analyse",
    "extend": "Extend",
    "exit": "Exit",
}


def markdown(source: str, cell_id: str) -> dict:
    return {
        "cell_type": "markdown",
        "id": cell_id,
        "metadata": {},
        "source": [line + "\n" for line in source.rstrip().splitlines()],
    }


def first_heading(cell: dict) -> str | None:
    if cell.get("cell_type") != "markdown":
        return None
    for line in cell.get("source", []):
        if re.match(r"^#{1,6}\s", line):
            return line.strip()
    return None


def demote_headings(cell: dict) -> None:
    """Nest existing content under a stage heading, capped at level four."""
    if cell.get("cell_type") != "markdown":
        return
    changed = []
    for line in cell.get("source", []):
        match = re.match(r"^(#{1,6})(\s+.*)$", line)
        if match:
            level = min(len(match.group(1)) + 1, 4)
            line = "#" * level + match.group(2)
        changed.append(line)
    cell["source"] = changed


def find_index(cells: list[dict], cell_id: str) -> int:
    for index, cell in enumerate(cells):
        if cell.get("id") == cell_id:
            return index
    raise KeyError(cell_id)


def stage(cell_id: str, key: str, extra: str = "") -> dict:
    body = f"# {STAGE_TITLES[key]}"
    if extra:
        body += "\n\n" + extra.strip()
    return markdown(body, f"workshop-stage-{cell_id}-{key}")


def split_title_preamble(cells: list[dict]) -> list[dict]:
    """Keep only the notebook title in cell zero; retain its prose after Context."""
    title = cells[0]
    if title.get("cell_type") != "markdown":
        return []
    text = "".join(title.get("source", []))
    lines = text.splitlines()
    if len(lines) <= 1 or not any(line.strip() for line in lines[1:]):
        return []
    title["source"] = [lines[0] + "\n"]
    prose = "\n".join(lines[1:]).strip()
    return [markdown(prose, f"{title.get('id', 'workshop')}-context-preamble")]


def rebuild(path: Path, boundaries: list[tuple[str, str]], *, extras=None) -> None:
    data = json.loads(path.read_text())
    if any(str(c.get("id", "")).startswith("workshop-stage-") for c in data["cells"]):
        print(f"already structured {path.relative_to(NOTEBOOKS)}")
        return
    cells = [c for c in data["cells"] if not str(c.get("id", "")).startswith("workshop-stage-")]

    for index, cell in enumerate(cells):
        if not cell.get("id"):
            cell["id"] = f"{path.parent.name}-cell-{index}"

    preamble = split_title_preamble(cells)
    for cell in cells[1:]:
        demote_headings(cell)

    insertions: list[tuple[int, dict]] = []
    for key, cell_id in boundaries:
        index = find_index(cells, cell_id)
        insertions.append((index, stage(path.parent.name, key)))

    for index, new_cell in sorted(insertions, key=lambda item: item[0], reverse=True):
        cells.insert(index, new_cell)

    if preamble:
        context_index = next(i for i, c in enumerate(cells) if c.get("id") == f"workshop-stage-{path.parent.name}-context")
        cells[context_index + 1:context_index + 1] = preamble

    if extras:
        extras(cells)

    data["cells"] = cells
    path.write_text(json.dumps(data, ensure_ascii=False, indent=1) + "\n")


def add_after(cells: list[dict], after_id: str, new_cell: dict) -> None:
    cells.insert(find_index(cells, after_id) + 1, new_cell)


def week7_extras(cells: list[dict]) -> None:
    exit_id = "workshop-stage-week07-exit"
    add_after(cells, exit_id, markdown(
        "Before leaving, record one result that came from the swarm as a whole and one modelling choice in the objective landscape that you would revisit.",
        "week07-exit-prompt",
    ))


def week9_extras(cells: list[dict]) -> None:
    extend_id = "workshop-stage-week09-extend"
    add_after(cells, extend_id, markdown(
        "Choose one change to the representation: compare another text, change the symbol set, or increase the block length. State what additional structure the revised distribution can retain and what it still discards.",
        "week09-extension-prompt",
    ))


def week10_extras(cells: list[dict]) -> None:
    extend_id = "workshop-stage-week10-extend"
    add_after(cells, extend_id, markdown(
        "Change one evolutionary mechanism at a time: mutation, selection strength, population structure, or update timing. Predict which individual histories and population-level outcomes should change before rerunning the model.",
        "week10-extension-prompt",
    ))
    checkpoint_index = find_index(cells, "week10-cell-34")
    cells.insert(checkpoint_index + 1, stage("week10", "exit"))
    add_after(cells, "workshop-stage-week10-exit", markdown(
        "Record the mechanism that most affected the evolutionary outcome and the evidence needed to distinguish a robust result from one history produced by one seed.",
        "week10-exit-prompt",
    ))


CONFIG = {
    "week01/WS_Introduction_to_complex_systems.ipynb": [
        ("context", "transferable-modelling-focus"), ("specify", "model-specification"),
        ("implement", "setup-intro"), ("simulate", "simulation-intro"),
        ("analyse", "analyse-one-run"), ("extend", "extensions"),
        ("exit", "8881e60f"),
    ],
    "week02/WS_Fractals.ipynb": [
        ("context", "transferable-modelling-focus"), ("specify", "sierpinski-intro"),
        ("implement", "sierpinski-function"), ("simulate", "sierpinski-generation-animation-note"),
        ("analyse", "box-count-intro"), ("extend", "extensions"),
        ("exit", "a634ad97"),
    ],
    "week03/WS_Reaction_diffusion.ipynb": [
        ("context", "transferable-modelling-focus"), ("specify", "gray-scott-model"),
        ("implement", "laplacian-intro"), ("simulate", "simulation-intro"),
        ("analyse", "observables-intro"), ("extend", "interpret-comparison"),
        ("exit", "week03-cell-32"),
    ],
    "week04/WS_Cellular_automata.ipynb": [
        ("context", "transferable-modelling-focus"), ("specify", "model-specification"),
        ("implement", "step-intro"), ("simulate", "simulate-intro"),
        ("analyse", "fair-comparison-intro"), ("extend", "extensions"),
        ("exit", "week04-cell-42"),
    ],
    "week05/WS_ABM.ipynb": [
        ("context", "transferable-modelling-focus"), ("specify", "specification"),
        ("implement", "periodic-intro"), ("simulate", "simulate-intro"),
        ("analyse", "polarisation-intro"), ("extend", "extensions"),
        ("exit", "52e0daff"),
    ],
    "week06/WS_Synchronisation.ipynb": [
        ("context", "transferable-modelling-focus"), ("specify", "uncoupled-intro"),
        ("implement", "step-intro"), ("simulate", "simulate-intro"),
        ("analyse", "coherence-intro"), ("extend", "cd3aaf3e"),
        ("exit", "exit-ticket"),
    ],
    "week07/WS_Intelligent_systems.ipynb": [
        ("context", "two-objectives"), ("specify", "optimisation-problem"),
        ("implement", "build-pso"), ("simulate", "rastrigin-animation-heading"),
        ("analyse", "ensemble-heading"), ("extend", "extension"),
        ("exit", "checkpoint"),
    ],
    "week08/WS_Critical_phenomena.ipynb": [
        ("context", "5849afab-ba07-4713-8d96-5adeecef9d21"), ("specify", "w8-build"),
        ("implement", "w8-code"), ("simulate", "w8-check"),
        ("analyse", "w8-measure"), ("extend", "w8-extension"),
        ("exit", "w8-takeaway"),
    ],
    "week09/WS_Information_theory.ipynb": [
        ("context", "w9w-objectives"), ("specify", "w9w-distributions"),
        ("implement", "w9w-distribution-plot"), ("simulate", "w9w-text"),
        ("analyse", "w9w-failure"), ("extend", "w9w-decision"),
        ("exit", "w9w-takeaway"),
    ],
    "week10/WS_Game_theory.ipynb": [
        ("context", "transferable-modelling-focus"), ("specify", "22a06975"),
        ("implement", "evolutionary-model-implementation"), ("simulate", "evolutionary-frequency-animation-note"),
        ("analyse", "evidence-checkpoint-evolution"), ("extend", "week10-cell-34"),
    ],
}


EXTRAS = {
    "week07/WS_Intelligent_systems.ipynb": week7_extras,
    "week09/WS_Information_theory.ipynb": week9_extras,
    "week10/WS_Game_theory.ipynb": week10_extras,
}


def main() -> None:
    for relative, boundaries in CONFIG.items():
        path = NOTEBOOKS / relative
        rebuild(path, boundaries, extras=EXTRAS.get(relative))
        print(f"updated {relative}")

    finalise_structure()


def finalise_structure() -> None:
    """Small, content-preserving corrections revealed by the hierarchy audit."""
    # Week 4 contains two canonical CA implementations. Put both definitions and
    # tests before their simulations, then analyse them together.
    path = NOTEBOOKS / "week04/WS_Cellular_automata.ipynb"
    data = json.loads(path.read_text())
    cells = data["cells"]
    if not any(c.get("id") == "week04-two-models-ordered" for c in cells):
        by_id = {c.get("id"): c for c in cells}
        life_define_ids = ["life-model", "life-functions", "life-tests-intro", "life-tests"]
        life_sim_ids = ["life-history-intro", "life-snapshots", "life-player", "life-investigation"]
        moved_ids = set(life_define_ids + life_sim_ids)
        cells = [c for c in cells if c.get("id") not in moved_ids]
        implement_at = next(i for i, c in enumerate(cells) if c.get("id") == "workshop-stage-week04-simulate")
        cells[implement_at:implement_at] = [by_id[i] for i in life_define_ids]
        analyse_at = next(i for i, c in enumerate(cells) if c.get("id") == "workshop-stage-week04-analyse")
        cells[analyse_at:analyse_at] = [by_id[i] for i in life_sim_ids]
        marker_at = next(i for i, c in enumerate(cells) if c.get("id") == "life-model")
        cells.insert(marker_at, markdown(
            "The same workflow now carries into a two-dimensional cellular automaton.",
            "week04-two-models-ordered",
        ))
        data["cells"] = cells
        path.write_text(json.dumps(data, ensure_ascii=False, indent=1) + "\n")

    # Week 9 deliberately constructs and inspects distributions rather than
    # forcing an animation stage that does not suit the canonical calculation.
    path = NOTEBOOKS / "week09/WS_Information_theory.ipynb"
    data = json.loads(path.read_text())
    for cell in data["cells"]:
        if cell.get("id") == "workshop-stage-week09-simulate":
            cell["source"] = ["# Construct and inspect distributions\n"]
    path.write_text(json.dumps(data, ensure_ascii=False, indent=1) + "\n")

    # Restore missing line breaks in inherited Week 10 headings. This changes
    # presentation only; the original wording remains intact.
    path = NOTEBOOKS / "week10/WS_Game_theory.ipynb"
    data = json.loads(path.read_text())
    replacements = {
        "## EvolutionTo evolve is to change over time": "## Evolution\n\nTo evolve is to change over time",
        "### Explaining global/macroscopic observationsi.e. the output": "### Explaining global/macroscopic observations\n\ni.e. the output",
        "### Mechanisms for evolutioni.e. the inputs required": "### Mechanisms for evolution\n\ni.e. the inputs required",
        "### An examplehttps://www.complexity-explorables.org/explorables/maggots-in-the-wiggle-room/": "### An example\n\nhttps://www.complexity-explorables.org/explorables/maggots-in-the-wiggle-room/",
        "#### FitnessEvolution is a change in a population's distribution of genotypes (may be hard to visualise)": "#### Fitness\n\nEvolution is a change in a population's distribution of genotypes (may be hard to visualise)",
        "#### Remember...Agents don't move over the fitness landscape (the genotype of an organism doesn't change)": "#### Remember...\n\nAgents don't move over the fitness landscape (the genotype of an organism doesn't change)",
        "### Building the required mechanisms for adaptation into the model1. Variation: initialise the population with a variety of genotypes (or could simply rely on mutation)": "### Building the required mechanisms for adaptation into the model\n\n1. Variation: initialise the population with a variety of genotypes (or could simply rely on mutation)",
        "### Successful strategiesSuccessful strategies in the tournament had the following properties:": "### Successful strategies\n\nSuccessful strategies in the tournament had the following properties:",
        "#### Tit for TatOne strategy, called Tit for Tat, cooperated in the first instance and then copied the opponents move in the previous round of play": "#### Tit for Tat\n\nOne strategy, called Tit for Tat, cooperated in the first instance and then copied the opponents move in the previous round of play",
        "### AnalysisWhat sorts of questions might we try and answer with a computational model of the tournament?": "### Analysis\n\nWhat sorts of questions might we try and answer with a computational model of the tournament?",
    }
    for cell in data["cells"]:
        if cell.get("cell_type") != "markdown":
            continue
        text = "".join(cell.get("source", [])).rstrip("\n")
        if text in replacements:
            cell["source"] = [line + "\n" for line in replacements[text].splitlines()]
    path.write_text(json.dumps(data, ensure_ascii=False, indent=1) + "\n")


if __name__ == "__main__":
    main()
