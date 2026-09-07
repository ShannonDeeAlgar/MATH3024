"""Regroup Week 6 lecture and Reader content under a small set of banners."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "notebooks/week06/L_Synchronisation.ipynb"


def text(cell: dict) -> str:
    return "".join(cell.get("source", []))


def markdown(source: str, slide_type: str = "", tags: list[str] | None = None) -> dict:
    metadata: dict = {"slideshow": {"slide_type": slide_type}}
    if tags:
        metadata["tags"] = tags
    return {
        "cell_type": "markdown",
        "metadata": metadata,
        "source": source.splitlines(keepends=True),
    }


def replace_heading(cell: dict, old: str, new: str) -> None:
    src = text(cell)
    if not src.startswith(old):
        raise ValueError(f"Expected heading {old!r}, found {src.splitlines()[0]!r}")
    cell["source"] = (new + src[len(old) :]).splitlines(keepends=True)


def index_of(cells: list[dict], prefix: str, start: int = 0) -> int:
    for i in range(start, len(cells)):
        if text(cells[i]).startswith(prefix):
            return i
    raise ValueError(f"Could not find {prefix!r}")


def move_cell(cells: list[dict], prefix: str, before_prefix: str) -> None:
    source_index = index_of(cells, prefix)
    cell = cells.pop(source_index)
    target_index = index_of(cells, before_prefix)
    cells.insert(target_index, cell)


nb = json.loads(PATH.read_text())
cells = nb["cells"]

# ---------------------------------------------------------------------------
# Slides: five horizontal arguments, with vertical development inside each.
# ---------------------------------------------------------------------------
slide_changes = {
    "# Spontaneous synchronisation\n": "# Real-world motivation\n",
    "# Begin with one phase oscillator\n": "# Model details\n\n## One phase oscillator\n",
    "# Canonical model · Kuramoto oscillators\n": "## Canonical model · Kuramoto oscillators\n",
    "# Measure collective coherence\n": "# Analysis\n\n## Quantitative analysis · collective coherence\n",
    "# Sweep coupling strength\n": "## Parameter sweep\n",
    "# What survives beyond the toy model?\n": "# Scope and connections\n",
}

for old, new in slide_changes.items():
    i = index_of(cells, old)
    replace_heading(cells[i], old, new)
    if new.startswith("##") or "\n## " in new:
        cells[i].setdefault("metadata", {}).setdefault("slideshow", {})["slide_type"] = "subslide"

# Move assumptions before the explorable so the explorable forms its own banner.
move_cell(cells, "## Make the assumptions visible\n", "## Explore the Kuramoto model\n")

explore_i = index_of(cells, "## Explore the Kuramoto model\n")
cells.insert(
    explore_i,
    markdown(
        "# Explorable\n\nUse the controls to connect heterogeneous internal clocks, coupling, and collective coherence.\n",
        "slide",
        ["slides-only"],
    ),
)

# The real bridge example deserves more than one table row.
firefly_i = index_of(cells, "## Synchronous fireflies\n")
cells.insert(
    firefly_i,
    markdown(
        "## The wobbling Millennium Bridge\n\n"
        "**Opening day, 2000:** pedestrian–bridge feedback produced large lateral oscillations.\n\n"
        "**Popular account:** walkers simply synchronised their footsteps.\n\n"
        "**More careful account:** each pedestrian altered the bridge's effective damping; strong wobble can emerge even without complete footstep synchrony. A sufficiently large crowd was the important threshold.\n\n"
        "The lesson is broader than the label: coupling changed both the pedestrians' motion and the structure they were walking on.\n\n"
        "<div class=\"discussion-marker\"><img src=\"images/discussion_marker.svg\" alt=\"Discussion prompt\"><span>Where is the coupling pathway, and which parts of this system have their own dynamics?</span></div>\n\n"
        "<p class=\"figure-credit\">See Strogatz et al. (2005) and Belykh et al. (2021).</p>\n",
        "subslide",
        ["slides-only"],
    ),
)

# ---------------------------------------------------------------------------
# Reader: retain the established order, but remove the forest of H1 headings.
# ---------------------------------------------------------------------------
reader_start = index_of(cells, "# Spontaneous synchronisation\n", start=index_of(cells, "# Scope and connections\n") + 1)
replace_heading(cells[reader_start], "# Spontaneous synchronisation\n", "# Real-world motivation\n\n## Spontaneous synchronisation\n")

fireflies_reader = index_of(cells, "# Fireflies\n", reader_start)
replace_heading(cells[fireflies_reader], "# Fireflies\n", "## Fireflies\n")

phase_reader = index_of(cells, "# A phase oscillator\n", reader_start)
cells.insert(
    phase_reader,
    markdown("# Model details\n", "", ["reader-only"]),
)
phase_reader += 1

reader_demotions = {
    "# A phase oscillator\n": "## A phase oscillator\n",
    "# Two uncoupled oscillators\n": "## Two uncoupled oscillators\n",
    "# Add coupling\n": "## Add coupling\n",
    "# Reduce to phase difference\n": "## Reduce to phase difference\n",
    "# From two oscillators to a network\n": "## Canonical model · Kuramoto oscillators\n",
    "# Dynamics on a network\n": "### Dynamics on a network\n",
}
for old, new in reader_demotions.items():
    i = index_of(cells, old, reader_start)
    replace_heading(cells[i], old, new)

watch_reader = index_of(cells, "# Watch phases organise\n", reader_start)
cells.insert(watch_reader, markdown("# Explorable\n", "", ["reader-only"]))
watch_reader += 1
replace_heading(cells[watch_reader], "# Watch phases organise\n", "## Watch phases organise\n")

analysis_reader = index_of(cells, "# Quantify phase coherence\n", reader_start)
cells.insert(analysis_reader, markdown("# Analysis\n", "", ["reader-only"]))
analysis_reader += 1

analysis_demotions = {
    "# Quantify phase coherence\n": "## Quantitative analysis · phase coherence\n",
    "# Replace many interactions with a mean field\n": "### Replace many interactions with a mean field\n",
    "# First sweep coupling strength\n": "## Parameter sweep\n",
    "# Then repeat each condition\n": "### Repeat each condition\n",
    "# What the model explains\n": "# Scope and connections\n\n## What the model explains\n",
    "# Connections\n": "## Connections\n",
    "# Canonical model at a glance\n": "## Canonical model at a glance\n",
}
for old, new in analysis_demotions.items():
    i = index_of(cells, old, reader_start)
    replace_heading(cells[i], old, new)

# The at-a-glance summary and pseudocode share one Reader cell.
glance_i = index_of(cells, "## Canonical model at a glance\n", reader_start)
glance_src = text(cells[glance_i]).replace(
    "# Canonical model in pseudocode\n", "## Canonical model in pseudocode\n"
)
cells[glance_i]["source"] = glance_src.splitlines(keepends=True)

# Give the bridge its own Reader subsection and preserve the qualification.
huygens_i = index_of(cells, "## From pendulum clocks to living systems\n", reader_start)
bridge_cell = markdown(
    "### The wobbling Millennium Bridge\n\n"
    "When London's Millennium Bridge opened in 2000, pedestrian–bridge feedback produced unexpectedly large lateral oscillations. The familiar story says that the walkers synchronised their footsteps with the bridge. That description is useful but incomplete. Later models and measurements show that substantial bridge motion does not require the whole crowd to march in step: pedestrian responses can instead reduce the structure's effective damping, with instability appearing above a critical crowd size.\n\n"
    "This makes the bridge a particularly useful example. The pedestrians have their own gait dynamics, the bridge has structural modes, and motion provides a two-way coupling pathway. The observed wobble is a property of the coupled pedestrian–bridge system.\n\n"
    "*Further reading:* [Strogatz et al. (2005), *Theoretical mechanics: Crowd synchrony on the Millennium Bridge*](https://doi.org/10.1038/438043a) and [Belykh et al. (2021), *Emergence of the London Millennium Bridge instability without synchronisation*](https://doi.org/10.1038/s41467-021-27568-y).\n",
    "",
    ["reader-only"],
)
cells.insert(huygens_i + 1, bridge_cell)

# Remove the old bridge paragraph from the general list now that it has a home.
for cell in cells:
    src = text(cell)
    old_para = (
        "Synchrony is therefore not automatically desirable. London's Millennium Bridge is a useful caution: pedestrian–bridge feedback produced large lateral wobble. It is often presented as simple crowd synchronisation, but later work shows that the mechanism is more nuanced than everyone stepping together. The robust lesson is that coupling between people and structure changed the collective dynamics.\n"
    )
    if old_para in src:
        cell["source"] = src.replace(
            old_para,
            "Synchrony is therefore not automatically desirable. The examples below include both useful coordination and coupling-driven instability.\n",
        ).splitlines(keepends=True)

PATH.write_text(json.dumps(nb, indent=1, ensure_ascii=False) + "\n")
print(f"Updated {PATH}")
