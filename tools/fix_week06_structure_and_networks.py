"""Apply the final Week 6 hierarchy, notation and network clarifications."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK = ROOT / "notebooks/week06/L_Synchronisation.ipynb"


def lines(text: str) -> list[str]:
    return text.splitlines(keepends=True)


nb = json.loads(NOTEBOOK.read_text())
cells = nb["cells"]
by_id = {cell.get("id"): cell for cell in cells}

# A tab had been introduced where the LaTeX command ``\theta`` belonged.
for cell in cells:
    source = "".join(cell.get("source", []))
    source = source.replace("$\theta_2-\theta_1$", "$\\theta_2-\\theta_1$")
    source = source.replace("$\\sin(\theta_2-\theta_1)$", "$\\sin(\\theta_2-\\theta_1)$")
    cell["source"] = lines(source)

# Keep the combined figure and explanation, but not a redundant heading.
cell = by_id["order-parameter"]
source = "".join(cell["source"])
source = source.replace("### Put the views together\n\n", "")
cell["source"] = lines(source)

slide_network = r'''## Networks: fixed, changing or adaptive

<div class="analysis-perspectives three">
<div><strong>Dynamics on a network</strong><p>Node states evolve on a fixed graph. Network Kuramoto models and epidemics on a fixed contact graph are examples.</p></div>
<div><strong>Dynamics of a network</strong><p>The graph itself grows or changes. Preferential attachment in the Barabási–Albert model is a standard example.</p></div>
<div><strong>Adaptive network</strong><p>Node states and edges affect one another. Adaptive Kuramoto and behaviour-changing epidemic models have this form.</p></div>
</div>

Standard Kuramoto is all-to-all. A fixed-network Kuramoto model is dynamics **on** a network; rewiring based on phase similarity makes it adaptive.
'''
by_id["w6-network-variant-slide"]["source"] = lines(slide_network)

reader_network = r'''### Networks: fixed, changing or adaptive

Mechanical, electrical, chemical and informational coupling describe different physical systems. Coupling may act one way or both ways, locally or globally, continuously or in pulses, immediately or after a delay. These are properties of the system being represented. The modelling choice is how much of that structure to retain.

For a network rather than all-to-all coupling, let $A_{ij}$ record whether oscillator $j$ influences oscillator $i$, and let $w_{ij}$ give the strength of that influence. One normalised form is

$$
\dot{\theta}_i
=\omega_i
+\frac{K}{s_i}\sum_{j=1}^{N}A_{ij}w_{ij}\sin(\theta_j-\theta_i),
\qquad
s_i=\sum_{j=1}^{N}A_{ij}w_{ij}.
$$

The complete, equally weighted graph recovers the standard Kuramoto interaction. Sparse, local or modular graphs change who can coordinate with whom. Keep $g(\omega)$ and the coupling law fixed when comparing them.

- **Dynamics on a network:** node states evolve while the graph remains fixed. A Kuramoto population on a fixed power-grid or neural network has this form. A classic non-oscillator example is an epidemic spreading over a fixed contact network.
- **Dynamics of a network:** the nodes or edges are the evolving object. The Barabási–Albert model is the classic example: a graph grows as new nodes attach preferentially to already well-connected nodes. This is not part of standard Kuramoto.
- **Adaptive or co-evolving network:** node states alter the graph and the changed graph alters later node dynamics. In an adaptive Kuramoto model, phase similarity might strengthen or create edges. In an adaptive epidemic model, infection changes behaviour, behaviour changes contacts and the new contacts change transmission.

The fixed-network equation above is dynamics **on** a network. The rewiring investigation in the Workshop becomes adaptive because phase similarity changes the edges and those new edges alter subsequent phase updates.
'''
by_id["w6-network-variant-reader"]["source"] = lines(reader_network)

# Remove the duplicated representation section, retaining a clean banner for the
# subsequent return to spatial and pulse-coupled systems.
by_id["scope"]["source"] = lines("# Return to the real systems\n")

# Use a new asset name so a running preview cannot reuse the pre-fix SVG.
for cell in cells:
    source = "".join(cell.get("source", []))
    source = source.replace(
        "images/kuramoto_realised_frequency.svg",
        "images/kuramoto_realised_frequency_drifter.svg",
    )
    cell["source"] = lines(source)

NOTEBOOK.write_text(json.dumps(nb, ensure_ascii=False, indent=1) + "\n")
