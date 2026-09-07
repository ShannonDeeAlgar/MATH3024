#!/usr/bin/env python3
"""Add a short drone-show coda after the Week 6 swarmalator material."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK = ROOT / "notebooks/week06/L_Synchronisation.ipynb"


def markdown_cell(cell_id: str, source: str, *, tags: list[str], slide_type: str) -> dict:
    return {
        "cell_type": "markdown",
        "id": cell_id,
        "metadata": {"tags": tags, "slideshow": {"slide_type": slide_type}},
        "source": [line for line in source.splitlines(keepends=True)],
    }


def main() -> None:
    notebook = json.loads(NOTEBOOK.read_text())
    cells = notebook["cells"]

    cells[:] = [
        cell
        for cell in cells
        if cell.get("id") not in {"w6-drone-shows-slide", "w6-drone-shows-reader"}
    ]

    slide = markdown_cell(
        "w6-drone-shows-slide",
        """## Drone shows: choreography or swarm?

Most drone shows are closer to synchronised swimming than to swarmalators. The images and timed trajectories are designed in advance; onboard controllers track those paths while a ground system monitors the fleet.

A more adaptive show could retain the choreography at the group level while allowing local autonomy to avoid collisions, reorganise safely and respond to an audience signal. Gesture-controlled swarm light painting has already demonstrated real-time human input. Fully emergent motion is possible, but it gives up some of the exact repeatability expected of a public performance.

<div class="reference-line">Huang et al. (2021), <a href="https://doi.org/10.3390/app11167687">UAV light-show systems</a>; Serpiva et al. (2021), <a href="https://doi.org/10.1145/3450550.3465349">DronePaint</a>; Balázs et al. (2024), <a href="https://doi.org/10.1007/s11721-024-00241-y">decentralised drone traffic</a>.</div>
""",
        tags=["slides-only"],
        slide_type="subslide",
    )

    slide_index = next(i for i, cell in enumerate(cells) if cell.get("id") == "w6-swarmalators-slide")
    cells.insert(slide_index + 1, slide)

    reader_note = "### Drone shows: choreography or swarm?\n\n"
    reader_note += (
        "Present-day drone light shows are mostly **top-down choreography**. A designer specifies the successive formations, software assigns drones to positions and constructs collision-free reference trajectories, and each aircraft tracks its allotted path. Positioning, telemetry and a ground station make the performance reliable, but the visible pattern is not normally emerging from local interactions. [Huang et al. (2021)](https://doi.org/10.3390/app11167687) describe this design, planning and monitoring pipeline.\n\n"
        "That need not be the only possible design. Decentralised control has already been demonstrated with 100 autonomous drones coordinating traffic from local information rather than a central path planner ([Balázs et al., 2024](https://doi.org/10.1007/s11721-024-00241-y)). Human-swarm systems can also alter a formation in real time: **DronePaint** used hand gestures to draw trajectories and reshape a small drone swarm ([Serpiva et al., 2021](https://doi.org/10.1145/3450550.3465349)).\n\n"
        "For a public show, the likely next step is therefore a hybrid. A choreographer or audience supplies a high-level target, perhaps through sound level, movement, voting or gesture, while autonomous local rules keep the formation safe and adapt the transition. This would be responsive without requiring spectators to pilot individual drones. Only when the displayed motion is produced through local interaction and collective feedback would it begin to resemble the emergent behaviour of swarmalators. Exact choreography and emergence are not mutually exclusive, but they answer to different priorities: repeatability on one side, adaptation on the other.\n"
    )

    reader_index = next(i for i, cell in enumerate(cells) if cell.get("id") == "w6-spatial-fireflies-reader")
    reader_source = "".join(cells[reader_index]["source"])
    marker = "\n\n### Pulse coupling"
    if marker not in reader_source:
        raise RuntimeError("Could not find the Pulse coupling insertion point")
    reader_source = reader_source.replace(marker, "\n\n" + reader_note + marker, 1)
    cells[reader_index]["source"] = reader_source.splitlines(keepends=True)

    NOTEBOOK.write_text(json.dumps(notebook, ensure_ascii=False, indent=1) + "\n")


if __name__ == "__main__":
    main()
