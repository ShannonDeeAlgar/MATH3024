"""Apply the second Reader hierarchy audit without deleting teaching content.

This pass moves intact cell blocks and changes heading levels only.  It is
idempotent so the hierarchy can be reapplied after later notebook refreshes.
"""

from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def text(cell: dict) -> str:
    return "".join(cell.get("source", []))


def set_text(cell: dict, value: str) -> None:
    cell["source"] = value.splitlines(keepends=True)


def tags(cell: dict) -> set[str]:
    return set(cell.get("metadata", {}).get("tags", []))


def active_markdown(cell: dict) -> bool:
    return cell.get("cell_type") == "markdown" and not ({"archive-only", "remove-cell"} & tags(cell))


def load(week: int, filename: str) -> tuple[Path, dict]:
    path = ROOT / "notebooks" / f"week{week:02d}" / filename
    return path, json.loads(path.read_text())


def save(path: Path, notebook: dict) -> None:
    path.write_text(json.dumps(notebook, ensure_ascii=False, indent=1) + "\n")


def cell_by_id(cells: list[dict], cell_id: str) -> dict:
    matches = [cell for cell in cells if cell.get("id") == cell_id]
    if len(matches) != 1:
        raise RuntimeError(f"Expected one cell {cell_id!r}; found {len(matches)}")
    return matches[0]


def index_by_id(cells: list[dict], cell_id: str) -> int:
    return cells.index(cell_by_id(cells, cell_id))


def cells_containing(cells: list[dict], needle: str, required_tag: str | None = None) -> list[dict]:
    return [
        cell for cell in cells
        if active_markdown(cell)
        and needle in text(cell)
        and (required_tag is None or required_tag in tags(cell))
    ]


def one_containing(cells: list[dict], needle: str, required_tag: str | None = None) -> dict:
    matches = cells_containing(cells, needle, required_tag)
    if len(matches) != 1:
        raise RuntimeError(
            f"Expected one active markdown cell containing {needle!r}"
            f" with tag {required_tag!r}; found {len(matches)}"
        )
    return matches[0]


def move_cells_before(cells: list[dict], block: list[dict], destination: dict) -> None:
    for cell in block:
        cells.remove(cell)
    index = cells.index(destination)
    cells[index:index] = block


def demote_exact(cells: list[dict], heading: str, required_tag: str | None = None) -> None:
    old = heading + "\n"
    new = "#" + heading + "\n"
    for cell in cells_containing(cells, old, required_tag):
        value = text(cell)
        if old in value:
            set_text(cell, value.replace(old, new, 1))


def replace_heading(cell: dict, old: str, new: str) -> None:
    value = text(cell)
    if old in value:
        set_text(cell, value.replace(old, new, 1))
    elif new not in value:
        raise RuntimeError(f"Neither old nor new heading found in {cell.get('id')}: {old!r}")


def replace_all_headings(cell: dict, replacements: dict[str, str]) -> None:
    for old, new in replacements.items():
        replace_heading(cell, old, new)


def move_ids_before(cells: list[dict], ids: list[str], before_id: str) -> None:
    block = [cell_by_id(cells, cell_id) for cell_id in ids]
    for cell in block:
        cells.remove(cell)
    destination = index_by_id(cells, before_id)
    cells[destination:destination] = block


def demote_heading_lines(cell: dict, levels: int = 1) -> None:
    lines = text(cell).splitlines(keepends=True)
    for index, line in enumerate(lines):
        if re.match(r"^#{1,6}\s", line):
            lines[index] = "#" * levels + line
    set_text(cell, "".join(lines))


