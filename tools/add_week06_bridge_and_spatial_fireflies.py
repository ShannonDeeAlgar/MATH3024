"""Add Millennium Bridge footage and a spatial-firefly return to Week 6."""

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "notebooks/week06/L_Synchronisation.ipynb"


def markdown_cell(cell_id: str, source: str, tags: list[str], slide_type: str) -> dict:
    return {
        "cell_type": "markdown",
        "id": cell_id,
        "metadata": {
            "slideshow": {"slide_type": slide_type},
            "tags": tags,
        },
        "source": source.splitlines(keepends=True),
    }


notebook = json.loads(PATH.read_text())
cells = notebook["cells"]

# Add opening-day footage to the existing bridge accounts.
bridge_embed = (
    '<iframe style="display:block;width:78%;height:360px;margin:0 auto" '
    'src="https://www.youtube.com/embed/y2FaOJxWqLE" '
    'title="The Millennium Bridge wobbling shortly after opening in June 2000" '
    'frameborder="0" allow="accelerometer; autoplay; clipboard-write; '
    'encrypted-media; gyroscope; picture-in-picture; web-share" '
    'allowfullscreen></iframe>\n\n'
    '<p class="figure-credit">Opening-day footage filmed in June 2000. '
    '<a href="https://www.youtube.com/watch?v=y2FaOJxWqLE">The Wibbly Wobbly Millennium Bridge in London</a>.</p>\n'
)

for cell in cells:
    if cell.get("id") != "w6-a3284fd926":
        continue
    text = "".join(cell.get("source", []))
    if "youtube.com/embed/y2FaOJxWqLE" in text:
        continue
    lines = text.splitlines(keepends=True)
    insert_at = 1
    while insert_at < len(lines) and not lines[insert_at].strip():
        insert_at += 1
    lines[insert_at:insert_at] = ["\n", bridge_embed, "\n"]
    cell["source"] = lines

# Keep the footage large and legible on its own slide rather than overloading
# the explanatory bridge slide.
bridge_slide = next(cell for cell in cells if cell.get("id") == "w6-b84357403f")
bridge_slide_text = "".join(bridge_slide.get("source", []))
if bridge_embed in bridge_slide_text:
    bridge_slide["source"] = bridge_slide_text.replace("\n" + bridge_embed + "\n", "\n").splitlines(keepends=True)

if not any(cell.get("id") == "w6-millennium-video-slide" for cell in cells):
    bridge_index = next(i for i, cell in enumerate(cells) if cell.get("id") == "w6-b84357403f")
    cells.insert(
        bridge_index,
        markdown_cell(
            "w6-millennium-video-slide",
            """## The wobbling Millennium Bridge

<iframe style="display:block;width:86%;height:500px;margin:0 auto" src="https://www.youtube.com/embed/y2FaOJxWqLE" title="The Millennium Bridge wobbling shortly after opening in June 2000" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>

<p class="figure-credit">Opening-day footage filmed in June 2000. <a href="https://www.youtube.com/watch?v=y2FaOJxWqLE">The Wibbly Wobbly Millennium Bridge in London</a>.</p>
""",
            ["slides-only"],
            "subslide",
        ),
    )

# Add a compact return slide immediately after the Scope banner.
if not any(cell.get("id") == "w6-spatial-fireflies-slide" for cell in cells):
    scope_index = next(i for i, cell in enumerate(cells) if cell.get("id") == "w6-scope")
    cells.insert(
        scope_index + 1,
        markdown_cell(
            "w6-spatial-fireflies-slide",
            """## Return to the fireflies · put them in space

The phase circle displays each oscillator's **internal clock**. Its location on that circle is not the firefly's location in a forest.

To model spatial fireflies, give firefly $i$ a position $\\mathbf x_i$ and replace all-to-all coupling by a distance-dependent weight:

$$
\\dot\\theta_i=\\omega_i+\\frac{K}{\\sum_j w_{ij}}\\sum_j w_{ij}\\sin(\\theta_j-\\theta_i),
\\qquad w_{ij}=W(\\lVert\\mathbf x_j-\\mathbf x_i\\rVert).
$$

Then decide whether fireflies move, whether flashes act as pulses, and whether vision has a finite range, delays or occlusion.

<div class="discussion-marker"><img src="images/discussion_marker.svg" alt="Discussion prompt"><span>Which extension changes only the interaction network, and which creates a genuinely coupled phase-and-motion model?</span></div>
""",
            ["slides-only"],
            "subslide",
        ),
    )

# Add the fuller Reader section before the existing connections.
if not any(cell.get("id") == "w6-spatial-fireflies-reader" for cell in cells):
    connections_index = next(i for i, cell in enumerate(cells) if cell.get("id") == "connections")
    cells.insert(
        connections_index,
        markdown_cell(
            "w6-spatial-fireflies-reader",
            """## Return to the fireflies: phase is not physical position

In the standard Kuramoto visualisation, oscillators are arranged around a circle according to phase. Two points drawn close together have similar internal clock readings; they are not necessarily nearby fireflies. The original all-to-all model does not give an oscillator a position in physical space.

If the aim were to model fireflies distributed through a forest, each firefly would need both a phase $\\theta_i$ and a position $\\mathbf x_i$. A simple first extension is to let interaction strength decrease with physical separation:

$$
\\dot\\theta_i=\\omega_i+\\frac{K}{\\sum_j w_{ij}}\\sum_j w_{ij}\\sin(\\theta_j-\\theta_i),
\\qquad
w_{ij}=W(\\lVert\\mathbf x_j-\\mathbf x_i\\rVert).
$$

The function $W$ might impose a fixed visual range or decay gradually with distance. This changes the complete interaction graph into a spatial network. It also introduces modelling decisions about obstacles, occlusion and communication delays.

Further extensions answer different questions:

- **Pulse coupling:** a flash produces a brief phase shift rather than continuous sinusoidal influence. This is often more natural for fireflies.
- **Motion:** specify an equation for $\\dot{\\mathbf x}_i$. If motion depends on phase, or phase coupling depends on the evolving positions, the model becomes a coupled phase-and-motion system, sometimes called a **swarmalator** model.
- **Heterogeneity and noise:** allow natural frequencies, visual sensitivity or response strengths to vary between individuals.

::: {.discussion}
The original Kuramoto model already includes heterogeneous internal frequencies. Which spatial extension would you add first if the question concerned synchronisation across a forest, and which would you add if the question concerned the formation of moving clusters?
:::

The correct extension depends on the empirical question. Adding physical positions is not merely a more realistic drawing: it changes who can interact with whom and can therefore change the collective dynamics.
""",
            ["reader-only"],
            "skip",
        ),
    )

PATH.write_text(json.dumps(notebook, indent=1, ensure_ascii=False) + "\n")
