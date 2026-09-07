"""Restore the Week 3 pattern hook and Turing context in the current notebook."""

from pathlib import Path

import nbformat


ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "notebooks/week03/L_Reaction_diffusion.ipynb"


def markdown(source: str, cell_id: str, slide_type: str = "subslide", tags=None):
    cell = nbformat.v4.new_markdown_cell(source.strip())
    cell.id = cell_id
    cell.metadata["slideshow"] = {"slide_type": slide_type}
    if tags:
        cell.metadata["tags"] = tags
    return cell


nb = nbformat.read(PATH, as_version=4)
by_id = {cell.id: cell for cell in nb.cells}


# Keep one sand/zebra comparison only, with the mechanism attached directly
# to the corresponding observation.
by_id["week03-sand-zebra-first"].source = """
# Similar patterns, different mechanisms

<div class="two-panel equal-panels">
<div class="image-panel">
<img src="images/SandDunes.png" alt="Parallel ridges in wind-blown sand" style="width:100%;">
<p><strong>Sand ridges</strong></p>
<p><strong>Mechanism · transport and flow</strong><br>Wind moves grains. Erosion and deposition organise the ridges.</p>
</div>
<div class="image-panel">
<img src="images/Zebras.png" alt="Zebra coat stripes" style="width:100%;">
<p><strong>Zebra stripes</strong></p>
<p><strong>Mechanism · reaction and diffusion</strong><br>Local biochemical and cellular interactions organise pigment.</p>
</div>
</div>
""".strip()


# Restore the original experiment video. The next slide makes the more useful
# garlic/Voronoi comparison without trying to fit three visuals in one panel.
by_id["7347319d-2e0d-49d0-a1c3-ac02ffcd446d"].source = """
# Similar form, different mechanisms

<div class="two-panel equal-panels">
<div class="image-panel">
<iframe width="100%" height="340" src="https://www.youtube.com/embed/nQUH9nGTZTY"
title="Rayleigh–Bénard convection experiment" frameborder="0"
referrerpolicy="strict-origin-when-cross-origin"
allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
allowfullscreen></iframe>
</div>
<div class="text-panel">
<p><strong>Rayleigh–Bénard convection</strong></p>
<p>Heating a fluid from below can organise circulation into persistent cells. The pattern is produced by buoyancy and flow, not biological growth.</p>
</div>
</div>

<p class="figure-reference"><a href="https://www.youtube.com/watch?v=nQUH9nGTZTY">Rayleigh–Bénard convection experiment</a>.</p>
""".strip()

voronoi = markdown(
    """
# Similar cells, different construction

<div class="two-panel equal-panels">
<div class="image-panel">
<img src="images/Garlic_intersection.jpeg" alt="Cell-like domains in a cut garlic bulb" style="display:block;width:88%;max-height:350px;object-fit:contain;margin:0 auto;">
<p><strong>Garlic bulb</strong></p>
<p>Growth and packing partition the tissue into domains.</p>
</div>
<div class="image-panel">
<img src="images/Voronoi_growth_euclidean.gif" alt="Growing discs meet and form a Voronoi-like partition" style="display:block;width:88%;max-height:350px;object-fit:contain;margin:0 auto;">
<p><strong>Growing domains</strong></p>
<p>Expanding regions stop where they meet, producing a Voronoi-like tessellation.</p>
</div>
</div>

<p class="figure-reference">Garlic photograph and growing-domain animation previously used in this unit.</p>
""",
    "week03-garlic-voronoi",
)


life_slide = markdown(
    """
# Alan Mathison Turing

<div class="two-panel equal-panels">
<div class="image-panel"><img src="images/Alan_Turing_(1951).jpg" alt="Alan Turing in 1951" style="display:block;width:72%;max-height:430px;object-fit:contain;margin:0 auto;"></div>
<div class="text-panel">
<p><strong>Mathison was his middle name.</strong></p>
<p>Turing helped establish theoretical computer science, worked in wartime cryptanalysis, designed early stored-program computers, and asked how machines might exhibit intelligence.</p>
<p>At Manchester he also turned to mathematical biology: how can an initially near-uniform embryo develop organised form?</p>
</div>
</div>

<p class="figure-reference">Alan Turing in 1951. National Portrait Gallery / Elliott &amp; Fry.</p>
""",
    "week03-alan-mathison-turing",
)

