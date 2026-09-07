import json
from pathlib import Path


path = Path(__file__).resolve().parents[1] / "notebooks/week06/L_Synchronisation.ipynb"
notebook = json.loads(path.read_text())
cells = notebook["cells"]

quantitative = cells[61]
measure = cells[62]

quantitative["source"] = [
    "## Quantitative analysis\n",
    "\n",
    "### Measure collective coherence\n",
    "\n",
    "Represent oscillator $j$ by the unit complex number\n",
    "\n",
    "$$\n",
    "z_j=e^{\\mathrm{i}\\theta_j}=\\cos\\theta_j+\\mathrm{i}\\sin\\theta_j.\n",
    "$$\n",
    "\n",
    "Its real and imaginary parts are the coordinates of a unit vector pointing at phase $\\theta_j$. Averaging these vectors gives\n",
    "\n",
    "$$\n",
    "r(t)e^{\\mathrm{i}\\psi(t)}\n",
    "=\\dfrac{1}{N}\\sum_{j=1}^{N}e^{\\mathrm{i}\\theta_j(t)}.\n",
    "$$\n",
    "\n",
    "The direction $\\psi$ is the circular mean phase. The magnitude $r$ is the order parameter:\n",
    "\n",
    "- $r\\approx0$ when vectors point around the circle and largely cancel;\n",
    "- $r\\approx1$ when they point in nearly the same direction;\n",
    "- intermediate $r$ records partial concentration without retaining every phase.\n",
    "\n",
    "This circular average treats phases just below $2\\pi$ and just above $0$ as neighbours. Week 5 used the same construction for Vicsek polarisation, written as the magnitude of the mean heading vector.\n",
    "\n",
    "<div class=\"ladder-marker\"><img src=\"images/ladder_marker.svg\" alt=\"Ladder of abstraction\"><span><strong>Up the ladder:</strong> replace the full phase configuration by the collective variables <i>ψ</i>(<i>t</i>) and <i>r</i>(<i>t</i>).</span></div>\n",
]

measure["source"] = [
    "### Put the views together\n",
    "\n",
    "The phase circle, individual histories, circular mean and coherence below all come from the same numerical run. The individual traces remain visible so that the collective summaries can be checked against what the oscillators actually did.\n",
    "\n",
    "<img src=\"images/kuramoto_phase_organisation.gif\" alt=\"Moving Kuramoto phases with their vector average, individual phase histories, mean phase and coherence\" style=\"display:block;width:82%;max-width:980px;margin:1rem auto\">\n",
    "\n",
    "The point of the combined view is not to add another measure. It shows exactly what is discarded when many phase histories are compressed into $\\psi(t)$ and $r(t)$.\n",
]

path.write_text(json.dumps(notebook, indent=1, ensure_ascii=False) + "\n")
