"""Apply the final Week 6 coherence, heterogeneity and duplication repairs."""

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
reader_path = ROOT / "notebooks/week06/L_Synchronisation.ipynb"
workshop_path = ROOT / "notebooks/week06/WS_Synchronisation.ipynb"


def set_source(cell, text):
    cell["source"] = text.splitlines(keepends=True)


reader = json.loads(reader_path.read_text())

# Remove duplicate slide content from the Reader build.
for cell in reader["cells"]:
    if cell.get("id") == "sync-types-slide":
        cell.setdefault("metadata", {})["tags"] = ["slides-only"]

    if cell.get("id") == "order-parameter":
        text = "".join(cell["source"])
        text = text.split('<div class="ladder-marker"', 1)[0].rstrip()
        text += '''

<div class="ladder-marker"><img src="images/ladder_marker.svg" alt="Ladder of abstraction"><span><strong>Up the ladder:</strong> replace the full phase configuration by the collective variables <i>ψ</i>(<i>t</i>) and <i>r</i>(<i>t</i>).</span></div>
'''
        set_source(cell, text)

    if cell.get("id") in {"w6-sweep", "w6-mean-field-return"}:
        text = "".join(cell["source"])
        text = text.split('<div class="ladder-marker"', 1)[0].rstrip()
        if cell.get("id") == "w6-sweep":
            marker = '<div class="ladder-marker"><img src="images/ladder_marker.svg" alt="Ladder of abstraction"><span><strong>Up the ladder twice:</strong> first replace each run by its long-time coherence <i>r</i><sub>∞</sub>; then compare those summaries across <i>K</i>, <i>N</i> and repeated populations.</span></div>'
        else:
            marker = '<div class="ladder-marker"><img src="images/ladder_marker.svg" alt="Ladder of abstraction"><span><strong>Up the ladder:</strong> replace a finite sample by a continuum frequency distribution.</span></div>'
        set_source(cell, text + "\n\n" + marker + "\n")

    if cell.get("id") == "mean-field":
        text = "".join(cell["source"])
        text = text.replace(
            'population density $g(\\omega)$.',
            'population density <i>g</i>(<i>ω</i>).',
        )
        set_source(cell, text)

    if cell.get("id") == "w6-spatial-fireflies-reader":
        text = "".join(cell["source"])
        marker = "\n### Pulse coupling\n"
        if marker in text:
            text = text.split(marker, 1)[0].rstrip() + "\n\n" + marker + text.split(marker, 1)[1].split(marker, 1)[0].strip() + "\n"
        set_source(cell, text)

    if cell.get("id") == "w6-second-order-kuramoto-reader":
        text = "".join(cell["source"])
        old = ('Two uses of “order” must be kept separate. A **second-order equation** contains a second time derivative. '
               'A **first-order-like transition** is a discontinuous macroscopic change. One does not imply the other, '
               'although inertia can change the transition observed in a Kuramoto population.')
        new = '''Three uses of “order” appear here, and they are separate ideas:

- **Equation order:** a second-order equation contains a second time derivative.
- **Transition order:** a first-order-like transition is a discontinuous macroscopic change.
- **Collective order:** the order parameter $r$ measures group-level coherence.

A second-order equation does not imply a first-order transition. Inertia can, however, alter the collective transition observed in a Kuramoto population.'''
        text = text.replace(old, new)
        set_source(cell, text)

# Explain what the comparison figure represents in the Reader itself.
for cell in reader["cells"]:
    if cell.get("id") == "w6-types-of-synchronisation-reader":
        text = "".join(cell["source"])
        prefix = r'''### Several forms of synchronisation

The circle below is **phase space**, not physical space. A point records the oscillator state $\theta_i$; moving around the circle means advancing through an oscillation cycle. The adjoining traces show an observable signal $y_i(t)=\cos\theta_i(t)$. Together they distinguish several kinds of coordination that a single final snapshot can conceal.

'''
        body = text.split("### Several forms of synchronisation", 1)[-1].lstrip()
        set_source(cell, prefix + body)

reader_path.write_text(json.dumps(reader, indent=1, ensure_ascii=False) + "\n")


workshop = json.loads(workshop_path.read_text())
for cell in workshop["cells"]:
    if cell.get("cell_type") != "code":
        continue
    text = "".join(cell.get("source", []))
    text = text.replace("rng.normal(0.0, 0.45, n)", "rng.normal(3.0, 0.45, n)")
    text = text.replace("rng.normal(0.0, 1.25, n)", "rng.normal(3.0, 0.85, n)")
    text = text.replace("1.1 * groups + rng.normal(0.0, 0.22, n)", "3.0 + 0.7 * groups + rng.normal(0.0, 0.22, n)")
    text = text.replace("rng.normal(0, frequency_sd, n)", "rng.normal(3.0, frequency_sd, n)")
    text = text.replace("frequencies -= frequencies.mean()\n    return phases, frequencies", "frequencies += 3.0 - frequencies.mean()\n    return phases, frequencies")
    text = text.replace("coupling: float = 2.4", "coupling: float = 3.2")
    text = text.replace("dt: float = 0.05", "dt: float = 0.02")
    cell["source"] = text.splitlines(keepends=True)

# Add a concise laboratory-frame note before the first heterogeneous experiment.
for cell in workshop["cells"]:
    if cell.get("cell_type") == "markdown" and "heterogene" in "".join(cell.get("source", [])).lower():
        text = "".join(cell["source"])
        if "laboratory frame" not in text:
            text += ("\n\nHere natural frequencies are centred at $3$ radians per unit time, so every oscillator advances "
                     "in the same direction in the laboratory frame. Subtracting the population mean would give an "
                     "equivalent co-rotating description centred at zero, but negative values there are relative drift, "
                     "not literal backwards motion through space.\n")
            set_source(cell, text)
        break

workshop_path.write_text(json.dumps(workshop, indent=1, ensure_ascii=False) + "\n")
