"""Finish the Week 6 qualitative/quantitative analysis hierarchy."""

from __future__ import annotations

import json
from pathlib import Path


PATH = Path(__file__).resolve().parents[1] / "notebooks/week06/L_Synchronisation.ipynb"


def text(cell: dict) -> str:
    return "".join(cell.get("source", []))


def set_text(cell: dict, source: str) -> None:
    cell["source"] = source.splitlines(keepends=True)


def is_tagged(cell: dict, tag: str) -> bool:
    return tag in cell.get("metadata", {}).get("tags", [])


nb = json.loads(PATH.read_text())
cells = nb["cells"]

# Slides: the animation is qualitative analysis, not part of the explorable.
watch_i = next(
    i
    for i, c in enumerate(cells)
    if text(c).startswith("## Watch phases organise\n") and is_tagged(c, "slides-only")
)
watch = cells.pop(watch_i)
set_text(
    watch,
    text(watch).replace(
        "## Watch phases organise\n", "## Qualitative analysis · watch phases organise\n", 1
    ),
)
analysis_i = next(i for i, c in enumerate(cells) if text(c).startswith("# Analysis\n"))
cells.insert(analysis_i + 1, watch)

# Reader: split the snapshots from the embedded explorable, then place both
# qualitative views after the Analysis banner.
combined_i = next(
    i
    for i, c in enumerate(cells)
    if is_tagged(c, "reader-only")
    and "<img src=\"images/Coherence_evolution.png\"" in text(c)
    and "## Explore the Kuramoto model" in text(c)
)
combined = cells.pop(combined_i)
before, after = text(combined).split("## Explore the Kuramoto model\n", 1)
snapshot_source = before.replace(
    "## Watch phases organise\n", "### From phases to coherence\n", 1
).strip() + "\n"
explore_source = "## Explore the Kuramoto model\n" + after

snapshot = json.loads(json.dumps(combined))
explore = json.loads(json.dumps(combined))
set_text(snapshot, snapshot_source)
set_text(explore, explore_source)

explorable_banner_i = next(
    i
    for i, c in enumerate(cells)
    if text(c).startswith("# Explorable\n") and is_tagged(c, "reader-only")
)
cells.insert(explorable_banner_i + 1, explore)

reader_watch_i = next(
    i
    for i, c in enumerate(cells)
    if text(c).startswith("## Watch phases organise\n") and is_tagged(c, "reader-only")
)
reader_watch = cells.pop(reader_watch_i)
set_text(
    reader_watch,
    text(reader_watch).replace(
        "## Watch phases organise\n", "## Qualitative analysis · watch phases organise\n", 1
    ),
)

reader_analysis_i = next(
    i
    for i, c in enumerate(cells)
    if text(c).startswith("# Analysis\n") and is_tagged(c, "reader-only")
)
cells.insert(reader_analysis_i + 1, reader_watch)
cells.insert(reader_analysis_i + 2, snapshot)

PATH.write_text(json.dumps(nb, indent=1, ensure_ascii=False) + "\n")
print(f"Updated {PATH}")
