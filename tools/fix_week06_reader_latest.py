"""Apply the final Week 6 reader structure and wording corrections."""

from pathlib import Path
import json


ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "notebooks/week06/L_Synchronisation.ipynb"


def lines(text):
    return text.strip("\n").splitlines(keepends=True)


with PATH.open() as handle:
    notebook = json.load(handle)

cells = notebook["cells"]
by_id = {cell.get("id"): cell for cell in cells}


# Put the phase-space clarification beside the first phase-circle diagram.
uncoupled = by_id["uncoupled"]
text = "".join(uncoupled["source"])
anchor = '<div class="two-panel wide-left">'
clarification = (
    "The circle in the diagram is **phase space**, not a map of physical position. "
    "A point moving around it advances through one oscillation cycle.\n\n"
)
if clarification not in text:
    text = text.replace(anchor, clarification + anchor)
uncoupled["source"] = lines(text)


# Keep the taxonomy concise and move empirical detection to the return to real systems.
types = by_id["w6-types-of-synchronisation-reader"]
text = "".join(types["source"])
phase_paragraph = (
    "The circle below is **phase space**, not physical space. A point records the oscillator state "
    "$\\theta_i$; moving around the circle means advancing through an oscillation cycle. The adjoining "
    "traces show an observable signal $y_i(t)=\\cos\\theta_i(t)$. Together they distinguish several "
    "kinds of coordination that a single final snapshot can conceal.\n\n"
)
text = text.replace(phase_paragraph, "")
detection_heading = "#### Detecting synchronisation from measured time series"
if detection_heading in text:
    text = text.split(detection_heading, 1)[0].rstrip() + "\n"
types["source"] = lines(text)


# One coherence section: its opening sentence now introduces the calculation.
order = by_id["order-parameter"]
order_text = "".join(order["source"])
opening = (
    "The animation keeps the individual phases visible while the order parameter $r$ records their "
    "collective alignment. We now replace the full phase configuration by that collective summary.\n\n"
)
if opening not in order_text:
    order_text = order_text.replace(
        "Represent oscillator $j$ by the unit complex number\n",
        opening + "Represent oscillator $j$ by the unit complex number\n",
    )
order["source"] = lines(order_text)
intro = by_id.get("w6-3465fc0be5")
if intro in cells:
    cells.remove(intro)


# The slides had repeated the same coherence equation on consecutive slides.
slide_order = by_id["w6-order"]
slide_equation = by_id.get("w6-order-parameter-equation")
slide_text = "".join(slide_order["source"])
vicsek_link = (
    "\nThis is the phase-oscillator counterpart of the polarisation order parameter used "
    "for Vicsek agents: both take the magnitude of an average of unit direction vectors.\n"
)
if "counterpart of the polarisation" not in slide_text:
    slide_text = slide_text.rstrip() + vicsek_link
slide_order["source"] = lines(slide_text)
if slide_equation in cells:
    cells.remove(slide_equation)


# Restore the non-all-to-all model explicitly, including optional edge weights.
network = by_id["network-specification"]
text = "".join(network["source"])
network_extension = r'''

For a network rather than all-to-all coupling, let $A_{ij}$ record whether oscillator $j$ influences oscillator $i$, and let $w_{ij}$ give the strength of that influence. One normalised form is

$$
\dot{\theta}_i
=\omega_i
+\frac{K}{s_i}\sum_{j=1}^{N}A_{ij}w_{ij}\sin(\theta_j-\theta_i),
\qquad
s_i=\sum_{j=1}^{N}A_{ij}w_{ij}.
$$

The complete, equally weighted network recovers the standard Kuramoto interaction. Sparse, local or modular choices change who can coordinate with whom.
'''
if "s_i=\\sum" not in text:
    text = text.rstrip() + network_extension
network["source"] = lines(text)


# Put the non-assessable note at the first mention of the inertial variant.
second = by_id["w6-second-order-kuramoto-reader"]
text = "".join(second["source"])
note = (
    "This is a reader extension rather than assessable material. See [Acebrón et al. "
    "(2005)](https://doi.org/10.1103/RevModPhys.77.137) for the wider Kuramoto family and "
    "[Choi, Ha and Yun (2011)](https://doi.org/10.1016/j.physd.2010.08.004) for finite inertia."
)
text = text.replace("\n\n" + note + "\n", "\n")
anchor = "The canonical Kuramoto equation is first order in time:"
text = text.replace(anchor, note + "\n\n" + anchor)
second["source"] = lines(text)


# Empirical detection belongs with the return from the idealised model to observations.
spatial = by_id["w6-spatial-fireflies-reader"]
text = "".join(spatial["source"])
detection = r'''

### Detecting synchronisation in measured data

In an experiment we may not observe phase directly. We instead record signals such as light intensity, displacement, voltage, breathing or heartbeat timing. Phase can be estimated from repeated events or reconstructed from a smoothly oscillating signal. We can then ask whether phase differences remain concentrated, whether average frequencies agree, or whether an $n:m$ relationship persists.

This detects coordination; it does not identify the coupling mechanism by itself. Schäfer et al. used heartbeat and respiratory time series to find intervals in which heartbeats occurred at preferred phases of the breathing cycle ([*Heartbeat synchronized with ventilation*, 1998](https://doi.org/10.1038/32567)).
'''
if "### Detecting synchronisation in measured data" not in text:
    text = text.rstrip() + detection
spatial["source"] = lines(text)


with PATH.open("w") as handle:
    json.dump(notebook, handle, indent=1, ensure_ascii=False)
    handle.write("\n")
