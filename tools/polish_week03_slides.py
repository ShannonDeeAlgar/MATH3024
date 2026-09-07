"""Consolidate legacy Week 3 slide fragments into the current house style."""
from pathlib import Path
import nbformat

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "notebooks/week03/L_Reaction_diffusion.ipynb"
nb = nbformat.read(PATH, as_version=4)
cells = {cell.id: cell for cell in nb.cells}

def set_source(cell_id, source):
    cells[cell_id].source = source.strip()

def reader_only(*ids):
    for cell_id in ids:
        cell = cells[cell_id]
        tags = set(cell.metadata.get("tags", []))
        tags.add("reader-only")
        tags.discard("slides")
        cell.metadata["tags"] = sorted(tags)
        cell.metadata["slideshow"] = {"slide_type": ""}

set_source("d0dd3fdf-7bad-4b0c-b3bb-594128690712", """
# Reaction-diffusion systems
## MATH3024 · Week 3

<div class="canonical-model-marker"><span>Canonical models:</span><strong>Random walk diffusion and Gray–Scott reaction–diffusion</strong></div>
""")

set_source("week03-same-mechanism-different-pattern", """
# Similar mechanisms, different patterns

<div class="two-panel equal-panels">
<div class="image-panel">
<img src="images/Cheetah_vs_leopard_vs_jaguar.jpg" alt="Coat patterns of a cheetah, leopard and jaguar" style="width:100%;">
<div class="image-label-row"><span>Cheetah</span><span>Leopard</span><span>Jaguar</span></div>
</div>
<div class="text-panel">
<p><strong>One reaction–diffusion family can select different patterns.</strong></p>
<p>Parameters, geometry, growth, and perturbations can select spots, rosettes, stripes, labyrinths, or a nearly uniform state.</p>
<p>This makes the mechanism plausible. The photograph alone does not prove it.</p>
</div>
</div>
""")

# Replace the old sequence of standalone captions and media with one comparison.
set_source("7347319d-2e0d-49d0-a1c3-ac02ffcd446d", """
# Similar form, different mechanisms

<div class="two-panel equal-panels">
<div class="image-panel">
<video autoplay loop muted playsinline aria-label="Rayleigh–Bénard convection cells viewed from above" style="display:block;width:100%;max-height:350px;object-fit:contain;">
  <source src="images/Bénard_cells_convection.ogv.480p.vp9.webm" type="video/webm">
</video>
<p><strong>Coffee and other heated fluids</strong></p>
<p>Buoyancy and heat flow organise convection cells.</p>
</div>
<div class="image-panel">
<img src="images/Garlic_intersection.jpeg" alt="Cell-like arrangement in a garlic cross-section" style="width:100%;">
<p><strong>Garlic bulb</strong></p>
<p>Growth and packing organise biological domains.</p>
</div>
</div>
""")
reader_only(
    "461b78ee-5bb0-43e7-bf03-63d7fcdd6874",
    "d0523d87-a29f-493f-b63c-7ba22a0e04e8",
    "7793fce9-8449-4370-9fc9-d242315fe91b",
    "cdf38106-a059-4da5-8d31-b2a4bf6e06a7",
    "491e85da-c778-4d46-ad4c-9a89210e42a4",
)

set_source("a0a1efe7-e26e-4f6d-a529-3db70b3fe94f", """
# Turing turns to morphogenesis

<div class="two-panel equal-panels">
<div class="image-panel"><img src="images/Turing_and_imitation_game.png" alt="Alan Turing and his work" style="width:100%;"></div>
<div class="text-panel">
<p><strong>The biological question was older than Turing.</strong></p>
<p>His 1952 contribution was to show mathematically how reacting and diffusing morphogens could destabilise a uniform state.</p>
<p>A mechanism could create spatial organisation without containing a map of the final pattern.</p>
</div>
</div>
""")
reader_only("afdf9f9c-ad1a-4efd-9aef-d7b036bf0cc6")

