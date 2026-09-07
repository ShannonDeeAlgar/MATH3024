"""Apply the flexible five-stage teaching hierarchy across Weeks 1--10.

The transformation preserves every existing cell and cell ID. It inserts broad
section banners, demotes former top-level teaching beats beneath those banners,
and makes the corresponding slide moves vertical. Week 4's empirical examples
are moved intact to the scope section after the analysis.
"""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def source(cell):
    return "".join(cell.get("source", []))


def first_line(cell):
    text = source(cell)
    return next((line for line in text.splitlines() if line.strip()), "")


def tags(cell):
    return set(cell.get("metadata", {}).get("tags", []))


def active(cell):
    return not ({"archive-only", "remove-cell"} & tags(cell))


def find(cells, title, required_tag=None):
    matches = [
        index
        for index, cell in enumerate(cells)
        if first_line(cell) == title
        and (required_tag is None or required_tag in tags(cell))
    ]
    if len(matches) != 1:
        raise RuntimeError(f"Expected one {title!r} with tag {required_tag!r}; found {matches}")
    return matches[0]


def make_banner(title, cell_id, destination):
    return {
        "cell_type": "markdown",
        "id": cell_id,
        "metadata": {
            "slideshow": {"slide_type": "slide" if destination != "reader-only" else "skip"},
            "tags": [destination],
        },
        "source": [f"# {title}\n"],
    }


def add_banner(cells, title, cell_id, before, destination="slides", anchor_tag=None):
    if any(cell.get("id") == cell_id for cell in cells):
        return
    index = find(cells, before, anchor_tag)
    cells.insert(index, make_banner(title, cell_id, destination))


def move_block(cells, start_title, end_title, before_title, required_tag):
    start = find(cells, start_title, required_tag)
    end = find(cells, end_title, required_tag)
    if end < start:
        # The block has already been moved past the analysis section.
        return
    if not start < end:
        raise RuntimeError(f"Unexpected block order for {start_title!r}")
    block = cells[start:end]
    del cells[start:end]
    destination = find(cells, before_title, required_tag)
    cells[destination:destination] = block


def demote_and_verticalise(cells, title_id, banner_ids):
    protected = {title_id, *banner_ids}
    for cell in cells:
        if cell.get("cell_type") != "markdown" or not active(cell):
            continue
        lines = source(cell).splitlines(keepends=True)
        if not lines:
            continue
        heading_index = next((i for i, line in enumerate(lines) if line.strip()), None)
        if heading_index is None:
            continue
        if lines[heading_index].startswith("# ") and cell.get("id") not in protected:
            lines[heading_index] = "#" + lines[heading_index]
            cell["source"] = lines
        slide_type = cell.get("metadata", {}).get("slideshow", {}).get("slide_type")
        if slide_type == "slide" and cell.get("id") not in protected:
            cell["metadata"]["slideshow"]["slide_type"] = "subslide"


def update_week(week, banners, moves=()):
    path = next((ROOT / "notebooks" / f"week{week:02d}").glob("L_*.ipynb"))
    notebook = json.loads(path.read_text())
    cells = notebook["cells"]
    original_ids = [cell.get("id") for cell in cells]

    requested_banner_ids = [banner["cell_id"] for banner in banners]
    hierarchy_already_present = all(cell_id in original_ids for cell_id in requested_banner_ids)
    if not hierarchy_already_present:
        for move in moves:
            move_block(cells, **move)

    banner_ids = []
    for banner in banners:
        add_banner(cells, **banner)
        banner_ids.append(banner["cell_id"])

    title_id = original_ids[0]
    demote_and_verticalise(cells, title_id, banner_ids)

    resulting_ids = [cell.get("id") for cell in cells]
    missing = [cell_id for cell_id in original_ids if cell_id not in resulting_ids]
    if missing:
        raise RuntimeError(f"Week {week}: lost original cells {missing}")
    expected_added = sum(cell_id not in original_ids for cell_id in banner_ids)
    if len(resulting_ids) != len(original_ids) + expected_added:
        raise RuntimeError(f"Week {week}: unexpected cell-count change")

    path.write_text(json.dumps(notebook, indent=1, ensure_ascii=False) + "\n")
    print(f"Week {week}: preserved {len(original_ids)} cells; inserted {expected_added} banners")


update_week(
    1,
    [
        dict(title="Real-world motivation", cell_id="w1-motivation-banner", before="# Two systems. Two modelling attempts."),
        dict(title="Explorable", cell_id="w1-explorable-banner", before="# Let's model!"),
        dict(title="Model details", cell_id="w1-model-banner", before="# Our turn: build the model"),
        dict(title="Analysis", cell_id="w1-analysis-banner", before="# Analyse one run"),
        dict(title="Scope and connections", cell_id="w1-scope-banner", before="# Final thoughts"),
    ],
)

update_week(
    2,
    [
        dict(title="Real-world motivation", cell_id="w2-motivation-banner", before="# Listen first · “Mandelbrot Set”"),
        dict(title="Explorable", cell_id="w2-explorable-banner", before="# Explore branching", destination="slides-only", anchor_tag="slides-only"),
        dict(title="Explorable", cell_id="w2-reader-explorable-banner", before="## Weeds & Trees: model and mechanism", destination="reader-only", anchor_tag="reader-only"),
        dict(title="Model details", cell_id="w2-model-banner", before="# Exact fractals and fractal-like forms"),
        dict(title="Analysis", cell_id="w2-analysis-banner", before="# Infinite detail changes what “size” means"),
        dict(title="Scope and connections", cell_id="w2-scope-banner", before="# Why this matters in Complex Systems"),
    ],
)

