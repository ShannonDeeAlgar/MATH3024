#!/usr/bin/env python3
"""Keep the Week 6 workshop investigative and move lecture-style material to the Reader."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WORKSHOP = ROOT / "notebooks/week06/WS_Synchronisation.ipynb"
LECTURE = ROOT / "notebooks/week06/L_Synchronisation.ipynb"


def source(cell: dict) -> str:
    return "".join(cell.get("source", []))


def set_source(cell: dict, text: str) -> None:
    cell["source"] = text.splitlines(keepends=True)


def replace_markdown(cells: list[dict], heading: str, text: str) -> None:
    matches = [cell for cell in cells if cell["cell_type"] == "markdown" and source(cell).startswith(heading)]
    if len(matches) != 1:
        raise RuntimeError(f"Expected one {heading!r} cell; found {len(matches)}")
    set_source(matches[0], text)


def replace_markdown_once(cells: list[dict], old_heading: str, new_heading: str, text: str) -> None:
    matches = [
        cell for cell in cells
        if cell["cell_type"] == "markdown"
        and (source(cell).startswith(old_heading) or source(cell).startswith(new_heading))
    ]
    if len(matches) != 1:
        raise RuntimeError(
            f"Expected one {old_heading!r}/{new_heading!r} cell; found {len(matches)}"
        )
    set_source(matches[0], text)


def replace_reader_markdown(cells: list[dict], heading: str, text: str) -> None:
    matches = [
        cell for cell in cells
        if cell["cell_type"] == "markdown"
        and source(cell).startswith(heading)
        and "reader-only" in cell.get("metadata", {}).get("tags", [])
    ]
    if len(matches) != 1:
        raise RuntimeError(f"Expected one reader-only {heading!r} cell; found {len(matches)}")
    set_source(matches[0], text)


def main() -> None:
    workshop = json.loads(WORKSHOP.read_text())
    cells = workshop["cells"]

    replace_markdown_once(
        cells,
        "## A compact toolkit for heterogeneity",
        "## Vary the heterogeneity",
        r"""## Vary the heterogeneity

Hold $K$, $N$, $\Delta t$, the interaction network and the observation window fixed. Vary only the standard deviation $\sigma_\omega$ of the natural-frequency distribution.

This is the modelling focus for the week: the update rule is unchanged, but the individuals are less alike. For every value of $\sigma_\omega$, run several independently sampled populations and record the long-time coherence.

> **Up the ladder:** replace each population by its long-time coherence $r_\infty$, then summarise repeated populations at the same $\sigma_\omega$.
""",
    )

    replace_markdown(
        cells,
        "## Further investigation",
        r"""## Further investigation

The core investigation varied the width of one unimodal natural-frequency distribution. A project could instead:

- compare unimodal and bimodal frequency distributions;
- assign different responsiveness values $K_i$ to the oscillators;
- replace all-to-all coupling with a fixed local, sparse or modular network;
- let the interaction network change with the oscillator states;
- change the observable, for example from phase to a brief flash;
- allow oscillators to move in physical space, as in a swarmalator model.

Choose one change. State what remains fixed, what will be varied, what will be measured and what comparison would answer the question. Avoid changing several parts of the model at once.
""",
    )

    cluster_cell = next(
        cell for cell in cells
        if cell["cell_type"] == "markdown"
        and (
            source(cell).startswith("#### Two coherent groups")
            or source(cell).startswith("### A low global coherence")
        )
    )
    set_source(
        cluster_cell,
        r"""### A low global coherence can hide local order

Two tight phase groups on opposite sides of the circle can have small global $r$ because their mean vectors cancel. This is a useful warning about any collective summary: return to the individual phases when the number does not match what the simulation appears to show.

> **Discuss:** What would you plot or calculate to distinguish two coherent groups from one disordered population?
""",
    )

    # The lecture-style material begins after the useful frequency-width sweep
    # and ends at the workshop extension. Remove the complete span so no helper
    # or animation code is left without its explanation.
    trim_starts = [
        i for i, cell in enumerate(cells)
        if cell["cell_type"] == "markdown"
        and source(cell).startswith("#### Change the shape of the distribution")
    ]
    if trim_starts:
        trim_start = trim_starts[0]
        trim_end = next(
            i for i, cell in enumerate(cells)
            if cell["cell_type"] == "markdown" and source(cell).startswith("# Extend")
        )
        trimmed = cells[:trim_start] + cells[trim_end:]
    else:
        trimmed = cells

    coherence_index = next(
        i for i, cell in enumerate(trimmed)
        if cell["cell_type"] == "code" and "def coherence(" in source(cell)
    )
    if cluster_cell not in trimmed:
        trimmed.insert(coherence_index + 1, cluster_cell)
    workshop["cells"] = trimmed
    WORKSHOP.write_text(json.dumps(workshop, indent=1, ensure_ascii=False) + "\n")

    lecture = json.loads(LECTURE.read_text())
    replace_reader_markdown(
        lecture["cells"],
        "## Qualitative analysis",
        r"""## Qualitative analysis

The earlier Complexity Explorable is the better place to roam through many parameter choices. Here one reproducible Kuramoto run is shown in several ways so that the representation can be separated from the dynamics.

<img src="images/kuramoto_phase_circle.gif" alt="The same Kuramoto simulation shown as positions in phase space and as fixed nodes that flash" style="display:block;width:66%;max-width:760px;margin:1rem auto">

On the phase circle, position records progress through an oscillation cycle; it is not physical location. In the fixed-node view, the nodes do not move and briefly flash as their phases pass a chosen point in the cycle. Both displays show the same stored state.

The same run can also be read as a time series. Each line below is one oscillator's wrapped phase. The repeated rise and reset records continued cycling, while the lines drawing together show the phases becoming coordinated.

<img src="images/kuramoto_phase_time_series.svg" alt="Wrapped phase time series for twelve oscillators approaching synchrony" style="display:block;width:72%;max-width:820px;margin:1rem auto">

A network diagram adds another choice. Fixed node positions make changing edges easy to see; arranging nodes by phase makes phase groups easy to see. Neither layout changes the simulated network. Likewise, colouring nodes by phase exposes the model state, while showing brief flashes represents something an observer might measure. These are alternative views of a run, not different Kuramoto equations.

The Workshop now concentrates on changing the model and measuring the response. These polished representations remain here because comparing representations is part of interpreting a simulation, not a separate numerical experiment.
""",
    )
    LECTURE.write_text(json.dumps(lecture, indent=1, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
