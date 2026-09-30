"""Remove Week 10 evolution slides and label Reader extensions."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK = ROOT / "notebooks/week10/L_Game_theory.ipynb"
MANIFEST = ROOT / "tools/equation_consistency.json"


OPTIONAL_FLAG = '<div class="optional-reader-flag"><strong>Optional extension</strong> These population-update examples extend the fixed-strategy tournament; they are not part of the assessed core.</div>\n\n'


def main() -> None:
    notebook = json.loads(NOTEBOOK.read_text())
    cells = {cell.get("id"): cell for cell in notebook["cells"]}

    # Slides devoted to evolutionary updating are not part of the lecture deck.
    remove_from_slides = {
        "w10-evolution-bridge-slide",
        "w10-prisoners-kaleidoscope-slide",
        "w10-tournament-evolution-slide",
        "w10-payoff-fitness-link-slide",
        "w10-selection-inheritance-mutation-slide",
        "w10-axelrod-slide",
        "w10-spatial-evolution-notation-slide",
    }
    for cell_id in remove_from_slides:
        cell = cells[cell_id]
        tags = set(cell.setdefault("metadata", {}).get("tags", []))
        tags.add("remove-cell")
        cell["metadata"]["tags"] = sorted(tags)

    # Keep the moving-population material in the Reader but not in slides.
    for cell_id in ("w10-rps-population", "w10-rps-arena"):
        cell = cells[cell_id]
        tags = set(cell.setdefault("metadata", {}).get("tags", []))
        tags.add("reader-only")
        cell["metadata"]["tags"] = sorted(tags)

    # Make the Reader status explicit for the evolutionary extensions.
    bridge = cells["w10-evolution-bridge"]
    bridge_source = "".join(bridge["source"])
    marker = '<div class="optional-reader-flag"><strong>Optional extension</strong> The population-update examples below extend the fixed-strategy tournament; they are not part of the assessed core.</div>\n\n'
    if marker not in bridge_source:
        bridge_source = bridge_source.rstrip() + "\n\n" + marker
    bridge["source"] = bridge_source.splitlines(keepends=True)

    for cell_id in ("a7e5e594", "w10-rps-population", "w10-evolutionary-ipd"):
        cell = cells[cell_id]
        source = "".join(cell["source"])
        if OPTIONAL_FLAG not in source:
            lines = source.splitlines(keepends=True)
            insert_at = 1 if lines and lines[0].startswith("#") else 0
            lines[insert_at:insert_at] = [OPTIONAL_FLAG]
            cell["source"] = lines

    NOTEBOOK.write_text(json.dumps(notebook, indent=1, ensure_ascii=False) + "\n")

    manifest = json.loads(MANIFEST.read_text())
    entry = manifest["notebooks"]["notebooks/week10/L_Game_theory.ipynb"]
    for cell_id in remove_from_slides:
        entry["math_signatures"].pop(cell_id, None)
    entry["displays"] = [link for link in entry["displays"] if link.get("slide") not in remove_from_slides]
    MANIFEST.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