update_week(
    3,
    [
        dict(title="Real-world motivation", cell_id="w3-motivation-banner", before="# How did the cheetah get its spots?"),
        dict(title="Explorable", cell_id="w3-explorable-banner", before="# Understanding diffusion"),
        dict(title="Model details", cell_id="w3-model-banner", before="# From particle motion to continuous equations"),
        dict(title="Analysis", cell_id="w3-analysis-banner", before="# Return to the Gray–Scott simulation"),
        dict(title="Scope and connections", cell_id="w3-scope-banner", before="# The modelling problem underneath the model"),
    ],
)

update_week(
    4,
    [
        dict(title="Real-world motivation", cell_id="w4-slides-motivation", before="# A machine with a state", destination="slides-only", anchor_tag="slides-only"),
        dict(title="Model details", cell_id="w4-slides-model", before="# Wolfram's elementary cellular automata", destination="slides-only", anchor_tag="slides-only"),
        dict(title="Analysis", cell_id="w4-slides-analysis", before="# Wolfram's four qualitative classes", destination="slides-only", anchor_tag="slides-only"),
        dict(title="Scope and connections", cell_id="w4-slides-scope", before="# Cellular automata in empirical systems", destination="slides-only", anchor_tag="slides-only"),
        dict(title="Real-world motivation", cell_id="w4-reader-motivation", before="# Cellular automata", destination="reader-only", anchor_tag="reader-only"),
        dict(title="Model details", cell_id="w4-reader-model", before="# Wolfram's elementary cellular automata", destination="reader-only", anchor_tag="reader-only"),
        dict(title="Analysis", cell_id="w4-reader-analysis", before="# Analysing cellular automata", destination="reader-only", anchor_tag="reader-only"),
        dict(title="Scope and connections", cell_id="w4-reader-scope", before="# Cellular automata in empirical systems", destination="reader-only", anchor_tag="reader-only"),
    ],
    moves=[
        dict(start_title="# Cellular automata in empirical systems", end_title="# Wolfram's four qualitative classes", before_title="# Beyond binary cells · Lenia", required_tag="slides-only"),
        dict(start_title="# Cellular automata in empirical systems", end_title="# Analysing cellular automata", before_title="# What cellular automata teach us", required_tag="reader-only"),
    ],
)

update_week(
    5,
    [
        dict(title="Real-world motivation", cell_id="w5-motivation-banner", before="# Collective behaviour without a conductor"),
        dict(title="Explorable", cell_id="w5-explorable-banner", before="## B · Statistical physics: Vicsek et al. (1995)"),
        dict(title="Model details", cell_id="w5-model-banner", before="# What goes into an agent-based model?"),
        dict(title="Analysis", cell_id="w5-analysis-banner", before="# Qualitative analysis"),
        dict(title="Scope and connections", cell_id="w5-scope-banner", before="## The Vicsek model became a family"),
    ],
)

# Week 6 was reorganised separately because its slide and Reader cells are
# deliberately parallel rather than shared.

update_week(
    7,
    [
        dict(title="Real-world motivation", cell_id="w7-slides-motivation", before="# What makes a system intelligent?", destination="slides-only", anchor_tag="slides-only"),
        dict(title="Model details", cell_id="w7-slides-model", before="# Supporting model · The perceptron", destination="slides-only", anchor_tag="slides-only"),
        dict(title="Analysis", cell_id="w7-slides-analysis", before="# The common mechanism", destination="slides-only", anchor_tag="slides-only"),
        dict(title="Scope and connections", cell_id="w7-slides-scope", before="# What should we ask of an intelligent system?", destination="slides-only", anchor_tag="slides-only"),
        dict(title="Real-world motivation", cell_id="w7-reader-motivation", before="## Starting point", destination="reader-only", anchor_tag="reader-only"),
        dict(title="Model details", cell_id="w7-reader-model", before="# Artificial intelligence (AI)", destination="reader-only", anchor_tag="reader-only"),
        dict(title="Analysis", cell_id="w7-reader-analysis", before="# Harnessing collective intelligence", destination="reader-only", anchor_tag="reader-only"),
        dict(title="Scope and connections", cell_id="w7-reader-scope", before="# Controlling collective intelligence", destination="reader-only", anchor_tag="reader-only"),
    ],
)

update_week(
    8,
    [
        dict(title="Real-world motivation", cell_id="w8-motivation-banner", before="## Starting point"),
        dict(title="Explorable", cell_id="w8-explorable-banner", before="## Percolation"),
        dict(title="Model details", cell_id="w8-model-banner", before="# Self-organised criticality"),
        dict(title="Analysis", cell_id="w8-analysis-banner", before="# Analytics"),
        dict(title="Scope and connections", cell_id="w8-scope-banner", before="# Conclusions"),
    ],
)

update_week(
    9,
    [
        dict(title="Real-world motivation", cell_id="w9-motivation-banner", before="# WHAT exactly is 'complexity'?"),
        dict(title="Model details", cell_id="w9-model-banner", before="# A brief origin story"),
        dict(title="Analysis", cell_id="w9-analysis-banner", before="# Putting it all together"),
        dict(title="Scope and connections", cell_id="w9-scope-banner", before="# Applications"),
    ],
)

update_week(
    10,
    [
        dict(title="Real-world motivation", cell_id="w10-motivation-banner", before="# Games"),
        dict(title="Model details", cell_id="w10-model-banner", before="# Prisoner's dilemma"),
        dict(title="Analysis", cell_id="w10-analysis-banner", before="## What should each player choose?"),
        dict(title="Scope and connections", cell_id="w10-scope-banner", before="# Reality"),
    ],
)