set_source("d112f5d4", """
# Build the Turing mechanism

<div class="analysis-perspectives">
<div><strong>Local activation</strong><br>Reinforce a change where it begins.</div>
<div><strong>Longer-range inhibition</strong><br>Suppress the same change nearby.</div>
</div>

<div class="two-panel equal-panels">
<div class="image-panel"><img src="images/Turing_1952_dappled.png" alt="Turing's manually computed dappled pattern" style="width:100%;"></div>
<div class="text-panel">
<p><strong>Turing's hand-computed example</strong></p>
<p>Repeated local updates produced a tissue-scale dappled pattern. No cell was assigned its final colour in advance.</p>
</div>
</div>
""")
reader_only("e5f79f48-d91b-473c-a24a-2d442239d788", "e6b584f8-26c4-45c2-8873-a6be6658da5a")

# Use a direct embed rather than exposing a Python display cell.
video = cells["11879310"]
video.cell_type = "markdown"
video.source = """
# Brownian motion: the physical phenomenon

<div class="reader-video">
<iframe width="800" height="450" src="https://www.youtube.com/embed/7orMPKrYPwE"
title="Brownian motion" frameborder="0"
allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
allowfullscreen></iframe>
</div>
"""
video.pop("outputs", None)
video.pop("execution_count", None)
video.metadata["tags"] = ["slides"]

set_source("week03-brownian-ensemble", r"""
# From one random walk to diffusion

<img src="images/brownian_ensemble_msd.svg" alt="One Brownian trajectory and an ensemble mean-square-displacement comparison with four D t" style="display:block;width:88%;margin:0 auto;">

In two dimensions, the ensemble mean-square displacement follows
$$
\langle \lVert \mathbf{x}(t)-\mathbf{x}(0)\rVert^2\rangle=4Dt.
$$

<div class="ladder-marker"><img src="images/ladder_marker.svg" alt=""><span><strong>Up the ladder over random paths:</strong> average over many trajectories to reveal a predictable spreading law.</span></div>
""")

# These legacy fragments are now incorporated into the Brownian-motion sequence
# and the later Turing-instability explanation.
reader_only("259fd509", "f7ee60e4")

set_source("54e20377-5977-4ea6-a97b-7482a438a6c9", """
# Explore the Gray–Scott parameter space

<div class="two-panel equal-panels">
<div class="image-panel"><img src="images/Hopfed_turingles.png" alt="Interactive Gray–Scott patterns" style="width:100%;"></div>
<div class="text-panel">
<p><strong>Feed and kill rates are direct controls.</strong></p>
<p>Vary them to see where uniform states, spots, stripes, and moving structures occur.</p>
<p><a href="https://www.complexity-explorables.org/explorables/hopfed-turingles/">Open the Complexity Explorable</a></p>
</div>
</div>
""")

set_source("e568a57f-c749-47ab-8fe7-fb411fa60a0e", """
# Return to the animal coats

<div class="two-panel equal-panels">
<div class="image-panel">
<img src="images/Cheetah_vs_leopard_vs_jaguar.jpg" alt="Cheetah, leopard and jaguar coat patterns" style="width:100%;">
<div class="image-label-row"><span>Cheetah</span><span>Leopard</span><span>Jaguar</span></div>
</div>
<div class="text-panel">
<p><strong>Shared mechanism does not imply identical output.</strong></p>
<p>Domain geometry, scale, growth, and parameters influence which spatial mode survives.</p>
<p>Biological evidence is still required to connect a mathematical mechanism to a species.</p>
</div>
</div>
""")
reader_only("05ae13c3-a003-461f-bf27-470d8c028aa4", "095f1046-4e61-4e60-9f8b-19666e8ba127")

# Combine headings with their equations and remove legacy continuation prose.
set_source("4fad79e4-e78d-468c-be71-d70d8c4c711e", r"""
# The transport equation

$$
\frac{\partial u}{\partial t}+\nabla\cdot(\mathbf{v}u)
=D\nabla^2u+R(u).
$$

<div class="analysis-perspectives three">
<div><strong>Advection</strong><br>$\nabla\cdot(\mathbf{v}u)$ transports by flow.</div>
<div><strong>Diffusion</strong><br>$D\nabla^2u$ smooths concentration gradients.</div>
<div><strong>Reaction</strong><br>$R(u)$ creates, removes, or transforms material locally.</div>
</div>
""")
reader_only("349945e6-9630-4b03-9928-ecbc2e849df9", "46d7a029-b86d-4fd4-9b5a-75c0b4294279", "c34f0c02-f649-4766-88ef-78423a575d4b")

