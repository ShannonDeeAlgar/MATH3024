"""Apply the July narrative and visual revision to the Week 3 notebook."""
from pathlib import Path
import nbformat

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "notebooks/week03/L_Reaction_diffusion.ipynb"
nb = nbformat.read(PATH, as_version=4)
cells = {cell.id: cell for cell in nb.cells}


def source(cell_id, text):
    cells[cell_id].source = text.strip()


def reader_only(*ids):
    for cell_id in ids:
        cell = cells[cell_id]
        tags = set(cell.metadata.get("tags", []))
        tags.add("reader-only")
        tags.discard("slides")
        cell.metadata["tags"] = sorted(tags)
        cell.metadata["slideshow"] = {"slide_type": ""}


def remove_cells(*ids):
    """Exclude superseded material from both the Reader and the slides."""
    for cell_id in ids:
        cell = cells[cell_id]
        tags = set(cell.metadata.get("tags", []))
        tags.add("remove-cell")
        tags.discard("slides")
        tags.discard("reader-only")
        cell.metadata["tags"] = sorted(tags)
        cell.metadata["slideshow"] = {"slide_type": ""}


source("9253675a-2529-494e-b524-48a841f31a6d", """
# Pattern formation
<div class="two-panel equal-panels">
<div class="image-panel"><img src="images/gray_scott_classic.svg" alt="A labyrinthine Gray–Scott pattern" style="width:100%;"></div>
<div class="text-panel"><p>Spatial order can appear without a blueprint.</p><p>A local rule, transport, and a small perturbation can produce a system-scale pattern.</p><div class="discussion-marker"><img src="images/discussion_marker.svg" alt=""><span>What would count as an explanation of this pattern?</span></div></div>
</div>
""")
source("week03-same-mechanism-different-pattern", """
# Similar mechanisms, different patterns
<div class="analysis-perspectives three coat-cards">
<div><img src="images/cheetah_coat_card.jpg" alt="Cheetah face and coat"><strong>Cheetah</strong><br>Small, mostly solid spots.</div>
<div><img src="images/leopard_coat_card.jpg" alt="Leopard face and coat"><strong>Leopard</strong><br>Rosettes without central spots.</div>
<div><img src="images/jaguar_coat_card.jpg" alt="Jaguar face and coat"><strong>Jaguar</strong><br>Larger rosettes, often with central spots.</div>
</div>
<p>Related developmental mechanisms can select different motifs as parameters, growth, and geometry change.</p>
""")
source("week03-sand-zebra-first", """
# Similar patterns, different mechanisms
<div class="two-panel equal-panels">
<div class="image-panel"><img src="images/SandDunes.png" alt="Striped sand dunes" style="width:100%;"><p><strong>Transport and flow</strong></p><p>Wind moves grains; erosion and deposition organise ridges.</p></div>
<div class="image-panel"><img src="images/Zebras.png" alt="Zebra stripes" style="width:100%;"><p><strong>Reaction and diffusion</strong></p><p>Local biochemical and cellular interactions can organise pigment.</p></div>
</div>
""")
reader_only("week03-many-pattern-mechanisms")
reader_only("d595aea9-d487-42a3-a0e8-df8978faf96a",
            "268dc768-98b9-496a-b555-9980cb86844d")

