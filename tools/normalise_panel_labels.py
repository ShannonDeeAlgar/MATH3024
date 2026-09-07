#!/usr/bin/env python3
"""Replace structural HTML headings used only as labels inside content panels."""

from pathlib import Path
import re

import nbformat


ROOT = Path(__file__).resolve().parents[1]
LECTURES = sorted((ROOT / "notebooks").glob("week*/L_*.ipynb"))
HEADING = re.compile(r"<h3>(.*?)</h3>", flags=re.DOTALL)


for path in LECTURES:
    nb = nbformat.read(path, as_version=4)
    changed = 0
    for cell in nb.cells:
        if cell.cell_type != "markdown" or '<div class="text-panel"' not in cell.source:
            continue
        revised, count = HEADING.subn(r"<p><strong>\1</strong></p>", cell.source)
        if count:
            cell.source = revised
            changed += count
    if changed:
        nbformat.write(nb, path)
        print(f"{path.relative_to(ROOT)}: replaced {changed} panel heading(s)")
