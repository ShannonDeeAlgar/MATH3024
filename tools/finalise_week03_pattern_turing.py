#!/usr/bin/env python3
import json
from pathlib import Path

path = Path(__file__).resolve().parents[1] / "notebooks/week03/L_Reaction_diffusion.ipynb"
nb = json.loads(path.read_text())

def set_cell(index, text, slide_type=None):
    cell = nb["cells"][index]
    cell["source"] = text.splitlines(keepends=True)
    if text and not text.endswith("\n"):
        cell["source"][-1] += "\n"
    if slide_type is not None:
        cell.setdefault("metadata", {}).setdefault("slideshow", {})["slide_type"] = slide_type

set_cell(7, '''## Convection cells

<div class="two-panel equal-panels">
<div class="image-panel">
<iframe width="100%" height="340" src="https://www.youtube.com/embed/nQUH9nGTZTY"
title="Rayleigh–Bénard convection experiment" frameborder="0"
referrerpolicy="strict-origin-when-cross-origin"
allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
allowfullscreen></iframe>
</div>
<div class="text-panel">
<p><strong>Rayleigh–Bénard convection:</strong> heating a fluid from below can organise circulation into persistent cells. The pattern is produced by buoyancy and flow, not biological growth.</p>
</div>
</div>

<p class="figure-reference">Video: <a href="https://www.youtube.com/watch?v=nQUH9nGTZTY">Rayleigh–Bénard convection experiment</a>.</p>
''')

set_cell(8, '''## Cell-like partitions

<div class="two-panel equal-panels">
<div class="image-panel">
<img src="images/Garlic_intersection.jpeg" alt="Cell-like domains in a cut garlic bulb" style="display:block;width:88%;max-height:350px;object-fit:contain;margin:0 auto;">
<p><strong>Garlic bulb:</strong> growth and packing partition the tissue into domains.</p>
</div>
<div class="image-panel">
<img src="images/Voronoi_growth_euclidean.gif" alt="Growing discs meet and form a Voronoi-like partition" style="display:block;width:88%;max-height:350px;object-fit:contain;margin:0 auto;">
<p><strong>Growing domains:</strong> expanding regions stop where they meet, producing a Voronoi-like tessellation.</p>
</div>
</div>

<p class="figure-reference">Garlic photograph and growing-domain animation previously used in this unit.</p>
''')

set_cell(10, '''## Folded surfaces
<div class="two-panel equal-panels">
<div class="text-panel"><p><strong>Mechanical instability:</strong> differential growth puts a surface layer into compression. Beyond a threshold it buckles. The same physical idea can organise living tissue and a swelling gel.</p></div>
<div class="image-panel"><img src="images/brain_folding_gel.gif" alt="A swelling gel developing brain-like folds" style="display:block;width:100%;max-height:420px;object-fit:contain;"><p class="figure-reference">A swelling-gel experiment makes the instability visible.</p></div>
</div>
''')

set_cell(13, '''## Travelling waves
<div class="two-panel equal-panels">
<div class="image-panel"><img src="images/dictyostelium_aggregation_waves.png" alt="Fluorescent and processed views of cAMP waves in slime mould" style="width:100%;max-height:390px;object-fit:contain;"><p><strong>cAMP waves in living cells:</strong> colour shows fluorescence; black-and-white panels are processed views used to identify cell streams.</p></div>
<div class="image-panel"><img src="images/belousov_zhabotinsky_spirals.jpg" alt="Spiral waves in a Belousov-Zhabotinsky reaction" style="width:100%;max-height:390px;object-fit:cover;"><p><strong>Belousov–Zhabotinsky reaction:</strong> an excitable chemical medium generates travelling fronts without moving cells.</p></div>
</div>
''')

set_cell(18, '''### A model is a deliberate simplification

<img src="images/Turing_1952_quote.png" alt="Turing describes the embryo model as a simplification and idealisation" style="display:block;width:86%;max-height:205px;object-fit:contain;margin:0.5rem auto 0.8rem;">

Turing begins by stating what the model will leave out. The question is whether the retained features capture the mechanism that matters.

<p class="figure-reference">Excerpt from A. M. Turing, <a href="https://doi.org/10.1098/rstb.1952.0012">“The Chemical Basis of Morphogenesis”</a>, <em>Philosophical Transactions of the Royal Society B</em> 237 (1952), 37–72.</p>
''')

