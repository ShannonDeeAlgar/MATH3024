#!/usr/bin/env python3
"""
Strips slides-only/presenter-notes cells from the lecture notebooks IN PLACE.

mystmd's remove-cell tag handling isn't actually enforced by the current
book-theme site template (the JS ships the tag names but not the logic that
acts on them), so slides-only and presenter-notes cells leak straight into
the published Reader. This modifies notebooks/*.ipynb directly before
`jupyter-book build` runs, so myst.yml's toc paths don't need to change
(keeping page URLs stable).

In CI this runs in a throwaway checkout, so no restoration is needed. For
local use, run via build_reader.sh instead of calling this directly. The
wrapper creates a temporary project copy and runs this script there, leaving
the working notebooks untouched.
"""
import json
from pathlib import Path

ROOT = Path(__file__).parent
SRC = ROOT / "notebooks"

TAGS_TO_STRIP = {"slides-only", "presenter-notes", "archive-only"}


def filter_notebook(path: Path) -> int:
    nb = json.loads(path.read_text())
    kept = []
    removed = 0
    for cell in nb["cells"]:
        tags = set(cell.get("metadata", {}).get("tags", []))
        if tags & TAGS_TO_STRIP:
            removed += 1
            continue
        kept.append(cell)
    if removed:
        nb["cells"] = kept
        path.write_text(json.dumps(nb, indent=1) + "\n")
    return removed


def main():
    total_removed = 0
    for path in sorted(SRC.rglob("*.ipynb")):
        if ".ipynb_checkpoints" in path.parts:
            continue
        total_removed += filter_notebook(path)

    print(f"Removed {total_removed} slides-only/presenter-notes cells from notebooks/ (in place)")


if __name__ == "__main__":
    main()
