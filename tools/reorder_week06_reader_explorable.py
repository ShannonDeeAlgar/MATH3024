#!/usr/bin/env python3
import json
from pathlib import Path

path = Path("notebooks/week06/L_Synchronisation.ipynb")
nb = json.loads(path.read_text())
cells = nb["cells"]

def get(cid):
    return next(c for c in cells if c.get("id") == cid)

def move_after(cid, anchor):
    cell = get(cid)
    cells.remove(cell)
    cells.insert(cells.index(get(anchor)) + 1, cell)

# Keep the contrast, but avoid turning it into a second definition of
# synchronisation or self-organisation.
contrast = get("w6-coordination-contrast-reader")
text = "".join(contrast["source"])
text = text.replace("### Not all synchrony is self-organised", "### Choreographed coordination")
contrast["source"] = text.splitlines(keepends=True)

# The modelling pause now precedes the explorable in both delivery formats.
move_after("w6-8bb38f86c6", "firefly-model")
move_after("kuramoto-video-reader", "w6-8bb38f86c6")

path.write_text(json.dumps(nb, ensure_ascii=False, indent=1) + "\n")