source("37090ea1-8469-43c1-82a4-15f95adc8616", """
# Similar folds, different material
<div class="two-panel equal-panels">
<div class="text-panel"><p><strong>Mechanical instability</strong></p><p>Differential growth puts a surface layer into compression. Beyond a threshold it buckles.</p><p>The same physical idea can organise living tissue and a swelling gel.</p></div>
<div class="image-panel"><img src="images/brain_folding_gel.gif" alt="A swelling gel developing brain-like folds" style="display:block;width:100%;max-height:420px;object-fit:contain;"><p class="figure-reference">A swelling-gel experiment makes the instability visible.</p></div>
</div>
""")
source("7530f174-b927-4f48-88af-1a06f5b4cfce", """
# Similar waves, different systems
<div class="two-panel equal-panels">
<div class="image-panel"><img src="images/dictyostelium_aggregation_waves.png" alt="Fluorescent and processed views of cAMP waves in slime mould" style="width:100%;max-height:390px;object-fit:contain;"><p><strong>cAMP waves in living cells</strong></p><p>Colour shows fluorescence; black-and-white panels are processed views used to identify cell streams.</p></div>
<div class="image-panel"><img src="images/belousov_zhabotinsky_spirals.jpg" alt="Spiral waves in a Belousov-Zhabotinsky reaction" style="width:100%;max-height:390px;object-fit:cover;"><p><strong>Belousov–Zhabotinsky reaction</strong></p><p>An excitable chemical medium generates travelling fronts without moving cells.</p></div>
</div>
""")
source("a0a1efe7-e26e-4f6d-a529-3db70b3fe94f", """
# Turing turns to morphogenesis
<div class="two-panel equal-panels">
<div class="image-panel"><img src="images/turing_1952_first_page.png" alt="Title page of Turing's 1952 paper" style="width:100%;max-height:570px;object-fit:contain;"></div>
<div class="text-panel"><p><strong>The biological question was older than Turing.</strong></p><p>His 1952 contribution was a mathematical mechanism: reacting and diffusing morphogens can destabilise a uniform state.</p><p>After hours of hand calculation, his numerical example produced a dappled pattern. No cell was assigned its final state in advance.</p><p class="figure-reference"><a href="https://www.damtp.cam.ac.uk/user/gold/pdfs/teaching/turing1952.pdf">A. M. Turing, “The Chemical Basis of Morphogenesis” (1952)</a></p></div>
</div>
""")
reader_only("b72f5b93", "d112f5d4")

source("8858f425-48a5-492b-9a5a-2d277dacc632", r"""
# Build the Gray–Scott model · 1. Reaction
$$U+2V\longrightarrow 3V,\qquad \text{local rate }UV^2.$$
<div class="analysis-perspectives">
<div><strong>$U$</strong><br>Feedstock consumed by the reaction.</div>
<div><strong>$V$</strong><br>Product that catalyses its own production.</div>
</div>
Locally, more $V$ can create still more $V$. This is the activating part of the mechanism.
""")
source("b7c839be-6ee3-4fef-9aae-72b880dbb4b9", r"""
# Random walk: a discrete model
At each step, choose one displacement from
$$ (\pm\Delta x,0),\qquad(0,\pm\Delta x). $$
After $n$ independent steps, position is the sum of those increments. One path is irregular; an ensemble has predictable spread.
<div class="ladder-marker"><img src="images/ladder_marker.svg" alt=""><span><strong>Stay low:</strong> follow one particle and make one step explicit.</span></div>
""")
source("11879310", r"""
# Brownian motion: the physical phenomenon
<div class="two-panel equal-panels">
<div class="image-panel"><iframe width="100%" height="360" src="https://www.youtube.com/embed/7orMPKrYPwE" title="Brownian motion" frameborder="0" allowfullscreen></iframe></div>
<div class="text-panel"><p>A $d$-dimensional Brownian motion $\mathbf B(t)$ has continuous paths and independent Gaussian increments:</p>
$$\mathbf B(t+\Delta t)-\mathbf B(t)\sim\mathcal N(\mathbf 0,2D\Delta t I_d).$$
<p>In two dimensions, $\mathbb E\lVert\mathbf B(t)-\mathbf B(0)\rVert^2=4Dt$.</p></div>
</div>
""")
source("562f3685-c727-4a03-ae6e-7e8ed6aaa9c6", """
# Diffusion can create instability
Reaction first creates a local difference. Diffusion determines how far each influence reaches.
<div class="analysis-perspectives">
<div><strong>Local activation</strong><br>A perturbation reinforces itself nearby.</div>
<div><strong>Longer-range inhibition</strong><br>A competing influence spreads farther and suppresses nearby activation.</div>
</div>
Unequal diffusion can destabilise a state that would be stable if perfectly mixed. Diffusion is not itself inhibition; it supplies different spatial ranges.
""")
reader_only("c5c3ba5e", "78500506-7c93-46a4-a0f6-c639fa9285d4",
            "e568a57f-c749-47ab-8fe7-fb411fa60a0e")

