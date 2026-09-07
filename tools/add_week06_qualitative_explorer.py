"""Install the focused Week 6 qualitative Kuramoto explorer."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "notebooks/week06/L_Synchronisation.ipynb"


def lines(text: str) -> list[str]:
    return [line + "\n" for line in text.rstrip().splitlines()]


nb = json.loads(PATH.read_text())
cells = nb["cells"]

slide = next(c for c in cells if c.get("id") == "w6-watch")
slide["source"] = lines(r'''# Qualitative analysis

<iframe src="images/kuramoto_qualitative_explorer.html" title="Interactive Kuramoto phase and flashing-node views" style="display:block;width:100%;height:455px;border:0;margin:0 auto"></iframe>

Use the time control to inspect a transient. Changing $K$ restarts the same sampled population, so the effect of coupling is not mixed with a new random initial condition.''')

reader = next(c for c in cells if c.get("id") == "kuramoto-video")
reader["source"] = lines(r'''## Qualitative analysis

The earlier Complexity Explorable is the better place to roam through a broad range of behaviours. The smaller tool below has a different purpose: it exposes one reproducible Kuramoto simulation and shows the same phases in two representations.

<iframe src="images/kuramoto_qualitative_explorer.html" title="Interactive Kuramoto phase and flashing-node views" style="display:block;width:96%;max-width:1120px;height:505px;border:0;margin:1rem auto"></iframe>

The left-hand circle is phase space: position around it records progress through an oscillation cycle, not physical location. The right-hand nodes remain fixed and flash as their phases pass zero. Use the time control to inspect the transient. Changing $K$ restarts the same sampled frequencies and initial phases, allowing a paired comparison of coupling strength.

This is not intended to reproduce every control or visual refinement in the Complexity Explorable. It makes the model-to-display connection inspectable and provides a scaffold that students can alter in the workshop.''')

PATH.write_text(json.dumps(nb, indent=1, ensure_ascii=False) + "\n")
print(f"Updated {PATH.relative_to(ROOT)}")
