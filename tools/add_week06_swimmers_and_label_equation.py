#!/usr/bin/env python3
import json
from pathlib import Path

path = Path("notebooks/week06/L_Synchronisation.ipynb")
nb = json.loads(path.read_text())
cells = nb["cells"]

def get(cid): return next(c for c in cells if c.get("id") == cid)

if not any(c.get("id") == "w6-choreographed-swimmers" for c in cells):
    slide = {
        "cell_type": "markdown",
        "id": "w6-choreographed-swimmers",
        "metadata": {"slideshow": {"slide_type": "slide"}, "tags": ["slides-only"]},
        "source": '''## Choreographed synchronisation

<iframe src="https://www.youtube.com/embed/qsRmVtvbrAE" title="Synchronised swimmers" style="display:block;width:82%;height:455px;border:0;margin:0 auto" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>

The swimmers coordinate through rehearsal, shared timing and a planned sequence. The synchronisation studied later arises from interacting systems that retain their own dynamics.
'''.splitlines(keepends=True),
    }
    cells.insert(cells.index(get("w6-hook")) + 1, slide)

cell = get("w6-one")
text = "".join(cell["source"])
text = text.replace(
    "\\theta(t)=\\theta_0+\\omega t \\pmod{2\\pi}\n$$",
    "\\theta(t)=\\theta_0+\\omega t \\pmod{2\\pi}. \\tag{1}\n$$",
)
start = "\nEquation 1 specifies uniform phase advance;"
if start in text:
    text = text[:text.index(start)].rstrip() + "\n"
cell["source"] = text.splitlines(keepends=True)

path.write_text(json.dumps(nb, ensure_ascii=False, indent=1) + "\n")
