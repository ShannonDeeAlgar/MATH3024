"""Apply the 25 August review corrections to the Week 6 Reader and slides."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK = ROOT / "notebooks/week06/L_Synchronisation.ipynb"


def set_source(cell: dict, text: str) -> None:
    cell["source"] = text.rstrip().splitlines(keepends=True)
    if cell["source"]:
        cell["source"][-1] += "\n"


nb = json.loads(NOTEBOOK.read_text())
cells = nb["cells"]
by_id = {cell.get("id"): cell for cell in cells}

# The contrast is conceptual rather than a label for one particular activity.
for cell_id in ("w6-choreographed-swimmers", "w6-coordination-contrast-reader"):
    cell = by_id[cell_id]
    source = "".join(cell["source"])
    source = source.replace("## Choreographed synchronisation", "## Not all synchrony is complex")
    source = source.replace("### Choreographed coordination", "## Not all synchrony is complex")
    set_source(cell, source)

slide_uncoupled = r"""## Two oscillators without coupling

<div class="two-panel wide-left compact-panels">
<div class="image-panel"><img src="images/two_phase_oscillators.svg" alt="Two independent phase oscillators on the unit circle" style="max-height:390px"></div>
<div class="text-panel">

| Symbol | Meaning |
|---|---|
| $\theta_i$ | phase: position within the cycle |
| $\omega_i$ | natural frequency: isolated rate of advance |
| $\phi=\theta_1-\theta_2$ | phase difference |

$$
\dot{\theta}_1=\omega_1, \qquad \dot{\theta}_2=\omega_2,
$$

$$
\dot{\phi}=\omega_1-\omega_2.
$$

The separation drifts unless the natural frequencies match.
</div>
</div>"""
set_source(by_id["w6-uncoupled"], slide_uncoupled)

reader_uncoupled = r"""## Two uncoupled oscillators

<div class="two-panel wide-left">
<div class="image-panel"><img src="images/two_phase_oscillators.svg" alt="Two independent phase oscillators on the unit circle" style="max-height:390px"></div>
<div class="text-panel">

| Symbol | Meaning |
|---|---|
| $\theta_i$ | phase: position within the cycle |
| $\omega_i$ | natural frequency: isolated rate of advance |
| $\phi=\theta_1-\theta_2$ | phase difference |

Without coupling, each phase follows its own internal dynamics:

$$
\dot{\theta}_1=\omega_1, \qquad \dot{\theta}_2=\omega_2,
$$

and therefore

$$
\dot{\phi}=\omega_1-\omega_2.
$$

Unless the natural frequencies match, the relative phase drifts.
</div>
</div>"""
set_source(by_id["uncoupled"], reader_uncoupled)

# The diagram now contains geometry only; its interpretation belongs in the
# normal slide content, using the same symbol-definition style as above.
order_slide = r"""## Measure collective coherence

$$
r(t)e^{\mathrm{i}\psi(t)}
=\dfrac{1}{N}\sum_{j=1}^{N}e^{\mathrm{i}\theta_j(t)}.
$$

<div class="two-panel equal-panels compact-panels">
<div class="text-panel">

| Symbol | Meaning |
|---|---|
| $\psi$ | circular mean phase |
| $r\approx0$ | phases cancel around the circle |
| $r\approx1$ | phases are tightly aligned |

<div class="ladder-marker"><img src="images/ladder_marker.svg" alt="Ladder of abstraction"><span><strong>Up the ladder:</strong> compress the phase configuration to one coherence measure.</span></div>
</div>
<div class="image-panel"><img src="images/kuramoto_order_parameter_geometry.svg" alt="Complex phase vectors and their average" style="max-height:325px"></div>
</div>"""
set_source(by_id["w6-order"], order_slide)

# Show the modelling questions before revealing the standard Kuramoto choices.
def move_before(cell_id: str, target_id: str) -> None:
    cell = next(c for c in cells if c.get("id") == cell_id)
    cells.remove(cell)
    target_index = next(i for i, c in enumerate(cells) if c.get("id") == target_id)
    cells.insert(target_index, cell)


move_before("w6-specify", "w6-assumptions")
move_before("firefly-model", "kuramoto-equation")

# The plotted relative phase is now shown modulo one full turn.
for cell_id in ("w6-beats", "reader-beats"):
    cell = by_id[cell_id]
    source = "".join(cell["source"])
    source = source.replace(
        "the unwrapped phase difference continues to drift. Phase is defined modulo $2\\pi$; wrapping the same curve would produce a sawtooth rather than a constant phase difference.",
        "the phase difference repeatedly wraps through $2\\pi$. The sawtooth records continuing drift around the phase circle, not phase locking.",
    )
    source = source.replace(
        "The phase-difference panel is deliberately unwrapped: its steady drift makes the absence of phase locking easy to see. Because phase is defined modulo $2\\pi$, wrapping it would give a sawtooth carrying the same circular information.",
        "The phase difference is wrapped modulo $2\\pi$. Its repeating sawtooth shows that one oscillator continues to lap the other rather than locking at a constant separation.",
    )
    set_source(cell, source)

NOTEBOOK.write_text(json.dumps(nb, indent=1, ensure_ascii=False) + "\n")
print(f"Updated {NOTEBOOK.relative_to(ROOT)}")