def week2() -> None:
    path, nb = load(2, "L_Fractals.ipynb")
    cells = nb["cells"]

    # Keep the broad teaching beats visible; make their supporting detail
    # subordinate so the contents page no longer reads as a flat list.
    supporting = [
        "## Defining properties", "## When smoothness fails", "## Canonical constructions",
        "## Multiple descriptions", "## Convergence of an IFS", "## L-systems",
        "## Comparing generation mechanisms", "## What does dimension measure?",
        "## Similarity dimension", "## Invent a fractal", "## Coastlines",
        "## A hierarchy of dimensions", "## Hausdorff dimension", "## Box counting",
        "## Choosing a scaling range", "## Choosing a dimension", "## Australian coastline",
        "## Characteristic scales", "## Scale-free", "## Power laws",
        "## Finite scaling ranges", "## A common language", "## From pattern to mechanism",
    ]
    for heading in supporting:
        demote_exact(cells, heading)

    # Two headings in one cell were competing for the same conceptual beat.
    cell = one_containing(cells, "An early mathematical")
    replace_all_headings(cell, {
        "### When smoothness fails": "### When smoothness fails: an early mathematical ‘monster’",
        "### An early mathematical “monster”\n": "",
    })
    save(path, nb)


def week3() -> None:
    path, nb = load(3, "L_Reaction_diffusion.ipynb")
    cells = nb["cells"]
    # Remove only the archived duplicate; the active heading and its content stay.
    duplicates = [
        cell for cell in cells
        if "The modelling problem underneath the model" in text(cell)
        and {"archive-only", "remove-cell"} & tags(cell)
    ]
    for cell in duplicates:
        cells.remove(cell)
    save(path, nb)


def week4() -> None:
    path, nb = load(4, "L_Cellular_automata.ipynb")
    cells = nb["cells"]

    # Scene-setting Explorables now precede formal model detail in the Reader.
    explorable = [
        one_containing(cells, "# Explorable\n", "reader-only"),
        one_containing(cells, "## Explore a one-dimensional cellular automaton", "reader-only"),
        one_containing(cells, "### Shell pigmentation: a space–time record", "reader-only"),
        one_containing(cells, "## Traffic as a one-dimensional cellular automaton", "reader-only"),
        one_containing(cells, "### Explore a two-dimensional cellular automaton", "reader-only"),
    ]
    move_cells_before(cells, explorable, one_containing(cells, "# Model details\n", "reader-only"))

    # Components of a CA sit beneath the Von Neumann introduction.
    for heading in ["## The world", "## State", "## Neighbourhood or network",
                    "## Update rule, boundary and clock", "## Earlier cellular-automaton ideas"]:
        demote_exact(cells, heading, "reader-only")

    # Model examples and analytical techniques retain clear parent headings.
    for heading in ["## The model", "## Observing the dynamics", "## Emergent structures in Game of Life",
                    "## Extensions", "## A. Elementary CA · state-transition diagrams",
                    "## B. Reversibility is a global property", "## C. Elementary CA · damage spreading",
                    "## D. Game of Life · mean-field approximation"]:
        demote_exact(cells, heading, "reader-only")

    # Empirical examples belong beneath one shared Scope subsection.
    for heading in ["## Rule 30 and shell pigmentation", "## A cellular automaton in living skin",
                    "## A two-dimensional wave across a bee colony", "## The same architecture, different models",
                    "## What cellular automata teach us", "## Cellular automata as computers"]:
        demote_exact(cells, heading, "reader-only")
    save(path, nb)