set_cell(19, '''### A remarkably short reference list

<div class="two-panel image-wide compact-panels">
  <div class="image-panel"><img src="images/TuringReferences.png" alt="The six references in Turing's 1952 morphogenesis paper" style="width:100%;height:245px;object-fit:contain;"></div>
  <div class="text-panel"><p><strong>Six references.</strong></p><p>Five are books. The only journal paper is Michaelis and Menten’s work on enzyme kinetics.</p><p>The list gives a sense of how little established reaction–diffusion biology Turing had to cite.</p></div>
</div>

<p class="figure-reference">Reference list in A. M. Turing, <a href="https://doi.org/10.1098/rstb.1952.0012">“The Chemical Basis of Morphogenesis”</a>, <em>Philosophical Transactions of the Royal Society B</em> 237 (1952), 37–72.</p>
''')

set_cell(21, '''## Turing’s mechanism: reaction and diffusion

Turing coupled two familiar processes.

<div class="two-panel equal-panels compact-panels">
  <div class="text-panel"><p><strong>Reaction:</strong> molecules meet and change identity locally.</p></div>
  <div class="text-panel"><p><strong>Diffusion:</strong> irregular motion carries chemicals between nearby locations.</p></div>
</div>

Small perturbations provide the spatial differences on which these processes act.
''', 'slide')

set_cell(22, r'''### Diffusion-driven instability

<div class="definition-panel"><strong>Diffusion-driven instability:</strong> diffusion destabilises a spatially uniform state that was stable to uniform perturbations.</div>

$$
\text{stable homogeneous reaction state}
+\text{differential diffusion}
\longrightarrow
\text{selected spatial pattern}
$$

<p><strong>Turing pattern:</strong> the stationary spatial pattern left when the growing variation saturates.</p>

<div class="discussion-marker"><img src="images/discussion_marker.svg" alt="Discussion prompt"><span>Diffusion normally smooths differences. How could it instead help a pattern grow?</span></div>

<p class="small-note reader-only-detail"><strong>Spatial mode:</strong> a repeating spatial variation with a particular wavelength. Different diffusion coefficients are required in the classical two-species mechanism, but that difference alone does not guarantee instability. Linear stability analysis determines which modes grow; it is useful context, but is not assessable here.</p>
''', 'slide')
nb["cells"][22].setdefault("metadata", {})["tags"] = ["slides"]

cell_24 = "".join(nb["cells"][24].get("source", []))
cell_24 = cell_24.replace(
    '<p class="figure-reference">Turing (1952), Fig. 2.</p>',
    '<p class="figure-reference">Figure 2 in A. M. Turing, <a href="https://doi.org/10.1098/rstb.1952.0012">“The Chemical Basis of Morphogenesis”</a>, <em>Philosophical Transactions of the Royal Society B</em> 237 (1952), 37–72.</p>',
)
nb["cells"][24]["source"] = cell_24.splitlines(keepends=True)

set_cell(20, '''### From an unusual proposal to a modern framework

The paper was not entirely unnoticed. The embryologist C. H. Waddington corresponded with Turing about biological applications. Even so, the work received limited attention for several decades. Then molecular genetics changed the centre of gravity of biology. The double-helix model appeared in 1953, and developmental biologists understandably concentrated on genes and molecular mechanisms. Turing's abstract morphogens were difficult to identify or measure, and direct chemical examples were scarce. DNA did not make the reaction–diffusion idea irrelevant, but it made the theory harder to test at the time.

That position has changed. Reaction–diffusion models are now a standard framework for studying spontaneous spatial pattern formation. Experimental support exists in chemical systems and in several developmental settings, including pigment patterns, hair and feather follicles, digits and mammalian palate patterning.

The phrase **Turing pattern** is often used for the stationary spots or stripes produced by a diffusion-driven instability. It is also used more broadly for patterns generated by Turing-type reaction–diffusion systems. We will use the surrounding context to say whether a pattern is stationary, oscillatory or travelling rather than treating the name as a rigid boundary.

Reaction–diffusion is not the explanation for every biological pattern, and visual similarity to a simulated pattern is not evidence of the mechanism. Modern studies use the model to make experimentally testable claims about molecules, interactions, transport rates and perturbations.

See Ball (2015), [“Forging patterns and making waves from biology to geology”](https://doi.org/10.1098/rstb.2014.0218), and Kondo (2022), [“The present and future of Turing models in developmental biology”](https://journals.biologists.com/dev/article/149/24/dev200974/286110/The-present-and-future-of-Turing-models-in).
''', 'skip')
nb["cells"][20].setdefault("metadata", {})["tags"] = ["reader-only"]