source("1c111a8d-516f-4637-95c0-080efdec3d90", r"""
# Continuous description · Diffusion field
<div class="two-panel equal-panels">
<div class="text-panel">$$\frac{\partial u}{\partial t}=D\nabla^2u.$$<p>The field $u(\mathbf x,t)$ records concentration. The Laplacian is positive in a local valley and negative at a local peak, so diffusion fills valleys and lowers peaks.</p><p>Advection is different: it carries the field with a velocity, like dye transported by a current.</p></div>
<div class="image-panel"><img src="images/Ficks_diffusion_micro_macro.gif" alt="Microscopic movement and macroscopic concentration and flux" style="display:block;width:100%;max-height:410px;object-fit:contain;"></div>
</div>
""")
source("4fad79e4-e78d-468c-be71-d70d8c4c711e", r"""
# Transport, smoothing, and local change
$$\frac{\partial u}{\partial t}+\nabla\cdot(\mathbf vu)=D\nabla^2u+R(u).$$
<div class="analysis-perspectives three">
<div><strong>Advection</strong><br>$\nabla\cdot(\mathbf vu)$ carries concentration with the velocity field.</div>
<div><strong>Diffusion</strong><br>$D\nabla^2u$ compares a point with its neighbours and smooths gradients.</div>
<div><strong>Reaction</strong><br>$R(u)$ creates, removes, or transforms material locally.</div>
</div>
""")
source("e501ec03-46e5-44ea-8535-46b96a148671", r"""
# Return to reaction–diffusion
This is now a coupled system of equations:
$$\frac{\partial U}{\partial t}=R_U(U,V)+D_U\nabla^2U,\qquad
\frac{\partial V}{\partial t}=R_V(U,V)+D_V\nabla^2V.$$
Reaction changes concentrations locally. The Laplacian compares each point with its neighbourhood, moving material down gradients and smoothing isolated peaks.

<div class="choice-marker"><img src="images/choice_marker.svg" alt=""><span><strong>Notation:</strong> lowercase $u$ denoted any transported scalar field. Uppercase $U$ and $V$ now denote the two specific Gray–Scott concentration fields.</span></div>
""")
source("534e95c9-97e8-4864-b3cc-66d3c2e9e0aa", """
# Discretise space
To simulate a continuous field, sample it at grid cells and replace spatial derivatives with neighbour comparisons.
<img src="images/diffusion_grid_numbers_t012.svg" alt="Numerical concentration values at times zero, one and two" style="display:block;width:82%;margin:0 auto;">
<div class="ladder-marker"><img src="images/ladder_marker.svg" alt=""><span><strong>Down the ladder:</strong> inspect the value stored in each cell and one explicit update.</span></div>
""")
reader_only("week03-diffusion-numbers-t012")
source("week03-diffusion-t012", """
# Reveal the spatial pattern
<img src="images/diffusion_grid_t012.svg" alt="Grid values represented using colour" style="display:block;width:82%;margin:0 auto;">
<div class="ladder-marker"><img src="images/ladder_marker.svg" alt=""><span><strong>Up the ladder over cell values:</strong> colour compresses many numbers into a visible spatial pattern.</span></div>
""")
source("ecd5c9ba-5acd-42ce-9fba-d6a584a56494", """
# Colour is part of the representation
<div class="two-panel equal-panels">
<div class="image-panel"><img src="images/accessible_matplotlib_colormaps.svg" alt="Viridis, cividis and plasma colour maps" style="width:100%;"></div>
<div class="text-panel"><p><strong>Use a perceptually ordered sequential map for concentration.</strong></p><p>Matplotlib provides accessible defaults including <code>viridis</code>, <code>cividis</code>, and <code>plasma</code>. Avoid rainbow scales and red–green contrasts where possible.</p><p><a href="https://matplotlib.org/stable/users/explain/colors/colormaps.html">Matplotlib: Choosing Colormaps</a></p></div>
</div>
""")
source("09eb9036-81a5-4e05-8806-69d16664865b", r"""
# From a continuous gradient to grid differences

<div class="two-panel equal-panels">
<div class="text-panel">
<p>In continuous space, $\nabla U$ is a vector pointing in the direction of steepest increase. Its components are limits of changes over arbitrarily small distances.</p>
<p>After discretising, $U$ is known only at grid points. There is no value at an arbitrarily small displacement, so the derivative definition cannot be evaluated directly.</p>
$$
\frac{\partial U}{\partial x}\bigg|_{i,j}
\approx\frac{U_{i+1,j}-U_{i-1,j}}{2\Delta x},
\qquad
\frac{\partial U}{\partial y}\bigg|_{i,j}
\approx\frac{U_{i,j+1}-U_{i,j-1}}{2\Delta y}.
$$
</div>
<div class="image-panel"><img src="images/grid_indexing_Uij.svg" alt="A five by five grid labelled with U sub i comma j" style="width:100%;max-height:430px;object-fit:contain;"></div>
</div>

<div class="choice-marker"><img src="images/choice_marker.svg" alt=""><span>Central differences use information equally far to either side. They approximate the continuous gradient and become more accurate as the grid spacing decreases.</span></div>
""")
source("f2e3c94d-6d0e-4d20-992a-8e23122ce6d0", r"""
# From a continuous Laplacian to a grid stencil

In continuous space,
$$
\nabla^2U=\nabla\cdot(\nabla U)
=\frac{\partial^2U}{\partial x^2}+\frac{\partial^2U}{\partial y^2}.
$$
It measures local curvature, or equivalently the net outward change of the gradient. In diffusion, it signals whether a point should gain or lose material.

On a grid we again lack arbitrarily close values, so we approximate:
$$
\Delta_hU_{i,j}
=\frac{U_{i+1,j}+U_{i-1,j}+U_{i,j+1}+U_{i,j-1}-4U_{i,j}}{\Delta x^2},
$$
for equal spacing in both directions.

The discrete version should reproduce the continuous behaviour: zero on a constant or linear field, negative at a local peak, and positive in a local valley.
""")
source("2d86506f-baf9-4f97-9a53-63015dd1e05f", r"""
# Convolve with the five-point stencil

<div class="two-panel equal-panels">
<div class="image-panel"><img src="images/laplacian_convolution_example.svg" alt="A numerical example of convolving a grid with the five-point Laplacian stencil" style="width:100%;"></div>
<div class="text-panel">
$$
L=\begin{bmatrix}0&1&0\\1&-4&1\\0&1&0\end{bmatrix}.
$$
<p>Place $L$ over one cell, multiply overlapping entries, and add. Then slide it to the next cell.</p>
<p>A constant patch gives zero. A high centre gives a negative result, so diffusion reduces it. A low centre gives a positive result, so diffusion raises it.</p>
<p>Convolution applies the same local comparison everywhere, turning one stencil into a field of approximate Laplacian values.</p>
</div>
</div>
""")
remove_cells(
    "73a9790e-fd88-41a9-9c96-0b17f58744d8",
    "eb7f54f7-9925-4880-a13f-4a358e34df86",
    "2e49e946-227b-4c19-a247-f225abdc5f47",
    "44c47b59-472a-48b6-8858-d4445ed0421f",
    "c6c02bff-a5ea-4efc-ae90-857084a0930f",
    "1a76982e-6025-415c-87fd-955fe49b069f",
    "6a6f19c7-690f-42f9-bd53-1106bb4e9d79",
)
source("0ac1d921-5f1e-4b64-8c65-8454c1e70e8f", r"""
# Gray–Scott regulation terms

$$
\frac{\partial U}{\partial t}=D_U\nabla^2U-UV^2+f(1-U),
\qquad
\frac{\partial V}{\partial t}=D_V\nabla^2V+UV^2-(f+k)V.
$$

<div class="analysis-perspectives three">
<div><strong>Feed</strong><br>$f(1-U)$ supplies $U$ from a reservoir and restores the background state.</div>
<div><strong>Kill and outflow</strong><br>$-(f+k)V$ removes $V$: $f$ represents dilution/outflow and $k$ conversion to inert product.</div>
<div><strong>Reaction</strong><br>$UV^2$ consumes $U$ and produces $V$ at exactly the same local rate.</div>
</div>

Without supply and removal, the closed batch reaction exhausts $U$ and the activity dies. Feed and kill keep the system driven away from equilibrium and become controls that select which patterns can persist.
""")
source("d3786649-2fd4-4766-8d86-df7cd2839294", r"""
# Assemble the Gray–Scott update

<div class="two-panel equal-panels">
<div class="text-panel">
<p><strong>Continuous model: coupled PDEs</strong></p>
$$
\frac{\partial U}{\partial t}=D_U\nabla^2U+f(1-U)-UV^2,
$$
$$
\frac{\partial V}{\partial t}=D_V\nabla^2V-(f+k)V+UV^2.
$$
</div>
<div class="text-panel">
<p><strong>Discrete model: explicit update</strong></p>
$$
U^{n+1}_{i,j}=U^n_{i,j}+\Delta t\left[D_U\Delta_hU^n_{i,j}+f(1-U^n_{i,j})-U^n_{i,j}(V^n_{i,j})^2\right],
$$
$$
V^{n+1}_{i,j}=V^n_{i,j}+\Delta t\left[D_V\Delta_hV^n_{i,j}-(f+k)V^n_{i,j}+U^n_{i,j}(V^n_{i,j})^2\right].
$$
</div>
</div>

<div class="ladder-marker"><img src="images/ladder_marker.svg" alt=""><span><strong>From local update to global pattern:</strong> repeat the same indexed calculation at every cell and through time.</span></div>
""")
source("week03-gray-scott-world", """
# Reaction–diffusion beyond the simulation

<div class="two-panel equal-panels">
<div class="image-panel">
<img src="images/cima_experimental_turing_patterns.webp" alt="Experimental setup and observed hexagonal and labyrinthine Turing patterns in a CIMA gel reactor" style="display:block;width:100%;height:365px;object-fit:cover;object-position:center bottom;">
<p><strong>CIMA gel reactor</strong></p>
<p>Stationary hexagonal and labyrinthine patterns have been observed in a driven chemical reaction–diffusion experiment.</p>
</div>
<div class="image-panel">
<img src="images/Zebrafish.jpg" alt="Zebrafish pigment stripes" style="display:block;width:100%;height:365px;object-fit:cover;">
<p><strong>Zebrafish pigment pattern</strong></p>
<p>Short- and long-range pigment-cell interactions reproduce Turing-like pattern dynamics, although the cells do not literally implement the Gray–Scott chemistry.</p>
</div>
</div>

<p class="figure-reference">Gray–Scott is our canonical mathematical model, not a claim that every pictured system uses its exact reactions. Sources: <a href="https://doi.org/10.3389/fphy.2024.1358766">Aizawa &amp; Asakura (2024)</a>; <a href="https://pmc.ncbi.nlm.nih.gov/articles/PMC2689028/">Nakamasu et al. (2009)</a>.</p>
""")
reader_only("week03-pattern-family",
            "a45a0945-5b93-4ba3-9345-168dd54d526c",
            "d5cb018d-702d-462f-b281-49a412e736f5")

order = [c.id for c in nb.cells]
def move_after(cell_id, anchor):
    order.remove(cell_id)
    order.insert(order.index(anchor) + 1, cell_id)
move_after("b7c839be-6ee3-4fef-9aae-72b880dbb4b9", "8858f425-48a5-492b-9a5a-2d277dacc632")
move_after("11879310", "b7c839be-6ee3-4fef-9aae-72b880dbb4b9")
move_after("week03-brownian-ensemble", "11879310")
move_after("562f3685-c727-4a03-ae6e-7e8ed6aaa9c6", "week03-brownian-ensemble")
move_after("d67005af-86fe-4102-b7b8-0cf9f629d586",
           "54e20377-5977-4ea6-a97b-7482a438a6c9")
nb.cells = [cells[cell_id] for cell_id in order]
for cell in nb.cells:
    # Week 3 is delivered without staged fragments. Discussion remains visible,
    # but nothing is withheld behind a click.
    cell.source = cell.source.replace(" fragment", "").replace("fragment ", "")
nbformat.write(nb, PATH)
