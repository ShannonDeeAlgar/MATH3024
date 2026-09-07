"""Restore the Garden of Eden slide immediately after reversibility."""

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "notebooks/week04/L_Cellular_automata.ipynb"
CELL_ID = "w4-garden-of-eden-slide"

SOURCE = """## Garden of Eden configurations

<div class="two-panel media-text compact-panels">
<div class="media-panel">
<img src="images/Garden_of_Eden_pattern.png" alt="Garden of Eden configuration in Conway's Game of Life" style="width:100%;max-height:540px;object-fit:contain;">
</div>
<div class="text-panel">
<p>A <strong>Garden of Eden</strong> has no predecessor:</p>
<p>$$\nexists c'\text{ such that }F(c')=c.$$</p>
<p>It is a possible configuration that the update rule can never produce.</p>
<p>The global map is therefore not <strong>onto</strong> (surjective), so it cannot be reversible.</p>
<p>Game of Life has Gardens of Eden as well as distinct histories that merge.</p>
</div>
</div>

<p class="media-credit">Example found by Roger Banks (1971).</p>
"""

notebook = json.loads(PATH.read_text())
notebook["cells"] = [cell for cell in notebook["cells"] if cell.get("id") != CELL_ID]

target = next(
    index for index, cell in enumerate(notebook["cells"])
    if "## Shift versus Rule 254" in "".join(cell.get("source", []))
)

cell = {
    "cell_type": "markdown",
    "id": CELL_ID,
    "metadata": {
        "tags": ["slides-only"],
        "slideshow": {"slide_type": "subslide"},
    },
    "source": SOURCE.splitlines(keepends=True),
}
notebook["cells"].insert(target + 1, cell)
PATH.write_text(json.dumps(notebook, indent=1, ensure_ascii=False) + "\n")
print(f"Inserted after cell {target}: {PATH.relative_to(ROOT)}")