def week6() -> None:
    path, nb = load(6, "L_Synchronisation.ipynb")
    cells = nb["cells"]

    # Reader: five broad banners.  Model specification precedes phase-oscillator
    # examples; the two-oscillator reduction begins Analysis.
    specification = [
        one_containing(cells, "# Model details\n\n## Specify the model", "reader-only"),
        one_containing(cells, "## Canonical model · Kuramoto oscillators", "reader-only"),
        one_containing(cells, "## Natural-frequency distribution", "reader-only"),
        one_containing(cells, "### Standard all-to-all coupling", "reader-only"),
    ]
    move_cells_before(cells, specification, one_containing(cells, "## A phase oscillator", "reader-only"))
    phase_banner = one_containing(cells, "# Phase oscillators\n", "reader-only")
    replace_heading(phase_banner, "# Phase oscillators", "# Model details")
    replace_heading(specification[0], "# Model details\n\n", "")
    replace_heading(one_containing(cells, "# Two-oscillator analysis", "reader-only"), "# Two-oscillator analysis", "# Analysis")
    population = one_containing(cells, "# Population analysis", "reader-only")
    replace_heading(population, "# Population analysis\n\n## Numerical experiments", "## Numerical population analysis")
    replace_heading(one_containing(cells, "## Qualitative analysis", "reader-only"), "## Qualitative analysis", "### Qualitative analysis")
    replace_heading(one_containing(cells, "## Quantitative analysis", "reader-only"), "## Quantitative analysis", "### Quantitative analysis")
    variants = one_containing(cells, "## Model variants", "reader-only")
    replace_heading(variants, "## Model variants", "# Scope and extensions\n\n## Model variants")
    replace_heading(one_containing(cells, "# Return to the real systems", "reader-only"), "# Return to the real systems", "## Return to real systems")
    replace_heading(one_containing(cells, "## Return to the fireflies: restore physical space", "reader-only"), "## Return to the fireflies: restore physical space", "### Return to the fireflies: restore physical space")
    replace_heading(one_containing(cells, "## Connections", "reader-only"), "## Connections", "### Connections")
    replace_heading(one_containing(cells, "## Kuramoto looks back", "reader-only"), "## Kuramoto looks back", "### Kuramoto looks back")

    # Slides use the same narrative names and the same five-banner logic.
    replace_heading(one_containing(cells, "# Phase oscillators", "slides-only"), "# Phase oscillators", "# Model details")
    replace_heading(one_containing(cells, "# Two-oscillator analysis", "slides-only"), "# Two-oscillator analysis", "# Analysis")
    replace_heading(one_containing(cells, "# Model details\n\n## Specify", "slides-only"), "# Model details\n\n", "")
    replace_heading(one_containing(cells, "# Population analysis", "slides-only"), "# Population analysis\n\n## Numerical experiments", "## Numerical population analysis")
    replace_heading(one_containing(cells, "# Model variants", "slides-only"), "# Model variants", "# Scope and extensions\n\n## Model variants")
    replace_heading(one_containing(cells, "# Return to the real systems", "slides-only"), "# Return to the real systems", "## Return to real systems")

    for cell in cells_containing(cells, "What changes with $N$?") + cells_containing(cells, "Effect of population size"):
        value = text(cell).replace("What changes with $N$?", "Finite-size effects").replace("Effect of population size", "Finite-size effects")
        set_text(cell, value)
    replace_heading(one_containing(cells, "## Drone shows: choreography or swarm?"), "## Drone shows: choreography or swarm?", "## Drone shows: choreography and swarm control")
    save(path, nb)


def week7() -> None:
    path, nb = load(7, "L_Intelligent_systems.ipynb")
    cell = one_containing(nb["cells"], "## What should we ask of an intelligent system?")
    replace_heading(cell, "## What should we ask of an intelligent system?", "## Evaluating an intelligent system")
    save(path, nb)


def week8() -> None:
    path, nb = load(8, "L_Critical_phenomena.ipynb")
    cell = one_containing(nb["cells"], "## Qualitative analysis")
    replace_heading(cell, "## Qualitative analysis", "# Analysis\n\n## Qualitative analysis")
    save(path, nb)


def week9() -> None:
    path, nb = load(9, "L_InformationTheory.ipynb")
    cells = nb["cells"]
    candidates = [cell for cell in cells if cell.get("cell_type") == "markdown" and "## Why measure information?" in text(cell)]
    if len(candidates) == 1:
        replace_heading(candidates[0], "## Why measure information?", "## Information as a system-level description")
    save(path, nb)


def week10() -> None:
    path, nb = load(10, "L_Game_theory.ipynb")
    cells = nb["cells"]
    evolution = [one_containing(cells, heading) for heading in [
        "# From games to evolution", "## Repeated play", "## Axelrod's tournaments",
        "## Tournament success and evolutionary success", "## Replicator dynamics", "## Structured populations",
    ]]
    move_cells_before(cells, evolution, one_containing(cells, "# Explorable"))
    replace_heading(evolution[0], "# From games to evolution", "## From games to evolution")
    for cell in evolution[1:]:
        first = next((line for line in text(cell).splitlines() if line.startswith("#")), "")
        if first.startswith("## "):
            demote_heading_lines(cell)
    save(path, nb)


def main() -> None:
    for transform in [week2, week3, week4, week6, week7, week8, week9, week10]:
        transform()
        print(f"Applied {transform.__name__}")


if __name__ == "__main__":
    main()