cell_23 = "".join(nb["cells"][23].get("source", []))
cell_23 = cell_23.replace(
    'Turing distinguished stationary waves from oscillatory travelling waves. His two-morphogen calculation included spatially uniform temporal oscillation, but he placed finite-wavelength travelling and shortest-wavelength oscillatory cases in the three-or-more-morphogen category. Modern reaction–diffusion theory allows a broader range of oscillatory and wave instabilities. In this unit, **Turing pattern** refers to the stationary diffusion-driven case.\n',
    'Turing distinguished stationary waves from oscillatory travelling waves. His two-morphogen calculation included spatially uniform temporal oscillation, but he placed finite-wavelength travelling and shortest-wavelength oscillatory cases in the three-or-more-morphogen category. Modern reaction–diffusion theory allows a broader range of oscillatory and wave instabilities.\n',
)
nb["cells"][23]["source"] = cell_23.splitlines(keepends=True)

# Remove the stand-alone “What else is in the 1952 paper?” section.
set_cell(25, "", "skip")
nb["cells"][25].setdefault("metadata", {})["tags"] = ["remove-cell"]

set_cell(27, '''Here $\\boldsymbol{\\xi}_m$ is the displacement on step $m$. Every panel uses the same eight possible directions and 45 unit-length steps; only the rule for choosing directions changes. Aligned directions carry a biased or persistent walk farther from its origin. An unbiased walk frequently retraces an edge, so several steps may lie on top of one another.

Unit steps have finite variance. Infinite step variance instead requires unbounded, sufficiently heavy-tailed step lengths, as in an ideal Lévy flight.
''', 'skip')
nb["cells"][27].setdefault("metadata", {})["tags"] = ["reader-only"]

set_cell(29, '''The film above contains many short microscope recordings of real Brownian motion. It runs for about 12 minutes; sampling a few snippets is sufficient.

$$
\\mathbf{B}(t+\\Delta t)-\\mathbf{B}(t)
\\sim \\mathcal{N}(\\mathbf{0},2D\\Delta t\\,I_d),
\\qquad
\\mathbb{E}\\!\\left[\\lVert\\mathbf{B}(t)-\\mathbf{B}(0)\\rVert^2\\right]=2dDt.
$$

The first expression describes one interval $\\Delta t$; the second describes displacement accumulated over elapsed time $t$. The matrix $I_d$ is the $d\\times d$ identity, so coordinate increments are independent and have equal variance. In two dimensions the expected squared distance is $4Dt$, while typical distance grows like $\\sqrt{4Dt}$.
''', 'skip')
nb["cells"][29].setdefault("metadata", {})["tags"] = ["reader-only"]

set_cell(31, '''<div class="choice-marker"><img src="images/choice_marker.svg" alt="Modelling choice" width="34" height="34"><span><strong>What should we measure?</strong> The observable must match the question.</span></div>

- **Mean displacement:** detects drift and is zero for an unbiased walk.
- **Mean-square displacement:** measures spreading and grows as $\\mathbb E[R^2(t)]=2dDt$.
- **Endpoint distribution:** approaches a Gaussian under the usual finite-variance assumptions.
- **First-passage time:** records when a path first reaches a target or boundary.
- **Step and turning-angle statistics:** distinguish unbiased, biased and persistent motion.

The diffusion equation describes how the ensemble density evolves, not where one walker will go.
''', 'skip')
nb["cells"][31].setdefault("metadata", {})["tags"] = ["reader-only"]

cell_36 = "".join(nb["cells"][36].get("source", []))
cell_36 = cell_36.replace(
    "Gray–Scott belongs to Turing's broader reaction–diffusion framework, but not every Gray–Scott pattern is a classical **Turing pattern**. That narrower label requires a uniform equilibrium that is stable without diffusion and destabilised by differential diffusion.\n\n",
    "Gray–Scott provides a concrete reaction–diffusion system in which we can connect reaction, transport and parameter choice to the patterns produced.\n\n",
)
nb["cells"][36]["source"] = cell_36.splitlines(keepends=True)

cell_55 = "".join(nb["cells"][55].get("source", []))
cell_55 = cell_55.replace(
    "That result alone does not prove a classical Turing instability. We must still ask:\n",
    "That result alone does not identify the mechanism. We must still ask:\n",
)
nb["cells"][55]["source"] = cell_55.splitlines(keepends=True)

path.write_text(json.dumps(nb, indent=1, ensure_ascii=False) + "\n")
print(path)