set_source("e501ec03-46e5-44ea-8535-46b96a148671", r"""
# Return to reaction–diffusion

$$
\frac{\partial U}{\partial t}=R_U(U,V)+D_U\nabla^2U,
\qquad
\frac{\partial V}{\partial t}=R_V(U,V)+D_V\nabla^2V.
$$

Two local reactions are coupled through two spatial fields. The diffusion rates need not be equal.
""")
reader_only("1413b506-1960-4cef-bbc6-84dc4b2d03cf")
reader_only(
    "8c608de1-7d80-4df2-bb0e-7412b15cf909",
    "62473a7a-f961-4853-8e22-07b9c8679dec",
    "4899601d-8952-4abd-9623-fb1535308af8",
    "08cfa598-60c6-4921-bfcd-56ddc8719df7",
)

set_source("ecd5c9ba-5acd-42ce-9fba-d6a584a56494", """
# Colour is a modelling and communication choice

<div class="two-panel equal-panels">
<div class="image-panel"><img src="images/Colourblind.svg" alt="Colour-vision accessibility test" style="width:100%;"></div>
<div class="text-panel">
<p><strong>A colour map should reveal order without excluding readers.</strong></p>
<p>Use perceptually ordered maps for concentration. Avoid rainbow scales and red–green contrasts where possible.</p>
<p>Always retain labels or another redundant cue when exact interpretation matters.</p>
</div>
</div>
""")
reader_only(
    "eb7f54f7-9925-4880-a13f-4a358e34df86",
    "44c47b59-472a-48b6-8858-d4445ed0421f",
    "1a76982e-6025-415c-87fd-955fe49b069f",
)
set_source("2d86506f-baf9-4f97-9a53-63015dd1e05f", r"""
# The five-point stencil

$$
L=\begin{bmatrix}
0&1&0\\
1&-4&1\\
0&1&0
\end{bmatrix}.
$$

Convolving the grid with $L$ compares each cell with its four axial neighbours. Uniform regions return zero; isolated peaks return a negative value.
""")

set_source("0ac1d921-5f1e-4b64-8c65-8454c1e70e8f", r"""
# Gray–Scott regulation terms

<div class="analysis-perspectives three">
<div><strong>Feed</strong><br>$f(1-U)$ replenishes $U$ without pushing it above its normalised maximum.</div>
<div><strong>Kill</strong><br>$-kV$ removes $V$ locally.</div>
<div><strong>Reaction</strong><br>$UV^2$ converts $U$ into $V$ when both are locally present.</div>
</div>
""")
reader_only(
    "955ed279-4fd0-434a-8214-8f51674944ad",
    "8087aba4-678b-497f-b40f-e3a4e7ae97d8",
    "3e0aa253-5a6e-4aaf-b3f6-a0613616754c",
    "14e1f12c-4b25-4022-a18b-4cb65eb241b2",
    "7dbdca5d-8d47-493d-af36-380745a52096",
)

set_source("week03-gray-scott-world", """
# Gray–Scott-like patterns in the world

<div class="analysis-perspectives three">
<div><img src="images/Zebrafish.jpg" alt="Zebrafish pigment stripes"><strong>Pigment stripes</strong><br>Cell contact and movement can complement reaction–diffusion.</div>
<div><img src="images/Hydra-Foto.jpg" alt="Hydra body pattern"><strong>Development</strong><br>Activator–inhibitor feedback can organise repeated features.</div>
<div><img src="images/Garlic_intersection.jpeg" alt="Garlic cellular domains"><strong>Cellular domains</strong><br>Similar geometry can also arise from growth and packing.</div>
</div>

<p class="figure-reference">These are mechanism comparisons, not claims that nature literally implements the Gray–Scott equations.</p>
""")
set_source("week03-pattern-family", """
# Reaction–diffusion is one route to pattern

<div class="analysis-perspectives three">
<div><strong>Flow and phase separation</strong><br>Transport, convection, and coarsening organise material.</div>
<div><strong>Mechanical instability</strong><br>Buckling and differential growth create folds and wrinkles.</div>
<div><strong>Excitable waves and aggregation</strong><br>Signals, moving fronts, and cell motion build dynamic structure.</div>
</div>

<div class="choice-marker"><img src="images/choice_marker.svg" alt=""><span>Choose between mechanisms using evidence: motion, conservation, wavelength, perturbation response, and time evolution.</span></div>
""")

nbformat.write(nb, PATH)