life_reader = markdown(
    """
## Alan Turing: a wider scientific life

Alan **Mathison** Turing (1912–1954) moved repeatedly between abstract mathematics and concrete mechanisms. His 1936 work on computable numbers introduced the mathematical machine now called a Turing machine. During the Second World War he worked at Bletchley Park on German naval Enigma. He later designed the Automatic Computing Engine at the National Physical Laboratory, worked on the Manchester computers, and published *Computing Machinery and Intelligence* in 1950.

Turing was prosecuted in 1952 for a homosexual relationship and subjected to hormonal treatment. He died in 1954. The British government apologised for his treatment in 2009, and he received a posthumous royal pardon in 2013. His life should not be reduced either to tragedy or to codebreaking. Morphogenesis was part of a broad programme concerned with how rules, computation, instability, and physical processes generate organised behaviour.
""",
    "week03-turing-life-reader",
    slide_type="",
    tags=["reader-only"],
)

paper_slide = markdown(
    """
# What Turing actually proposed

<div class="two-panel equal-panels">
<div class="image-panel"><img src="images/turing_1952_first_page.png" alt="First page of Turing's 1952 paper" style="display:block;width:82%;max-height:440px;object-fit:contain;margin:0 auto;"></div>
<div class="text-panel">
<p><strong>A homogeneous state can become unstable.</strong></p>
<p>Random disturbances are amplified into organised spatial structure when reaction and diffusion act together.</p>
<p>Turing studied both discrete cells and continuous tissue, and considered rings, spheres, dappling, Hydra tentacles, leaf whorls, gastrulation, and phyllotaxis.</p>
</div>
</div>

<p class="figure-reference">A. M. Turing (1952), <a href="https://doi.org/10.1098/rstb.1952.0012">“The Chemical Basis of Morphogenesis”</a>.</p>
""",
    "week03-turing-paper-scope",
)

paper_reader = markdown(
    """
## What else is in the 1952 paper?

The paper is broader and more cautious than the phrase “spots and stripes” suggests.

- Turing defines a **morphogen** simply as a “form producer”. He does not require it to be one particular molecule.
- He develops both a **discrete cell model** and a **continuous tissue model**. That choice anticipates our later movement between random walks, concentration fields, and numerical grids.
- He focuses on the **onset of instability**. Small random departures from symmetry matter because an unstable mode can amplify them.
- The six cases classify early linear behaviour near a homogeneous equilibrium. They are not six finished animal-coat patterns.
- His examples include Hydra tentacles, leaf whorls, gastrulation, dappling, and phyllotaxis.
- He explicitly says that nonlinear development will require particular computational experiments using digital computers.

His description of modelling is also unusually direct:

<div class="reader-voice">
  <div class="reader-voice-quote">This model will be a simplification and an idealization, and consequently a falsification.</div>
  <div class="reader-voice-attr">Alan Turing, 1952</div>
</div>

The useful question is therefore not whether the model reproduces every biological detail. It is whether the deliberately retained reaction, diffusion, geometry, and instability are sufficient to explain a feature we care about.
""",
    "week03-turing-paper-reader",
    slide_type="",
    tags=["reader-only"],
)


# The current Turing-question slide becomes the bridge from biography to the
# specific biological problem rather than carrying the paper title page again.
by_id["a0a1efe7-e26e-4f6d-a529-3db70b3fe94f"].source = """
# Turing’s question: how does form emerge?

<div class="two-panel equal-panels">
<div class="image-panel"><img src="images/Turing_and_imitation_game.png" alt="Alan Turing and representations of his work" style="display:block;width:88%;max-height:410px;object-fit:contain;margin:0 auto;"></div>
<div class="text-panel">
<p>An embryo begins close to uniform, yet organised differences appear.</p>
<p>Could familiar physical processes create structure without a pre-drawn template?</p>
<p>Turing’s candidate mechanism joined <strong>local chemical reaction</strong> to <strong>spatial diffusion</strong>.</p>
</div>
</div>
""".strip()


# Insert or replace authored cells without disturbing the remainder of the
# heavily revised notebook.
for cell_id in [
    "week03-garlic-voronoi",
    "week03-alan-mathison-turing",
    "week03-turing-life-reader",
    "week03-turing-paper-scope",
    "week03-turing-paper-reader",
]:
    nb.cells = [cell for cell in nb.cells if cell.id != cell_id]

index = next(i for i, cell in enumerate(nb.cells) if cell.id == "7347319d-2e0d-49d0-a1c3-ac02ffcd446d")
nb.cells.insert(index + 1, voronoi)

index = next(i for i, cell in enumerate(nb.cells) if cell.id == "a0a1efe7-e26e-4f6d-a529-3db70b3fe94f")
nb.cells[index:index] = [life_slide, life_reader]
index = next(i for i, cell in enumerate(nb.cells) if cell.id == "a0a1efe7-e26e-4f6d-a529-3db70b3fe94f")
nb.cells[index + 1:index + 1] = [paper_slide, paper_reader]

nbformat.write(nb, PATH)
print(f"Updated {PATH}")
